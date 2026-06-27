from pathlib import Path

from automation_pipeline_orchestrator.cli import main
from automation_pipeline_orchestrator.contract import PipelineResult, StageResult


def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["automation-orchestrator"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Run RADAR Services automation pipelines" in captured.out


def test_cli_run_success(tmp_path: Path, monkeypatch, capsys):
    pipeline_file = tmp_path / "pipeline.yaml"
    log_file = tmp_path / "logs" / "pipeline.json"
    pipeline_file.write_text(
        """
pipeline_id: cli_pipeline
version: "0.1.0"

workflow:
  command: workflow-runner
  workflow_file: examples/workflow.sample.yaml
  log_json: logs/execution.sample.json

notification:
  command: telegram-notifier
  mode: send-log
  log_file: tmp_path / "pipeline-log.json"
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "automation_pipeline_orchestrator.cli.run_pipeline",
        lambda pipeline: PipelineResult(
            pipeline_id=pipeline.pipeline_id,
            status="success",
            stages=[
                StageResult(
                    stage_id="workflow",
                    status="success",
                    command=["workflow-runner"],
                    exit_code=0,
                ),
                StageResult(
                    stage_id="notification",
                    status="success",
                    command=["telegram-notifier"],
                    exit_code=0,
                ),
            ],
        ),
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "automation-orchestrator",
            "run",
            str(pipeline_file),
            "--log-json",
            str(log_file),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Pipeline completed: cli_pipeline" in captured.out
    assert "Status: success" in captured.out
    assert "Stages executed: 2" in captured.out
    assert "Pipeline log written:" in captured.out
    assert log_file.exists()


def test_cli_run_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["automation-orchestrator", "run", "missing.pipeline.yaml"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Pipeline failed to start" in captured.err


def test_cli_run_with_json_log(tmp_path: Path, monkeypatch, capsys):
    pipeline_file = tmp_path / "pipeline.yaml"
    log_file = tmp_path / "logs" / "pipeline.json"

    pipeline_file.write_text(
        """
pipeline_id: cli_pipeline
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

    monkeypatch.setattr(
        "automation_pipeline_orchestrator.cli.run_pipeline",
        lambda pipeline: PipelineResult(
            pipeline_id=pipeline.pipeline_id,
            status="success",
            stages=[
                StageResult(
                    stage_id="workflow",
                    status="success",
                    command=["workflow-runner"],
                    exit_code=0,
                ),
                StageResult(
                    stage_id="notification",
                    status="success",
                    command=["telegram-notifier"],
                    exit_code=0,
                ),
            ],
        ),
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "automation-orchestrator",
            "run",
            str(pipeline_file),
            "--log-json",
            str(log_file),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Pipeline log written:" in captured.out
    assert log_file.exists()
