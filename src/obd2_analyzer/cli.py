from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import AnalysisResult, analyze_file


LABELS = {
    "rpm": ("RPM", "rpm"),
    "speed_kph": ("Speed", "km/h"),
    "coolant_temp_c": ("Coolant", "°C"),
    "battery_voltage": ("Battery", "V"),
    "stft_percent": ("STFT", "%"),
    "ltft_percent": ("LTFT", "%"),
    "maf_gps": ("MAF", "g/s"),
    "throttle_percent": ("Throttle", "%"),
}


def _format_metric(name: str, result: AnalysisResult) -> str | None:
    metric = result.metrics[name]

    if metric.minimum is None or metric.maximum is None:
        return None

    label, unit = LABELS[name]
    return f"{label}: {metric.minimum:.1f} - {metric.maximum:.1f} {unit}"


def print_summary(result: AnalysisResult) -> None:
    print("OBD-II Log Summary")
    print("------------------")
    print(f"Samples: {result.samples}")

    for name in LABELS:
        line = _format_metric(name, result)
        if line:
            print(line)

    print(f"DTCs: {', '.join(result.dtcs) if result.dtcs else 'None'}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")
    else:
        print("\nWarnings: None")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a CSV OBD-II log and print a health summary."
    )
    parser.add_argument("csv_file", type=Path, help="Path to OBD-II CSV log")
    parser.add_argument(
        "--json",
        dest="json_output",
        type=Path,
        help="Optional JSON output path",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = analyze_file(args.csv_file)
    print_summary(result)

    if args.json_output:
        args.json_output.write_text(
            json.dumps(result.to_dict(), indent=2),
            encoding="utf-8",
        )
        print(f"\nJSON report written to {args.json_output}")


if __name__ == "__main__":
    main()
