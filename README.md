# lerobot-quality-gates

`lerobot-quality-gates` checks a LeRobot-style dataset's metadata, episode
records, sensor and video references, intervention labels, and dataset-card
disclosures before training or publication review.

## At a Glance

| | |
| --- | --- |
| Job | Fail fast on deterministic dataset packaging and documentation gaps. |
| Built for | Robotics dataset teams, training pipeline owners, and release reviewers. |
| Differentiator | Local checks plus lightweight Hugging Face metadata inspection without downloading media. |
| Produces | Markdown, JSON, Hugging Face card snippets, or badge JSON with severity-ranked findings. |

## Install

```bash
python -m pip install "lerobot-quality-gates==0.1.7"
```

## Verified Quickstart

Run from a source checkout:

```bash
lerobot-quality-gates check examples/mock_lerobot_v3_good \
  --format json \
  --out /tmp/lerobot-quality-report.json \
  --fail-on high
```

The bundled good fixture contains two episodes and returns zero findings. The
bad fixture is intentionally incomplete and can return exit code `1`.

## Gate Families

- required `meta/info.json` fields and declared feature shapes;
- `meta/episodes.json` IDs, tasks, frame counts, timestamps, and data references;
- timestamp monotonicity and frame-count consistency;
- declared action/state shape consistency;
- camera feature to video-file reference coverage;
- intervention and recovery labels when the dataset claims those modes;
- README disclosure for mock/tutorial data and limitations.

The v1 checks inspect metadata and file references. They do not decode videos,
load training shards, evaluate demonstrations, or establish model readiness.

## Lightweight Hugging Face Inspection

```bash
lerobot-quality-gates check \
  --hf-repo owner/dataset-name \
  --format hf-card \
  --out /tmp/QA.md
```

This mode requests only `README.md`, `meta/info.json`, and
`meta/episodes.json` from `huggingface.co`. It does not request videos or full
data shards.

## GitHub Action

Pin the published Action to its immutable release commit:

```yaml
- uses: auraoneai/lerobot-quality-gates@4357e8229337af4f33091bccf96fee4886e829f7 # v0.1.6
  with:
    path: datasets/review-candidate
    fail-on: high
    format: markdown
```

See [`docs/github-action.md`](docs/github-action.md) for the complete workflow.
The Action supports local paths only and writes its report to the job log.

## Runtime, Data, and Network Boundary

- Local mode reads dataset metadata, README text, and referenced file paths. It
  does not make network requests.
- Local JSON and Markdown reports include an absolute dataset root plus finding
  paths. Review them before sharing.
- `--hf-repo` performs outbound HTTPS reads to Hugging Face for the three
  lightweight files listed above.
- The composite Action may contact the configured Python package index while
  installing build requirements.

## Limitations

- The checks operate on metadata and file references. They do not decode videos,
  inspect shard contents, or measure demonstration quality.
- Passing gates does not establish training readiness, benchmark quality, robot
  safety, or completeness of a downstream dataset review.

## Compatibility

`robostudio-engine` exposes a direct `robostudio quality-gates` integration that
imports this package or invokes its CLI when installed. The output remains a
dataset quality diagnostic, not a robot safety certification, benchmark, or
expert-review claim.

## Publication Status

Verified on 2026-07-13:

- PyPI: [`lerobot-quality-gates==0.1.7`](https://pypi.org/project/lerobot-quality-gates/0.1.7/)
- GitHub Action release: [`v0.1.7`](https://github.com/auraoneai/lerobot-quality-gates/releases/tag/v0.1.7)
- The Action and PyPI package share release `0.1.7`; the Action installs the
  package source from its checked-out immutable commit.
- All checked-in datasets are synthetic tutorial fixtures.

## Next Action

Run the gate on a review candidate before training, triage every high finding,
and paste the generated Hugging Face snippet into the dataset card.
