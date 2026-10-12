# Legacy evidence brief validator

Optional tooling for the `evidence-brief/v1` artifact format. This directory is not an installed skill; the new research skill does not require this format or its restrictive accounting rules.

Read [the format contract](references/evidence-brief-schema.md) when validating an existing artifact. From this directory, run:

```bash
python3 scripts/validate_evidence_brief.py /path/to/evidence-brief.json
python3 -m unittest discover -s tests -p 'test_*.py'
```

The validator checks structural and semantic consistency against the old contract. Passing it does not prove source accuracy or that the research question was answered.
