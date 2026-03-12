// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║  REPORT TEMPLATE                                                             ║
// ║  Layout, colours, and components for the US Economic Intelligence Dashboard  ║
// ╚══════════════════════════════════════════════════════════════════════════════╝

// ── Title-page colour palette ─────────────────────────────────────────────────
#let tp-accent   = rgb("#2dd4a0")
#let tp-text     = rgb("#94d4c8")
#let tp-dim      = rgb("#2a5a48")
#let tp-blue-mid = rgb("#0d7a9a")
#let tp-purple   = rgb("#818cf8")

// ── Content-page colour palette ───────────────────────────────────────────────
#let c-accent    = rgb("#1a9a78")   // darkened teal — readable on white
#let c-blue      = rgb("#0d4f8b")
#let c-text      = rgb("#1e2a28")   // near-black body text
#let c-label     = rgb("#3a7a6a")   // muted teal for labels / captions
#let c-border    = rgb("#c0dcd6")   // light teal border
#let c-card-fill = rgb("#f0faf8")   // very light teal card background
#let c-rule      = rgb("#0d7a9a")   // blue rule under section headings

// ══════════════════════════════════════════════════════════════════════════════
// CONTENT-PAGE COMPONENTS
// ══════════════════════════════════════════════════════════════════════════════

/// Numbered section heading with a teal rule underneath.
#let section-label(n, title) = [
  #text(size: 7pt, fill: c-label, tracking: 0.12em)[SECTION #n]
  #v(0.25em)
  #text(size: 18pt, weight: "bold", fill: c-accent)[#title]
  #v(0.2em)
  #line(length: 100%, stroke: (paint: c-rule, thickness: 0.5pt))
  #v(0.9em)
]

/// Rounded, bordered container for figures / charts.
#let fig-block(body) = block(
  width: 100%,
  radius: 8pt,
  clip: true,
  stroke: (paint: c-border, thickness: 0.75pt),
  body,
)

/// Small muted caption text.
#let caption-text(body) = text(size: 8pt, fill: c-label)[#body]

/// Small all-caps label above a chart (e.g. "REVENUE INDEX · 24-MONTH TREND").
#let chart-label(body) = text(size: 7.5pt, fill: c-label, tracking: 0.08em)[#upper(body)]

/// Metric card used in the KPI summary row.
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

/// Tinted card for notes, methodology blocks, etc.
#let note-block(title: "NOTE", body) = block(
  width: 100%,
  radius: 8pt,
  stroke: (paint: c-border, thickness: 0.5pt),
  fill: c-card-fill,
  inset: (x: 16pt, y: 12pt),
)[
  #text(size: 7.5pt, fill: c-label, tracking: 0.1em)[#upper(title)]
  #v(0.4em)
  #text(size: 8.5pt, fill: c-text)[#body]
]

// ══════════════════════════════════════════════════════════════════════════════
// REPORT TEMPLATE FUNCTION
// ══════════════════════════════════════════════════════════════════════════════

/// Top-level template.  Apply with:
///   #show: report.with(title: ..., subtitle: ..., ...)
///
/// Parameters
///   title      — array of strings, one per title line
///   subtitle   — subtitle string shown below the title
///   stats      — array of (value, label, accent) dictionaries for the stat row
///   disclaimer — all-caps notice at the bottom of the title page
///   generator  — tool credits line at the very bottom
///   body       — document body (injected automatically by #show: …)
#let report(
  title:      ("US ECONOMIC", "INTELLIGENCE DASHBOARD"),
  subtitle:   "Annual Indicators Report · 50 States · 2024–2025",
  stats: (
    (value: "50", label: "STATES",  accent: tp-accent),
    (value: "5",  label: "SECTORS", accent: tp-blue-mid),
    (value: "24", label: "MONTHS",  accent: tp-purple),
  ),
  disclaimer: "SIMULATED DATA · FOR DEMONSTRATION PURPOSES ONLY",
  generator:  "Generated with Marimo · DuckDB · Plotly · Typst",
  body,
) = {

  // ── Title page (full-bleed dark gradient) ─────────────────────────────────
  page(
    margin: 0pt,
    fill: gradient.linear(
      rgb("#05080f"), rgb("#0c1e36"), rgb("#05140e"),
      angle: 135deg,
    ),
  )[
    #align(center + horizon)[
      #v(1fr)

      #rect(width: 56pt, height: 3pt, fill: tp-accent, radius: 1.5pt)
      #v(1.8em)

      #for line in title [
        #text(size: 32pt, weight: "bold", fill: tp-accent, tracking: 0.05em)[#line]
        #v(0.1em)
      ]

      #v(1.2em)
      #text(size: 11pt, fill: tp-text)[#subtitle]

      #v(2em)
      #line(length: 160pt, stroke: (paint: tp-accent, thickness: 0.4pt, dash: "dashed"))
      #v(1.8em)

      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 0pt,
        ..stats.map(s => align(center)[
          #text(size: 20pt, weight: "bold", fill: s.accent)[#s.value]
          #linebreak()
          #text(size: 7.5pt, fill: tp-dim, tracking: 0.1em)[#s.label]
        ]),
      )

      #v(1fr)

      #text(size: 7.5pt, fill: tp-dim, tracking: 0.08em)[#disclaimer]
      #v(1.2em)
      #text(size: 7pt, fill: rgb("#1a3828"))[#generator]
      #v(2.4em)
    ]
  ]

  // ── Content-page defaults (apply to all pages that follow) ────────────────
  set page(paper: "us-letter", margin: (x: 48pt, y: 48pt), fill: white)
  set text(fill: c-text, font: "Arial", size: 10pt)
  set par(leading: 0.65em)

  body
}
