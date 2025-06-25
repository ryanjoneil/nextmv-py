import unittest

import nextmv_ortools as nortools


class TestVersion(unittest.TestCase):
    def test_version(self):
        exported_version = nortools.VERSION
        expected_version = nortools.__about__.__version__
        self.assertEqual(exported_version, expected_version)


if __name__ == "__main__":
    unittest.main()