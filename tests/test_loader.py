from pathlib import Path

import pytest

from automation_pipeline_orchestrator.loader import (
    PipelineLoadError,
    load_pipeline,
    load_yaml_file,
)


def test_load_yaml_file(tmp_path: Path):
    pipeline_file = tmp_path / "pipeline.yaml"
    pipeline_file.write_text(
        """
pipeline_id: sample_pipeline
version: "0.1.0"

workflow:
  command: workflow-runner
  workflow_file: examples/workflow.sample.yaml
  log_json: logs/execution.sample.json

notification:
  command: telegram-notifier
  mode: send-log
  log_file: logs/execution.sample.json
""",
        encoding="utf-8",
    )

    payload = load_yaml_file(pipeline_file)

    assert payload["pipeline_id"] == "sample_pipeline"
    assert payload["version"] == "0.1.0"
    assert payload["workflow"]["command"] == "workflow-runner"
    assert payload["notification"]["command"] == "telegram-notifier"


def test_load_pipeline(tmp_path: Path):
    pipeline_file = tmp_path / "pipeline.yaml"
    pipeline_file.write_text(
        """
pipeline_id: sample_pipeline
version: "0.1.0"

workflow:
  command: workflow-runner
  workflow_file: examples/workflow.sample.yaml
  log_json: logs/execution.sample.json

notification:
  command: telegram-notifier
  mode: send-log
  log_file: logs/execution.sample.json
""",
        encoding="utf-8",
    )

    pipeline = load_pipeline(pipeline_file)

    assert pipeline.pipeline_id == "sample_pipeline"
    assert pipeline.version == "0.1.0"
    assert pipeline.workflow.command == "workflow-runner"
    assert pipeline.workflow.workflow_file == "examples/workflow.sample.yaml"
    assert pipeline.workflow.log_json == "logs/execution.sample.json"
    assert pipeline.notification.command == "telegram-notifier"
    assert pipeline.notification.mode == "send-log"
    assert pipeline.notification.log_file == "logs/execution.sample.json"


def test_load_missing_pipeline_file():
    with pytest.raises(PipelineLoadError, match="Pipeline file not found"):
        load_pipeline("missing.pipeline.yaml")


def test_load_empty_pipeline_file(tmp_path: Path):
    pipeline_file = tmp_path / "empty.pipeline.yaml"
    pipeline_file.write_text("", encoding="utf-8")

    with pytest.raises(PipelineLoadError, match="Pipeline file is empty"):
        load_pipeline(pipeline_file)


def test_load_invalid_yaml_root(tmp_path: Path):
    pipeline_file = tmp_path / "invalid-root.pipeline.yaml"
    pipeline_file.write_text(
        """
- item1
- item2
""",
        encoding="utf-8",
    )

    with pytest.raises(
        PipelineLoadError, match="Pipeline YAML root must be a dictionary"
    ):
        load_pipeline(pipeline_file)
