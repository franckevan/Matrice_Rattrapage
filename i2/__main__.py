"""Pipeline : python -m i2 [--input FICHIER] [--out DOSSIER]"""
import argparse
import json
from pathlib import Path

from .dashboard import render_dashboard
from .metrics import compute_metrics
from .normalize import process

HERE = Path(__file__).parent


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=HERE / "data" / "seances.ndjson")
    p.add_argument("--out", type=Path, default=HERE / "out")
    a = p.parse_args()

    lines = a.input.read_text(encoding="utf-8").splitlines()
    res = process(lines)
    m = compute_metrics(res)

    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "seances_normalisees.ndjson").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res.accepted), encoding="utf-8")
    write_json(a.out / "rejets.json", res.rejected)
    write_json(a.out / "doublons.json", res.duplicates)
    write_json(a.out / "metriques.json", m)
    (a.out / "dashboard.html").write_text(
        render_dashboard(m, res.rejected, res.duplicates), encoding="utf-8")
    print(json.dumps(m, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
