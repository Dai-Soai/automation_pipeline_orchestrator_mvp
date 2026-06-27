import json
from pathlib import Path

from automation_pipeline_orchestrator.contract import PipelineResult, StageResult
from automation_pipeline_orchestrator.logger import (
    pipeline_result_to_dict,
    write_pipeline_log,
)


def test_pipeline_result_to_dict():
    result = PipelineResult(
        pipeline_id="sample_pipeline",
        status="success",
        stages=[
            StageResult(
                stage_id="workflow",
                status="success",
                command=[
                    "workflow-runner",
                    "run",
                    "examples/workflow.sample.yaml",
                    "--log-json",
                    "logs/execution.sample.json",
                ],
                exit_code=0,
                output="Workflow completed",
            ),
            StageResult(
                stage_id="notification",
                status="success",
                command=[
                    "telegram-notifier",
                    "send-log",
                    "logs/execution.sample.json",
                ],
                exit_code=0,
                output="Telegram sent",
            ),
        ],
    )

    payload = pipeline_result_to_dict(result)

    assert payload["event_type"] == "pipeline_execution"
    assert payload["pipeline_id"] == "sample_pipeline"
    assert payload["status"] == "success"
    assert payload["stages_executed"] == 2
    assert payload["error"] is None
    assert "timestamp" in payload
    assert payload["stages"][0]["stage_id"] == "workflow"
    assert payload["stages"][1]["stage_id"] == "notification"


def test_write_pipeline_log(tmp_path: Path):
    log_file = tmp_path / "logs" / "pipeline.json"

    result = PipelineResult(
        pipeline_id="sample_pipeline",
        status="failed",
        stages=[
            StageResult(
                stage_id="workflow",
                status="success",
                command=["workflow-runner"],
                exit_code=0,
                output="Workflow completed",
            ),
            StageResult(
                stage_id="notification",
                status="failed",
                command=["telegram-notifier"],
                exit_code=1,
                error="Telegram failed",
            ),
        ],
        error="Telegram failed",
    )

    info = write_pipeline_log(result, log_file)

    assert log_file.exists()
    assert info["log_path"] == str(log_file)
    assert info["bytes_written"] > 0

    payload = json.loads(log_file.read_text(encoding="utf-8"))

    assert payload["event_type"] == "pipeline_execution"
    assert payload["pipeline_id"] == "sample_pipeline"
    assert payload["status"] == "failed"
    assert payload["stages_executed"] == 2
    assert payload["error"] == "Telegram failed"
    assert payload["stages"][1]["status"] == "failed"
