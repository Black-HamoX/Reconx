import re
import json
import os
from datetime import datetime
from pathlib import Path

EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")

RECONX_DIR = Path.home() / "reconx"


def is_valid_email(email):
    return bool(EMAIL_RE.match(email))


def is_valid_domain(domain):
    return bool(DOMAIN_RE.match(domain))


def clean_domain(domain):
    return domain.replace("http://", "").replace("https://", "").split("/")[0].strip()


def save_results(data, target, outdir=None):
    if outdir is None:
        outdir = RECONX_DIR
    else:
        outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    safe = target.replace("/", "_").replace("@", "_at_").replace(":", "_").replace("\\", "_")
    filename = f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = outdir / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return str(path)