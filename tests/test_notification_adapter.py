import subprocess

from automation_pipeline_orchestrator.contract import NotificationStageConfig
from automation_pipeline_orchestrator.notification_adapter import (
    build_notification_command,
    run_notification_stage,
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


def make_notification_config() -> NotificationStageConfig:
    return NotificationStageConfig(
        command="telegram-notifier",
        mode="send-log",
        log_file="logs/execution.sample.json",
    )


def test_build_notification_command():
    config = make_notification_config()

    command = build_notification_command(config)

    assert command == [
        "telegram-notifier",
        "send-log",
        "logs/execution.sample.json",
    ]


def test_run_notification_stage_success():
    config = make_notification_config()
    runner = FakeCommandRunner(
        subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="Telegram workflow notification sent",
            stderr="",
        )
    )

    result = run_notification_stage(config, runner=runner)

    assert result.stage_id == "notification"
    assert result.status == "success"
    assert result.exit_code == 0
    assert result.output == "Telegram workflow notification sent"
    assert result.error is None
    assert runner.last_command == [
        "telegram-notifier",
        "send-log",
        "logs/execution.sample.json",
    ]


def test_run_notification_stage_failure():
    config = make_notification_config()
    runner = FakeCommandRunner(
        subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="Telegram workflow notification failed",
        )
    )

    result = run_notification_stage(config, runner=runner)

    assert result.stage_id == "notification"
    assert result.status == "failed"
    assert result.exit_code == 1
    assert result.output == ""
    assert result.error == "Telegram workflow notification failed"


def test_run_notification_stage_exception():
    config = make_notification_config()
    runner = RaisingCommandRunner()

    result = run_notification_stage(config, runner=runner)

    assert result.stage_id == "notification"
    assert result.status == "failed"
    assert result.exit_code is None
    assert result.error == "command not found"
