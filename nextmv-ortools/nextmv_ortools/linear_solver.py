"""Defines OR-Tools linear solver interoperability.

This module provides functions for integrating Nextmv with OR-Tools linear programming optimization.

Functions
---------
LinearSolver
    Creates an OR-Tools linear solver that can be used to solve optimization problems.
LinearSolverSolution
    Creates a solution dictionary from an OR-Tools linear solver.
LinearSolverStatistics
    Creates statistics from an OR-Tools linear solver.

Classes
-------
LinearSolverOptions
    Options for the OR-Tools linear solver that can be converted to Nextmv options.
"""

import time
from typing import Any, Optional

from ortools.linear_solver import pywraplp

import nextmv


class LinearSolverOptions:
    """Options for the OR-Tools linear solver with conversion to Nextmv options format.

    You can import the `LinearSolverOptions` class directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import LinearSolverOptions
    ```

    This class provides basic options for linear programming solvers in OR-Tools.

    Attributes
    ----------
    options : list[nextmv.Option]
        List of Nextmv options for linear solver configuration.

    Methods
    -------
    to_nextmv()
        Converts the options to a Nextmv options object.

    Examples
    --------
    >>> from nextmv_ortools import LinearSolverOptions
    >>> options = LinearSolverOptions()
    >>> nextmv_options = options.to_nextmv()
    >>> # These options can now be used with a Nextmv model
    """

    def __init__(self):
        """Initialize LinearSolverOptions with basic linear programming parameters."""
        self.options = [
            nextmv.Option(
                name="solver_type",
                option_type=str,
                default="GLOP_LINEAR_PROGRAMMING",
                description="The linear programming solver to use",
                choices=["GLOP_LINEAR_PROGRAMMING", "CLP_LINEAR_PROGRAMMING", "GLPK_LINEAR_PROGRAMMING"]
            ),
            nextmv.Option(
                name="time_limit",
                option_type=float,
                default=60.0,
                description="Time limit for the solver in seconds"
            ),
            nextmv.Option(
                name="num_threads",
                option_type=int,
                default=1,
                description="Number of threads to use"
            ),
            nextmv.Option(
                name="enable_output",
                option_type=bool,
                default=False,
                description="Enable solver output"
            ),
        ]

    def to_nextmv(self) -> nextmv.Options:
        """Convert LinearSolverOptions to Nextmv options format.

        Returns
        -------
        nextmv.Options
            A Nextmv options object containing the linear solver options.
        """
        return nextmv.Options(*self.options)


def LinearSolver(options: nextmv.Options) -> pywraplp.Solver:
    """
    Creates an OR-Tools linear solver that can be used to solve optimization problems.

    This function sets up a linear programming solver with the specified configuration
    and redirects solver output to stderr for consistent logging.

    Parameters
    ----------
    options : nextmv.Options
        The options for the OR-Tools linear solver. Any option that matches a linear solver
        parameter will be applied to the solver.

    Returns
    -------
    pywraplp.Solver
        The OR-Tools linear solver instance that can be used to define and solve
        optimization problems.

    Examples
    --------
    >>> import nextmv
    >>> from nextmv_ortools import LinearSolver
    >>>
    >>> # Create options
    >>> options = nextmv.Options()
    >>> options.solver_type = "GLOP_LINEAR_PROGRAMMING"
    >>> options.time_limit = 60.0
    >>>
    >>> # Create OR-Tools linear solver with Nextmv options
    >>> solver = LinearSolver(options)
    >>>
    >>> # Use solver as any other OR-Tools linear solver
    >>> x = solver.NumVar(0, 10, "x")
    >>> y = solver.NumVar(0, 10, "y")
    >>> solver.Add(x + y <= 5)
    >>> solver.Maximize(x + y)
    >>> status = solver.Solve()
    """

    # Solver chatter is logged to stderr.
    nextmv.redirect_stdout()

    # Get solver type from options
    solver_type = getattr(options, "solver_type", "GLOP_LINEAR_PROGRAMMING")
    
    # Create the solver
    solver = pywraplp.Solver.CreateSolver(solver_type)
    if not solver:
        # Fallback to GLOP if requested solver is not available
        solver = pywraplp.Solver.CreateSolver("GLOP_LINEAR_PROGRAMMING")
        if not solver:
            raise RuntimeError("Unable to create OR-Tools linear solver")

    # Apply options to the solver
    if hasattr(options, "time_limit"):
        solver.SetTimeLimit(int(getattr(options, "time_limit") * 1000))  # OR-Tools expects milliseconds

    if hasattr(options, "num_threads"):
        solver.SetNumThreads(getattr(options, "num_threads"))

    if hasattr(options, "enable_output") and getattr(options, "enable_output"):
        solver.EnableOutput()
    else:
        solver.SuppressOutput()

    options.provider = "ortools_linear"

    return solver


def LinearSolverSolution(solver: pywraplp.Solver) -> Optional[dict[str, Any]]:
    """
    Creates a basic solution dictionary from an OR-Tools linear solver.

    You can import the `LinearSolverSolution` function directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import LinearSolverSolution
    ```

    The simple solution dictionary contains the variable name and the value of the
    variable for each variable in the solver. If the solver has not been solved,
    it will return `None`.

    Parameters
    ----------
    solver : pywraplp.Solver
        The OR-Tools linear solver that has been solved.

    Returns
    -------
    dict[str, Any] or None
        A dictionary with variable names as keys and their optimal values as values.
        Returns None if the solver has not found a solution.

    Examples
    --------
    >>> from ortools.linear_solver import pywraplp
    >>> from nextmv_ortools import LinearSolverSolution
    >>>
    >>> # Create and solve a simple model
    >>> solver = pywraplp.Solver.CreateSolver("GLOP_LINEAR_PROGRAMMING")
    >>> x = solver.NumVar(0, 10, "x")
    >>> y = solver.NumVar(0, 10, "y")
    >>> solver.Add(x + y <= 5)
    >>> solver.Maximize(x + y)
    >>> status = solver.Solve()
    >>>
    >>> # Get the solution dictionary
    >>> solution = LinearSolverSolution(solver)
    >>> print(solution)
    {'x': 2.5, 'y': 2.5}
    """

    # Check if solver has a valid solution
    if solver.Solve() != pywraplp.Solver.OPTIMAL:
        return None

    # Extract variable values
    solution = {}
    for i in range(solver.NumVariables()):
        var = solver.variable(i)
        solution[var.name()] = var.solution_value()

    return solution


def LinearSolverStatistics(solver: pywraplp.Solver, run_duration_start: Optional[float] = None) -> nextmv.Statistics:
    """
    Creates a Nextmv statistics object from an OR-Tools linear solver, once it has been solved.

    You can import the `LinearSolverStatistics` function directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import LinearSolverStatistics
    ```

    The statistics returned are basic and should be extended according to the
    custom metrics that the user wants to track. The optional `run_duration_start`
    parameter can be used to set the start time of the whole run.

    Parameters
    ----------
    solver : pywraplp.Solver
        The OR-Tools linear solver after solving.
    run_duration_start : float, optional
        The start time of the run in seconds since the epoch, as returned by `time.time()`.
        If provided, the total run duration will be calculated.

    Returns
    -------
    nextmv.Statistics
        The Nextmv statistics object containing run information, result statistics,
        and series data.

    Examples
    --------
    >>> import time
    >>> from nextmv_ortools import LinearSolver, LinearSolverOptions, LinearSolverStatistics
    >>>
    >>> start_time = time.time()
    >>> options = LinearSolverOptions().to_nextmv()
    >>> solver = LinearSolver(options)
    >>> # Create and configure your model
    >>> status = solver.Solve()
    >>> stats = LinearSolverStatistics(solver, start_time)
    """

    run = nextmv.RunStatistics()
    if run_duration_start is not None:
        run.duration = time.time() - run_duration_start

    # Map OR-Tools status to string
    status_map = {
        pywraplp.Solver.OPTIMAL: "OPTIMAL",
        pywraplp.Solver.FEASIBLE: "FEASIBLE",
        pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
        pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
        pywraplp.Solver.ABNORMAL: "ABNORMAL",
        pywraplp.Solver.MODEL_INVALID: "MODEL_INVALID",
        pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
    }

    status = solver.Solve()
    objective_value = solver.Objective().Value() if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE] else None

    return nextmv.Statistics(
        run=run,
        result=nextmv.ResultStatistics(
            duration=solver.WallTime() / 1000.0,  # Convert milliseconds to seconds
            value=objective_value,
            custom={
                "status": status_map.get(status, "UNKNOWN"),
                "variables": solver.NumVariables(),
                "constraints": solver.NumConstraints(),
                "iterations": solver.Iterations(),
            },
        ),
        series_data=nextmv.SeriesData(),
    )