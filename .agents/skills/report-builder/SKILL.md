---
name: report-builder
description: "Build polished Bitwise ad hoc reports using AnalystKit's canonical HTML/PDF report shell, including cover pages, KPI cards, tables, SVG/Plotly chart panels, export, and visual QA. Use for client-request reports, CIO readouts, workflow audits, portfolio simulation summaries, and similar one-off materials."
---

# AnalystKit Report Builder

Use this skill when the user asks for an ad hoc Bitwise report, client request
report, research readout, CIO note, workflow audit, or polished PDF/HTML
summary. The goal is to use the shared AnalystKit report style instead of
copying report code from Simmons or chart-generator folders.

When working from the AnalystKit repository, read:

1. `REPORT_RECIPES.md` for the production report workflow and examples.
2. `AI_REFERENCE.md` for exact function signatures.
3. `CHART_RECIPES.md` if the report includes Plotly charts.

## Setup

```python
import analystkit as ak
```

## Default Workflow

1. Load, normalize, and audit the source data.
2. Save support materials such as cleaned CSVs, analysis JSON, or workbooks.
3. Build a report with `ak.ReportDocument` and `ak.ReportPage`.
4. Use built-in components before writing custom HTML/CSS:
   `ak.metric_grid`, `ak.panel`, `ak.bullet_list`, `ak.html_table`,
   `ak.chart_panel`, `ak.image_panel`, `ak.line_chart_svg`,
   `ak.horizontal_bar_svg`.
5. Save HTML first.
6. Export PDF with `ReportDocument.export_pdf()` or `ak.export_report_pdf()`.
7. Render PDF pages and make a contact sheet when layout matters.

## Design Defaults

- Letter pages, zero print margins, Playwright PDF export.
- Dark Bitwise cover with brand, eyebrow, Items title, subtitle, three meta
  tiles, and a small note.
- Interior pages use a Bitwise header, mono page kicker, Items section title,
  short intro, dense cards/panels/tables/charts, and footer page number.
- Use report-native SVG helpers for compact operational charts.
- Use Plotly + `ak.apply_theme()` for analytical centerpiece charts, then embed
  the exported image with `ak.image_panel()`.
- Keep audit and methodology visible, usually as a final page or method note.

## Quality Bar

- Every metric on the cover or cards should tie back to the saved support data.
- Tables should right-align numeric columns with `numeric_columns=[...]`.
- Inspect HTML and rendered PDF output; make a contact sheet for multi-page
  reports.
- Keep generated outputs in a predictable folder such as `outputs/<report_slug>/`.
- Do not commit private source data or generated client outputs unless the user
  explicitly asks.
