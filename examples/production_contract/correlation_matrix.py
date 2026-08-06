"""Synthetic square correlation matrix using the portable contract."""

import analystkit as ak
import plotly.graph_objects as go


def make_figure(profile="deck", start_date=None, end_date=None):
    labels = ["Bitcoin", "Gold", "U.S. Equities", "Bonds"]
    matrix = [[1, .18, .42, -.12], [.18, 1, .09, .20], [.42, .09, 1, -.26], [-.12, .20, -.26, 1]]
    fig = go.Figure(go.Heatmap(z=matrix, x=labels, y=labels, zmin=-1, zmax=1, colorscale="RdBu", reversescale=True, showscale=False))
    fig = ak.apply_chart_profile(fig, profile=profile, size_preset="1:1", margin_preset="minimal", auto_colors=False)
    if profile == "standalone": fig.update_layout(title="Synthetic 90-Day Asset Correlations")
    ak.attach_chart_metadata(fig, chart_id="reference.correlation_matrix", display_name="Synthetic Correlation Matrix",
                             requested_end_date="2026-06-30", actual_end_date="2026-06-30", data_as_of="2026-06-30",
                             source_labels=["Deterministic synthetic fixture"], units="correlation", audit_fingerprint="synthetic-v1")
    return fig


def build_figure(start_date=None, end_date=None):
    return make_figure("deck", start_date, end_date)


def main(output_dir="outputs/production_contract"):
    return ak.export_chart_bundle(build_figure(), output_dir, "correlation_matrix", formats=("png", "svg", "html", "json"))
