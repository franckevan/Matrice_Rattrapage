"""Alertes déterministes sur le journal MATRiCE (module C3).

Aucune IA, aucun score : mêmes lignes en entrée -> mêmes alertes en sortie.
"""
import re
from collections import defaultdict, deque

from .redact import mask_secrets

_KV = re.compile(r'(\w+)=("[^"]*"|\S+)')
_TS = re.compile(r"^(\d{2}):(\d{2}):(\d{2})\s")

# --- Paramètres de la règle principale (documentés dans DOSSIER.md) ---
SIG_THRESHOLD = 3   # nombre d'échecs de signature ...
SIG_WINDOW_S = 60   # ... dans cette fenêtre glissante (secondes), par source


def parse_line(line):
    """'10:00:00 a=b c="d e"' -> dict ; None si la ligne n'est pas un événement."""
    m = _TS.match(line)
    if not m:
        return None
    h, mi, s = (int(x) for x in m.groups())
    ev = {"t": h * 3600 + mi * 60 + s, "time": line[:8]}
    for k, v in _KV.findall(line[m.end():]):
        ev[k] = v.strip('"')
    return ev


def rule_signature_burst(events, threshold=SIG_THRESHOLD, window_s=SIG_WINDOW_S):
    """WEBHOOK_SIGNATURE_BURST : >= `threshold` rejets 401/bad_signature d'une MÊME source
    dans une fenêtre glissante de `window_s` secondes.

    Ne comptent que : component=webhook ET status=401 ET reason=bad_signature.
    Une alerte par rafale : la file de la source est vidée après déclenchement.
    """
    alerts, recent = [], defaultdict(deque)
    for e in events:
        if not (e.get("component") == "webhook" and e.get("status") == "401"
                and e.get("reason") == "bad_signature"):
            continue
        source = e.get("source", "inconnue")
        q = recent[source]
        q.append(e)
        while q and e["t"] - q[0]["t"] > window_s:  # on retire ce qui sort de la fenêtre
            q.popleft()
        if len(q) >= threshold:
            alerts.append({"rule": "WEBHOOK_SIGNATURE_BURST", "severity": "high",
                           "time": e["time"], "source": source,
                           "events": [x.get("event") for x in q],
                           "detail": f"{len(q)} signatures invalides en {window_s}s max"})
            q.clear()
    return alerts


def rule_delivery_quarantine(events):
    """DELIVERY_QUARANTINE : une livraison passe en quarantaine = synchronisation en échec."""
    fails, alerts = defaultdict(int), []
    for e in events:
        if e.get("component") != "delivery":
            continue
        d = e.get("delivery", "?")
        if e.get("status", "0").isdigit() and int(e["status"]) >= 500:
            fails[d] += 1
        if e.get("state") == "quarantine":
            alerts.append({"rule": "DELIVERY_QUARANTINE", "severity": "medium",
                           "time": e["time"], "delivery": d, "failed_attempts": fails[d],
                           "detail": "synchronisation en échec, rejeu manuel nécessaire"})
    return alerts


def rule_ai_review(events):
    """AI_REVIEW_FLAG : le classifieur a marqué un texte 'a_revoir' -> investigation humaine."""
    return [{"rule": "AI_REVIEW_FLAG", "severity": "medium", "time": e["time"],
             "event": e.get("event"),
             "detail": "texte signalé, à traiter comme NON FIABLE : "
                       + mask_secrets(e.get("text", ""))[:80]}
            for e in events if e.get("component") == "classifier" and e.get("tag") == "a_revoir"]


def evaluate(lines):
    events = [e for e in map(parse_line, lines) if e]
    events.sort(key=lambda e: e["t"])  # tri stable : l'ordre d'arrivée départage les égalités
    alerts = (rule_signature_burst(events) + rule_delivery_quarantine(events)
              + rule_ai_review(events))
    return sorted(alerts, key=lambda a: a["time"])
