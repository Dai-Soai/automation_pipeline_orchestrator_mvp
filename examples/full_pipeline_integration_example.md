# Full Pipeline Integration Example

## Purpose

This document describes how Utility #10 — Automation Pipeline Orchestrator MVP connects Utility #7, Utility #8, and Utility #9 through contract-based integration.

## Integration Flow

```text
Utility #7 — File Watcher Automation MVP
        ↓
file event JSON
        ↓
Utility #10 — Automation Pipeline Orchestrator MVP
        ↓
pipeline YAML
        ↓
Utility #8 — Workflow Runner MVP
        ↓
execution log JSON
        ↓
Utility #9 — Telegram Notification Hub MVP
        ↓
Telegram notification
        ↓
Utility #10 — pipeline execution log JSON
```

## Contract Boundary

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

## Locked Decision

No direct package dependency is introduced between Utility #7, Utility #8, Utility #9 and Utility #10.

Utility #10 coordinates the pipeline through CLI adapters and JSON/YAML contracts.
