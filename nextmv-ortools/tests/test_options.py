import unittest

import nextmv_ortools as nortools


class TestLinearSolverOptions(unittest.TestCase):
    def test_to_nextmv(self):
        """Test that LinearSolverOptions can be converted to nextmv.Options"""
        options = nortools.LinearSolverOptions()
        nextmv_options = options.to_nextmv()
        
        # Check that we get the expected options
        options_dict = nextmv_options.options_dict()
        self.assertIsInstance(options_dict, list)
        self.assertGreater(len(options_dict), 0)
        
        # Check for specific expected parameters
        option_names = [option["name"] for option in options_dict]
        self.assertIn("solver_type", option_names)
        self.assertIn("time_limit", option_names)
        self.assertIn("num_threads", option_names)
        self.assertIn("enable_output", option_names)


class TestCpModelOptions(unittest.TestCase):
    def test_to_nextmv(self):
        """Test that CpModelOptions can be converted to nextmv.Options"""
        options = nortools.CpModelOptions()
        nextmv_options = options.to_nextmv()
        
        # Check that we get the expected options
        options_dict = nextmv_options.options_dict()
        self.assertIsInstance(options_dict, list)
        self.assertGreater(len(options_dict), 0)
        
        # Check for specific expected parameters
        option_names = [option["name"] for option in options_dict]
        self.assertIn("max_time_in_seconds", option_names)
        self.assertIn("num_search_workers", option_names)
        self.assertIn("log_search_progress", option_names)


class TestKnapsackSolverOptions(unittest.TestCase):
    def test_to_nextmv(self):
        """Test that KnapsackSolverOptions can be converted to nextmv.Options"""
        options = nortools.KnapsackSolverOptions()
        nextmv_options = options.to_nextmv()
        
        # Check that we get the expected options
        options_dict = nextmv_options.options_dict()
        self.assertIsInstance(options_dict, list)
        self.assertGreater(len(options_dict), 0)
        
        # Check for specific expected parameters
        option_names = [option["name"] for option in options_dict]
        self.assertIn("solver_name", option_names)
        self.assertIn("time_limit", option_names)
        self.assertIn("use_reduction", option_names)


if __name__ == "__main__":
    unittest.main()