from __future__ import annotations

import argparse
import sys

from automation_pipeline_orchestrator.loader import PipelineLoadError, load_pipeline
from automation_pipeline_orchestrator.logger import write_pipeline_log
from automation_pipeline_orchestrator.orchestrator import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="automation-orchestrator",
        description="Run RADAR Services automation pipelines.",
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="Run a pipeline YAML file.",
    )
    run_parser.add_argument(
        "pipeline_file",
        help="Path to pipeline YAML file.",
    )
    run_parser.add_argument(
        "--log-json",
        help="Write pipeline execution log to a JSON file.",
    )

    return parser


def run_command(args: argparse.Namespace) -> int:
    try:
        pipeline = load_pipeline(args.pipeline_file)
        result = run_pipeline(pipeline)
    except PipelineLoadError as exc:
        print(f"Pipeline failed to start: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print(f"Pipeline completed: {result.pipeline_id}")
    print(f"Status: {result.status}")
    print(f"Stages executed: {result.stages_executed}")

    if args.log_json:
        log_info = write_pipeline_log(result, args.log_json)
        print(f"Pipeline log written: {log_info['log_path']}")

    if result.error:
        print(f"Error: {result.error}", file=sys.stderr)

    return 0 if result.status == "success" else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        return run_command(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
