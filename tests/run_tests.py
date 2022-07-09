import unittest
OneLiner = __import__("one-liner").OneLiner


class RunAllTests(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(OneLiner([]))

    def test_env_vars(self):
        import os
        mock_one_liner_file = '.one-liner'
        mock_one_liner_python = 'python'
        os.environ["ONELINER_PATH"] = mock_one_liner_file
        os.environ["ONELINER_PYTHON_EXEC"] = mock_one_liner_python

        oneLiner = OneLiner([])
        self.assertEqual(oneLiner.one_liner_alias_file, mock_one_liner_file)
        self.assertEqual(oneLiner.one_liner_python_exec, mock_one_liner_python)



if __name__ == "__main__":
    unittest.main()

