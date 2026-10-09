"""Check evidence records for required fields and duplicate ids."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
evidence = json.loads((ROOT / "data/evidence/LRRK2.json").read_text())
records = evidence["records"]
ids = [r["evidence_id"] for r in records]
assert len(records) == 5 and len(set(ids)) == 5
assert len({r["pmid"] for r in records}) == 5
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
for record in records:
    assert all(record.get(key) for key in required), record["evidence_id"]
    assert record["source_url"] == f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/"
    assert record["target_id"] == "ENSG00000188906"
    assert record["disease_id"] == "MONDO_0005180"
print(f"PASS: {len(records)} evidence records; required fields and source links resolve.")
