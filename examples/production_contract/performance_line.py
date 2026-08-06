"""Synthetic multi-series return chart using the portable AnalystKit contract."""

from pathlib import Path

import analystkit as ak
import pandas as pd
import plotly.graph_objects as go


def _data():
    dates = pd.date_range("2026-01-01", periods=12, freq="W")
    return pd.DataFrame({"date": dates, "Bitcoin": [0, 3, -1, 7, 5, 9, 12, 10, 15, 13, 18, 21],
                         "Gold": [0, 1, 2, 1, 4, 3, 5, 6, 5, 8, 7, 9]})


def make_figure(profile="deck", start_date=None, end_date=None):
    data = _data()
    for field in ("date",):
        data[field] = pd.to_datetime(data[field])
    data = data[(data.date >= pd.Timestamp(start_date or data.date.min())) & (data.date <= pd.Timestamp(end_date or data.date.max()))]
    fig = go.Figure()
    for label, color in zip(("Bitcoin", "Gold"), ak.get_color_palette(2)):
        fig.add_trace(go.Scatter(x=data.date, y=data[label], mode="lines", name=label, line=dict(color=color, width=3)))
    fig = ak.apply_chart_profile(fig, profile=profile, size_preset="3:1", margin_preset="minimal", auto_colors=False)
    if profile == "standalone":
        fig.update_layout(title="Bitcoin vs. Gold: Synthetic Performance")
    ak.attach_chart_metadata(fig, chart_id="reference.performance_line", display_name="Synthetic Bitcoin vs. Gold Performance",
                             requested_start_date=str(start_date or data.date.min().date()), requested_end_date=str(end_date or data.date.max().date()),
                             actual_start_date=str(data.date.min().date()), actual_end_date=str(data.date.max().date()), data_as_of=str(data.date.max().date()),
                             source_labels=["Deterministic synthetic fixture"], units="percent return", time_series=True)
    return fig


def build_figure(start_date=None, end_date=None):
    return make_figure("deck", start_date, end_date)


def main(output_dir="outputs/production_contract"):
    return ak.export_chart_bundle(build_figure(), output_dir, "performance_line", formats=("png", "svg", "html", "json"))


if __name__ == "__main__":
    print(main())
