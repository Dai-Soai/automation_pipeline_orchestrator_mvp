from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PipelineStatus = Literal["success", "failed"]
StageStatus = Literal["success", "failed", "skipped"]


@dataclass(frozen=True)
class WorkflowStageConfig:
    """
    Configuration for the Workflow Runner stage.
    """

    command: str
    workflow_file: str
    log_json: str


@dataclass(frozen=True)
class NotificationStageConfig:
    """
    Configuration for the Telegram Notification Hub stage.
    """

    command: str
    mode: str
    log_file: str


@dataclass(frozen=True)
class PipelineDefinition:
    """
    Top-level pipeline definition.
    """

    pipeline_id: str
    version: str
    workflow: WorkflowStageConfig
    notification: NotificationStageConfig


@dataclass(frozen=True)
class StageResult:
    """
    Result of one pipeline stage.
    """

    stage_id: str
    status: StageStatus
    command: list[str]
    exit_code: int | None = None
    output: str | None = None
    error: str | None = None


@dataclass(frozen=True)
class PipelineResult:
    """
    Final pipeline execution result.
    """

    pipeline_id: str
    status: PipelineStatus
    stages: list[StageResult] = field(default_factory=list)
    error: str | None = None

    @property
    def stages_executed(self) -> int:
        return len(self.stages)

    @property
    def failed_stages(self) -> list[StageResult]:
        return [stage for stage in self.stages if stage.status == "failed"]

    @property
    def succeeded_stages(self) -> list[StageResult]:
        return [stage for stage in self.stages if stage.status == "success"]


def pipeline_from_dict(payload: dict) -> PipelineDefinition:
    workflow_payload = payload.get("workflow") or {}
    notification_payload = payload.get("notification") or {}

    workflow = WorkflowStageConfig(
        command=str(workflow_payload.get("command", "")),
        workflow_file=str(workflow_payload.get("workflow_file", "")),
        log_json=str(workflow_payload.get("log_json", "")),
    )

    notification = NotificationStageConfig(
        command=str(notification_payload.get("command", "")),
        mode=str(notification_payload.get("mode", "")),
        log_file=str(notification_payload.get("log_file", "")),
    )

    return PipelineDefinition(
        pipeline_id=str(payload.get("pipeline_id", "")),
        version=str(payload.get("version", "")),
        workflow=workflow,
        notification=notification,
    )
