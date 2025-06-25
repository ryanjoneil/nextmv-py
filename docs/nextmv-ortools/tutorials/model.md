# Model

!!! tip "Reference"

    Find the reference for the solver modules in the reference section.

Use the solver classes to create OR-Tools models from Nextmv options. Each
solver type provides a convenient wrapper around the native OR-Tools solver
that integrates with the Nextmv platform.

## Linear Solver

```python
import nextmv_ortools as nor

options = nor.LinearSolverOptions().to_nextmv()
solver = nor.LinearSolver(options)

# Define variables and constraints
x = solver.NumVar(0, 10, "x")
y = solver.NumVar(0, 10, "y")
solver.Add(x + y <= 5)
solver.Maximize(x + y)

# Solve
status = solver.Solve()
```

## CP-SAT Solver

```python
import nextmv_ortools as nor

options = nor.CpSatOptions().to_nextmv()
model = nor.CpSat(options)

# Define variables and constraints
x = model.NewIntVar(0, 10, "x")
y = model.NewIntVar(0, 10, "y")
model.Add(x + y <= 5)
model.Maximize(x + y)

# Solve
solver = nor.cp_model.CpSolver()
status = solver.Solve(model)
```

## Knapsack Solver

```python
import nextmv_ortools as nor

options = nor.KnapsackOptions().to_nextmv()
solver = nor.KnapsackSolver(options)

# Define problem
values = [60, 100, 120]
weights = [10, 20, 30]
capacities = [50]

solver.Init(values, weights, capacities)
computed_value = solver.Solve()
```

## Vehicle Routing

```python
import nextmv_ortools as nor

options = nor.RoutingOptions().to_nextmv()
manager = nor.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
routing = nor.RoutingModel(manager, options)

# Define distance callback
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Solve
solution = routing.SolveWithParameters(search_parameters)
```

## Graph Algorithms

```python
import nextmv_ortools as nor

# Linear Sum Assignment
options = nor.LinearSumAssignmentOptions().to_nextmv()
assignment = nor.LinearSumAssignment(options)

# Max Flow
options = nor.MaxFlowOptions().to_nextmv()
max_flow = nor.MaxFlow(options)

# Min Cost Flow
options = nor.MinCostFlowOptions().to_nextmv()
min_cost_flow = nor.MinCostFlow(options)
```

Each solver integrates seamlessly with the Nextmv platform while providing
access to the full power of OR-Tools.