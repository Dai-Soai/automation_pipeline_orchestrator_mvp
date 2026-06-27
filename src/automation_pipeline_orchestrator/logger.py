from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from automation_pipeline_orchestrator.contract import PipelineResult


def pipeline_result_to_dict(result: PipelineResult) -> dict[str, Any]:
    return {
        "event_type": "pipeline_execution",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_id": result.pipeline_id,
        "status": result.status,
        "stages_executed": result.stages_executed,
        "error": result.error,
        "stages": [
            {
                "stage_id": stage.stage_id,
                "status": stage.status,
                "command": stage.command,
                "exit_code": stage.exit_code,
                "output": stage.output,
                "error": stage.error,
            }
            for stage in result.stages
        ],
    }


def write_pipeline_log(
    result: PipelineResult,
    log_path: str | Path,
) -> dict[str, Any]:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = pipeline_result_to_dict(result)

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "log_path": str(path),
        "bytes_written": path.stat().st_size,
    }
