# NeuroEvidence

Investigate a gene’s connection to Parkinson’s through cited findings and inspectable evidence.

## Milestone 1: LRRK2 reference example — complete

- Five selected original studies stored in `data/evidence/LRRK2.json`.
- Seven brief statements linked to evidence IDs in `data/briefs/LRRK2.json`.
- Five study findings and two explicitly labeled interpretations checked in `data/briefs/LRRK2-claim-checks.json`.
- Readable brief and claim-check table in `outputs/`.
- Project scope copied into `outputs/NeuroEvidence-project-scope.md`.

Run the dependency-free structural check:

```sh
python3 scripts/validate_data.py
```

This validates record completeness, duplicates, and citation references. Scientific support was checked separately by the assistant against original-study abstracts; it is not assessed by the script. Independent researcher review is still pending.

## Evidence conventions

`supporting_passage` contains a short exact excerpt; an ellipsis marks an omission. `passage_context` paraphrases the surrounding abstract to preserve variant, population, and trial context. Limitations are labeled reviewer interpretations. The gene uses Ensembl `ENSG00000188906`; Parkinson’s uses `MONDO_0005180`, with legacy EFO mapping recorded alongside its source.

This collection is manually curated from the papers selected during planning. It is not an Open Targets data import, comprehensive review, or current treatment assessment. Source URLs and excerpts were checked using primary publication records during this conversation. Some PubMed pages required indexed abstracts or the author institution’s publication record because live pages returned incomplete content.

## Next milestone

Choose nine more genes based on evidence availability and build three to five reviewed study records per gene using this format. Keep citation review explicit as the collection grows.
