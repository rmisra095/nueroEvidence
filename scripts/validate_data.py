"""Check evidence records for required fields and duplicate ids."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = sorted((ROOT / "data" / "evidence").glob("*.json"))
assert files, "no evidence files"
required = [
    "finding",
    "supporting_passage",
    "passage_context",
    "source_location",
    "source_title",
    "source_url",
    "doi",
    "review_method",
    "reviewed_on",
]
seen_ids = set()
seen_pmids = set()
total = 0
for path in files:
    records = json.loads(path.read_text())["records"]
    assert len(records) >= 3, path.name
    assert len({r["gene_symbol"] for r in records}) == 1, path.name
    assert len({r["target_id"] for r in records}) == 1, path.name
    for record in records:
        assert all(record.get(key) for key in required), record["evidence_id"]
        assert record["evidence_id"].startswith(f"{record['gene_symbol']}_PD_")
        assert record["source_url"] == f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/"
        assert record["disease_id"] == "MONDO_0005180"
        assert record["evidence_id"] not in seen_ids, record["evidence_id"]
        assert record["pmid"] not in seen_pmids, record["pmid"]
        seen_ids.add(record["evidence_id"])
        seen_pmids.add(record["pmid"])
    total += len(records)
print(
    f"PASS: {len(files)} evidence files, {total} records; "
    "required fields and source links resolve."
)
