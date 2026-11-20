# lerobot-quality-gates

**LeRobot dataset validator.** Check a LeRobot-style dataset's metadata, episode
records, sensor and video references, intervention labels, and dataset-card
disclosures before training or publication review.

[![PyPI](https://img.shields.io/pypi/v/lerobot-quality-gates)](https://pypi.org/project/lerobot-quality-gates/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/auraoneai/lerobot-quality-gates/blob/main/LICENSE)

```bash
python -m pip install "lerobot-quality-gates==0.1.7"
lerobot-quality-gates check examples/mock_lerobot_v3_good --format json --fail-on high
```

Output on the bundled fixture, run from a source checkout (exit code `0`; `root`
shortened):

```json
{
  "counts": {},
  "episode_count": 2,
  "finding_count": 0,
  "findings": [],
  "remote": false,
  "root": "./examples/mock_lerobot_v3_good",
  "source": "local"
}
```

Add it to CI with the published Action:

```yaml
- uses: auraoneai/lerobot-quality-gates@v0.1.7
  with:
    path: datasets/review-candidate
    fail-on: high
```

## What It Does and Doesn't Do

It does:

- validate `meta/info.json`, `meta/episodes.json`, timestamps, frame counts,
  action/state shapes, camera-to-video references, and intervention labels;
- check the dataset README for mock/tutorial and limitation disclosures;
- emit Markdown, JSON, Hugging Face card snippets, or badge JSON, and fail CI
  at a chosen severity.

It doesn't:

- decode videos, load training shards, or measure demonstration quality;
- establish training readiness, benchmark quality, or robot safety.

Part of the AuraOne robotics dataset QA workflow:
[lerobot-quality-gates](https://auraone.ai/open/lerobot-quality-gates) →
[Robotics Studio](https://auraone.ai/open/robotics-studio).

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
- uses: auraoneai/lerobot-quality-gates@3d46690c322914e9a90b1310b86ea7f3bba32747 # v0.1.7
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

---

Need reviewed demonstration data or dataset quality operations at scale?
[Talk to AuraOne](https://auraone.ai/contact?from=open:lerobot-quality-gates)
