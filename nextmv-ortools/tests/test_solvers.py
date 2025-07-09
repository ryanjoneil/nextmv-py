import sys
import unittest
from unittest.mock import patch

import nextmv_ortools as nortools


class TestLinearSolver(unittest.TestCase):
    @patch.object(sys, "argv", ["test"])
    def test_linear_solver_creation(self):
        """Test that LinearSolver can be created with default options"""
        options = nortools.LinearSolverOptions().to_nextmv()
        # Set options manually to avoid command line parsing
        options.solver_type = "GLOP_LINEAR_PROGRAMMING"
        options.time_limit = 30.0

        solver = nortools.LinearSolver(options)

        # Check that solver is created and has expected attributes
        self.assertIsNotNone(solver)
        self.assertTrue(hasattr(solver, "NumVar"))
        self.assertTrue(hasattr(solver, "Add"))
        self.assertTrue(hasattr(solver, "Solve"))


class TestCpModel(unittest.TestCase):
    @patch.object(sys, "argv", ["test"])
    def test_cp_model_creation(self):
        """Test that CpModel can be created with default options"""
        options = nortools.CpModelOptions().to_nextmv()
        # Set options manually to avoid command line parsing
        options.max_time_in_seconds = 30.0
        options.num_search_workers = 1

        model, solver = nortools.CpModel(options)

        # Check that model and solver are created and have expected attributes
        self.assertIsNotNone(model)
        self.assertIsNotNone(solver)
        self.assertTrue(hasattr(model, "NewIntVar"))
        self.assertTrue(hasattr(model, "Add"))
        self.assertTrue(hasattr(solver, "Solve"))


class TestKnapsackSolver(unittest.TestCase):
    @patch.object(sys, "argv", ["test"])
    def test_knapsack_solver_creation(self):
        """Test that KnapsackSolver can be created with default options"""
        options = nortools.KnapsackSolverOptions().to_nextmv()
        # Set options manually to avoid command line parsing
        options.solver_name = "TestSolver"
        options.time_limit = 30.0

        solver = nortools.KnapsackSolver(options)

        # Check that solver is created and has expected attributes
        self.assertIsNotNone(solver)
        self.assertTrue(hasattr(solver, "init"))
        self.assertTrue(hasattr(solver, "solve"))


class TestGraphSolvers(unittest.TestCase):
    @patch.object(sys, "argv", ["test"])
    def test_linear_sum_assignment_creation(self):
        """Test that SimpleLinearSumAssignment can be created"""
        options = nortools.SimpleLinearSumAssignmentOptions().to_nextmv()
        # Set options manually to avoid command line parsing
        options.solver_name = "TestAssignment"

        assignment = nortools.SimpleLinearSumAssignment(options)

        # Check that assignment solver is created
        self.assertIsNotNone(assignment)

    @patch.object(sys, "argv", ["test"])
    def test_max_flow_creation(self):
        """Test that SimpleMaxFlow can be created"""
        options = nortools.SimpleMaxFlowOptions().to_nextmv()
        # Set options manually to avoid command line parsing
        options.solver_name = "TestMaxFlow"

        max_flow_solver = nortools.SimpleMaxFlow(options)

        # Check that max flow solver is created
        self.assertIsNotNone(max_flow_solver)

    @patch.object(sys, "argv", ["test"])
    def test_min_cost_flow_creation(self):
        """Test that SimpleMinCostFlow can be created"""
        options = nortools.SimpleMinCostFlowOptions().to_nextmv()
        # Set options manually to avoid command line parsing
        options.solver_name = "TestMinCostFlow"

        min_cost_flow_solver = nortools.SimpleMinCostFlow(options)

        # Check that min cost flow solver is created
        self.assertIsNotNone(min_cost_flow_solver)


if __name__ == "__main__":
    unittest.main()
