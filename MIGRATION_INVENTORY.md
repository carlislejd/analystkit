# AnalystKit migration inventory

Generated 2026-08-05 with the read-only AST auditor. The auditor inspected
Python source only; it did not import, query, or execute either target project.

| Target | Ready | Small adapter | Manual refactor | Total |
| --- | ---: | ---: | ---: | ---: |
| Chart Generator | 0 | 144 | 48 | 192 |
| Composite Deck charts | 20 | 24 | 9 | 53 |

## Patterns

- Chart Generator has 144 AnalystKit-using files, but none exposes the
  `build_figure(start_date=None, end_date=None)` convention. All 192 therefore
  need that small structural adapter before a governed migration.
- 28 Chart Generator files call Plotly `write_image` or `write_html` directly;
  the new bundle helper can replace only that output concern.
- Composite Deck is the most migration-ready pool: 20 of 53 scripts already
  meet the static contract. Thirty scripts merit review for embedded titles or
  source furniture, and four retain direct Plotly exports.
- The 48 Chart Generator and nine Composite Deck manual-refactor candidates do
  not import AnalystKit. The auditor found one possible Chart Generator
  import-time side effect; that script should be isolated before migration.

## Proposed first tranche

| Chart | Current home / owner of business and data logic | Migration value |
| --- | --- | --- |
| `quarterly/bitcoin_etf_flows.py` | Composite Deck | Existing build convention; direct pilot for flow bars and metadata. |
| `quarterly/ethereum_etf_flows.py` | Composite Deck | Same recurring flow family; validates reusable adapter. |
| `quarterly/select_assets_correlation_matrix.py` | Composite Deck | Matrix pilot and current deck metadata pattern. |
| `composite/bitwise10_returns.py` | Composite Deck | Long/short time-window return convention. |
| `quarterly/btc_sp500_correlation.py` | Composite Deck | Time-series range-tick contract. |
| `quarterly/btc_30d_volatility.py` | Composite Deck | Repeating risk-metric chart family. |
| `Bitcoin vs Gold 8-Week Performance.py` | Chart Generator | Multi-series performance reference and standalone/deck split. |
| `Bitcoin ETF Flows.py` | Chart Generator | Direct-export cleanup and monthly-flow reference. |
| `SICAV Correlation Matrix.py` | Chart Generator | Correlation-matrix standardization without changing source logic. |
| `Total Crypto Market Capitalization.py` | Chart Generator | High-value market series and as-of metadata pilot. |

The calling project continues to own all queries, credentials, calculations,
schedule, and delivery. AnalystKit owns the profile, metadata, validation,
artifact bundle, and visual/export conventions.

## Remaining primitives after pilots

No additional mandatory primitive is evident. The only candidates to revisit
after the first tranche are a standardized annotation/footnote exception
record and a reusable separate-overlay export helper. Neither should be added
until a migration demonstrates a repeated, stable interface.
