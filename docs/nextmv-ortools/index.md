# Overview

<!-- markdownlint-disable MD033 MD013 -->

<p align="center">
  <a href="https://nextmv.io"><img src="https://cdn.prod.website-files.com/60dee0fad10d14c8ab66dd74/66bded64436a6d10a64138c3_blog-banner-the-sushi-is-ready-bunny-p-2000.png" alt="Nextmv" width="45%"></a>
</p>
<p align="center">
    <em>Nextmv: The home for all your optimization work</em>
</p>
<p align="center">
<a href="https://pypi.org/project/nextmv-ortools" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/nextmv-ortools.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/nextmv-ortools" target="_blank">
    <img src="https://img.shields.io/pypi/v/nextmv-ortools?color=%2334D058&label=nextmv-ortools" alt="Package version">
</a>
</p>

<!-- markdownlint-enable MD033 MD013 -->

The [Nextmv & OR-Tools Python SDK][nextmv-ortools], `nextmv-ortools`, is a
package to interact programmatically with Nextmv and OR-Tools solvers from
Python. This package provides standardized integration points for multiple
OR-Tools solver types including linear programming, constraint programming SAT,
knapsack optimization, vehicle routing, and graph algorithms.

A great way to get started is to check out the [community
apps][community-apps-get-started].

!!! warning

    Please note that `nextmv-ortools` is provided as _source-available_
    software (not _open-source_). For further information, please refer to the
    [LICENSE](https://github.com/nextmv-io/nextmv-py/blob/develop/nextmv-ortools/LICENSE) file.

## Installation

The package is hosted on [PyPI][nextmv-ortools-pypi]. Python `>=3.9` is
required.

Install via `pip`:

```bash
pip install nextmv-ortools
```

!!! tip

    Note that `nextmv-ortools` installs the `nextmv_ortools` package, which is
    the importable name for the SDK.

## Supported Solvers

The package provides integration for the following OR-Tools solvers:

- **Linear Programming** - `ortools.linear_solver.pywraplp.Solver`
- **Constraint Programming SAT** - `ortools.sat.python.cp_model.CpModel`
- **Knapsack Optimization** - `ortools.algorithms.python.knapsack_solver.KnapsackSolver`
- **Vehicle Routing** - `ortools.constraint_solver.pywrapcp.RoutingModel`
- **Linear Sum Assignment** - `ortools.graph.python.linear_sum_assignment.SimpleLinearSumAssignment`
- **Max Flow** - `ortools.graph.python.max_flow.SimpleMaxFlow`
- **Min Cost Flow** - `ortools.graph.python.min_cost_flow.SimpleMinCostFlow`

Each solver provides the same 4 integration components:
- **Options** - Maps solver parameters to command line flags
- **Solver** - Handles solver instantiation based on command line options
- **Solution** - Maps optimized models to solution dictionaries for JSON serialization
- **Statistics** - Extracts standard run statistics for the Nextmv environment

[nextmv-ortools-pypi]: https://pypi.org/project/nextmv-ortools/
[nextmv-ortools]: https://github.com/nextmv-io/nextmv-py/tree/develop/nextmv-ortools
[community-apps-get-started]: https://docs.nextmv.io/docs/use-cases/community-apps/get-started