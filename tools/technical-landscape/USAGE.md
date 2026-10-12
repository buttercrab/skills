# Legacy landscape validator

Optional tooling for the `landscape/v2` artifact format. This directory is not an installed skill; the new research skill does not require this format, its coverage accounting, or its inference rules.

Read [the format contract](references/landscape-schema.md) and [the JSON Schema](references/landscape-v2.schema.json) when validating an existing artifact. From this directory, run:

```bash
python3 scripts/validate_landscape.py /path/to/landscape.json
python3 -m unittest discover -s tests -p 'test_*.py'
```

The validator checks structural and semantic consistency against the old contract. Passing it does not prove exhaustive discovery or source accuracy.
