# Production-contract reference recipes

Each recipe uses deterministic data, exposes `build_figure(start_date=None,
end_date=None)`, and keeps its output work in `main()`. The default build is
deck-native; use `make_figure("standalone")` or `make_figure("report")` when
embedding context or a report-panel-sized chart is appropriate.

Run a recipe with `python examples/production_contract/performance_line.py`.
It creates PNG/SVG/HTML/JSON artifacts plus a hash manifest when Kaleido and a
working headless Chrome runtime are installed. Otherwise request `("html",
"json")` from `ak.export_chart_bundle()` for dependency-free contract checks,
then perform rendered visual QA in a working export environment.
