import subprocess

from automation_pipeline_orchestrator.contract import WorkflowStageConfig
from automation_pipeline_orchestrator.workflow_adapter import (
    build_workflow_command,
    run_workflow_stage,
)


class FakeCommandRunner:
    def __init__(self, completed: subprocess.CompletedProcess[str]) -> None:
        self.completed = completed
        self.last_command: list[str] | None = None

    def run(
        self,
        command: list[str],
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        self.last_command = command
        return self.completed


class RaisingCommandRunner:
    def run(
        self,
        command: list[str],
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        raise RuntimeError("command not found")


def make_workflow_config() -> WorkflowStageConfig:
    return WorkflowStageConfig(
        command="workflow-runner",
        workflow_file="examples/workflow.sample.yaml",
        log_json="logs/execution.sample.json",
    )


def test_build_workflow_command():
    config = make_workflow_config()

    command = build_workflow_command(config)

    assert command == [
        "workflow-runner",
        "run",
        "examples/workflow.sample.yaml",
        "--log-json",
        "logs/execution.sample.json",
    ]


def test_run_workflow_stage_success():
    config = make_workflow_config()
    runner = FakeCommandRunner(
        subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="Workflow completed",
            stderr="",
        )
    )

    result = run_workflow_stage(config, runner=runner)

    assert result.stage_id == "workflow"
    assert result.status == "success"
    assert result.exit_code == 0
    assert result.output == "Workflow completed"
    assert result.error is None
    assert runner.last_command == [
        "workflow-runner",
        "run",
        "examples/workflow.sample.yaml",
        "--log-json",
        "logs/execution.sample.json",
    ]


def test_run_workflow_stage_failure():
    config = make_workflow_config()
    runner = FakeCommandRunner(
        subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="Workflow failed",
        )
    )

    result = run_workflow_stage(config, runner=runner)

    assert result.stage_id == "workflow"
    assert result.status == "failed"
    assert result.exit_code == 1
    assert result.output == ""
    assert result.error == "Workflow failed"


def test_run_workflow_stage_exception():
    config = make_workflow_config()
    runner = RaisingCommandRunner()

    result = run_workflow_stage(config, runner=runner)

    assert result.stage_id == "workflow"
    assert result.status == "failed"
    assert result.exit_code is None
    assert result.error == "command not found"
