# Statistics

!!! tip "Reference"

    Find the reference for the statistics modules in the reference section.

Use the statistics classes to extract run metrics from OR-Tools solvers for
reporting and analysis. Each solver type provides a statistics class that
captures relevant performance information.

## Linear Solver Statistics

```python
import nextmv_ortools as nor

# After solving the model
solver = nor.LinearSolver(options)
# ... define and solve model ...

stats = nor.LinearSolverStatistics(solver)
stats_dict = stats.to_dict()
```

## CP-SAT Statistics

```python
import nextmv_ortools as nor

# After solving the model
model = nor.CpSat(options)
solver = nor.cp_model.CpSolver()
# ... define and solve model ...

stats = nor.CpSatStatistics(solver)
stats_dict = stats.to_dict()
```

## Knapsack Statistics

```python
import nextmv_ortools as nor

# After solving the model
solver = nor.KnapsackSolver(options)
# ... define and solve model ...

stats = nor.KnapsackStatistics(solver)
stats_dict = stats.to_dict()
```

## Routing Statistics

```python
import nextmv_ortools as nor

# After solving the model
manager = nor.RoutingIndexManager(...)
routing = nor.RoutingModel(manager, options)
# ... define and solve model ...

stats = nor.RoutingStatistics(routing)
stats_dict = stats.to_dict()
```

## Graph Algorithm Statistics

```python
import nextmv_ortools as nor

# Linear Sum Assignment
assignment = nor.LinearSumAssignment(options)
# ... solve assignment ...
stats = nor.LinearSumAssignmentStatistics(assignment)
stats_dict = stats.to_dict()

# Max Flow
max_flow = nor.MaxFlow(options)
# ... solve flow ...
stats = nor.MaxFlowStatistics(max_flow)
stats_dict = stats.to_dict()

# Min Cost Flow
min_cost_flow = nor.MinCostFlow(options)
# ... solve flow ...
stats = nor.MinCostFlowStatistics(min_cost_flow)
stats_dict = stats.to_dict()
```

## Example Usage

```python
import nextmv
import nextmv_ortools as nor

# Configure and solve
options = nor.LinearSolverOptions().to_nextmv()
solver = nor.LinearSolver(options)

# Define and solve problem
x = solver.NumVar(0, 10, "x")
y = solver.NumVar(0, 10, "y")
solver.Add(x + y <= 5)
solver.Maximize(x + y)
status = solver.Solve()

# Extract statistics
stats = nor.LinearSolverStatistics(solver)

# Output with statistics
output = nextmv.Output(
    solution={"status": "OPTIMAL"},
    statistics=stats.to_dict()
)
print(output.json_string())
```

## Common Statistics

All statistics classes typically provide information about:

- **Runtime**: Time taken to solve the model
- **Status**: Final solver status (optimal, feasible, infeasible, etc.)
- **Iterations**: Number of solver iterations (where applicable)
- **Objective Value**: Final objective value (for optimization problems)
- **Memory Usage**: Peak memory consumption (where available)

Each statistics class provides a standardized interface to extract performance
metrics from the corresponding OR-Tools solver, enabling consistent monitoring
and analysis across different solver types.