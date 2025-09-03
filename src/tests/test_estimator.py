import unittest
import math
from estima.core.estimator import estimate_resources
from estima.core.predictor import normalize_metrics
from estima.core.formatter import format_output

class TestEstimator(unittest.TestCase):

    def test_estimate_resources_normal_case(self):
        metrics = {
            "peak_memory_mb": 100,
            "avg_cpu_percent": 50,
            "total_io_mb": 200
        }
        features = {
            "size_mb": 50,
            "duration_sec": 60, 
            "channels": 4,
            "bitrate_kbps": 256
        }
        expected_ram = 100 + (50 * 0.1) + (4 * 50)  # 100 + 5 + 200 = 305
        expected_cpu = (50 / 100) + (60 * 0.01) + (4 * 0.05) # 0.5 + 0.6 + 0.2 = 1.3
        expected_io = 200 + (50 * 0.05) + (256 * 0.001) # 200 + 2.5 + 0.256 = 202.756

        result = estimate_resources(metrics, features)

        self.assertAlmostEqual(result["ram_mb"], round(expected_ram, 2), places=2)
        self.assertAlmostEqual(result["cpu_cores"], round(expected_cpu, 2), places=2)
        self.assertAlmostEqual(result["io_mb"], round(expected_io, 2), places=2)
        self.assertEqual(result["confidence"], "High")

    # Test with a low duration to ensure 'Medium' confidence is set.
    def test_estimate_resources_low_duration_medium_confidence(self):
        metrics = {"peak_memory_mb": 50, "avg_cpu_percent": 20, "total_io_mb": 100}
        features = {"size_mb": 10, "duration_sec": 20, "channels": 2, "bitrate_kbps": 64} # duration < 30
        result = estimate_resources(metrics, features)
        self.assertEqual(result["confidence"], "Medium")

    # an edge case where features might be absent or minimal.
    def test_estimate_resources_zero_inputs(self):
        metrics = {"peak_memory_mb": 0, "avg_cpu_percent": 0, "total_io_mb": 0}
        features = {"size_mb": 0, "duration_sec": 0, "channels": 0, "bitrate_kbps": 0}

        expected_ram = 0.0
        expected_cpu = 0.0
        expected_io = 0.0

        result = estimate_resources(metrics, features)
        self.assertAlmostEqual(result["ram_mb"], expected_ram, places=2)
        self.assertAlmostEqual(result["cpu_cores"], expected_cpu, places=2)
        self.assertAlmostEqual(result["io_mb"], expected_io, places=2)
        self.assertEqual(result["confidence"], "Medium") # duration_sec = 0

    
    # Test with unusually large inputs to ensure the calculations scale correctly
    # and don't produce unexpected overflow or underflow     def test_estimate_resources_large_inputs(self):
        metrics = {"peak_memory_mb": 10000, "avg_cpu_percent": 99, "total_io_mb": 5000}
        features = {"size_mb": 1000, "duration_sec": 3600, "channels": 100, "bitrate_kbps": 10000}

        expected_ram = 10000 + (1000 * 0.1) + (100 * 50)  # 10000 + 100 + 5000 = 15100
        expected_cpu = (99 / 100) + (3600 * 0.01) + (100 * 0.05) # 0.99 + 36 + 5 = 41.99
        expected_io = 5000 + (1000 * 0.05) + (10000 * 0.001) # 5000 + 50 + 10 = 5060

        result = estimate_resources(metrics, features)
        self.assertAlmostEqual(result["ram_mb"], round(expected_ram, 2), places=2)
        self.assertAlmostEqual(result["cpu_cores"], round(expected_cpu, 2), places=2)
        self.assertAlmostEqual(result["io_mb"], round(expected_io, 2), places=2)
        self.assertEqual(result["confidence"], "High")

    def test_normalize_metrics_basic_stream(self):
        """
        Test normalize_metrics with a basic stream of data.
        Ensures correct average CPU, peak memory, and total I/O are calculated.
        This tests the `deque` usage for its intended purpose.
        """
        raw_stream = [
            {"cpu": 10, "memory": 50, "io": 5},
            {"cpu": 20, "memory": 60, "io": 10},
            {"cpu": 30, "memory": 70, "io": 15},
        ]
        result = normalize_metrics(raw_stream)
        self.assertAlmostEqual(result["avg_cpu_percent"], (10 + 20 + 30) / 3)
        self.assertEqual(result["peak_memory_mb"], 70)
        self.assertEqual(result["total_io_mb"], (5 + 10 + 15))

    def test_normalize_metrics_sliding_window_effect(self):
        """
        Test normalize_metrics to confirm the sliding window behavior of `deque` (maxlen=10).
        Only the last 10 samples should influence the result.
        """
        raw_stream = []
        for i in range(1, 15): # 14 samples, only last 10 should be considered
            raw_stream.append({"cpu": i, "memory": i * 10, "io": i * 2})

        result = normalize_metrics(raw_stream)

        # Expected values based on the last 10 samples (i=5 to i=14)
        expected_cpu_sum = sum(range(5, 15))
        expected_memory_peak = 14 * 10
        expected_io_sum = sum(i * 2 for i in range(5, 15))

        self.assertAlmostEqual(result["avg_cpu_percent"], expected_cpu_sum / 10)
        self.assertEqual(result["peak_memory_mb"], expected_memory_peak)
        self.assertEqual(result["total_io_mb"], expected_io_sum)

    def test_normalize_metrics_empty_stream(self):
        """
        Test normalize_metrics with an empty stream.
        Should handle division by zero for avg_cpu_percent and return 0 for peak/total,
        or raise an appropriate error if not designed to handle it
        This highlights a DSA consideration: handling empty data sets for aggregation.
        """
        raw_stream = []
        with self.assertRaises(ZeroDivisionError):
            normalize_metrics(raw_stream)

    def test_normalize_metrics_single_sample(self):
        """
        Test normalize_metrics with a single sample in the stream.
        """
        raw_stream = [{"cpu": 25, "memory": 100, "io": 10}]
        result = normalize_metrics(raw_stream)
        self.assertAlmostEqual(result["avg_cpu_percent"], 25)
        self.assertEqual(result["peak_memory_mb"], 100)
        self.assertEqual(result["total_io_mb"], 10)

    def test_normalize_metrics_mixed_values(self):
        """
        Test with mixed positive and negative (if applicable) or zero values.
        Ensures `max` works correctly for peak memory.
        """
        raw_stream = [
            {"cpu": 0, "memory": 0, "io": 0},
            {"cpu": 50, "memory": 200, "io": 30},
            {"cpu": 10, "memory": 150, "io": 5}
        ]
        result = normalize_metrics(raw_stream)
        self.assertAlmostEqual(result["avg_cpu_percent"], (0 + 50 + 10) / 3)
        self.assertEqual(result["peak_memory_mb"], 200)
        self.assertEqual(result["total_io_mb"], (0 + 30 + 5))

    def test_format_output(self):
        """
        Test format_output to ensure the output string is correctly formatted.
        """
        estimate = {
            "ram_mb": 305.00,
            "cpu_cores": 1.30,
            "io_mb": 202.76,
            "confidence": "High"
        }
        expected_output = (
            f"\n📊 Resource Estimation Summary\n"
            f"• Estimated RAM: 305.0 MB\n"
            f"• Estimated CPU: 1.3 cores\n"
            f"• Estimated I/O: 202.76 MB\n"
            f"• Confidence Level: High\n"
        )
        self.assertEqual(format_output(estimate), expected_output)

    def test_format_output_zero_values(self):
        """
        Test format_output with zero values to ensure consistent formatting.
        """
        estimate = {
            "ram_mb": 0.0,
            "cpu_cores": 0.0,
            "io_mb": 0.0,
            "confidence": "Medium"
        }
        expected_output = (
            f"\n📊 Resource Estimation Summary\n"
            f"• Estimated RAM: 0.0 MB\n"
            f"• Estimated CPU: 0.0 cores\n"
            f"• Estimated I/O: 0.0 MB\n"
            f"• Confidence Level: Medium\n"
        )
        self.assertEqual(format_output(estimate), expected_output)

if __name__ == "__main__":
    unittest.main()
