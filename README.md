# Dashboard Demo

An interactive economic intelligence dashboard built with [Marimo](https://marimo.io), powered by [DuckDB](https://duckdb.org) for in-memory data generation, [Plotly](https://plotly.com/python) for interactive maps, and [Typst](https://typst.app) for PDF report generation.

## What it is

`dash.py` is a reactive Marimo notebook that simulates a US state-level economic dataset entirely in-memory using DuckDB SQL — no external data files required. It renders a dark-themed intelligence dashboard with:

- **Choropleth map** — interactive Plotly map of median household income by state
- **Sector revenue line chart** — 24-month trend for 5 industry sectors (SVG)
- **Innovation vs GDP scatter plot** — state-level bubble chart encoded by unemployment and population (SVG)
- **KPI cards** — national aggregates (avg income, unemployment, GDP growth, population, top innovator)
- **Export button** — saves all figures and compiles a PDF report via Typst

## Stack

| Tool | Role |
|------|------|
| [Marimo](https://marimo.io) | Reactive notebook / app framework |
| [DuckDB](https://duckdb.org) | In-memory SQL for deterministic data generation |
| [Plotly](https://plotly.com/python) | Interactive choropleth map |
| [Kaleido](https://github.com/plotly/Kaleido) | Static PNG export of Plotly figures |
| [Typst](https://typst.app) | PDF report compilation |

## Project structure

```
dashboard_demo/
├── dash.py          # Marimo notebook (the dashboard)
├── report.typ       # Typst report template
├── figures/         # Generated on first export
│   ├── map.png
│   ├── line_chart.svg
│   ├── scatter.svg
│   └── kpis.typ     # KPI values injected at export time
└── report.pdf       # Output — generated on first export
```

## Getting started

Install dependencies with [uv](https://docs.astral.sh/uv):

```bash
uv sync
```

Run the dashboard:

```bash
uv run marimo run dash.py
```

Or open it as an editable notebook:

```bash
uv run marimo edit dash.py
```

## Exporting the report

Click the **Export PDF Report** button at the bottom of the dashboard. This will:

1. Save `figures/map.png` (Plotly choropleth via Kaleido)
2. Save `figures/line_chart.svg` and `figures/scatter.svg`
3. Write `figures/kpis.typ` with the current KPI values
4. Compile `report.typ` → `report.pdf` using the Typst Python package

The PDF includes a dark-themed title page and white content pages with all three figures and a KPI summary row.

## Data

All data is synthetically generated using deterministic DuckDB arithmetic on state row-numbers. There are no real-world measurements — values are designed to look plausible for demonstration purposes.
