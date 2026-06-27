import json
from pathlib import Path

from automation_pipeline_orchestrator.loader import load_pipeline


def test_file_event_sample_exists():
    event_file = Path("examples/file_event.sample.json")

    assert event_file.exists()


def test_file_event_sample_contract():
    event_file = Path("examples/file_event.sample.json")
    payload = json.loads(event_file.read_text(encoding="utf-8"))

    assert payload["event_type"] == "file_detected"
    assert payload["source_utility"] == "file_watcher_automation_mvp"
    assert payload["event_id"] == "sample-file-event-001"
    assert payload["file_path"] == "data/inbox/sample.txt"
    assert payload["pipeline_file"] == "pipelines/sample.pipeline.yaml"


def test_pipeline_execution_sample_exists():
    log_file = Path("examples/pipeline_execution.sample.json")

    assert log_file.exists()


def test_pipeline_execution_sample_contract():
    log_file = Path("examples/pipeline_execution.sample.json")
    payload = json.loads(log_file.read_text(encoding="utf-8"))

    assert payload["event_type"] == "pipeline_execution"
    assert payload["pipeline_id"] == "sample_file_to_notification"
    assert payload["status"] == "success"
    assert payload["stages_executed"] == 2
    assert payload["stages"][0]["stage_id"] == "workflow"
    assert payload["stages"][1]["stage_id"] == "notification"


def test_sample_pipeline_yaml_loads():
    pipeline = load_pipeline("pipelines/sample.pipeline.yaml")

    assert pipeline.pipeline_id == "sample_file_to_notification"
    assert pipeline.workflow.command == "workflow-runner"
    assert pipeline.notification.command == "telegram-notifier"


def test_full_pipeline_integration_doc_exists():
    doc_file = Path("examples/full_pipeline_integration_example.md")

    assert doc_file.exists()

    content = doc_file.read_text(encoding="utf-8")

    assert "Utility #7" in content
    assert "Utility #8" in content
    assert "Utility #9" in content
    assert "Utility #10" in content
    assert "No direct package dependency" in content
    assert "JSON/YAML contracts" in content
