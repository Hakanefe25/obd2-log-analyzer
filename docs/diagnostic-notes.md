# Diagnostic notes

This project uses intentionally simple thresholds.

They are not manufacturer-specific and are not intended to replace service information, scan-tool procedures or professional diagnosis.

## Coolant temperature

The analyzer currently warns at 105 °C or higher.

Whether that temperature is abnormal depends on the engine, cooling strategy, operating conditions and manufacturer specification.

## Fuel trims

The analyzer currently warns if STFT or LTFT reaches an absolute value of 15% or greater.

Fuel trims must always be interpreted with operating conditions in mind.

## Battery voltage

A voltage below 12.0 V is flagged.

Charging-system diagnosis requires more context than one sampled voltage value.

## DTCs

DTCs are collected and displayed, but the tool does not attempt to diagnose the cause of a code.

For example, P0420 does not automatically mean the catalytic converter itself is faulty.
