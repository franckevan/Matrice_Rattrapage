"""Indicateurs du module I2."""
from collections import Counter

SESSION_HOURS = 3.5


def compute_metrics(res):
    acc = res.accepted
    by_domain = Counter(r["domain"] for r in acc)

    # AUTO n'a pas de formateur -> jamais compté côté formateur.
    by_teacher = Counter(r["teacherId"] for r in acc
                         if r["teacherId"] is not None and r["mode"] != "AUTO")
    teacher_hours = {t: n * SESSION_HOURS for t, n in sorted(by_teacher.items())}

    # Heures-apprenant : couples (date, période) DISTINCTS du groupe + Promotion.
    learner_hours = {}
    for g in ("A", "B"):
        slots = {(r["date"], r["period"]) for r in acc if r["group"] in (g, "Promotion")}
        learner_hours[g] = len(slots) * SESSION_HOURS

    assigned = [r for r in acc if r["teacherId"] is not None and r["mode"] != "AUTO"]
    confirmed = [r for r in assigned if r["status"] == "confirmed"]
    rate = len(confirmed) / len(assigned) if assigned else None  # None = non applicable

    return {
        "lines_total": res.total,
        "accepted": len(acc),
        "rejected": len(res.rejected),
        "duplicates": len(res.duplicates),
        "sessions_by_domain": dict(sorted(by_domain.items())),
        "teacher_hours": teacher_hours,
        "learner_hours": learner_hours,
        "confirmation": {"confirmed": len(confirmed), "assigned": len(assigned), "rate": rate},
    }
