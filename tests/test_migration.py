from pathlib import Path

from analystkit.migration import audit_file, audit_path, render_table


def test_auditor_is_static_and_reports_contract(tmp_path: Path):
    chart = tmp_path / "chart.py"
    chart.write_text("import analystkit as ak\n\ndef build_figure(start_date=None, end_date=None):\n return None\n", encoding="utf-8")
    result = audit_file(chart)
    assert result["readiness"] == "ready"
    report = audit_path(tmp_path)
    assert "readiness" in render_table(report)


def test_auditor_detects_export_and_import_side_effect(tmp_path: Path):
    chart = tmp_path / "chart.py"
    chart.write_text("import requests\nfig.write_image('x.png')\n", encoding="utf-8")
    result = audit_file(chart)
    assert result["direct_export"]
    assert "missing_build_figure_contract" in result["findings"]
