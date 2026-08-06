"""Synthetic positive/negative monthly flow chart using the portable contract."""

import analystkit as ak
import pandas as pd
import plotly.graph_objects as go


def make_figure(profile="deck", start_date=None, end_date=None):
    dates = pd.date_range("2025-07-01", periods=12, freq="MS")
    frame = pd.DataFrame({"date": dates, "flow": [1.2, -0.8, 2.1, 0.4, -1.6, 3.0, 2.2, -0.4, 1.1, 2.8, -0.7, 1.9]})
    frame = frame[(frame.date >= pd.Timestamp(start_date or frame.date.min())) & (frame.date <= pd.Timestamp(end_date or frame.date.max()))]
    colors = [ak.BITWISE_COLORS[0] if value >= 0 else "#E15759" for value in frame.flow]
    fig = go.Figure(go.Bar(x=frame.date.dt.strftime("%b '%y"), y=frame.flow, marker_color=colors, showlegend=False))
    fig = ak.apply_chart_profile(fig, profile=profile, size_preset="3:1", margin_preset="minimal", auto_colors=False)
    fig.update_yaxes(tickprefix="$", ticksuffix="B")
    if profile == "standalone": fig.update_layout(title="Synthetic U.S. Spot Bitcoin ETF Monthly Net Flows")
    ak.attach_chart_metadata(fig, chart_id="reference.monthly_flows", display_name="Synthetic Monthly Net Flows",
                             requested_start_date=str(start_date or frame.date.min().date()), requested_end_date=str(end_date or frame.date.max().date()),
                             actual_start_date=str(frame.date.min().date()), actual_end_date=str(frame.date.max().date()), data_as_of=str(frame.date.max().date()),
                             source_labels=["Deterministic synthetic fixture"], units="USD billions", time_series=True)
    return fig


def build_figure(start_date=None, end_date=None):
    return make_figure("deck", start_date, end_date)


def main(output_dir="outputs/production_contract"):
    return ak.export_chart_bundle(build_figure(), output_dir, "monthly_flows", formats=("png", "svg", "html", "json"))
