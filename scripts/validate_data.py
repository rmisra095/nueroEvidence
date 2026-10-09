"""Check reference integrity; does not assess scientific claim support."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
evidence = json.loads((ROOT / 'data/evidence/LRRK2.json').read_text())
brief = json.loads((ROOT / 'data/briefs/LRRK2.json').read_text())
review = json.loads((ROOT / 'data/briefs/LRRK2-claim-checks.json').read_text())
records = evidence['records']
ids = [r['evidence_id'] for r in records]
assert len(records) == 5 and len(set(ids)) == 5
assert len({r['pmid'] for r in records}) == 5
required = ['finding', 'supporting_passage', 'passage_context', 'source_location',
            'source_title', 'source_url', 'doi', 'review_method', 'reviewed_on']
for record in records:
    assert all(record.get(key) for key in required), record['evidence_id']
    assert record['source_url'] == f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/"
    assert record['target_id'] == 'ENSG00000188906'
    assert record['disease_id'] == brief['disease_id']
claims = [c for section in brief['sections'] for c in section['claims']]
claim_ids = {c['claim_id'] for c in claims}
assert len(claim_ids) == len(claims)
for claim in claims:
    assert claim['evidence_ids'] and set(claim['evidence_ids']) <= set(ids)
assert {c['claim_id'] for c in review['checks']} == claim_ids
for question in brief['research_questions']:
    assert question['prompted_by'] and set(question['prompted_by']) <= set(ids)
print(f'PASS: {len(records)} evidence records, {len(claims)} checked claims, '
      f"{len(brief['research_questions'])} research questions; all references resolve.")
