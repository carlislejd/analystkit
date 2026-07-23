from pathlib import Path

import analystkit as ak


def test_report_document_renders_expected_shell(tmp_path: Path):
    doc = ak.ReportDocument(
        title="Sample Report",
        pages=[
            ak.ReportPage(
                title="Sample Cover",
                cover=True,
                eyebrow="Example",
                subtitle="A short report.",
                meta=[
                    ak.ReportMetaItem("Rows", "10"),
                    ak.ReportMetaItem("Prepared", "Today"),
                    ak.ReportMetaItem("Owner", "Research"),
                ],
            ),
            ak.ReportPage(
                title="Signal is concentrated.",
                kicker="Executive readout",
                intro="A compact summary page.",
                page_number=2,
                content=ak.metric_grid(
                    [
                        ak.ReportMetric("Rows", "10", "All rows."),
                        ak.ReportMetric("Themes", "3"),
                        ak.ReportMetric("Done", "8", tone="positive"),
                    ]
                )
                + ak.panel("Takeaways", ak.bullet_list(["One", "Two"]), trusted_html=True),
            ),
        ],
    )

    html = doc.render_html()
    assert "bitwise." in html
    assert "Sample Cover" in html
    assert "metric-card--positive" in html
    assert "PP Neue Montreal Mono" in html

    path = doc.save_html(tmp_path / "sample.html")
    assert path.exists()
    assert path.read_text(encoding="utf-8").startswith("<!doctype html>")


def test_report_helpers_escape_untrusted_values():
    table = ak.html_table([{"Name": "<x>", "Value": 3}], numeric_columns=["Value"])
    assert "&lt;x&gt;" in table
    assert 'class="num"' in table

    panel = ak.panel("Title", "<script>")
    assert "&lt;script&gt;" in panel


def test_svg_helpers_render_report_charts():
    rows = [{"Month": "Jan", "Requests": 1}, {"Month": "Feb", "Requests": 4}]
    line = ak.line_chart_svg(rows, x="Month", y="Requests", title="Monthly")
    bars = ak.horizontal_bar_svg(rows, label="Month", value="Requests", title="By month")

    assert "<svg" in line
    assert "Monthly" in line
    assert "<rect" in bars
    assert "By month" in bars
