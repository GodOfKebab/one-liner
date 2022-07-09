import unittest
OneLiner = __import__("one-liner").OneLiner


class RunAllTests(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(OneLiner([]))


if __name__ == "__main__":
    unittest.main()

