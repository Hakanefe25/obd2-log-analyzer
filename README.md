# OBD-II Log Analyzer

A small Python CLI tool for turning raw OBD-II CSV logs into a cleaner vehicle health summary.

It is designed as a learning project around **automotive diagnostics, data parsing and Python tooling**.

## What it does

- Reads OBD-II logs from CSV
- Calculates basic statistics for common PIDs
- Extracts DTCs
- Flags suspicious coolant temperature
- Flags large short-term / long-term fuel trims
- Detects unusually low battery voltage
- Produces a readable terminal summary
- Can export the analysis as JSON
- Includes tests and GitHub Actions

## Supported columns

The analyzer understands these CSV fields when present:

- `timestamp`
- `rpm`
- `speed_kph`
- `coolant_temp_c`
- `battery_voltage`
- `stft_percent`
- `ltft_percent`
- `maf_gps`
- `throttle_percent`
- `dtc`

You do not need every column. Missing values are ignored.

## Example

```bash
python -m obd2_analyzer.cli sample_data/example_log.csv
```

Example output:

```text
OBD-II Log Summary
------------------
Samples: 12
RPM: 780 - 3120 rpm
Speed: 0 - 86 km/h
Coolant: 74.0 - 108.0 °C
Battery: 12.2 - 14.4 V
DTCs: P0420

Warnings:
- Coolant temperature reached 108.0 °C
- Combined fuel trim reached +18.4%
```

Export JSON:

```bash
python -m obd2_analyzer.cli sample_data/example_log.csv --json report.json
```

## Install

Requires Python 3.10+.

```bash
git clone https://github.com/Hakanefe25/obd2-log-analyzer.git
cd obd2-log-analyzer

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

On Windows:

```powershell
.venv\Scripts\activate
pip install -e .
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Repository layout

```text
.
├── .github/workflows/ci.yml
├── docs/diagnostic-notes.md
├── sample_data/example_log.csv
├── src/obd2_analyzer/
│   ├── __init__.py
│   ├── analyzer.py
│   └── cli.py
├── tests/test_analyzer.py
├── pyproject.toml
└── README.md
```

## Why this exists

I am interested in both software and automotive diagnostics. This project combines the two: taking data similar to what an OBD-II scan session can produce and turning it into something easier to inspect.

It is intentionally not a replacement for a real diagnostic tool. Thresholds are simplified and should be treated as learning-oriented heuristics, not repair advice.

## Roadmap

- Support more PIDs
- Add graph generation
- Add live ELM327 input
- Add manufacturer-specific profiles
- Compare multiple logs
- Add HTML reports
- Add anomaly detection

## License

MIT
