# Theme 09 · Pipeline-to-Runbook Auto-Documenter · Starter kit

**Intent:** As a support engineer taking over a project, I want accurate documentation generated from the actual code, so that I can run and fix it without calling the build team.

## What's in this kit

```
project/                          A complete "Contoso Retail" project, as exported from source control
  adf/pipeline/                   4 Azure Data Factory pipelines (master, 2 ingest, transform)
  adf/trigger/                    Schedules
  adf/linkedService/, adf/dataset/
  databricks/bronze|silver|gold/  6 notebooks (Databricks source format)
  powerbi/retail_sales_model.json The downstream semantic model
templates/
  runbook_template.md             Suggested runbook structure (one per pipeline)
  lineage_template.csv
```

There is no other documentation. Everything a support engineer needs is somewhere in the code.

## What you build

1. A parser for pipelines, triggers, linked services, datasets and notebooks.
2. A data flow diagram (Mermaid).
3. Table-level lineage.
4. A schedule and dependency map.
5. A failure runbook for each pipeline: what to check, what to do, whether a rerun is safe.

## Output contract

| File | Content |
|---|---|
| runbook_<pipeline>.md | One per pipeline |
| lineage.csv | source, target, transform, notebook_or_activity |
| dataflow.mmd | Mermaid data flow diagram |

## How you'll be judged on proof

A support engineer who has never seen the project answers 5 operational questions using only your generated documents.

## Ground rules

- All data in this kit is synthetic. Names, emails and identifiers are invented.
- Do not upload any customer data, and do not put credentials or secrets in prompts or code.
- Use only the approved AI tools on the provided sandbox.
- Anything that changes data or systems needs a human approval step.
- If you can't explain it in Q&A, it doesn't count.
