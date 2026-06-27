from __future__ import annotations

from automation_pipeline_orchestrator.contract import (
    PipelineDefinition,
    PipelineResult,
    StageResult,
)
from automation_pipeline_orchestrator.notification_adapter import run_notification_stage
from automation_pipeline_orchestrator.workflow_adapter import run_workflow_stage


def run_pipeline(pipeline: PipelineDefinition) -> PipelineResult:
    stages: list[StageResult] = []

    workflow_result = run_workflow_stage(pipeline.workflow)
    stages.append(workflow_result)

    if workflow_result.status == "failed":
        return PipelineResult(
            pipeline_id=pipeline.pipeline_id,
            status="failed",
            stages=stages,
            error=workflow_result.error or "workflow stage failed",
        )

    notification_result = run_notification_stage(pipeline.notification)
    stages.append(notification_result)

    if notification_result.status == "failed":
        return PipelineResult(
            pipeline_id=pipeline.pipeline_id,
            status="failed",
            stages=stages,
            error=notification_result.error or "notification stage failed",
        )

    return PipelineResult(
        pipeline_id=pipeline.pipeline_id,
        status="success",
        stages=stages,
    )
