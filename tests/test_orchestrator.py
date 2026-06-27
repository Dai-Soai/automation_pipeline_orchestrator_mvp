from automation_pipeline_orchestrator.contract import (
    NotificationStageConfig,
    PipelineDefinition,
    StageResult,
    WorkflowStageConfig,
)
from automation_pipeline_orchestrator import orchestrator


def make_pipeline() -> PipelineDefinition:
    return PipelineDefinition(
        pipeline_id="sample_pipeline",
        version="0.1.0",
        workflow=WorkflowStageConfig(
            command="workflow-runner",
            workflow_file="examples/workflow.sample.yaml",
            log_json="logs/execution.sample.json",
        ),
        notification=NotificationStageConfig(
            command="telegram-notifier",
            mode="send-log",
            log_file="logs/execution.sample.json",
        ),
    )


def test_run_pipeline_success(monkeypatch):
    monkeypatch.setattr(
        orchestrator,
        "run_workflow_stage",
        lambda config: StageResult(
            stage_id="workflow",
            status="success",
            command=["workflow-runner"],
            exit_code=0,
            output="Workflow completed",
        ),
    )
    monkeypatch.setattr(
        orchestrator,
        "run_notification_stage",
        lambda config: StageResult(
            stage_id="notification",
            status="success",
            command=["telegram-notifier"],
            exit_code=0,
            output="Telegram sent",
        ),
    )

    result = orchestrator.run_pipeline(make_pipeline())

    assert result.status == "success"
    assert result.pipeline_id == "sample_pipeline"
    assert result.stages_executed == 2
    assert len(result.failed_stages) == 0


def test_run_pipeline_stops_on_workflow_failure(monkeypatch):
    monkeypatch.setattr(
        orchestrator,
        "run_workflow_stage",
        lambda config: StageResult(
            stage_id="workflow",
            status="failed",
            command=["workflow-runner"],
            exit_code=1,
            error="workflow failed",
        ),
    )

    result = orchestrator.run_pipeline(make_pipeline())

    assert result.status == "failed"
    assert result.stages_executed == 1
    assert result.failed_stages[0].stage_id == "workflow"
    assert result.error == "workflow failed"


def test_run_pipeline_fails_on_notification_failure(monkeypatch):
    monkeypatch.setattr(
        orchestrator,
        "run_workflow_stage",
        lambda config: StageResult(
            stage_id="workflow",
            status="success",
            command=["workflow-runner"],
            exit_code=0,
        ),
    )
    monkeypatch.setattr(
        orchestrator,
        "run_notification_stage",
        lambda config: StageResult(
            stage_id="notification",
            status="failed",
            command=["telegram-notifier"],
            exit_code=1,
            error="notification failed",
        ),
    )

    result = orchestrator.run_pipeline(make_pipeline())

    assert result.status == "failed"
    assert result.stages_executed == 2
    assert result.failed_stages[0].stage_id == "notification"
    assert result.error == "notification failed"
