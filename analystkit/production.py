"""Production contracts for portable, inspectable AnalystKit charts.

This module deliberately owns presentation, metadata, validation, and
artifact bookkeeping only. Callers remain responsible for their data,
calculations, and delivery.
"""

import hashlib
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

from .charts import _KALEIDO_FORMATS, export_chart
from .colors import BITWISE_COLORS, CHART_COLORS, FONT_FAMILIES, SIZE_PRESETS
from .plotly_theme import apply_theme


CHART_PROFILES = ("deck", "standalone", "report")
_METADATA_KEY = "analystkit"


def _json_safe(value):
    """Return ``value`` after proving it is JSON serializable."""
    try:
        return json.loads(json.dumps(value, default=str))
    except (TypeError, ValueError) as exc:
        raise ValueError("Chart metadata must be JSON-serializable") from exc


def _layout_meta(fig):
    meta = fig.layout.meta
    if meta is None:
        return {}
    if not isinstance(meta, dict):
        raise ValueError("fig.layout.meta must be a mapping for AnalystKit metadata")
    return meta.to_plotly_json() if hasattr(meta, "to_plotly_json") else dict(meta)


def apply_chart_profile(fig, profile="deck", size_preset=None, margin_preset="minimal",
                        width=None, height=None, auto_colors=True):
    """Theme a figure and apply semantic defaults for ``deck``, ``standalone``, or ``report``.

    Profiles compose with existing size and margin controls. A deck profile clears
    presentation furniture owned by the slide; the other profiles preserve it.
    """
    if profile not in CHART_PROFILES:
        raise ValueError("Unknown profile {!r}. Use one of {}".format(profile, CHART_PROFILES))
    if size_preset is None:
        size_preset = "18:9" if profile == "report" else "full"
    fig = apply_theme(fig, size_preset=size_preset, margin_preset=margin_preset,
                      width=width, height=height, auto_colors=auto_colors)
    if profile == "deck":
        fig.update_layout(title=None)
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)
    attach_chart_metadata(fig, profile=profile)
    return fig


def attach_chart_metadata(fig, metadata=None, **fields):
    """Merge JSON-safe contract metadata into ``fig.layout.meta`` without discarding caller data."""
    existing = _layout_meta(fig)
    contract = dict(existing.get(_METADATA_KEY, {}))
    if metadata:
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a mapping")
        contract.update(metadata)
    contract.update(fields)
    contract.setdefault("analystkit_version", _runtime_version())
    existing[_METADATA_KEY] = _json_safe(contract)
    fig.update_layout(meta=_json_safe(existing))
    return fig


def get_chart_metadata(fig):
    """Return only AnalystKit's contract metadata, or an empty dictionary."""
    return dict(_layout_meta(fig).get(_METADATA_KEY, {}))


def _runtime_version():
    from . import __version__
    return __version__


def _title_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(getattr(value, "text", "") or "").strip()


def _axis_title_text(axis):
    return _title_text(getattr(axis, "title", None))


def validate_chart(fig, profile=None, exceptions=None):
    """Return a JSON-safe, profile-aware validation report.

    ``exceptions`` is an iterable of check codes deliberately allowed by a
    particular recipe (for example ``{"deck_title"}``).
    """
    exceptions = set(exceptions or [])
    metadata = get_chart_metadata(fig)
    profile = profile or metadata.get("profile")
    errors, warnings = [], []

    def add(bucket, code, message):
        if code not in exceptions:
            bucket.append({"code": code, "message": message})

    if profile not in CHART_PROFILES:
        add(errors, "missing_profile", "Set a chart profile with apply_chart_profile or attach_chart_metadata.")
    if not getattr(fig.layout, "width", None) or not getattr(fig.layout, "height", None):
        add(errors, "missing_dimensions", "Chart width and height must be set before export.")
    try:
        _json_safe(_layout_meta(fig))
    except ValueError:
        add(errors, "invalid_metadata", "fig.layout.meta is not JSON-serializable.")

    if profile == "deck":
        if _title_text(fig.layout.title):
            add(errors, "deck_title", "Deck charts must not include an embedded title.")
        for name in ("xaxis", "yaxis"):
            if _axis_title_text(getattr(fig.layout, name)):
                add(errors, "deck_axis_title", "Deck charts must not include axis-title text.")
                break
        annotations = fig.layout.annotations or []
        if any("source" in str(getattr(a, "text", "")).lower() for a in annotations):
            add(errors, "deck_source_footer", "Deck charts must keep source text in slide metadata.")

    if metadata.get("time_series") and not (metadata.get("actual_start_date") and metadata.get("actual_end_date")):
        add(errors, "missing_actual_coverage", "Time-series charts require actual_start_date and actual_end_date.")
    if metadata.get("time_series") and not metadata.get("data_as_of"):
        add(errors, "missing_data_as_of", "Time-series charts require data_as_of.")

    font = getattr(fig.layout, "font", None)
    family = getattr(font, "family", None) if font else None
    if family and family not in FONT_FAMILIES.values():
        add(warnings, "non_bitwise_font", "Layout font is not a registered Bitwise font.")
    known_colors = set(BITWISE_COLORS) | set(CHART_COLORS.values())
    for trace in fig.data:
        color = getattr(getattr(trace, "line", None), "color", None) or getattr(getattr(trace, "marker", None), "color", None)
        if isinstance(color, str) and color.startswith("#") and color.upper() not in {c.upper() for c in known_colors}:
            add(warnings, "custom_color", "Chart includes a custom hard-coded color.")
            break

    return {"valid": not errors, "profile": profile, "errors": errors, "warnings": warnings,
            "metadata": metadata}


def validate_build_function(function):
    """Validate the portable ``build_figure(start_date=None, end_date=None)`` signature."""
    signature = inspect.signature(function)
    parameters = signature.parameters
    errors = []
    for name in ("start_date", "end_date"):
        parameter = parameters.get(name)
        if parameter is None or parameter.default is inspect.Parameter.empty:
            errors.append({"code": "build_signature", "message": "build_figure must accept {}=None".format(name)})
    return {"valid": not errors, "errors": errors}


def export_chart_bundle(fig, output_dir, stem, formats=("png", "svg", "html", "json"),
                        profile=None, exceptions=None, scale=2):
    """Export requested artifacts and write a hashed ``<stem>.manifest.json``.

    Explicit static requests fail clearly when Kaleido is unavailable; callers
    that need dependency-free output can request ``html`` and/or ``json``.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    stem = Path(stem).stem
    validation = validate_chart(fig, profile=profile, exceptions=exceptions)
    artifacts = []
    for requested in formats:
        fmt = requested.lower().lstrip(".")
        if fmt not in _KALEIDO_FORMATS | {"html", "json"}:
            raise ValueError("Unsupported bundle format {!r}".format(fmt))
        path = output / "{}.{}".format(stem, fmt)
        export_chart(fig, str(path), format=fmt, scale=scale)
        payload = path.read_bytes()
        artifacts.append({"filename": path.name, "format": fmt, "bytes": len(payload),
                          "sha256": hashlib.sha256(payload).hexdigest(),
                          "width": fig.layout.width, "height": fig.layout.height,
                          "scale": scale if fmt in {"png", "jpg", "jpeg", "webp"} else 1})
    manifest = {"analystkit_version": _runtime_version(),
                "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "metadata": get_chart_metadata(fig), "validation": validation,
                "artifacts": artifacts}
    manifest_path = output / "{}.manifest.json".format(stem)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"manifest": str(manifest_path), "artifacts": artifacts, "validation": validation}
