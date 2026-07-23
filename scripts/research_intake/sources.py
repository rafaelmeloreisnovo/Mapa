from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any


def fetch_json(url: str, params: dict[str, str], user_agent: str) -> Any:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{url}?{query}", headers={"User-Agent": user_agent, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310: reviewed endpoints only
        return json.loads(response.read().decode("utf-8"))


def network_collect(config: dict[str, Any], query: str, limit: int, mailto: str) -> list[dict[str, Any]]:
    """Bounded metadata sample. Adapters fail closed and never scrape Google Scholar."""
    records: list[dict[str, Any]] = []
    user_agent = f"MapaResearchIntake/1.0 (mailto:{mailto or 'TOKEN_VAZIO'})"
    for source in config["sources"]:
        if source.get("enabled") != "true":
            continue
        sid, endpoint = source["id"], source["endpoint"]
        try:
            if sid == "crossref":
                payload = fetch_json(endpoint, {"query.bibliographic": query, "rows": str(limit), "mailto": mailto}, user_agent)
                for item in payload.get("message", {}).get("items", []):
                    date = item.get("published-print") or item.get("published-online") or {}
                    records.append({"source": sid, "source_record_id": item.get("DOI", ""),
                        "title": (item.get("title") or [""])[0],
                        "year": (date.get("date-parts") or [[None]])[0][0],
                        "authors": [" ".join(filter(None, [a.get("given"), a.get("family")])) for a in item.get("author", [])],
                        "doi": item.get("DOI", ""), "domain": source["domain"], "url": item.get("URL", "")})
            elif sid == "openalex":
                payload = fetch_json(endpoint, {"search": query, "per-page": str(limit), "mailto": mailto}, user_agent)
                for item in payload.get("results", []):
                    records.append({"source": sid, "source_record_id": item.get("id", ""),
                        "title": item.get("display_name", ""), "year": item.get("publication_year"),
                        "authors": [a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])],
                        "doi": (item.get("doi") or "").removeprefix("https://doi.org/"),
                        "domain": source["domain"], "url": item.get("id", "")})
            elif sid == "semantic_scholar":
                payload = fetch_json(endpoint, {"query": query, "limit": str(limit),
                    "fields": "title,year,authors,externalIds,url"}, user_agent)
                for item in payload.get("data", []):
                    ext = item.get("externalIds") or {}
                    records.append({"source": sid, "source_record_id": item.get("paperId", ""),
                        "title": item.get("title", ""), "year": item.get("year"),
                        "authors": [a.get("name", "") for a in item.get("authors", [])],
                        "doi": ext.get("DOI", ""), "arxiv_id": ext.get("ArXiv", ""), "pmid": ext.get("PubMed", ""),
                        "domain": source["domain"], "url": item.get("url", "")})
            elif sid == "europe_pmc":
                payload = fetch_json(endpoint, {"query": query, "pageSize": str(limit),
                    "format": "json", "resultType": "core"}, user_agent)
                for item in payload.get("resultList", {}).get("result", []):
                    records.append({"source": sid, "source_record_id": item.get("id", ""),
                        "title": item.get("title", ""), "year": item.get("pubYear"),
                        "authors": [a.get("fullName", "") for a in (item.get("authorList") or {}).get("author", [])],
                        "doi": item.get("doi", ""), "pmid": item.get("pmid", ""), "domain": source["domain"],
                        "url": f"https://europepmc.org/article/{item.get('source','')}/{item.get('id','')}"})
            else:
                # arXiv Atom and SciELO OAI-PMH remain TOKEN_VAZIO_CODE until dedicated parsers/tests.
                continue
        except Exception as exc:
            records.append({"source": sid, "source_record_id": f"NETWORK-ERROR-{type(exc).__name__}",
                            "title": "", "year": None, "authors": [], "domain": "TOKEN_VAZIO", "url": ""})
    return records
