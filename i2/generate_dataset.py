"""Recrée data/seances.ndjson à partir des deux tableaux de l'énoncé."""
import json
from pathlib import Path

# (id, date, période, groupe, mode) — lignes 1 à 11, valeurs brutes
TABLE1 = [
    ("s01", "19/10/2026", "matin", "A", "DG"),
    ("s02", "2026-10-19", "am", "B", "DG"),
    ("s03", "2026-10-19", "pm", "Promotion", "CE"),
    ("s01", "2026-10-19", "am", "A", "DG"),
    ("s04", "20/10/2026", "matin", "A", "DG"),
    ("s05", "2026-10-20", "am", "B", "DG"),
    ("bad1", "2026-10-20", "pm", "Promotion", "AUTO"),
    ("bad2", "2026-02-30", "am", "A", "DG"),
    ("bad3", "2026-10-20", "soir", "A", "DG"),
    ("s02", "2026-10-19", "am", "B", "DG"),
    ("s06", "2026-10-20", "après-midi", "Promotion", "AUTO"),
]
# (titre, domaine, teacherId, statut) — même ordre ; None = null JSON
TABLE2 = [
    ("React composants", "web", "t1", "confirme"),
    ("React événements", "web", "t2", "confirmed"),
    ("Données et SQL", "data", "t1", "confirmed"),
    ("Copie React", "web", "t1", "confirmed"),
    ("Authentification", "cyber", "t2", "propose"),
    ("Revue de projet", "projet", "t3", "proposed"),
    ("", "projet", None, "proposed"),
    ("Date invalide", "web", "t1", "proposed"),
    ("Période invalide", "web", "t1", "proposed"),
    ("Copie B", "web", "t2", "confirmed"),
    ("Travail autonome", "projet", None, "proposed"),
]
MALFORMED = '{"id":"bad4","title":"JSON tronqué"'  # ligne 12, telle quelle


def build_lines():
    lines = []
    for (sid, d, period, group, mode), (title, domain, teacher, status) in zip(TABLE1, TABLE2):
        obj = {"id": sid, "date": d, "period": period, "group": group, "mode": mode,
               "title": title, "domain": domain, "teacherId": teacher, "status": status}
        lines.append(json.dumps(obj, ensure_ascii=False))
    lines.append(MALFORMED)
    return lines


if __name__ == "__main__":
    out = Path(__file__).parent / "data" / "seances.ndjson"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(build_lines()) + "\n", encoding="utf-8")
    print(f"{out} écrit ({len(build_lines())} lignes)")
