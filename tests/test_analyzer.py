import unittest

from obd2_analyzer.analyzer import analyze_rows


class AnalyzerTests(unittest.TestCase):
    def test_detects_warning_conditions(self):
        rows = [
            {
                "rpm": "800",
                "speed_kph": "0",
                "coolant_temp_c": "92",
                "battery_voltage": "14.1",
                "stft_percent": "3.5",
                "ltft_percent": "5.0",
                "dtc": "",
            },
            {
                "rpm": "2500",
                "speed_kph": "65",
                "coolant_temp_c": "108",
                "battery_voltage": "11.7",
                "stft_percent": "16.0",
                "ltft_percent": "4.2",
                "dtc": "P0420",
            },
        ]

        result = analyze_rows(rows)

        self.assertEqual(result.samples, 2)
        self.assertIn("P0420", result.dtcs)
        self.assertTrue(any("Coolant" in item for item in result.warnings))
        self.assertTrue(any("Battery" in item for item in result.warnings))
        self.assertTrue(any("Fuel trim" in item for item in result.warnings))

    def test_missing_values_are_ignored(self):
        rows = [
            {"rpm": "900", "speed_kph": "", "dtc": ""},
            {"rpm": "1200", "speed_kph": None, "dtc": "P0300; P0171"},
        ]

        result = analyze_rows(rows)

        self.assertEqual(result.metrics["rpm"].minimum, 900.0)
        self.assertEqual(result.metrics["rpm"].maximum, 1200.0)
        self.assertEqual(result.metrics["speed_kph"].minimum, None)
        self.assertEqual(result.dtcs, ["P0171", "P0300"])


if __name__ == "__main__":
    unittest.main()
