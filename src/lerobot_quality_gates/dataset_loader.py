from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Episode:
    episode_id: int
    task: str | None
    frames: int | None
    start_time: float | None
    end_time: float | None
    data_path: str | None
    video_paths: dict[str, str]
    action_shape: list[int] | None
    state_shape: list[int] | None
    timestamps: list[float]
    interventions: list[dict[str, Any]]


@dataclass(frozen=True)
class DatasetInfo:
    root: Path
    info: dict[str, Any]
    episodes: list[Episode]
    readme: str


def load_dataset(path: str | Path) -> DatasetInfo:
    root = Path(path).resolve()
    info = _read_json(root / "meta" / "info.json")
    episodes_payload = _read_json(root / "meta" / "episodes.json")
    episodes_raw = episodes_payload.get("episodes", episodes_payload if isinstance(episodes_payload, list) else [])
    episodes = [_episode_from_dict(item) for item in episodes_raw if isinstance(item, dict)]
    readme = _read_optional_text(root / "README.md")
    return DatasetInfo(root=root, info=info if isinstance(info, dict) else {}, episodes=episodes, readme=readme)


def _episode_from_dict(item: dict[str, Any]) -> Episode:
    return Episode(
        episode_id=int(item.get("episode_id", item.get("id", -1))),
        task=item.get("task"),
        frames=_int_or_none(item.get("frames")),
        start_time=_float_or_none(item.get("start_time")),
        end_time=_float_or_none(item.get("end_time")),
        data_path=item.get("data_path"),
        video_paths=dict(item.get("video_paths", {})),
        action_shape=_shape_or_none(item.get("action_shape")),
        state_shape=_shape_or_none(item.get("state_shape")),
        timestamps=[float(value) for value in item.get("timestamps", []) if isinstance(value, int | float)],
        interventions=list(item.get("interventions", [])),
    )


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _read_optional_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf8")
    except OSError:
        return ""


def _int_or_none(value: Any) -> int | None:
    return value if isinstance(value, int) else None


def _float_or_none(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) else None


def _shape_or_none(value: Any) -> list[int] | None:
    if isinstance(value, list) and all(isinstance(item, int) for item in value):
        return value
    return None
