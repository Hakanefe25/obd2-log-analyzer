from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean
from typing import Iterable


NUMERIC_FIELDS = (
    "rpm",
    "speed_kph",
    "coolant_temp_c",
    "battery_voltage",
    "stft_percent",
    "ltft_percent",
    "maf_gps",
    "throttle_percent",
)


@dataclass
class MetricSummary:
    minimum: float | None = None
    maximum: float | None = None
    average: float | None = None


@dataclass
class AnalysisResult:
    samples: int
    metrics: dict[str, MetricSummary]
    dtcs: list[str]
    warnings: list[str]

    def to_dict(self) -> dict:
        return {
            "samples": self.samples,
            "metrics": {key: asdict(value) for key, value in self.metrics.items()},
            "dtcs": self.dtcs,
            "warnings": self.warnings,
        }


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None

    value = value.strip()
    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def load_csv(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)

        if not reader.fieldnames:
            raise ValueError("CSV file does not contain a header row.")

        return list(reader)


def _summarize(values: Iterable[float]) -> MetricSummary:
    values = list(values)

    if not values:
        return MetricSummary()

    return MetricSummary(
        minimum=min(values),
        maximum=max(values),
        average=mean(values),
    )


def analyze_rows(rows: list[dict[str, str]]) -> AnalysisResult:
    metric_values: dict[str, list[float]] = {field: [] for field in NUMERIC_FIELDS}
    dtcs: set[str] = set()

    for row in rows:
        for field in NUMERIC_FIELDS:
            value = _parse_float(row.get(field))
            if value is not None:
                metric_values[field].append(value)

        raw_dtc = (row.get("dtc") or "").strip().upper()
        if raw_dtc:
            for code in raw_dtc.replace(";", ",").split(","):
                code = code.strip()
                if code:
                    dtcs.add(code)

    metrics = {field: _summarize(values) for field, values in metric_values.items()}
    warnings = build_warnings(metrics)

    return AnalysisResult(
        samples=len(rows),
        metrics=metrics,
        dtcs=sorted(dtcs),
        warnings=warnings,
    )


def build_warnings(metrics: dict[str, MetricSummary]) -> list[str]:
    warnings: list[str] = []

    coolant = metrics["coolant_temp_c"].maximum
    if coolant is not None and coolant >= 105:
        warnings.append(f"Coolant temperature reached {coolant:.1f} °C")

    battery_min = metrics["battery_voltage"].minimum
    if battery_min is not None and battery_min < 12.0:
        warnings.append(f"Battery voltage dropped to {battery_min:.1f} V")

    stft = metrics["stft_percent"]
    ltft = metrics["ltft_percent"]

    trim_candidates = []
    for summary in (stft, ltft):
        if summary.minimum is not None:
            trim_candidates.append(abs(summary.minimum))
        if summary.maximum is not None:
            trim_candidates.append(abs(summary.maximum))

    if trim_candidates:
        max_trim = max(trim_candidates)
        if max_trim >= 15:
            warnings.append(f"Fuel trim reached {max_trim:.1f}%")

    return warnings


def analyze_file(path: str | Path) -> AnalysisResult:
    return analyze_rows(load_csv(path))
