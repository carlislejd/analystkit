"""Bitwise ad hoc report building utilities.

The report layer is intentionally small: callers own the analysis and pass
already-prepared text, metrics, tables, SVG snippets, screenshots, or chart
exports into a canonical Bitwise HTML-to-PDF shell.
"""

from __future__ import annotations

import html
import math
import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

from .colors import BITWISE_COLORS, COLOR_HIERARCHY


PACKAGE_ROOT = Path(__file__).resolve().parent
FONT_DIR = PACKAGE_ROOT / "fonts"


REPORT_COLORS = {
    "paper": "#ffffff",
    "page": "#fafafa",
    "ink": "#6c6b71",
    "muted": "#8a8990",
    "rule": "#e5e5e5",
    "teal": "#006472",
    "teal_soft": "#62a0ad",
    "green": "#45b979",
    "green_soft": "#a7d8b5",
    "navy": "#1e2028",
    "soft": "#f7faf8",
    "positive": "#2e7d32",
    "negative": "#c62828",
}


REPORT_SERIES_COLORS = [
    REPORT_COLORS["teal"],
    REPORT_COLORS["green"],
    REPORT_COLORS["teal_soft"],
    "#f2c14e",
    "#f78154",
    "#d95d59",
    "#7b6d8d",
    "#6c8ead",
    "#89b6a5",
    "#c6a15b",
]


def _as_file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def _attrs(attrs: Mapping[str, Any]) -> str:
    pairs = []
    for key, value in attrs.items():
        if value is None or value is False:
            continue
        if value is True:
            pairs.append(key)
        else:
            pairs.append(f'{key}="{_escape(value)}"')
    return (" " + " ".join(pairs)) if pairs else ""


@dataclass
class ReportMetric:
    """A compact KPI card for executive-readout pages."""

    label: str
    value: Any
    note: str = ""
    tone: str = "default"

    def render(self) -> str:
        tone_class = "" if self.tone == "default" else f" metric-card--{_escape(self.tone)}"
        note = f'<div class="metric-note">{_escape(self.note)}</div>' if self.note else ""
        return (
            f'<div class="metric-card{tone_class}">'
            f'<div class="metric-label">{_escape(self.label)}</div>'
            f'<div class="metric-value">{_escape(self.value)}</div>'
            f"{note}</div>"
        )


@dataclass
class ReportMetaItem:
    """A cover-page metadata tile."""

    label: str
    value: Any

    def render(self) -> str:
        return f"<div><span>{_escape(self.label)}</span><strong>{_escape(self.value)}</strong></div>"


@dataclass
class ReportPage:
    """One letter-sized report page.

    Set ``cover=True`` for the dark Bitwise cover page. For interior pages,
    ``content`` should contain trusted component HTML produced by the helpers
    in this module or by the caller.
    """

    title: str
    content: str = ""
    kicker: str = ""
    intro: str = ""
    cover: bool = False
    subtitle: str = ""
    eyebrow: str = ""
    meta: Sequence[ReportMetaItem] = field(default_factory=list)
    note: str = ""
    page_number: Optional[int] = None
    footer_label: str = ""
    extra_class: str = ""

    def render(self, document_title: str) -> str:
        if self.cover:
            meta = "".join(item.render() for item in self.meta)
            note = f'<p class="cover-note">{_escape(self.note)}</p>' if self.note else ""
            subtitle = f'<p class="cover-subtitle">{_escape(self.subtitle)}</p>' if self.subtitle else ""
            eyebrow = f'<div class="eyebrow">{_escape(self.eyebrow)}</div>' if self.eyebrow else ""
            return f"""
            <section class="page cover {self.extra_class}">
              <div class="brand">bitwise.</div>
              <div class="cover-main">
                {eyebrow}
                <h1>{_escape(self.title)}</h1>
                {subtitle}
              </div>
              <div class="cover-meta">{meta}</div>
              {note}
            </section>
            """

        intro = f'<p class="section-intro">{_escape(self.intro)}</p>' if self.intro else ""
        footer_label = self.footer_label or document_title
        footer = ""
        if self.page_number is not None:
            footer = (
                f'<div class="footer"><span>{_escape(footer_label)}</span>'
                f"<span>{_escape(self.page_number)}</span></div>"
            )
        kicker = self.kicker or document_title
        return f"""
        <section class="page {self.extra_class}">
          <header class="page-header">
            <div class="brand">bitwise.</div>
            <div class="page-kicker">{_escape(kicker)}</div>
          </header>
          <h2 class="section-title">{_escape(self.title)}</h2>
          {intro}
          {self.content}
          {footer}
        </section>
        """


@dataclass
class ReportDocument:
    """A complete Bitwise report ready for HTML and optional PDF export."""

    title: str
    pages: Sequence[ReportPage]
    report_date: str = field(default_factory=lambda: f"{date.today():%B} {date.today().day}, {date.today():%Y}")
    css_overrides: str = ""

    def render_html(self) -> str:
        css = report_css() + "\n" + self.css_overrides
        pages = "\n".join(page.render(self.title) for page in self.pages)
        return (
            "<!doctype html>\n"
            '<html lang="en">\n'
            "<head>\n"
            '<meta charset="utf-8">\n'
            f"<title>{_escape(self.title)}</title>\n"
            f"<style>{css}</style>\n"
            "</head>\n"
            f"<body>{pages}</body>\n"
            "</html>\n"
        )

    def save_html(self, path: Union[str, Path]) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.render_html(), encoding="utf-8")
        return output

    def export_pdf(self, path: Union[str, Path], html_path: Optional[Union[str, Path]] = None) -> Path:
        if html_path is None:
            html_path = Path(path).with_suffix(".html")
        html_file = self.save_html(html_path)
        return export_report_pdf(html_file, path)


def report_css() -> str:
    """Return the canonical Bitwise report stylesheet."""

    font_book = _as_file_uri(FONT_DIR / "PPNeueMontreal-Book.otf")
    font_mono = _as_file_uri(FONT_DIR / "PPNeueMontrealMono-Variable.ttf")
    font_items = _as_file_uri(FONT_DIR / "Items-Regular.otf")
    c = REPORT_COLORS
    return f"""
    @font-face {{ font-family: 'PP Neue Montreal'; src: url('{font_book}') format('opentype'); font-weight: 400; }}
    @font-face {{ font-family: 'PP Neue Montreal Mono'; src: url('{font_mono}') format('truetype'); font-weight: 400; }}
    @font-face {{ font-family: 'Items'; src: url('{font_items}') format('opentype'); font-weight: 400; }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: {c['page']};
      color: {c['ink']};
      font-family: 'PP Neue Montreal', Arial, sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    @page {{ size: Letter; margin: 0; }}
    .page {{
      width: 8.5in;
      height: 11in;
      padding: 0.46in 0.54in 0.74in;
      background: {c['paper']};
      position: relative;
      overflow: hidden;
      break-after: page;
    }}
    .page:last-child {{ break-after: auto; }}
    .cover {{
      background: {c['navy']};
      color: #fff;
      display: flex;
      flex-direction: column;
      padding: 0.52in 0.64in;
    }}
    .brand {{
      font-family: 'Items', Georgia, serif;
      font-size: 25px;
      color: inherit;
      letter-spacing: 0;
    }}
    .cover-main {{ margin-top: 1.0in; max-width: 6.4in; }}
    .eyebrow, .page-kicker, .metric-label, th {{
      font-family: 'PP Neue Montreal Mono', monospace;
      text-transform: uppercase;
      letter-spacing: 1.2px;
    }}
    .eyebrow {{ font-size: 9px; color: {c['teal_soft']}; margin-bottom: 14px; }}
    h1, h2, h3 {{ margin: 0; font-weight: 400; color: inherit; }}
    h1 {{ font-family: 'Items', Georgia, serif; font-size: 57px; line-height: 0.98; }}
    .cover-subtitle {{ margin-top: 22px; font-size: 18px; line-height: 1.45; color: #cdd1da; max-width: 6.1in; }}
    .cover-meta {{ margin-top: auto; display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid rgba(255,255,255,0.10); border-bottom: 1px solid rgba(255,255,255,0.10); }}
    .cover-meta div {{ padding: 18px 16px; border-right: 1px solid rgba(255,255,255,0.08); min-height: 72px; }}
    .cover-meta div:last-child {{ border-right: 0; }}
    .cover-meta span {{ display: block; font-family: 'PP Neue Montreal Mono', monospace; font-size: 8px; letter-spacing: 1.1px; text-transform: uppercase; color: #87909d; margin-bottom: 7px; }}
    .cover-meta strong {{ font-size: 15px; font-weight: 400; color: #e7e9ed; }}
    .cover-note {{ color: #9299a5; font-size: 9px; line-height: 1.5; margin-top: 18px; max-width: 6.8in; }}
    .page-header {{ display: flex; align-items: baseline; justify-content: space-between; border-bottom: 1px solid {c['rule']}; padding-bottom: 13px; margin-bottom: 20px; }}
    .page-kicker {{ font-size: 8px; color: {c['muted']}; }}
    .section-title {{ font-family: 'Items', Georgia, serif; font-size: 33px; color: {c['ink']}; line-height: 1.06; margin-bottom: 11px; }}
    .section-intro {{ font-size: 13.5px; line-height: 1.48; color: {c['ink']}; max-width: 7.0in; margin: 0 0 16px; }}
    .metric-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 16px 0 16px; }}
    .metric-card, .panel, .chart-panel, .image-panel {{ border: 1px solid {c['rule']}; border-radius: 8px; background: #fff; }}
    .metric-card {{ padding: 14px 13px; min-height: 88px; }}
    .metric-label {{ font-size: 8px; color: {c['muted']}; margin-bottom: 9px; }}
    .metric-value {{ font-size: 25px; color: {c['teal']}; line-height: 1; }}
    .metric-card--positive .metric-value {{ color: {c['positive']}; }}
    .metric-card--negative .metric-value {{ color: {c['negative']}; }}
    .metric-note {{ margin-top: 8px; color: {c['muted']}; font-size: 10px; line-height: 1.35; }}
    .panel {{ padding: 16px 17px; margin-top: 12px; }}
    .panel h3 {{ font-family: 'PP Neue Montreal Mono', monospace; font-size: 8px; letter-spacing: 1.1px; text-transform: uppercase; color: {c['teal']}; margin-bottom: 9px; }}
    .panel p, li {{ font-size: 12px; line-height: 1.48; color: {c['ink']}; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li + li {{ margin-top: 7px; }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 13px; }}
    .chart-panel {{ padding: 12px 14px 8px; min-height: 3.05in; overflow: hidden; }}
    .chart-panel.compact {{ min-height: 2.72in; }}
    .chart-panel.tall {{ min-height: 3.58in; }}
    .image-panel {{ overflow: hidden; display: flex; align-items: center; justify-content: center; background: #f3f4f4; }}
    .image-panel img {{ width: 100%; height: 100%; object-fit: cover; object-position: top left; display: block; }}
    svg {{ width: 100%; height: 100%; display: block; }}
    .chart-title {{ font-family: 'PP Neue Montreal Mono', monospace; font-size: 12px; fill: {c['teal']}; text-transform: uppercase; letter-spacing: 1px; }}
    .axis {{ font-size: 10px; fill: {c['muted']}; }}
    .label {{ font-size: 10.5px; fill: {c['ink']}; }}
    .legend {{ font-size: 9px; fill: {c['muted']}; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 10.2px; }}
    th {{ background: {c['soft']}; color: {c['teal']}; font-size: 7.5px; text-align: left; padding: 8px; border-top: 1px solid {c['rule']}; border-bottom: 1px solid {c['rule']}; }}
    td {{ padding: 8px; border-bottom: 1px solid {c['rule']}; vertical-align: top; line-height: 1.3; }}
    td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .method-note {{ border-left: 4px solid {c['green']}; background: {c['soft']}; padding: 8px 13px; margin-top: 10px; font-size: 9.8px; line-height: 1.32; }}
    .footer {{ position: absolute; bottom: 0.25in; left: 0.54in; right: 0.54in; display: flex; justify-content: space-between; font-family: 'PP Neue Montreal Mono', monospace; color: #b1b1b6; font-size: 8px; letter-spacing: 0.6px; border-top: 1px solid {c['rule']}; padding-top: 8px; text-transform: uppercase; }}
    """


def metric_grid(metrics: Sequence[Union[ReportMetric, Mapping[str, Any]]]) -> str:
    """Render a three-column metric grid."""

    rendered = []
    for metric in metrics:
        if isinstance(metric, ReportMetric):
            rendered.append(metric.render())
        else:
            rendered.append(ReportMetric(**metric).render())
    return f'<div class="metric-grid">{"".join(rendered)}</div>'


def panel(title: str, body: str, *, trusted_html: bool = False, class_name: str = "") -> str:
    """Render a bordered report panel."""

    content = body if trusted_html else f"<p>{_escape(body)}</p>"
    classes = "panel" + (f" {class_name}" if class_name else "")
    return f'<div class="{classes}"><h3>{_escape(title)}</h3>{content}</div>'


def bullet_list(items: Iterable[Any]) -> str:
    """Render a report-ready unordered list."""

    return "<ul>" + "".join(f"<li>{_escape(item)}</li>" for item in items) + "</ul>"


def html_table(
    rows: Sequence[Union[Mapping[str, Any], Sequence[Any]]],
    columns: Optional[Sequence[str]] = None,
    *,
    numeric_columns: Sequence[str] = (),
) -> str:
    """Render a compact Bitwise table.

    ``rows`` can be dictionaries or sequences. When dictionaries are supplied
    and ``columns`` is omitted, the first row's key order is used.
    """

    if not rows:
        return "<table><tbody></tbody></table>"

    first = rows[0]
    if columns is None:
        if isinstance(first, Mapping):
            columns = list(first.keys())
        else:
            columns = [str(i + 1) for i in range(len(first))]

    numeric = set(numeric_columns)
    header = "".join(
        f'<th class="{"num" if column in numeric else ""}">{_escape(column)}</th>'
        for column in columns
    )
    body_rows = []
    for row in rows:
        cells = []
        for idx, column in enumerate(columns):
            value = row.get(column, "") if isinstance(row, Mapping) else row[idx]
            cls = ' class="num"' if column in numeric else ""
            cells.append(f"<td{cls}>{_escape(value)}</td>")
        body_rows.append(f"<tr>{''.join(cells)}</tr>")

    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def chart_panel(svg_or_html: str, *, compact: bool = False, tall: bool = False, class_name: str = "") -> str:
    """Wrap trusted SVG/HTML chart markup in the standard chart panel."""

    classes = ["chart-panel"]
    if compact:
        classes.append("compact")
    if tall:
        classes.append("tall")
    if class_name:
        classes.append(class_name)
    return f'<div class="{" ".join(classes)}">{svg_or_html}</div>'


def image_panel(path: Union[str, Path], *, alt: str = "", height: str = "3.6in") -> str:
    """Render a local image inside a report panel."""

    uri = _as_file_uri(Path(path))
    return (
        f'<div class="image-panel" style="height:{_escape(height)}">'
        f'<img src="{uri}" alt="{_escape(alt)}"></div>'
    )


def nice_axis(max_value: float, steps: int = 5) -> Tuple[float, List[float]]:
    """Return a clean y-axis top and tick list for SVG helpers."""

    if max_value <= 0:
        return 1.0, [0.0, 1.0]
    raw = max_value / steps
    magnitude = 10 ** math.floor(math.log10(raw))
    step = math.ceil(raw / magnitude) * magnitude
    top = float(step * steps)
    return top, [float(step * i) for i in range(steps + 1)]


def line_chart_svg(
    rows: Sequence[Mapping[str, Any]],
    *,
    x: str,
    y: str,
    title: str,
    width: int = 760,
    height: int = 280,
    color: str = REPORT_COLORS["teal"],
) -> str:
    """Create a compact report-native SVG line chart."""

    left, right, top, bottom = 52, 24, 32, 42
    plot_w = width - left - right
    plot_h = height - top - bottom
    values = [float(row[y]) for row in rows]
    ymax, ticks = nice_axis(max(values), 4)

    def x_for(idx: int) -> float:
        return left + (idx / max(1, len(rows) - 1)) * plot_w

    def y_for(value: float) -> float:
        return top + (1 - value / ymax) * plot_h

    points = [(x_for(i), y_for(v)) for i, v in enumerate(values)]
    path = " ".join(f"{'M' if i == 0 else 'L'} {px:.1f} {py:.1f}" for i, (px, py) in enumerate(points))
    pieces = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{_escape(title)}">',
        f'<text x="{left}" y="20" class="chart-title">{_escape(title)}</text>',
    ]
    for tick in ticks:
        ty = y_for(tick)
        pieces.append(f'<line x1="{left}" y1="{ty:.1f}" x2="{width-right}" y2="{ty:.1f}" stroke="{REPORT_COLORS["rule"]}"/>')
        pieces.append(f'<text x="{left-10}" y="{ty+4:.1f}" text-anchor="end" class="axis">{tick:g}</text>')
    pieces.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    for px, py in points:
        pieces.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="{color}"/>')
    for i, row in enumerate(rows):
        if i % 2 == 0 or i in {0, len(rows) - 1}:
            pieces.append(f'<text x="{x_for(i):.1f}" y="{height-18}" text-anchor="middle" class="axis">{_escape(row[x])}</text>')
    pieces.append("</svg>")
    return "".join(pieces)


def horizontal_bar_svg(
    rows: Sequence[Mapping[str, Any]],
    *,
    label: str,
    value: str,
    title: str,
    width: int = 760,
    height: int = 300,
    limit: int = 10,
    colors: Optional[Sequence[str]] = None,
) -> str:
    """Create a compact report-native horizontal bar SVG."""

    chart_rows = list(rows)[:limit]
    left, right, top, bottom = 220, 58, 34, 24
    plot_w = width - left - right
    row_h = (height - top - bottom) / max(1, len(chart_rows))
    max_value = max(float(row[value]) for row in chart_rows) if chart_rows else 1
    palette = list(colors or REPORT_SERIES_COLORS or COLOR_HIERARCHY.get(len(chart_rows), BITWISE_COLORS))
    pieces = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{_escape(title)}">',
        f'<text x="0" y="20" class="chart-title">{_escape(title)}</text>',
    ]
    for i, row in enumerate(chart_rows):
        raw_value = float(row[value])
        row_y = top + i * row_h
        bar_w = (raw_value / max_value) * plot_w if max_value else 0
        color = palette[i % len(palette)]
        label_text = str(row[label])
        if len(label_text) > 34:
            label_text = label_text[:31] + "..."
        pieces.append(f'<text x="{left-12}" y="{row_y + row_h * 0.62:.1f}" text-anchor="end" class="axis">{_escape(label_text)}</text>')
        pieces.append(f'<rect x="{left}" y="{row_y + row_h * 0.22:.1f}" width="{bar_w:.1f}" height="{row_h * 0.48:.1f}" rx="4" fill="{color}"/>')
        pieces.append(f'<text x="{left + bar_w + 8:.1f}" y="{row_y + row_h * 0.62:.1f}" class="label">{raw_value:g}</text>')
    pieces.append("</svg>")
    return "".join(pieces)


def export_report_pdf(
    html_path: Union[str, Path],
    pdf_path: Union[str, Path],
    *,
    viewport_width: int = 816,
    viewport_height: int = 1056,
) -> Path:
    """Export report HTML to PDF with Playwright.

    Playwright is optional and imported lazily so AnalystKit chart usage does
    not require browser dependencies.
    """

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("PDF export requires Playwright: pip install playwright && playwright install chromium") from exc

    html_file = Path(html_path)
    output = Path(pdf_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": viewport_width, "height": viewport_height}, device_scale_factor=1)
        page.goto(html_file.resolve().as_uri(), wait_until="load", timeout=20000)
        page.emulate_media(media="print")
        page.pdf(
            path=str(output),
            format="Letter",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
    return output


def render_pdf_pages(
    pdf_path: Union[str, Path],
    output_prefix: Union[str, Path],
    *,
    pdftoppm: str = "pdftoppm",
    resolution: int = 130,
) -> List[Path]:
    """Render PDF pages to PNG files for visual QA."""

    prefix = Path(output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [pdftoppm, "-png", "-r", str(resolution), str(pdf_path), str(prefix)],
        check=True,
    )
    return sorted(prefix.parent.glob(f"{prefix.name}-*.png"))


def make_contact_sheet(
    pages: Sequence[Union[str, Path]],
    output_path: Union[str, Path],
    *,
    thumb_size: Tuple[int, int] = (260, 340),
    columns: int = 3,
) -> Path:
    """Create a contact sheet from rendered report pages."""

    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError("Contact-sheet generation requires Pillow: pip install pillow") from exc

    images = []
    for page_path in pages:
        image = Image.open(page_path).convert("RGB")
        image.thumbnail(thumb_size)
        images.append(image.copy())
    if not images:
        raise ValueError("No page images supplied for contact sheet.")

    rows = math.ceil(len(images) / columns)
    sheet = Image.new("RGB", (columns * 300, rows * 380), "white")
    draw = ImageDraw.Draw(sheet)
    for idx, image in enumerate(images):
        x = (idx % columns) * 300 + 20
        y = (idx // columns) * 380 + 20
        sheet.paste(image, (x, y))
        draw.text((x, y + image.height + 8), f"Page {idx + 1}", fill=(80, 80, 80))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    return output
