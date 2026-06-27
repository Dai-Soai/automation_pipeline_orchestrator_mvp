# Automation Pipeline Orchestrator MVP

A minimal orchestration layer for RADAR Services automation pipelines.

## Status

MVP in progress.

## Purpose

Coordinates existing RADAR Services utilities through YAML pipeline configs.

## Target Flow

```text
pipeline.yaml
    ↓
workflow-runner
    ↓
execution_log.json
    ↓
telegram-notifier
    ↓
pipeline_log.json
