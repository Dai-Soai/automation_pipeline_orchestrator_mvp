from automation_pipeline_orchestrator.contract import (
    NotificationStageConfig,
    PipelineDefinition,
    PipelineResult,
    StageResult,
    WorkflowStageConfig,
    pipeline_from_dict,
)


def test_pipeline_contract_dataclasses():
    pipeline = PipelineDefinition(
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

    assert pipeline.pipeline_id == "sample_pipeline"
    assert pipeline.version == "0.1.0"
    assert pipeline.workflow.command == "workflow-runner"
    assert pipeline.workflow.workflow_file == "examples/workflow.sample.yaml"
    assert pipeline.workflow.log_json == "logs/execution.sample.json"
    assert pipeline.notification.command == "telegram-notifier"
    assert pipeline.notification.mode == "send-log"
    assert pipeline.notification.log_file == "logs/execution.sample.json"


def test_pipeline_result_helpers():
    result = PipelineResult(
        pipeline_id="sample_pipeline",
        status="failed",
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
                status="failed",
                command=[
                    "telegram-notifier",
                    "send-log",
                    "logs/execution.sample.json",
                ],
                exit_code=1,
                error="Telegram notification failed",
            ),
        ],
        error="notification failed",
    )

    assert result.stages_executed == 2
    assert len(result.succeeded_stages) == 1
    assert len(result.failed_stages) == 1
    assert result.failed_stages[0].stage_id == "notification"


def test_pipeline_from_dict():
    payload = {
        "pipeline_id": "sample_pipeline",
        "version": "0.1.0",
        "workflow": {
            "command": "workflow-runner",
            "workflow_file": "examples/workflow.sample.yaml",
            "log_json": "logs/execution.sample.json",
        },
        "notification": {
            "command": "telegram-notifier",
            "mode": "send-log",
            "log_file": "logs/execution.sample.json",
        },
    }

    pipeline = pipeline_from_dict(payload)

    assert pipeline.pipeline_id == "sample_pipeline"
    assert pipeline.version == "0.1.0"
    assert pipeline.workflow.command == "workflow-runner"
    assert pipeline.workflow.workflow_file == "examples/workflow.sample.yaml"
    assert pipeline.workflow.log_json == "logs/execution.sample.json"
    assert pipeline.notification.command == "telegram-notifier"
    assert pipeline.notification.mode == "send-log"
    assert pipeline.notification.log_file == "logs/execution.sample.json"
