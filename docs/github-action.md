# GitHub Action

The composite Action checks a local LeRobot-style dataset directory and fails
when findings meet the configured severity threshold. The Action writes the
selected report format to the job log; use the CLI when a durable report file is
required.

Use immutable commit pins:

```yaml
name: dataset-quality

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  lerobot-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: auraoneai/lerobot-quality-gates@3d46690c322914e9a90b1310b86ea7f3bba32747 # v0.1.7
        with:
          path: datasets/review-candidate
          fail-on: high
          format: markdown
```

The Action does not expose the CLI's `--hf-repo` mode and does not download
dataset media. It installs its Python package from the Action checkout. The
Action and PyPI package are released as `0.1.7`.

To save a report as an artifact, run the registry package directly:

```yaml
- run: python -m pip install "lerobot-quality-gates==0.1.7"
- run: lerobot-quality-gates check datasets/review-candidate --format json --out lerobot-quality-report.json
```
