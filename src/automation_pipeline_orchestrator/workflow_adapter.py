from __future__ import annotations

import subprocess
from typing import Protocol

from automation_pipeline_orchestrator.contract import StageResult, WorkflowStageConfig


class CommandRunner(Protocol):
    def run(
        self,
        command: list[str],
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]: ...


class SubprocessCommandRunner:
    def run(
        self,
        command: list[str],
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            capture_output=capture_output,
            text=text,
        )


def build_workflow_command(config: WorkflowStageConfig) -> list[str]:
    return [
        config.command,
        "run",
        config.workflow_file,
        "--log-json",
        config.log_json,
    ]


def run_workflow_stage(
    config: WorkflowStageConfig,
    runner: CommandRunner | None = None,
) -> StageResult:
    command = build_workflow_command(config)
    command_runner = runner or SubprocessCommandRunner()

    try:
        completed = command_runner.run(
            command,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        return StageResult(
            stage_id="workflow",
            status="failed",
            command=command,
            error=str(exc),
        )

    if completed.returncode == 0:
        return StageResult(
            stage_id="workflow",
            status="success",
            command=command,
            exit_code=completed.returncode,
            output=completed.stdout,
            error=completed.stderr or None,
        )

    return StageResult(
        stage_id="workflow",
        status="failed",
        command=command,
        exit_code=completed.returncode,
        output=completed.stdout,
        error=completed.stderr or None,
    )
