from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_readme_discovery_sections():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for section in (
        "## At a Glance",
        "## Install",
        "## Verified Quickstart",
        "## GitHub Action",
        "## Runtime, Data, and Network Boundary",
        "## Limitations",
        "## Publication Status",
        "## Next Action",
    ):
        assert section in readme


def test_pyproject_discovery_metadata():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["readme"] == "README.md"
    assert project["authors"][0]["email"] == "opensource@auraone.ai"
    assert {"lerobot", "training-readiness", "robotics-datasets"} <= set(project["keywords"])
    assert "Topic :: Scientific/Engineering :: Artificial Intelligence" in project["classifiers"]
    assert "Topic :: Scientific/Engineering :: Robotics" not in project["classifiers"]
    assert {"Source", "Documentation", "Issues", "Changelog", "Security", "GitHub Action"} <= set(project["urls"])


def test_action_metadata_stays_checkout_installable():
    action = (ROOT / "action.yml").read_text(encoding="utf-8")
    assert 'python -m pip install "${{ github.action_path }}"' in action
    assert 'description: Repository-relative path to the local LeRobot-style dataset directory.' in action
