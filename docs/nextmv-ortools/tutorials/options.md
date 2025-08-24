# Options

!!! tip "Reference"

    Find the reference for the `options` modules in the reference section.

Use options to capture parameters (i.e.: configurations) for the run. Each
solver type in `nextmv-ortools` provides its own options class that captures
the native OR-Tools parameters, and the `to_nextmv()` method allows you to
convert them to [`nextmv` options][nextmv-options], for convenience.

## Linear Solver Options

```python
import nextmv_ortools as nor

options = nor.LinearSolverOptions().to_nextmv()
options.parse()
```

## CP-SAT Options

```python
import nextmv_ortools as nor

options = nor.CpSatOptions().to_nextmv()
options.parse()
```

## Knapsack Options

```python
import nextmv_ortools as nor

options = nor.KnapsackOptions().to_nextmv()
options.parse()
```

## Routing Options

```python
import nextmv_ortools as nor

options = nor.RoutingOptions().to_nextmv()
options.parse()
```

## Graph Solver Options

For graph algorithms (Linear Sum Assignment, Max Flow, Min Cost Flow):

```python
import nextmv_ortools as nor

# Linear Sum Assignment
options = nor.LinearSumAssignmentOptions().to_nextmv()
options.parse()

# Max Flow
options = nor.MaxFlowOptions().to_nextmv()
options.parse()

# Min Cost Flow
options = nor.MinCostFlowOptions().to_nextmv()
options.parse()
```

```bash
$ python main.py --help
```

For more information on how to use options, see the [`nextmv`
options][nextmv-options] documentation.

[nextmv-options]: ../../nextmv/tutorials/options.md