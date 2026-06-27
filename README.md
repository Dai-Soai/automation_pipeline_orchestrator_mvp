# Automation Pipeline Orchestrator MVP

A minimal orchestration layer for RADAR Services automation pipelines.

## Status

MVP Stable

Current version:

```text
v0.1.0
```

Current test status:

```text
32 passed
```

## Purpose

Automation Pipeline Orchestrator MVP coordinates existing RADAR Services utilities through YAML pipeline configs.

It does not replace File Watcher, Workflow Runner, or Telegram Notification Hub.  
It orchestrates them through CLI adapters and JSON/YAML contracts.

## Core Flow

```text
pipeline.yaml
    ↓
Workflow Runner
    ↓
execution_log.json
    ↓
Telegram Notification Hub
    ↓
pipeline_log.json
```

## Integrated Utilities

```text
Utility #7 — File Watcher Automation MVP
Utility #8 — Workflow Runner MVP
Utility #9 — Telegram Notification Hub MVP
Utility #10 — Automation Pipeline Orchestrator MVP
```

## Features

- YAML pipeline definition
- Pipeline contract dataclasses
- YAML pipeline loader
- Workflow Runner adapter
- Telegram Notification Hub adapter
- CLI orchestrator
- JSON pipeline execution log
- Full pipeline integration example
- Pytest coverage

## Example Pipeline YAML

```yaml
pipeline_id: sample_file_to_notification
version: "0.1.0"

workflow:
  command: workflow-runner
  workflow_file: examples/workflow.sample.yaml
  log_json: logs/execution.sample.json

notification:
  command: telegram-notifier
  mode: send-log
  log_file: logs/execution.sample.json
```

## Installation

Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install package in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

## Usage

Show CLI help:

```bash
automation-orchestrator
```

Run sample pipeline:

```bash
automation-orchestrator run pipelines/sample.pipeline.yaml
```

Run sample pipeline and write pipeline log:

```bash
automation-orchestrator run pipelines/sample.pipeline.yaml \
  --log-json logs/pipeline.sample.json
```

Expected output:

```text
Pipeline completed: sample_file_to_notification
Status: success
Stages executed: 2
Pipeline log written: logs/pipeline.sample.json
```

## Pipeline Log Example

```json
{
  "event_type": "pipeline_execution",
  "pipeline_id": "sample_file_to_notification",
  "status": "success",
  "stages_executed": 2,
  "error": null,
  "stages": [
    {
      "stage_id": "workflow",
      "status": "success"
    },
    {
      "stage_id": "notification",
      "status": "success"
    }
  ]
}
```

## Integration Boundary

Utility #7 owns:

- file detection
- file event JSON
- inbox/archive movement
- file watcher event log

Utility #8 owns:

- workflow YAML loading
- workflow validation
- sequential step execution
- workflow execution log JSON

Utility #9 owns:

- workflow execution log reading
- notification formatting
- Telegram delivery

Utility #10 owns:

- pipeline YAML loading
- orchestration order
- CLI adapter execution
- pipeline execution log JSON

No direct package dependency is introduced between Utility #7, Utility #8, Utility #9, and Utility #10.

Utility #10 coordinates the pipeline through CLI adapters and JSON/YAML contracts.

## Project Structure

```text
automation_pipeline_orchestrator_mvp/
├── README.md
├── pyproject.toml
├── examples/
│   ├── file_event.sample.json
│   ├── full_pipeline_integration_example.md
│   └── pipeline_execution.sample.json
├── pipelines/
│   └── sample.pipeline.yaml
├── src/
│   └── automation_pipeline_orchestrator/
│       ├── __init__.py
│       ├── cli.py
│       ├── contract.py
│       ├── loader.py
│       ├── logger.py
│       ├── notification_adapter.py
│       ├── orchestrator.py
│       └── workflow_adapter.py
└── tests/
    ├── test_bootstrap.py
    ├── test_cli.py
    ├── test_contract.py
    ├── test_integration_examples.py
    ├── test_loader.py
    ├── test_logger.py
    ├── test_notification_adapter.py
    ├── test_orchestrator.py
    └── test_workflow_adapter.py
```

## Development

Run tests:

```bash
pytest
```

Expected:

```text
32 passed
```

## Package Build

Install build tool:

```bash
python -m pip install build
```

Build package:

```bash
python -m build
```

Expected artifacts:

```text
dist/
├── automation_pipeline_orchestrator_mvp-0.1.0.tar.gz
└── automation_pipeline_orchestrator_mvp-0.1.0-py3-none-any.whl
```

## MVP Scope

Locked for v0.1.0:

- Local YAML pipeline execution
- Sequential two-stage orchestration
- Workflow Runner adapter
- Telegram Notification Hub adapter
- JSON pipeline log
- CLI runner
- Full integration example

Out of scope for v0.1.0:

- Parallel stage execution
- Retry queue
- Scheduler
- Dynamic plugin discovery
- Runtime event bus
- Dashboard UI
- Remote execution
- Direct package dependency between utilities

## Roadmap

Future ideas:

- Retry policy
- Timeout policy
- Conditional stages
- Multi-pipeline routing
- File Watcher direct trigger mode
- Scheduler integration
- Pipeline template registry
- Job history viewer
- Dashboard integration
- RADAR Runtime bridge

## Release Notes

### v0.1.0

Initial MVP release.

Completed milestones:

- M1 Bootstrap Project
- M2 Pipeline Contract
- M3 YAML Pipeline Loader
- M4 Workflow Runner Adapter
- M5 Notification Hub Adapter
- M6 CLI Orchestrator
- M7 JSON Pipeline Log
- M8 Full Pipeline Integration Example

Test status:

```text
32 passed
```

## License

Internal RADAR Services utility.
