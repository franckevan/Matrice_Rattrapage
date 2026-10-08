"""Normalisation, validation et déduplication des séances (module I2)."""
import json
import re
from dataclasses import dataclass, field
from datetime import date

_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_FR = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")

PERIODS = {"matin": "am", "am": "am", "après-midi": "pm", "apres-midi": "pm", "pm": "pm"}
STATUSES = {"propose": "proposed", "proposed": "proposed",
            "confirme": "confirmed", "confirmed": "confirmed"}
GROUPS = {"A": "A", "B": "B", "Promotion": "Promotion"}
MODES = {"DG": "DG", "CE": "CE", "AUTO": "AUTO"}
TEACHERS = {"t1", "t2", "t3"}


def normalize_date(value):
    """YYYY-MM-DD ou DD/MM/YYYY -> YYYY-MM-DD ; ValueError si invalide."""
    if not isinstance(value, str):
        raise ValueError("date absente ou non textuelle")
    value = value.strip()
    m = _ISO.match(value)
    if m:
        y, mo, d = (int(x) for x in m.groups())
    else:
        m = _FR.match(value)
        if not m:
            raise ValueError(f"format de date inconnu : {value!r}")
        d, mo, y = (int(x) for x in m.groups())
    try:
        return date(y, mo, d).isoformat()  # refuse 2026-02-30
    except ValueError:
        raise ValueError(f"date inexistante : {value!r}") from None


def _text(raw, key, errors):
    v = raw.get(key)
    if not isinstance(v, str) or not v.strip():
        errors.append(f"{key} vide ou absent")
        return None
    return v.strip()


def _choice(raw, key, table, errors, lower=False):
    v = raw.get(key)
    if isinstance(v, str):
        k = v.strip().lower() if lower else v.strip()
        if k in table:
            return table[k]
    errors.append(f"{key} invalide : {v!r}")
    return None


def normalize_record(raw):
    """Retourne (enregistrement normalisé, []) ou (None, [motifs de rejet])."""
    if not isinstance(raw, dict):
        return None, ["l'objet JSON attendu est absent"]
    errors = []
    rec = {"id": _text(raw, "id", errors)}
    try:
        rec["date"] = normalize_date(raw.get("date"))
    except ValueError as exc:
        errors.append(str(exc))
    rec["period"] = _choice(raw, "period", PERIODS, errors, lower=True)
    rec["group"] = _choice(raw, "group", GROUPS, errors)
    rec["mode"] = _choice(raw, "mode", MODES, errors)
    rec["title"] = _text(raw, "title", errors)
    rec["domain"] = _text(raw, "domain", errors)
    rec["status"] = _choice(raw, "status", STATUSES, errors, lower=True)

    if "teacherId" not in raw:
        errors.append("teacherId absent")
    else:
        t = raw["teacherId"]
        if t is None:
            rec["teacherId"] = None
        elif isinstance(t, str) and t.strip() in TEACHERS:
            rec["teacherId"] = t.strip()
        else:
            errors.append(f"teacherId invalide : {t!r}")

    if not errors:  # règles métier, évaluées sur des champs déjà valides
        if rec["mode"] == "AUTO" and (rec["teacherId"] is not None or rec["status"] != "proposed"):
            errors.append("AUTO exige teacherId null et status proposed")
        if rec["status"] == "confirmed" and rec["teacherId"] is None:
            errors.append("confirmed exige un formateur")
    return (None, errors) if errors else (rec, [])


@dataclass
class Result:
    total: int = 0
    accepted: list = field(default_factory=list)
    rejected: list = field(default_factory=list)
    duplicates: list = field(default_factory=list)


def process(lines):
    """Valide d'abord, déduplique ensuite : 1re occurrence VALIDE d'un id retenue."""
    res = Result()
    first_line = {}
    for n, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        res.total += 1
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            res.rejected.append({"line": n, "raw": line.strip(),
                                 "reasons": [f"JSON malformé : {exc.msg}"]})
            continue
        rec, errors = normalize_record(raw)
        if errors:
            res.rejected.append({"line": n, "raw": line.strip(), "reasons": errors})
        elif rec["id"] in first_line:
            res.duplicates.append({"line": n, "id": rec["id"], "first_line": first_line[rec["id"]]})
        else:
            first_line[rec["id"]] = n
            res.accepted.append(rec)
    return res
