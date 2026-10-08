"""Dashboard HTML autonome (SVG inline, aucune dépendance)."""
from html import escape


def fmt(v):
    return f"{v:g}".replace(".", ",")


def bar_chart(title, items, unit=""):
    if not items:
        return f"<p class='empty'>Aucune donnée pour « {escape(title)} ».</p>"
    width, row, label_w = 460, 34, 110
    maxv = max(v for _, v in items) or 1
    parts = []
    for i, (label, v) in enumerate(items):
        y = i * row + 5
        w = (width - label_w - 80) * v / maxv
        parts.append(
            f'<text x="0" y="{y + 17}" class="lbl">{escape(str(label))}</text>'
            f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="22" rx="4"/>'
            f'<text x="{label_w + w + 6:.1f}" y="{y + 17}" class="val">{fmt(v)}{unit}</text>')
    return (f'<svg viewBox="0 0 {width} {len(items) * row + 10}" role="img" '
            f'aria-label="{escape(title)}">{"".join(parts)}</svg>')


def render_dashboard(m, rejected, duplicates):
    c = m["confirmation"]
    rate = "non applicable" if c["rate"] is None else f"{c['rate'] * 100:.0f} %"
    kpis = [("Lignes lues", m["lines_total"]), ("Acceptées", m["accepted"]),
            ("Rejets", m["rejected"]), ("Doublons", m["duplicates"]),
            ("Taux de confirmation", rate)]
    kpi_html = "".join(f'<div class="kpi"><b>{escape(str(v))}</b><span>{escape(k)}</span></div>'
                       for k, v in kpis)
    rej_rows = "".join(
        f"<tr><td>{r['line']}</td><td><code>{escape(r['raw'])}</code></td>"
        f"<td>{escape('; '.join(r['reasons']))}</td></tr>" for r in rejected
    ) or "<tr><td colspan='3'>Aucun rejet</td></tr>"
    dup_rows = "".join(
        f"<tr><td>{d['line']}</td><td>{escape(d['id'])}</td><td>{d['first_line']}</td></tr>"
        for d in duplicates) or "<tr><td colspan='3'>Aucun doublon</td></tr>"
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MATRiCE — Dashboard des séances</title>
<style>
:root{{--bg:#fff;--fg:#1f1b2e;--accent:#5b46a8;--card:#f4f2fb}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16131f;--fg:#ece9f7;--accent:#9d8cf0;--card:#221e33}}}}
body{{font-family:system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:960px;margin:2rem auto;padding:0 1rem}}
h1,h2{{color:var(--accent)}} .kpis{{display:flex;gap:.75rem;flex-wrap:wrap}}
.kpi{{background:var(--card);border-radius:10px;padding:.8rem 1.1rem;display:flex;flex-direction:column}}
.kpi b{{font-size:1.5rem}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:1.5rem}}
svg{{width:100%}} rect{{fill:var(--accent)}} text{{fill:var(--fg);font-size:13px}}
table{{border-collapse:collapse;width:100%;font-size:.9rem;display:block;overflow-x:auto}}
td,th{{border:1px solid var(--card);padding:.35rem .6rem;text-align:left}} .empty{{opacity:.7}}
</style></head><body>
<h1>Dashboard des séances</h1>
<div class="kpis">{kpi_html}</div>
<div class="grid">
<section><h2>Séances par domaine</h2>{bar_chart("Séances par domaine", list(m["sessions_by_domain"].items()))}</section>
<section><h2>Heures par formateur</h2>{bar_chart("Heures par formateur", list(m["teacher_hours"].items()), " h")}</section>
<section><h2>Heures-apprenant par groupe</h2>{bar_chart("Heures-apprenant", list(m["learner_hours"].items()), " h")}</section>
<section><h2>Confirmation</h2><p>{c['confirmed']} confirmée(s) sur {c['assigned']} affectée(s) hors AUTO : <b>{rate}</b></p></section>
</div>
<h2>Lignes rejetées</h2>
<table><tr><th>Ligne</th><th>Contenu</th><th>Motif</th></tr>{rej_rows}</table>
<h2>Doublons ignorés</h2>
<table><tr><th>Ligne</th><th>id</th><th>1re occurrence (ligne)</th></tr>{dup_rows}</table>
</body></html>"""
