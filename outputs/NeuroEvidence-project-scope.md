# NeuroEvidence — project scope and build checklist

## Purpose

Help a researcher investigate a gene’s connection to Parkinson’s disease in minutes. The user selects a gene, reads a cited research brief, inspects the evidence behind each finding, and sees limitations and unanswered questions.

The product supports research investigation. A gene–disease association alone does not establish treatment benefit.

## First-version scope

- One disease: Parkinson’s.
- Ten supported genes, starting with LRRK2. Select the remaining nine after checking evidence availability.
- Three to five selected original studies per gene: approximately 30–50 studies total. Label this as a curated starting collection, not a comprehensive literature review.
- Evidence categories: human genetics, laboratory studies, and clinical studies, where available.
- One results screen with an overview, evidence cards, and research questions.
- Clickable citations, expandable supporting passages, and a downloadable research brief.

Do not add an open-ended chatbot, multiple diseases, user accounts, automatic target rankings, or custom model training to the first version.

## User journey

1. Select a supported gene; Parkinson’s is fixed.
2. Click **Investigate**.
3. Read a short brief: what supports the gene, what the limits are, and what remains unanswered.
4. Click a citation to inspect the supporting passage and open the original source.
5. Download the brief with citations and its evidence review date.

## Recommended technical setup

Use one small Next.js application with TypeScript. Keep the reviewed evidence in version-controlled JSON files initially. Generate briefs through a server-side language-model API call, validate the response, and cache approved results. Keep API keys on the server.

| Component | Responsibility | Concrete output |
|---|---|---|
| Open Targets | Discover target–disease evidence and source references | Candidate studies for each gene |
| Original papers | Supply findings and supporting text | Verified excerpts with source locations |
| Evidence JSON | Store reviewed, structured findings | One file per gene |
| Retrieval | Select records matching the chosen gene and disease | Relevant reviewed records only |
| Language model | Extract draft fields and synthesize evidence | Structured draft brief |
| Validation | Check source IDs, required fields, and claim support | Accepted brief or flagged draft |
| Web interface | Display brief and inspectable evidence | Working investigation screen |
| Export | Save the displayed brief and references | Markdown download; browser print is optional |

An exact gene–disease lookup is enough for retrieval at this size. A vector database is unnecessary initially. A curated dataset also lets you test synthesis before automating literature collection.

## Data structure

Each evidence record should contain:

```json
{
  "evidence_id": "LRRK2_PD_001",
  "gene_symbol": "LRRK2",
  "target_id": "<verified Ensembl identifier>",
  "disease_name": "Parkinson’s disease",
  "disease_id": "<verified ontology identifier>",
  "evidence_type": "human_genetics",
  "finding": "<one precise finding>",
  "supporting_passage": "<verified excerpt with enough context>",
  "source_location": "Abstract, results sentence",
  "source_title": "<paper title>",
  "source_url": "<original paper or PubMed URL>",
  "pmid": "<if available>",
  "doi": "<if available>",
  "publication_year": 2004,
  "text_scope": "abstract",
  "limitations": ["<study-specific limitation or labeled interpretation>"],
  "review_status": "verified",
  "reviewed_on": "<YYYY-MM-DD>"
}
```

Keep passages short, preserve their context, and follow source reuse terms. Record whether you reviewed an abstract or full text. Deduplicate studies by PMID or DOI. Missing evidence is not evidence against a gene.

The brief should store three sections, with evidence IDs attached to every factual claim. Store research questions separately so they are clearly distinguished from established findings.

## Deliverables and checkpoints

Complete these in order. Move on when the completion condition is met.

### 1. Finish the LRRK2 reference example

**Deliverables:** one evidence JSON file containing the five selected studies; one manually checked brief; one claim-check table.

**Tasks:** verify gene/disease identifiers, source metadata, passages, and passage locations. Preserve the surrounding context identified in our citation check. Separate study findings from your interpretations.

**Done when:** every factual sentence in the brief points to evidence that supports it, and every citation opens the intended source.

**Current status:** complete. Five studies are in `data/evidence/LRRK2.json`, the brief is in `data/briefs/LRRK2.json`, and claim checks are in `data/briefs/LRRK2-claim-checks.json`. `scripts/validate_data.py` checks structure and citation IDs. Independent researcher review is still pending.

### 2. Build the ten-gene evidence collection

**Deliverables:** a supported-gene list and ten evidence JSON files covering approximately 30–50 selected studies.

**Tasks:** use Open Targets to find candidate references; inspect original sources; extract findings, context, and limitations; manually review all records. Include differing results where found, without forcing a disagreement into every gene.

**Done when:** each gene has at least three reviewed findings, complete source links, and explicit notes about gaps in the collection.

### 3. Automate brief generation

**Deliverables:** a server-side brief generator, structured output schema, and saved outputs for the ten genes.

**Tasks:** provide only matching reviewed records to the model. Require evidence IDs on factual claims. Instruct it to stay within the supplied evidence and label interpretations and research questions. Reject missing or unknown citation IDs. Review semantic claim support manually before approving outputs.

**Done when:** all ten briefs follow the three-section format, contain valid citations, and pass manual claim review. Valid citation IDs alone do not prove that the cited text supports a claim.

### 4. Build the investigation interface

**Deliverables:** working gene selector, results screen, expandable passages, source links, and brief download.

**Tasks:** show loading and error states; show the evidence review date and curated scope; let each citation open its evidence card; keep source text easy to compare with the generated claim.

**Done when:** someone can select any supported gene, inspect its cited findings, and download the brief without developer help.

### 5. Evaluate accuracy and usefulness

**Deliverables:** an evaluation sheet, recorded results, and a short list of fixes.

**Accuracy check:** review all factual claims in the ten briefs. Mark each as supported, partially supported, unsupported, or contradicted. Record the reason and corrected wording.

**Usability check:** ask three to five researchers or biology students to investigate a target using ordinary sources and using NeuroEvidence. Use comparable tasks, alternate task order, and require the same output: three supported findings, one limitation, and one research question. Record time and answer quality. Treat this small study as preliminary feedback.

**Proposed demo gates:**

- 100% of factual claims have valid evidence references.
- At least 95% are fully supported before final correction; correct or remove every remaining problematic claim before the demo.
- Zero broken source links in the reviewed collection.
- Median investigation time is at least 30% lower with NeuroEvidence, without lower answer quality. If this is missed, report the result and improve the workflow before claiming time savings.

### 6. Package the demo

**Deliverables:** runnable application, setup README, reviewed dataset, evaluation results, and a short demo walkthrough.

**Done when:** a reviewer can run the app, reproduce the LRRK2 example, inspect its evidence, and understand both the measured results and the limits of the collection. Public deployment is optional.

## Definition of finished

- [ ] Ten Parkinson’s genes are supported.
- [ ] Approximately 30–50 selected studies are structured and reviewed.
- [ ] Each gene has a cited, checked brief.
- [ ] Users can trace factual claims to supporting passages and original sources.
- [ ] Limitations, interpretations, and research questions are clearly labeled.
- [ ] Brief generation, interface, and export work end to end.
- [ ] Accuracy and task-time results are recorded.
- [ ] README and demo walkthrough are complete.

## Immediate next task

Save the five LRRK2 findings as the first evidence JSON file, including their source context, and encode the example brief with evidence IDs. Use this single example to establish the format before expanding the dataset.

## Starting references

- [Open Targets evidence documentation](https://platform-docs.opentargets.org/evidence)
- [Zimprich et al., 2004](https://pubmed.ncbi.nlm.nih.gov/15541309/)
- [Gilks et al., 2005](https://pubmed.ncbi.nlm.nih.gov/15680457/)
- [Healy et al., 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2832754/)
- [Steger et al., 2016](https://pubmed.ncbi.nlm.nih.gov/26824392/)
- [Jennings et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35675433/)
