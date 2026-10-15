#!/usr/bin/env python3
"""Construit veille-data.json à partir de flux publics de sécurité."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADERS = {"User-Agent": "PortfolioVeille/1.0 (veille pédagogique)"}


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


def cert_fr_items():
    url = "https://www.cert.ssi.gouv.fr/feed/"
    root = ET.fromstring(fetch(url))
    items = []
    for node in root.findall(".//item")[:12]:
        title = (node.findtext("title") or "Publication CERT-FR").strip()
        link = (node.findtext("link") or "https://www.cert.ssi.gouv.fr/").strip()
        description = " ".join((node.findtext("description") or "").split())
        pub_date = date_iso(node.findtext("pubDate"))
        items.append({
            "title": title, "url": link, "date": pub_date,
            "source": "CERT-FR / ANSSI",
            "summary": description[:450],
            "kind": "Avis et alertes de sécurité"
        })
    return items


def cisa_items():
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    data = json.loads(fetch(url))
    vulnerabilities = data.get("vulnerabilities", [])
    vulnerabilities.sort(key=lambda x: x.get("dateAdded", ""), reverse=True)
    items = []
    for vuln in vulnerabilities[:15]:
        cve = vuln.get("cveID", "CVE non précisée")
        product = vuln.get("product", "Produit non précisé")
        vendor = vuln.get("vendorProject", "")
        items.append({
            "title": f"{cve} — {vendor} {product}".strip(),
            "url": f"https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search={cve}",
            "date": vuln.get("dateAdded", ""),
            "source": "CISA — Known Exploited Vulnerabilities",
            "summary": vuln.get("shortDescription", ""),
            "kind": "Exploitation connue signalée par CISA",
            "cve": cve,
            "action": vuln.get("requiredAction", ""),
            "dueDate": vuln.get("dueDate", "")
        })
    return items


def main():
    items = []
    errors = []
    for name, loader in (("CERT-FR", cert_fr_items), ("CISA KEV", cisa_items)):
        try:
            items.extend(loader())
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
    if not items:
        raise SystemExit("Aucune source n'a pu être récupérée : " + "; ".join(errors))
    items.sort(key=lambda item: item.get("date", ""), reverse=True)
    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sources": ["CERT-FR / ANSSI", "CISA Known Exploited Vulnerabilities Catalog"],
        "items": items,
        "warnings": errors
    }
    (ROOT / "veille-data.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"{len(items)} entrées écrites dans veille-data.json")
    if errors:
        print("Certaines sources n'ont pas répondu : " + "; ".join(errors))


if __name__ == "__main__":
    main()
