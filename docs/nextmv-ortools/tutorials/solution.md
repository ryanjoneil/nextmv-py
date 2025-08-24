# Solution

!!! tip "Reference"

    Find the reference for the solution modules in the reference section.

Use the solution classes to transform OR-Tools models into dictionaries for JSON
serialization. Each solver type provides a solution class that extracts relevant
information from the solved model.

## Linear Solver Solution

```python
import nextmv_ortools as nor

# After solving the model
solver = nor.LinearSolver(options)
# ... define and solve model ...

solution = nor.LinearSolverSolution(solver)
solution_dict = solution.to_dict()
```

## CP-SAT Solution

```python
import nextmv_ortools as nor

# After solving the model
model = nor.CpSat(options)
solver = nor.cp_model.CpSolver()
# ... define and solve model ...

solution = nor.CpSatSolution(model, solver)
solution_dict = solution.to_dict()
```

## Knapsack Solution

```python
import nextmv_ortools as nor

# After solving the model
solver = nor.KnapsackSolver(options)
# ... define and solve model ...

solution = nor.KnapsackSolution(solver)
solution_dict = solution.to_dict()
```

## Routing Solution

```python
import nextmv_ortools as nor

# After solving the model
manager = nor.RoutingIndexManager(...)
routing = nor.RoutingModel(manager, options)
# ... define and solve model ...

solution = nor.RoutingSolution(manager, routing, solution)
solution_dict = solution.to_dict()
```

## Graph Algorithm Solutions

```python
import nextmv_ortools as nor

# Linear Sum Assignment
assignment = nor.LinearSumAssignment(options)
# ... solve assignment ...
solution = nor.LinearSumAssignmentSolution(assignment)
solution_dict = solution.to_dict()

# Max Flow
max_flow = nor.MaxFlow(options)
# ... solve flow ...
solution = nor.MaxFlowSolution(max_flow)
solution_dict = solution.to_dict()

# Min Cost Flow
min_cost_flow = nor.MinCostFlow(options)
# ... solve flow ...
solution = nor.MinCostFlowSolution(min_cost_flow)
solution_dict = solution.to_dict()
```

## Example Usage

```python
import json
import nextmv
import nextmv_ortools as nor

# Configure and solve
options = nor.LinearSolverOptions().to_nextmv()
solver = nor.LinearSolver(options)

# Define problem
x = solver.NumVar(0, 10, "x")
y = solver.NumVar(0, 10, "y")
solver.Add(x + y <= 5)
solver.Maximize(x + y)

# Solve and extract solution
status = solver.Solve()
solution = nor.LinearSolverSolution(solver)

# Output as JSON
output = nextmv.Output(solution=solution.to_dict())
print(output.json_string())
```

Each solution class provides a standardized interface to extract results from
the corresponding OR-Tools solver, making it easy to integrate with the Nextmv
platform.