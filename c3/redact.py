"""Journalisation sans secret : liste blanche d'en-têtes + masquage défensif du texte libre."""
import re

# Liste BLANCHE : tout en-tête absent de cette liste n'est jamais journalisé.
ALLOWED_HEADERS = {"user-agent", "content-type", "content-length", "x-request-id", "accept"}

_BEARER = re.compile(r"(?i)\b(bearer|basic)\s+[A-Za-z0-9._~+/=-]+")
_KEYVAL = re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key|signature|authorization)=\S+")


def safe_headers(headers):
    return {k.lower(): v for k, v in headers.items() if k.lower() in ALLOWED_HEADERS}


def mask_secrets(text):
    text = _BEARER.sub(lambda m: f"{m.group(1)} [REDACTED]", text)
    return _KEYVAL.sub(lambda m: f"{m.group(1)}=[REDACTED]", text)


def safe_log_line(time, fields, headers=None):
    parts = [time]
    for k, v in fields.items():
        v = mask_secrets(str(v))
        parts.append(f'{k}="{v}"' if " " in v else f"{k}={v}")
    for k, v in safe_headers(headers or {}).items():
        v = mask_secrets(str(v))
        parts.append(f'hdr_{k}="{v}"' if " " in v else f"hdr_{k}={v}")
    return " ".join(parts)
