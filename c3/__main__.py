"""python -m c3 [journal]  -> alertes au format JSON"""
import json
import sys
from pathlib import Path

from .detect import evaluate

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "data" / "journal.log"
alerts = evaluate(path.read_text(encoding="utf-8").splitlines())
print(json.dumps(alerts, ensure_ascii=False, indent=2))
