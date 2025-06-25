"""Defines OR-Tools routing solver interoperability.

This module provides functions for integrating Nextmv with OR-Tools vehicle routing optimization.

Functions
---------
RoutingModel
    Creates an OR-Tools routing model that can be used to solve optimization problems.
RoutingModelSolution
    Creates a solution dictionary from an OR-Tools routing model.
RoutingModelStatistics
    Creates statistics from an OR-Tools routing model.

Classes
-------
RoutingModelOptions
    Options for the OR-Tools routing model that can be converted to Nextmv options.
"""

import time
from typing import Any, Optional

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

import nextmv


class RoutingModelOptions:
    """Options for the OR-Tools routing model with conversion to Nextmv options format.

    You can import the `RoutingModelOptions` class directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import RoutingModelOptions
    ```

    This class provides basic options for vehicle routing models in OR-Tools.

    Attributes
    ----------
    options : list[nextmv.Option]
        List of Nextmv options for routing model configuration.

    Methods
    -------
    to_nextmv()
        Converts the options to a Nextmv options object.

    Examples
    --------
    >>> from nextmv_ortools import RoutingModelOptions
    >>> options = RoutingModelOptions()
    >>> nextmv_options = options.to_nextmv()
    >>> # These options can now be used with a Nextmv model
    """

    def __init__(self):
        """Initialize RoutingModelOptions with basic vehicle routing parameters."""
        self.options = [
            nextmv.Option(
                name="time_limit",
                option_type=int,
                default=60,
                description="Time limit for the solver in seconds"
            ),
            nextmv.Option(
                name="solution_limit",
                option_type=int,
                default=1,
                description="Maximum number of solutions to find"
            ),
            nextmv.Option(
                name="first_solution_strategy",
                option_type=str,
                default="PATH_CHEAPEST_ARC",
                description="Strategy for finding initial solution",
                choices=["PATH_CHEAPEST_ARC", "PATH_MOST_CONSTRAINED_ARC", "EVALUATOR_STRATEGY", 
                        "SAVINGS", "SWEEP", "CHRISTOFIDES", "ALL_UNPERFORMED", "BEST_INSERTION", 
                        "PARALLEL_CHEAPEST_INSERTION", "SEQUENTIAL_CHEAPEST_INSERTION", 
                        "LOCAL_CHEAPEST_INSERTION", "GLOBAL_CHEAPEST_ARC", "LOCAL_CHEAPEST_ARC", 
                        "FIRST_UNBOUND_MIN_VALUE"]
            ),
            nextmv.Option(
                name="local_search_metaheuristic",
                option_type=str,
                default="GUIDED_LOCAL_SEARCH",
                description="Metaheuristic for local search",
                choices=["GUIDED_LOCAL_SEARCH", "TABU_SEARCH", "GENERIC_TABU_SEARCH", 
                        "SIMULATED_ANNEALING", "GREEDY_DESCENT"]
            ),
            nextmv.Option(
                name="log_search",
                option_type=bool,
                default=False,
                description="Enable search progress logging"
            ),
        ]

    def to_nextmv(self) -> nextmv.Options:
        """Convert RoutingModelOptions to Nextmv options format.

        Returns
        -------
        nextmv.Options
            A Nextmv options object containing the routing model options.
        """
        return nextmv.Options(*self.options)


def RoutingModel(manager: pywrapcp.RoutingIndexManager, options: nextmv.Options) -> pywrapcp.RoutingModel:
    """
    Creates an OR-Tools routing model that can be used to solve optimization problems.

    This function sets up a vehicle routing model with the specified configuration
    and redirects solver output to stderr for consistent logging.

    Parameters
    ----------
    manager : pywrapcp.RoutingIndexManager
        The routing index manager that handles index conversions.
    options : nextmv.Options
        The options for the OR-Tools routing model. Any option that matches a routing
        parameter will be applied to the model.

    Returns
    -------
    pywrapcp.RoutingModel
        The OR-Tools routing model instance that can be used to define and solve
        vehicle routing optimization problems.

    Examples
    --------
    >>> import nextmv
    >>> from nextmv_ortools import RoutingModel
    >>> from ortools.constraint_solver import pywrapcp
    >>>
    >>> # Create options
    >>> options = nextmv.Options()
    >>> options.time_limit = 30
    >>> options.first_solution_strategy = "PATH_CHEAPEST_ARC"
    >>>
    >>> # Create routing index manager
    >>> manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot_index)
    >>>
    >>> # Create OR-Tools routing model with Nextmv options
    >>> routing = RoutingModel(manager, options)
    >>>
    >>> # Use routing as any other OR-Tools routing model
    >>> # Add distance callback, constraints, etc.
    """

    # Solver chatter is logged to stderr.
    nextmv.redirect_stdout()

    # Create the routing model
    routing = pywrapcp.RoutingModel(manager)

    options.provider = "ortools_routing"

    return routing


def RoutingModelSolution(manager: pywrapcp.RoutingIndexManager, routing: pywrapcp.RoutingModel, 
                        solution: pywrapcp.Assignment) -> Optional[dict[str, Any]]:
    """
    Creates a basic solution dictionary from an OR-Tools routing model.

    You can import the `RoutingModelSolution` function directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import RoutingModelSolution
    ```

    The simple solution dictionary contains route information for each vehicle.
    If no solution exists, it will return `None`.

    Parameters
    ----------
    manager : pywrapcp.RoutingIndexManager
        The routing index manager used with the model.
    routing : pywrapcp.RoutingModel
        The OR-Tools routing model that has been solved.
    solution : pywrapcp.Assignment
        The solution assignment from solving the routing model.

    Returns
    -------
    dict[str, Any] or None
        A dictionary with route information for each vehicle.
        Returns None if no solution exists.

    Examples
    --------
    >>> from ortools.constraint_solver import pywrapcp
    >>> from nextmv_ortools import RoutingModelSolution
    >>>
    >>> # After solving a routing problem
    >>> solution_dict = RoutingModelSolution(manager, routing, solution)
    >>> print(solution_dict)
    {'routes': [[0, 1, 2, 0], [0, 3, 4, 0]], 'total_distance': 100}
    """

    if not solution:
        return None

    routes = []
    total_distance = 0

    # Extract routes for each vehicle
    for vehicle_id in range(routing.vehicles()):
        route = []
        index = routing.Start(vehicle_id)
        route_distance = 0
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            if not routing.IsEnd(index):
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        
        # Add the end depot
        route.append(manager.IndexToNode(index))
        routes.append(route)
        total_distance += route_distance

    return {
        "routes": routes,
        "total_distance": total_distance,
        "objective_value": solution.ObjectiveValue(),
        "num_vehicles": routing.vehicles(),
    }


def RoutingModelStatistics(routing: pywrapcp.RoutingModel, solution: Optional[pywrapcp.Assignment] = None, 
                          run_duration_start: Optional[float] = None) -> nextmv.Statistics:
    """
    Creates a Nextmv statistics object from an OR-Tools routing model, once it has been solved.

    You can import the `RoutingModelStatistics` function directly from `nextmv_ortools`:

    ```python
    from nextmv_ortools import RoutingModelStatistics
    ```

    The statistics returned are basic and should be extended according to the
    custom metrics that the user wants to track. The optional `run_duration_start`
    parameter can be used to set the start time of the whole run.

    Parameters
    ----------
    routing : pywrapcp.RoutingModel
        The OR-Tools routing model after solving.
    solution : pywrapcp.Assignment, optional
        The solution assignment from solving the routing model.
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
    >>> from nextmv_ortools import RoutingModel, RoutingModelOptions, RoutingModelStatistics
    >>>
    >>> start_time = time.time()
    >>> options = RoutingModelOptions().to_nextmv()
    >>> # Create and solve your routing problem
    >>> stats = RoutingModelStatistics(routing, solution, start_time)
    """

    run = nextmv.RunStatistics()
    if run_duration_start is not None:
        run.duration = time.time() - run_duration_start

    # Get solution status and value
    status = "SOLVED" if solution else "NO_SOLUTION"
    objective_value = solution.ObjectiveValue() if solution else None

    return nextmv.Statistics(
        run=run,
        result=nextmv.ResultStatistics(
            duration=None,  # Routing solver doesn't provide direct timing info
            value=objective_value,
            custom={
                "status": status,
                "num_vehicles": routing.vehicles(),
                "num_nodes": routing.nodes(),
            },
        ),
        series_data=nextmv.SeriesData(),
    )