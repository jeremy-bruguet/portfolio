#!/usr/bin/env python3
"""Publie une seule actualité récente du CERT-FR, sans doublons."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_URL = "https://www.cert.ssi.gouv.fr/feed/"
HEADERS = {"User-Agent": "PortfolioVeille/1.0 (veille pédagogique)"}
CVE_PATTERN = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.IGNORECASE)


def fetch(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read()


def date_iso(value):
    if not value:
        return ""
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return value


def main():
    root = ET.fromstring(fetch(FEED_URL))
    candidates = []
    seen = set()
    for node in root.findall(".//item"):
        title = " ".join((node.findtext("title") or "").split())
        link = (node.findtext("link") or "").strip()
        if not title or not link or link in seen:
            continue
        seen.add(link)
        summary = " ".join((node.findtext("description") or "").split())[:700]
        item = {"title": title, "url": link, "date": date_iso(node.findtext("pubDate")), "source": "CERT-FR / ANSSI", "summary": summary, "kind": "Dernière publication officielle du CERT-FR"}
        cves = CVE_PATTERN.findall(title + " " + summary)
        if cves:
            item["cve"] = cves[0].upper()
        candidates.append(item)
    candidates.sort(key=lambda item: item.get("date", ""), reverse=True)
    if not candidates:
        raise SystemExit("Le flux CERT-FR ne contient aucune publication exploitable.")
    output = {"generatedAt": datetime.now(timezone.utc).isoformat(), "sources": ["CERT-FR / ANSSI"], "items": candidates[:1], "warnings": []}
    (ROOT / "veille-data.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Une seule actualité récente publiée dans veille-data.json : " + candidates[0]["title"])


if __name__ == "__main__":
    main()
