import unittest
from health_check import evaluate, exit_code


class HealthCheckTests(unittest.TestCase):
    def check_device(self, **fields):
        return evaluate({"devices": [{"name": "r1", **fields}]})

    def test_healthy(self):
        result = self.check_device(bgp=[{"peer": "192.0.2.1", "state": "Established"}])
        self.assertEqual(exit_code(result), 0)

    def test_down_peer(self):
        result = self.check_device(bgp=[{"peer": "192.0.2.1", "state": "Idle"}])
        self.assertEqual(exit_code(result), 1)

    def test_missing_and_empty_are_unknown(self):
        for fields in ({}, {"bgp": []}, {"bgp": [None]}, {"error": "timeout"}):
            self.assertEqual(exit_code(self.check_device(**fields)), 2)

    def test_partial_failure_preserves_unknown_information(self):
        result = self.check_device(bgp=[{"peer": "x", "state": "Idle"}, {}])
        self.assertEqual(exit_code(result), 1)
        self.assertIn("incomplete", result[0]["detail"])

    def test_bad_schema(self):
        for data in ([], {}, {"devices": []}, {"devices": [None]}):
            with self.assertRaises(ValueError):
                evaluate(data)

    def test_duplicate_devices_rejected(self):
        with self.assertRaises(ValueError):
            evaluate({"devices": [{"name": "r1"}, {"name": "r1"}]})

    def test_duplicate_peers_unknown(self):
        peer = {"peer": "192.0.2.1", "state": "Established"}
        self.assertEqual(exit_code(self.check_device(bgp=[peer, peer])), 2)


if __name__ == "__main__":
    unittest.main()
