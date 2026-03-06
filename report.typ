// ── Title-page colour palette ─────────────────────────────────────────────────
#let tp-accent    = rgb("#2dd4a0")
#let tp-text      = rgb("#94d4c8")
#let tp-dim       = rgb("#2a5a48")
#let tp-blue-mid  = rgb("#0d7a9a")

// ── Content-page colour palette ───────────────────────────────────────────────
#let c-accent     = rgb("#1a9a78")   // darkened teal — readable on white
#let c-blue       = rgb("#0d4f8b")
#let c-text       = rgb("#1e2a28")   // near-black body text
#let c-label      = rgb("#3a7a6a")   // muted teal for labels / captions
#let c-border     = rgb("#c0dcd6")   // light teal border
#let c-card-fill  = rgb("#f0faf8")   // very light teal card background
#let c-rule       = rgb("#0d7a9a")   // blue rule under section headings

// ── Defaults (white pages) ────────────────────────────────────────────────────
#set page(paper: "us-letter", margin: (x: 48pt, y: 48pt), fill: white)
#set text(fill: c-text, font: "Arial", size: 10pt)
#set par(leading: 0.65em)

// ── KPI data (written by dash.py export) ─────────────────────────────────────
#import "figures/kpis.typ": kpi-data

// ── Content-page helpers ──────────────────────────────────────────────────────
#let section-label(n, title) = [
  #text(size: 7pt, fill: c-label, tracking: 0.12em)[SECTION #n]
  #v(0.25em)
  #text(size: 18pt, weight: "bold", fill: c-accent)[#title]
  #v(0.2em)
  #line(length: 100%, stroke: (paint: c-rule, thickness: 0.5pt))
  #v(0.9em)
]

#let fig-block(body) = block(
  width: 100%,
  radius: 8pt,
  clip: true,
  stroke: (paint: c-border, thickness: 0.75pt),
  body,
)

#let caption-text(body) = text(size: 8pt, fill: c-label)[#body]

#let kpi-card(label, value, accent) = block(
  width: 100%,
  radius: 6pt,
  stroke: (paint: accent.lighten(50%), thickness: 0.5pt),
  fill: accent.lighten(88%),
  inset: (x: 10pt, y: 10pt),
)[
  #text(size: 7pt, fill: c-label, tracking: 0.06em)[#upper(label)]
  #v(0.35em)
  #text(size: 17pt, weight: "bold", fill: accent)[#value]
]

// ══════════════════════════════════════════════════════════════════════════════
// TITLE PAGE  (dark gradient override)
// ══════════════════════════════════════════════════════════════════════════════
#page(
  margin: 0pt,
  fill: gradient.linear(rgb("#05080f"), rgb("#0c1e36"), rgb("#05140e"), angle: 135deg),
)[
  #align(center + horizon)[
    #v(1fr)

    #rect(width: 56pt, height: 3pt, fill: tp-accent, radius: 1.5pt)
    #v(1.8em)

    #text(size: 32pt, weight: "bold", fill: tp-accent, tracking: 0.05em)[
      US ECONOMIC
    ]
    #v(0.1em)
    #text(size: 32pt, weight: "bold", fill: tp-accent, tracking: 0.05em)[
      INTELLIGENCE DASHBOARD
    ]

    #v(1.2em)
    #text(size: 11pt, fill: tp-text)[
      Annual Indicators Report · 50 States · 2024–2025
    ]

    #v(2em)
    #line(length: 160pt, stroke: (paint: tp-accent, thickness: 0.4pt, dash: "dashed"))
    #v(1.8em)

    #grid(
      columns: (1fr, 1fr, 1fr),
      gutter: 0pt,
      align(center)[
        #text(size: 20pt, weight: "bold", fill: tp-accent)[50]
        #linebreak()
        #text(size: 7.5pt, fill: tp-dim, tracking: 0.1em)[STATES]
      ],
      align(center)[
        #text(size: 20pt, weight: "bold", fill: tp-blue-mid)[5]
        #linebreak()
        #text(size: 7.5pt, fill: tp-dim, tracking: 0.1em)[SECTORS]
      ],
      align(center)[
        #text(size: 20pt, weight: "bold", fill: rgb("#818cf8"))[24]
        #linebreak()
        #text(size: 7.5pt, fill: tp-dim, tracking: 0.1em)[MONTHS]
      ],
    )

    #v(1fr)

    #text(size: 7.5pt, fill: tp-dim, tracking: 0.08em)[
      SIMULATED DATA · FOR DEMONSTRATION PURPOSES ONLY
    ]
    #v(1.2em)
    #text(size: 7pt, fill: rgb("#1a3828"))[
      Generated with Marimo · DuckDB · Plotly · Typst
    ]
    #v(2.4em)
  ]
]

// ══════════════════════════════════════════════════════════════════════════════
// SECTION 01 – GEOGRAPHIC OVERVIEW
// ══════════════════════════════════════════════════════════════════════════════
#pagebreak()
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

// KPI summary row
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

  // ── Line chart ─────────────────────────────────────────────────────────────
  [
    #text(size: 7.5pt, fill: c-label, tracking: 0.08em)[
      REVENUE INDEX · 24-MONTH TREND
    ]
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

  // ── Scatter chart ──────────────────────────────────────────────────────────
  [
    #text(size: 7.5pt, fill: c-label, tracking: 0.08em)[
      INNOVATION INDEX vs GDP GROWTH
    ]
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

// ── Methodology note ──────────────────────────────────────────────────────────
#block(
  width: 100%,
  radius: 8pt,
  stroke: (paint: c-border, thickness: 0.5pt),
  fill: c-card-fill,
  inset: (x: 16pt, y: 12pt),
)[
  #text(size: 7.5pt, fill: c-label, tracking: 0.1em)[DATA METHODOLOGY]
  #v(0.4em)
  #text(size: 8.5pt, fill: c-text)[
    All data in this report is synthetically generated using DuckDB deterministic
    arithmetic on state row-numbers. Values are designed to produce plausible
    distributions without representing real-world measurements. Sector revenue
    indices follow linear trend models with periodic noise. State-level indicators
    use fixed modular arithmetic to ensure reproducibility across runs.
  ]
]
