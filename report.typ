#import "layout.typ": *
#import "figures/kpis.typ": kpi-data

#show: report.with(
  title: ("US ECONOMIC", "INTELLIGENCE DASHBOARD"),
  subtitle: "Annual Indicators Report · 50 States · 2024–2025",
  stats: (
    (value: "50", label: "STATES",  accent: tp-accent),
    (value: "5",  label: "SECTORS", accent: tp-blue-mid),
    (value: "24", label: "MONTHS",  accent: tp-purple),
  ),
  disclaimer: "SIMULATED DATA · FOR DEMONSTRATION PURPOSES ONLY",
  generator:  "Generated with Marimo · DuckDB · Plotly · Typst",
)

// ══════════════════════════════════════════════════════════════════════════════
// SECTION 01 – GEOGRAPHIC OVERVIEW
// ══════════════════════════════════════════════════════════════════════════════

#section-label("01", "Geographic Overview")

#caption-text[
  The choropleth map below shows simulated median household income across all
  50 US states. Deep blue tones indicate lower income levels; teal–green tones
  signal higher values. Hover data includes unemployment rate, innovation index,
  GDP growth, and total population.
]
#v(0.8em)

#fig-block[
  #image("figures/map.png", width: 100%)
]

#v(1.2em)

#grid(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  gutter: 10pt,
  ..kpi-data.map(((label, value, accent)) => kpi-card(label, value, accent))
)

// ══════════════════════════════════════════════════════════════════════════════
// SECTION 02 – SECTOR & STATE ANALYTICS
// ══════════════════════════════════════════════════════════════════════════════

#pagebreak()
#section-label("02", "Sector & State Analytics")

#grid(
  columns: (1fr, 1fr),
  gutter: 14pt,

  [
    #chart-label[Revenue Index · 24-Month Trend]
    #v(0.45em)
    #fig-block[
      #image("figures/line_chart.svg", width: 100%)
    ]
    #v(0.5em)
    #caption-text[
      Monthly sector revenue index for Technology, Healthcare, Manufacturing,
      Finance, and Energy over a simulated 24-month period (Jan 2024 – Dec 2025).
      Technology leads with the steepest growth trajectory.
    ]
  ],

  [
    #chart-label[Innovation Index vs GDP Growth]
    #v(0.45em)
    #fig-block[
      #image("figures/scatter.svg", width: 100%)
    ]
    #v(0.5em)
    #caption-text[
      Each bubble represents a US state. Colour encodes unemployment rate
      (blue = high, teal = low). Bubble size scales proportionally with
      simulated population.
    ]
  ],
)

#v(1.4em)

#note-block(title: "Data Methodology")[
  All data in this report is synthetically generated using DuckDB deterministic
  arithmetic on state row-numbers. Values are designed to produce plausible
  distributions without representing real-world measurements. Sector revenue
  indices follow linear trend models with periodic noise. State-level indicators
  use fixed modular arithmetic to ensure reproducibility across runs.
]
