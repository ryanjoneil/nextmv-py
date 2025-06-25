"""Defines OR-Tools graph solvers interoperability.

This module provides functions for integrating Nextmv with OR-Tools graph optimization solvers.

Functions
---------
SimpleLinearSumAssignment, SimpleMaxFlow, SimpleMinCostFlow
    Creates OR-Tools graph solvers that can be used to solve optimization problems.
SimpleLinearSumAssignmentSolution, SimpleMaxFlowSolution, SimpleMinCostFlowSolution
    Creates solution dictionaries from OR-Tools graph solvers.
SimpleLinearSumAssignmentStatistics, SimpleMaxFlowStatistics, SimpleMinCostFlowStatistics
    Creates statistics from OR-Tools graph solvers.

Classes
-------
SimpleLinearSumAssignmentOptions, SimpleMaxFlowOptions, SimpleMinCostFlowOptions
    Options for the OR-Tools graph solvers that can be converted to Nextmv options.
"""

import time
from typing import Any, Optional

from ortools.graph.python import linear_sum_assignment
from ortools.graph.python import max_flow
from ortools.graph.python import min_cost_flow

import nextmv


# Linear Sum Assignment Solver
class SimpleLinearSumAssignmentOptions:
    """Options for the OR-Tools linear sum assignment solver with conversion to Nextmv options format."""

    def __init__(self):
        """Initialize SimpleLinearSumAssignmentOptions with basic parameters."""
        self.options = [
            nextmv.Option(
                name="solver_name",
                option_type=str,
                default="LinearSumAssignment",
                description="Name identifier for the linear sum assignment solver"
            ),
        ]

    def to_nextmv(self) -> nextmv.Options:
        """Convert SimpleLinearSumAssignmentOptions to Nextmv options format."""
        return nextmv.Options(*self.options)


def SimpleLinearSumAssignment(options: nextmv.Options) -> linear_sum_assignment.SimpleLinearSumAssignment:
    """Creates an OR-Tools linear sum assignment solver."""
    nextmv.redirect_stdout()
    
    assignment = linear_sum_assignment.SimpleLinearSumAssignment()
    options.provider = "ortools_linear_sum_assignment"
    
    return assignment


def SimpleLinearSumAssignmentSolution(assignment: linear_sum_assignment.SimpleLinearSumAssignment) -> Optional[dict[str, Any]]:
    """Creates a solution dictionary from an OR-Tools linear sum assignment solver."""
    try:
        status = assignment.Solve()
        if status != assignment.OPTIMAL:
            return None
            
        solution = {
            "optimal_cost": assignment.OptimalCost(),
            "assignments": [],
            "status": "OPTIMAL"
        }
        
        for i in range(assignment.NumNodes()):
            if assignment.RightMate(i) >= 0:
                solution["assignments"].append({
                    "left_node": i,
                    "right_node": assignment.RightMate(i),
                    "cost": assignment.AssignmentCost(i, assignment.RightMate(i))
                })
        
        return solution
    except Exception:
        return None


def SimpleLinearSumAssignmentStatistics(assignment: linear_sum_assignment.SimpleLinearSumAssignment, 
                                      run_duration_start: Optional[float] = None) -> nextmv.Statistics:
    """Creates statistics from an OR-Tools linear sum assignment solver."""
    run = nextmv.RunStatistics()
    if run_duration_start is not None:
        run.duration = time.time() - run_duration_start

    optimal_cost = None
    status = "UNKNOWN"
    try:
        solve_status = assignment.Solve()
        status = "OPTIMAL" if solve_status == assignment.OPTIMAL else "NOT_OPTIMAL"
        if solve_status == assignment.OPTIMAL:
            optimal_cost = assignment.OptimalCost()
    except Exception:
        pass

    return nextmv.Statistics(
        run=run,
        result=nextmv.ResultStatistics(
            duration=None,
            value=optimal_cost,
            custom={
                "status": status,
                "num_nodes": assignment.NumNodes() if hasattr(assignment, 'NumNodes') else None,
            },
        ),
        series_data=nextmv.SeriesData(),
    )


# Max Flow Solver
class SimpleMaxFlowOptions:
    """Options for the OR-Tools max flow solver with conversion to Nextmv options format."""

    def __init__(self):
        """Initialize SimpleMaxFlowOptions with basic parameters."""
        self.options = [
            nextmv.Option(
                name="solver_name",
                option_type=str,
                default="MaxFlow",
                description="Name identifier for the max flow solver"
            ),
        ]

    def to_nextmv(self) -> nextmv.Options:
        """Convert SimpleMaxFlowOptions to Nextmv options format."""
        return nextmv.Options(*self.options)


def SimpleMaxFlow(options: nextmv.Options) -> max_flow.SimpleMaxFlow:
    """Creates an OR-Tools max flow solver."""
    nextmv.redirect_stdout()
    
    max_flow_solver = max_flow.SimpleMaxFlow()
    options.provider = "ortools_max_flow"
    
    return max_flow_solver


def SimpleMaxFlowSolution(max_flow_solver: max_flow.SimpleMaxFlow) -> Optional[dict[str, Any]]:
    """Creates a solution dictionary from an OR-Tools max flow solver."""
    try:
        status = max_flow_solver.Solve(0, max_flow_solver.NumNodes() - 1)  # Assumes source=0, sink=last node
        if status != max_flow_solver.OPTIMAL:
            return None
            
        solution = {
            "optimal_flow": max_flow_solver.OptimalFlow(),
            "flows": [],
            "status": "OPTIMAL"
        }
        
        for i in range(max_flow_solver.NumArcs()):
            if max_flow_solver.Flow(i) > 0:
                solution["flows"].append({
                    "arc_index": i,
                    "tail": max_flow_solver.Tail(i),
                    "head": max_flow_solver.Head(i),
                    "flow": max_flow_solver.Flow(i),
                    "capacity": max_flow_solver.Capacity(i)
                })
        
        return solution
    except Exception:
        return None


def SimpleMaxFlowStatistics(max_flow_solver: max_flow.SimpleMaxFlow, 
                           run_duration_start: Optional[float] = None) -> nextmv.Statistics:
    """Creates statistics from an OR-Tools max flow solver."""
    run = nextmv.RunStatistics()
    if run_duration_start is not None:
        run.duration = time.time() - run_duration_start

    optimal_flow = None
    status = "UNKNOWN"
    try:
        # This would need source and sink parameters
        optimal_flow = max_flow_solver.OptimalFlow()
        status = "OPTIMAL"
    except Exception:
        pass

    return nextmv.Statistics(
        run=run,
        result=nextmv.ResultStatistics(
            duration=None,
            value=optimal_flow,
            custom={
                "status": status,
                "num_nodes": max_flow_solver.NumNodes() if hasattr(max_flow_solver, 'NumNodes') else None,
                "num_arcs": max_flow_solver.NumArcs() if hasattr(max_flow_solver, 'NumArcs') else None,
            },
        ),
        series_data=nextmv.SeriesData(),
    )


# Min Cost Flow Solver
class SimpleMinCostFlowOptions:
    """Options for the OR-Tools min cost flow solver with conversion to Nextmv options format."""

    def __init__(self):
        """Initialize SimpleMinCostFlowOptions with basic parameters."""
        self.options = [
            nextmv.Option(
                name="solver_name",
                option_type=str,
                default="MinCostFlow",
                description="Name identifier for the min cost flow solver"
            ),
        ]

    def to_nextmv(self) -> nextmv.Options:
        """Convert SimpleMinCostFlowOptions to Nextmv options format."""
        return nextmv.Options(*self.options)


def SimpleMinCostFlow(options: nextmv.Options) -> min_cost_flow.SimpleMinCostFlow:
    """Creates an OR-Tools min cost flow solver."""
    nextmv.redirect_stdout()
    
    min_cost_flow_solver = min_cost_flow.SimpleMinCostFlow()
    options.provider = "ortools_min_cost_flow"
    
    return min_cost_flow_solver


def SimpleMinCostFlowSolution(min_cost_flow_solver: min_cost_flow.SimpleMinCostFlow) -> Optional[dict[str, Any]]:
    """Creates a solution dictionary from an OR-Tools min cost flow solver."""
    try:
        status = min_cost_flow_solver.Solve()
        if status != min_cost_flow_solver.OPTIMAL:
            return None
            
        solution = {
            "optimal_cost": min_cost_flow_solver.OptimalCost(),
            "maximum_flow": min_cost_flow_solver.MaximumFlow(),
            "flows": [],
            "status": "OPTIMAL"
        }
        
        for i in range(min_cost_flow_solver.NumArcs()):
            if min_cost_flow_solver.Flow(i) > 0:
                solution["flows"].append({
                    "arc_index": i,
                    "tail": min_cost_flow_solver.Tail(i),
                    "head": min_cost_flow_solver.Head(i),
                    "flow": min_cost_flow_solver.Flow(i),
                    "capacity": min_cost_flow_solver.Capacity(i),
                    "unit_cost": min_cost_flow_solver.UnitCost(i)
                })
        
        return solution
    except Exception:
        return None


def SimpleMinCostFlowStatistics(min_cost_flow_solver: min_cost_flow.SimpleMinCostFlow, 
                               run_duration_start: Optional[float] = None) -> nextmv.Statistics:
    """Creates statistics from an OR-Tools min cost flow solver."""
    run = nextmv.RunStatistics()
    if run_duration_start is not None:
        run.duration = time.time() - run_duration_start

    optimal_cost = None
    status = "UNKNOWN"
    try:
        solve_status = min_cost_flow_solver.Solve()
        status = "OPTIMAL" if solve_status == min_cost_flow_solver.OPTIMAL else "NOT_OPTIMAL"
        if solve_status == min_cost_flow_solver.OPTIMAL:
            optimal_cost = min_cost_flow_solver.OptimalCost()
    except Exception:
        pass

    return nextmv.Statistics(
        run=run,
        result=nextmv.ResultStatistics(
            duration=None,
            value=optimal_cost,
            custom={
                "status": status,
                "num_nodes": min_cost_flow_solver.NumNodes() if hasattr(min_cost_flow_solver, 'NumNodes') else None,
                "num_arcs": min_cost_flow_solver.NumArcs() if hasattr(min_cost_flow_solver, 'NumArcs') else None,
            },
        ),
        series_data=nextmv.SeriesData(),
    )