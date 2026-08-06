# Standalone chart visual references

This is a durable design brief distilled from four finished Bitwise charts
reviewed on 2026-08-06. The source images were supplied from a transient
clipboard location and are intentionally not copied into the repository.

## What to preserve

- Use a large, left-aligned Items title with generous space before the plot for
  self-contained research/chart-generator deliverables.
- Keep the canvas quiet: white background, thin cool-gray horizontal gridlines,
  no vertical grid, and a more distinct zero/reference line when it matters.
- Make semantic hierarchy obvious. The active/primary series uses Bitwise
  green; secondary series may use gold, soft green, or charcoal when those
  colors carry meaning rather than merely distinguish categories.
- Place a compact, marker-dot legend at the upper right or above the plot.
  For performance charts, include the ending return in the legend label.
- Use deliberate finance labels: percentages with parentheses for negatives,
  `$T`/`$K` units, bounded correlation ticks from -1 to 1, and a log axis only
  when its meaning is stated in the legend or nearby context.
- Use dual axes sparingly and name each axis in the legend so the relationship
  remains readable without axis titles.
- Source/date footer and Bitwise wordmark are appropriate for standalone
  publishing. They do not belong in `deck` profile exports because the slide
  owns them.

## Dense deck-chart language

The additional reviewed charts establish a compact, titleless deck language.
Use this when the surrounding slide already supplies the story.

- Place a centered, top horizontal dot legend above the plot for stacked bars,
  overlay comparisons, and other multi-series charts. Use a stable semantic
  order rather than sorting the legend by value on each refresh.
- For stacked bars, use a green-to-teal primary hierarchy, then restrained
  blue-gray and gray tail categories. Set `bargap` deliberately and rotate
  dense quarter/month labels vertically rather than shrinking them until they
  become illegible.
- For raw-versus-derived data, render the noisy/raw series as a translucent
  green area or thin line and the rolling average/trend as a dark, opaque line
  above it. Explain the window in the legend label.
- Keep a single-series historical line exceptionally quiet: one green line,
  no legend, carefully bounded unit ticks, and no ornamental annotations.
- For positive/negative bars, use green above zero and muted red below zero;
  give zero a clear reference line and format negatives with parentheses.
- Add direct value labels only when the number is the point of the chart, as
  in a 12-bar seasonal comparison. Avoid labels on dense time-series marks.
- Use fixed, explicit tick arrays for billions, millions, thousands, and
  percentages. The label cadence is part of the chart's editorial judgment,
  not an automatic Plotly decision.

## Comparative and cumulative composition

The latest references make the hierarchy for grouped bars and cumulative
composition especially clear.

- For a two-series grouped bar comparison, reserve Bitwise green for the lead
  series and charcoal for the comparator. Keep the legend short, centered, and
  above the plot; use side-by-side bars rather than stacked bars when the
  comparison between the two values is the point.
- For cumulative market, reserve, supply, or treasury composition, use solid
  stacked areas with no separating outlines. Put the dominant category on the
  baseline, secondary material above it, and the residual/"Others" category at
  the top in charcoal or gray.
- Preserve a consistent series order and color assignment across chart refreshes
  and related visuals. This is more important than automatically re-sorting
  categories at each date.
- Leave generous upper plot space for the legend, not a redundant title. The
  chart should still read from the y-axis unit, time axis, and legend alone.

## When to use this style

Use it for a standalone research graphic, client-ready one-off, or chart
generator image. Do not treat it as a universal default: a Composite Deck
asset should use the existing deck profile and omit title, source, footer, and
wordmark.

## Implementation shape

```python
fig = ak.apply_chart_profile(fig, "standalone", size_preset="18:9",
                             margin_preset="standard", auto_colors=False)
fig.update_layout(
    title=dict(text="Bitcoin vs. Gold: 8-Week Performance", x=0.03,
               xanchor="left", font=dict(family=ak.FONT_FAMILIES["title"])),
    legend=dict(orientation="h", x=1, xanchor="right", y=1.02,
                yanchor="bottom"),
    margin=dict(l=100, r=60, t=135, b=135),
)
fig.update_yaxes(zeroline=True, zerolinecolor="#7D8080")
```

Keep project-specific source text, dated footer, and wordmark rendering in the
calling project until a stable shared branding asset/interface is agreed.
