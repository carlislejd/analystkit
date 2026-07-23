# AnalystKit Report Recipes for Agents

This is the house style for ad hoc Bitwise reports: the kind of polished,
client-request, CIO-readout, workflow-audit, or internal research report that
used to get copied from Simmons or chart generator project folders.

## What the Reviewed Reports Do

The reusable pattern came from Simmons portfolio reports and the latest chart
generator request-log analysis report produced on July 23, 2026.

Common traits:

- Build deterministic analysis first, then render a self-contained HTML report.
- Use Letter pages, zero print margins, and Playwright HTML-to-PDF export.
- Start with a dark Bitwise cover: `bitwise.`, an eyebrow, a large Items title,
  supporting copy, and three metadata tiles.
- Use compact interior pages with a page header, chapter kicker, Items section
  title, one short intro paragraph, metric cards, charts, tables, and panels.
- Use PP Neue Montreal for body text, PP Neue Montreal Mono for labels/tables,
  and Items for brand/title text.
- Keep report charts simple and legible. Native SVG is useful for compact
  report charts; AnalystKit Plotly charts are better for data-dense figures.
- Always render the PDF pages and make or inspect a contact sheet when layout
  matters.

## Basic Setup

```python
import analystkit as ak
```

## Minimal Report

```python
doc = ak.ReportDocument(
    title="Client Request Analysis",
    pages=[
        ak.ReportPage(
            title="What clients asked the sales team",
            cover=True,
            eyebrow="Research request log analysis",
            subtitle="A cleaned and audited view of client questions.",
            meta=[
                ak.ReportMetaItem("Source rows", "312"),
                ak.ReportMetaItem("Analyzed rows", "284"),
                ak.ReportMetaItem("Prepared", "July 23, 2026"),
            ],
            note="Internal research workflow analysis.",
        ),
        ak.ReportPage(
            title="The signal is concentrated.",
            kicker="Executive readout",
            intro="A small number of themes and requesters account for most volume.",
            page_number=2,
            content=ak.metric_grid([
                ak.ReportMetric("Rows analyzed", "284", "91.0% of source rows."),
                ak.ReportMetric("Top requester", "42", "Highest cleaned requester."),
                ak.ReportMetric("Top theme", "69", "Product mechanics."),
            ]) + ak.panel(
                "Key takeaways",
                ak.bullet_list([
                    "Product mechanics led the request log.",
                    "Workflow status was strong but completion-date gaps remain.",
                ]),
                trusted_html=True,
            ),
        ),
    ],
)

html_path = doc.save_html("outputs/client_request_report.html")
pdf_path = doc.export_pdf("outputs/client_request_report.pdf", html_path=html_path)
```

## Report Components

Use these helpers before hand-writing CSS:

- `ak.ReportDocument`, `ak.ReportPage`, `ak.ReportMetaItem`, `ak.ReportMetric`
- `ak.metric_grid([...])`
- `ak.panel(title, body)` or `ak.panel(title, html, trusted_html=True)`
- `ak.bullet_list([...])`
- `ak.html_table(rows, numeric_columns=[...])`
- `ak.chart_panel(svg_or_html, compact=True|False, tall=True|False)`
- `ak.image_panel(path, alt="...", height="...")`
- `ak.line_chart_svg(...)`
- `ak.horizontal_bar_svg(...)`
- `ak.export_report_pdf(html_path, pdf_path)`
- `ak.render_pdf_pages(pdf_path, output_prefix)`
- `ak.make_contact_sheet(page_pngs, output_path)`

## When To Use Native SVG vs Plotly

Use native SVG helpers for small report panels:

- request counts by month
- top-ten horizontal bars
- simple ranked operational metrics
- audit bridges and compact trend sparklines

Use Plotly plus `ak.apply_theme()` when:

- the chart is the analytical centerpiece
- dates or units need precise tick handling
- there are many series, dual panels, stacked areas, heatmaps, or financial axes
- the same chart also needs standalone export

When embedding a Plotly static export in a report, save the chart as PNG/SVG
with AnalystKit, then use `ak.image_panel(path)`.

## Production Workflow

1. Normalize and audit the data. Write support CSV/JSON files next to the report.
2. Draft the page story: cover, executive readout, trend/driver pages, audit page.
3. Build report components with AnalystKit helpers.
4. Save HTML first for quick browser inspection.
5. Export PDF with Playwright.
6. Render pages to PNG and inspect a contact sheet.
7. Deliver the PDF, HTML, and any support workbook/CSVs.

## Design Rules

- Keep pages dense but calm. Avoid marketing-page spacing.
- Use one clear thought per page title; keep intro text short.
- Prefer three metric cards per row; use six cards for executive summaries.
- Put methodology/audit notes in `.method-note` or a final audit page.
- Do not overload the cover. Three metadata tiles are the default.
- Tables should be compact, with mono uppercase headers and right-aligned
  numeric columns.
- Charts inside reports should have their own small mono title, but do not use
  large standalone chart titles inside panels.
- Render and inspect the output; HTML that looks fine in a browser can still
  overflow when printed to Letter PDF.

