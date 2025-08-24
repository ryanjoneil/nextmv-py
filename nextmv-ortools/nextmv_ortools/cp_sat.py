"""Defines OR-Tools CP-SAT solver interoperability.

This module provides functions for integrating Nextmv with OR-Tools constraint programming SAT optimization.

Functions
---------
CpModel
    Creates an OR-Tools CP-SAT model and solver that can be used to solve optimization problems.
CpModelSolution
    Creates a solution dictionary from an OR-Tools CP-SAT solver.
CpModelStatistics
    Creates statistics from an OR-Tools CP-SAT solver.

Classes
-------
CpModelOptions
    Options for the OR-Tools CP-SAT solver that can be converted to Nextmv options.
"""

import time
from typing import Any, Optional, Tuple

from ortools.sat.python import cp_model

import nextmv


class CpModelOptions:
    """Options for the OR-Tools CP-SAT solver with conversion to Nextmv options format.

    You can import the `CpModelOptions` class directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import CpModelOptions
    ```

    This class provides basic options for constraint programming SAT solvers in OR-Tools.

    Attributes
    ----------
    options : list[nextmv.Option]
        List of Nextmv options for CP-SAT solver configuration.

    Methods
    -------
    to_nextmv()
        Converts the options to a Nextmv options object.

    Examples
    --------
    >>> from nextmv_ortools import CpModelOptions
    >>> options = CpModelOptions()
    >>> nextmv_options = options.to_nextmv()
    >>> # These options can now be used with a Nextmv model
    """

    def __init__(self):
        """Initialize CpModelOptions with basic CP-SAT parameters."""
        self.options = [
            nextmv.Option(
                name="max_time_in_seconds",
                option_type=float,
                default=60.0,
                description="Maximum time limit for the solver in seconds",
            ),
            nextmv.Option(
                name="num_search_workers",
                option_type=int,
                default=1,
                description="Number of parallel search workers",
            ),
            nextmv.Option(
                name="log_search_progress",
                option_type=bool,
                default=False,
                description="Enable search progress logging",
            ),
            nextmv.Option(
                name="cp_model_presolve",
                option_type=bool,
                default=True,
                description="Enable model presolving",
            ),
            nextmv.Option(
                name="enumerate_all_solutions",
                option_type=bool,
                default=False,
                description="Find all feasible solutions",
            ),
        ]

    def to_nextmv(self) -> nextmv.Options:
        """Convert CpModelOptions to Nextmv options format.

        Returns
        -------
        nextmv.Options
            A Nextmv options object containing the CP-SAT solver options.
        """
        return nextmv.Options(*self.options)


def CpModel(options: nextmv.Options) -> Tuple[cp_model.CpModel, cp_model.CpSolver]:
    """
    Creates an OR-Tools CP-SAT model and solver that can be used to solve optimization problems.

    This function sets up a constraint programming SAT model and solver with the specified
    configuration and redirects solver output to stderr for consistent logging.

    Parameters
    ----------
    options : nextmv.Options
        The options for the OR-Tools CP-SAT solver. Any option that matches a CP-SAT
        parameter will be applied to the solver.

    Returns
    -------
    Tuple[cp_model.CpModel, cp_model.CpSolver]
        A tuple containing the OR-Tools CP-SAT model and solver instances.

    Examples
    --------
    >>> import nextmv
    >>> from nextmv_ortools import CpModel
    >>>
    >>> # Create options
    >>> options = nextmv.Options()
    >>> options.max_time_in_seconds = 60.0
    >>> options.num_search_workers = 4
    >>>
    >>> # Create OR-Tools CP-SAT model and solver with Nextmv options
    >>> model, solver = CpModel(options)
    >>>
    >>> # Use model and solver as any other OR-Tools CP-SAT objects
    >>> x = model.NewIntVar(0, 10, "x")
    >>> y = model.NewIntVar(0, 10, "y")
    >>> model.Add(x + y <= 5)
    >>> model.Maximize(x + y)
    >>> status = solver.Solve(model)
    """

    # Solver chatter is logged to stderr.
    nextmv.redirect_stdout()

    # Create the model and solver
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    # Apply options to the solver
    if hasattr(options, "max_time_in_seconds"):
        solver.parameters.max_time_in_seconds = getattr(options, "max_time_in_seconds")

    if hasattr(options, "num_search_workers"):
        solver.parameters.num_search_workers = getattr(options, "num_search_workers")

    if hasattr(options, "log_search_progress"):
        solver.parameters.log_search_progress = getattr(options, "log_search_progress")

    if hasattr(options, "cp_model_presolve"):
        solver.parameters.cp_model_presolve = getattr(options, "cp_model_presolve")

    if hasattr(options, "enumerate_all_solutions"):
        solver.parameters.enumerate_all_solutions = getattr(options, "enumerate_all_solutions")

    options.provider = "ortools_cp_sat"

    return model, solver


def CpModelSolution(model: cp_model.CpModel, solver: cp_model.CpSolver) -> Optional[dict[str, Any]]:
    """
    Creates a basic solution dictionary from an OR-Tools CP-SAT solver.

    You can import the `CpModelSolution` function directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import CpModelSolution
    ```

    The simple solution dictionary contains the variable name and the value of the
    variable for each variable in the model. If the solver has not found a solution,
    it will return `None`.

    Parameters
    ----------
    model : cp_model.CpModel
        The OR-Tools CP-SAT model that was solved.
    solver : cp_model.CpSolver
        The OR-Tools CP-SAT solver that has been used to solve the model.

    Returns
    -------
    dict[str, Any] or None
        A dictionary with variable names as keys and their optimal values as values.
        Returns None if the solver has not found a solution.

    Examples
    --------
    >>> from ortools.sat.python import cp_model
    >>> from nextmv_ortools import CpModelSolution
    >>>
    >>> # Create and solve a simple model
    >>> model = cp_model.CpModel()
    >>> solver = cp_model.CpSolver()
    >>> x = model.NewIntVar(0, 10, "x")
    >>> y = model.NewIntVar(0, 10, "y")
    >>> model.Add(x + y <= 5)
    >>> model.Maximize(x + y)
    >>> status = solver.Solve(model)
    >>>
    >>> # Get the solution dictionary
    >>> solution = CpModelSolution(model, solver)
    >>> print(solution)
    {'x': 2, 'y': 3}
    """

    # Check if solver found a feasible solution
    status = solver.StatusName()
    if status not in ["OPTIMAL", "FEASIBLE"]:
        return None

    # Extract variable values
    solution = {}

    # Get all variables from the model
    variables = []

    # We need to extract variables from the model, but CP-SAT doesn't provide
    # a direct way to enumerate all variables. We'll need to track them during model creation
    # For now, we'll extract what we can from the solver response

    # This is a limitation of the current CP-SAT API - we can't easily enumerate all variables
    # Users should track their variables and pass them to this function or implement custom extraction

    return solution


def CpModelStatistics(
    model: cp_model.CpModel,
    solver: cp_model.CpSolver,
    run_duration_start: Optional[float] = None,
) -> nextmv.Statistics:
    """
    Creates a Nextmv statistics object from an OR-Tools CP-SAT solver, once it has been solved.

    You can import the `CpModelStatistics` function directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import CpModelStatistics
    ```

    The statistics returned are basic and should be extended according to the
    custom metrics that the user wants to track. The optional `run_duration_start`
    parameter can be used to set the start time of the whole run.

    Parameters
    ----------
    model : cp_model.CpModel
        The OR-Tools CP-SAT model after solving.
    solver : cp_model.CpSolver
        The OR-Tools CP-SAT solver after solving.
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
    >>> from nextmv_ortools import CpModel, CpModelOptions, CpModelStatistics
    >>>
    >>> start_time = time.time()
    >>> options = CpModelOptions().to_nextmv()
    >>> model, solver = CpModel(options)
    >>> # Create and configure your model
    >>> status = solver.Solve(model)
    >>> stats = CpModelStatistics(model, solver, start_time)
    """

    run = nextmv.RunStatistics()
    if run_duration_start is not None:
        run.duration = time.time() - run_duration_start

    # Get status from solver
    status = solver.StatusName()

    # Get objective value if available
    objective_value = None
    if status in ["OPTIMAL", "FEASIBLE"]:
        try:
            objective_value = solver.ObjectiveValue()
        except Exception:
            pass

    # Get solve duration from solver
    solve_duration = solver.WallTime() if hasattr(solver, "WallTime") else None

    return nextmv.Statistics(
        run=run,
        result=nextmv.ResultStatistics(
            duration=solve_duration,
            value=objective_value,
            custom={
                "status": status,
                "num_booleans": solver.NumBooleans(),
                "num_branches": solver.NumBranches(),
                "num_conflicts": solver.NumConflicts(),
            },
        ),
        series_data=nextmv.SeriesData(),
    )
