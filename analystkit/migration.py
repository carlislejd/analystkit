"""Read-only AST audit for chart migration readiness."""

import argparse
import ast
import json
from pathlib import Path


NETWORK_NAMES = {"requests", "snowflake", "sqlalchemy", "yfinance", "boto3", "urllib", "httpx"}


def _call_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return "{}.{}".format(parent, node.attr) if parent else node.attr
    return ""


def audit_file(path):
    """Statically inspect one Python file. Never import or execute it."""
    path = Path(path)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError) as exc:
        return {"path": str(path), "readiness": "manual_refactor", "parse_error": str(exc), "findings": ["parse_error"]}
    imports_ak = False
    build = None
    calls, findings = [], []
    top_level_risky = False
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names]
            if (isinstance(node, ast.Import) and "analystkit" in names) or (isinstance(node, ast.ImportFrom) and node.module == "analystkit"):
                imports_ak = True
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "build_figure":
            args = [a.arg for a in node.args.args]
            build = args[:2] == ["start_date", "end_date"]
        if isinstance(node, ast.Call):
            name = _call_name(node.func)
            calls.append(name)
    for statement in tree.body:
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            name = _call_name(statement.value.func)
            if any(token in name.lower() for token in ("write_", "savefig", "request", "connect", "query", "fetch")):
                top_level_risky = True
        if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Call):
            name = _call_name(statement.value.func)
            if any(token in name.lower() for token in ("request", "connect", "query", "fetch")):
                top_level_risky = True
    direct_export = any(name.endswith("write_image") or name.endswith("write_html") for name in calls)
    title_like = any(name.endswith("update_layout") for name in calls)
    if not imports_ak: findings.append("no_analystkit_import")
    if build is not True: findings.append("missing_build_figure_contract")
    if direct_export: findings.append("direct_plotly_export")
    if top_level_risky: findings.append("possible_import_side_effect")
    if title_like: findings.append("review_embedded_titles_or_sources")
    readiness = "ready" if imports_ak and build is True and not direct_export and not top_level_risky else ("small_adapter" if imports_ak or build else "manual_refactor")
    return {"path": str(path), "imports_analystkit": imports_ak, "build_figure": build is True,
            "direct_export": direct_export, "possible_import_side_effect": top_level_risky,
            "readiness": readiness, "findings": findings}


def audit_path(target):
    path = Path(target)
    ignored = {".git", ".venv", "venv", "node_modules", "site-packages", "build", "dist", "__pycache__"}
    files = [path] if path.is_file() else sorted(p for p in path.rglob("*.py") if not ignored.intersection(p.parts))
    items = [audit_file(item) for item in files]
    counts = {key: sum(item["readiness"] == key for item in items) for key in ("ready", "small_adapter", "manual_refactor")}
    return {"target": str(path), "counts": counts, "items": items}


def render_table(report):
    rows = ["readiness       analystkit build export side-effect  path"]
    for item in report["items"]:
        rows.append("{:<15} {:<10} {:<5} {:<6} {:<12} {}".format(item["readiness"], str(item.get("imports_analystkit", False)), str(item.get("build_figure", False)), str(item.get("direct_export", False)), str(item.get("possible_import_side_effect", False)), item["path"]))
    return "\n".join(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only AnalystKit migration audit")
    parser.add_argument("target")
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args(argv)
    report = audit_path(args.target)
    print(render_table(report))
    payload = json.dumps(report, indent=2)
    if args.json_path:
        Path(args.json_path).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
