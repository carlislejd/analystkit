import json
from pathlib import Path

import analystkit as ak
import plotly.graph_objects as go
import pytest


def _figure():
    return go.Figure(go.Scatter(x=[1, 2], y=[2, 3], line=dict(color=ak.BITWISE_COLORS[0])))


def test_profile_and_metadata_preserve_caller_fields():
    fig = _figure()
    fig.update_layout(meta={"caller_fact": "kept"})
    ak.apply_chart_profile(fig, "deck", size_preset="3:1")
    ak.attach_chart_metadata(fig, chart_id="test", source_labels=["fixture"], table_values={"x": 1})
    assert fig.layout.title.text is None
    assert fig.layout.meta["caller_fact"] == "kept"
    assert ak.get_chart_metadata(fig)["chart_id"] == "test"
    json.dumps(fig.layout.meta)


def test_theme_handles_categorical_heatmap_axes():
    fig = go.Figure(go.Heatmap(z=[[1, 2], [3, 4]], x=["A", "B"], y=["A", "B"]))
    themed = ak.apply_theme(fig, size_preset="1:1")
    assert themed.layout.width == ak.SIZE_PRESETS["1:1"]["width"]


def test_validation_is_profile_aware_and_supports_exceptions():
    fig = ak.apply_chart_profile(_figure(), "deck")
    fig.update_layout(title="Not deck-safe")
    result = ak.validate_chart(fig)
    assert not result["valid"]
    assert result["errors"][0]["code"] == "deck_title"
    assert ak.validate_chart(fig, exceptions={"deck_title"})["valid"]


def test_time_series_requires_coverage_and_as_of():
    fig = ak.apply_chart_profile(_figure(), "deck")
    ak.attach_chart_metadata(fig, time_series=True)
    codes = {item["code"] for item in ak.validate_chart(fig)["errors"]}
    assert {"missing_actual_coverage", "missing_data_as_of"} <= codes


def test_bundle_has_hashes_and_runtime_version(tmp_path: Path):
    fig = ak.apply_chart_profile(_figure(), "deck")
    result = ak.export_chart_bundle(fig, tmp_path, "test chart", formats=("html", "json"))
    manifest = json.loads(Path(result["manifest"]).read_text())
    assert manifest["analystkit_version"] == ak.__version__
    assert {item["format"] for item in manifest["artifacts"]} == {"html", "json"}
    assert all(len(item["sha256"]) == 64 for item in manifest["artifacts"])


def test_explicit_static_bundle_needs_kaleido_when_not_installed(tmp_path: Path, monkeypatch):
    fig = ak.apply_chart_profile(_figure(), "deck")
    import analystkit.charts as charts
    monkeypatch.setitem(__import__("sys").modules, "kaleido", None)
    with pytest.raises(ImportError):
        ak.export_chart_bundle(fig, tmp_path, "chart", formats=("png",))


def test_build_function_convention():
    def build_figure(start_date=None, end_date=None):
        return _figure()
    assert ak.validate_build_function(build_figure)["valid"]

    def wrong_build(start_date, end_date=None):
        return _figure()
    assert not ak.validate_build_function(wrong_build)["valid"]
