from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from automation_pipeline_orchestrator.contract import (
    PipelineDefinition,
    pipeline_from_dict,
)


class PipelineLoadError(Exception):
    """Raised when pipeline YAML cannot be loaded."""


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    pipeline_path = Path(path)

    if not pipeline_path.exists():
        raise PipelineLoadError(f"Pipeline file not found: {pipeline_path}")

    if not pipeline_path.is_file():
        raise PipelineLoadError(f"Pipeline path is not a file: {pipeline_path}")

    try:
        payload = yaml.safe_load(pipeline_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PipelineLoadError(f"Invalid pipeline YAML: {pipeline_path}") from exc

    if payload is None:
        raise PipelineLoadError(f"Pipeline file is empty: {pipeline_path}")

    if not isinstance(payload, dict):
        raise PipelineLoadError(
            f"Pipeline YAML root must be a dictionary: {pipeline_path}"
        )

    return payload


def load_pipeline(path: str | Path) -> PipelineDefinition:
    payload = load_yaml_file(path)
    return pipeline_from_dict(payload)
