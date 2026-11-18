# Trash refinery: sorted MSW to gasification + Fischer-Tropsch SAF: TEA results

## Conventions

- Real 2026 US dollars (pre-tax). Canadian and euro figures converted at the fx rates below.
- Unit costs are entered at NOAK (Nth of a kind). The cost of getting there is shown separately with Wright's-law learning curves.
- **Boundary:** Residual MSW at the gate to SAF, co-products and recyclables at the plant gate. Excludes collection.
- **Functional units:** Levelized SAF supply cost ($/t fuel); cost of CO2e avoided ($/t).
- Company discount rate 10%, customer discount rate 8%, horizon 15 years.

## Headline

| Metric | Value |
|---|---|
| NPV | -$786.9M |
| IRR | 4% |
| Probability NPV > 0 (Monte Carlo) | 7% |
| Peak cash need | $2.79B |
| Cash breakeven year | not within horizon |
| Revenue in final year | $715.0M |
| NOAK reached in year | 12 |
| Extra cost paid while learning (FOAK to NOAK) | $410.3M |
| NPV if costs started at NOAK (no learning period) | -$549.6M |

## Customer cost vs BAU

**SAF supply cost (levelized over plant life)** ($/t fuel)

| Option | Value | vs ours |
|---|---|---|
| Ours at NOAK (MSP) | $1,756 | 1.00x |
| Ours, first plant (FOAK MSP) | $2,426 | 1.38x |
| HEFA SAF market price (incumbent SAF) | $2,214 | 1.26x |
| Projected SAF price in 2035 (this model) | $1,718 | 0.98x |
| Fossil jet | $735 | 0.42x |
| Fossil jet + ReFuelEU penalty | $3,693 | 2.10x |

MSP credits co-products and other revenue. The penalty is at least twice the SAF-jet price gap per tonne missed.

**Cost of CO2e avoided** ($/t CO2e)

| Option | Value | vs ours |
|---|---|---|
| Ours at NOAK | $314 | 1.00x |
| HEFA SAF at market price | $455 | 1.45x |

Price premium over fossil jet divided by life-cycle CO2e avoided per tonne.

**Mass balance per plant (t/yr at 100% availability)**

| Stream | t/yr |
|---|---|
| feed | 500,000 |
| recyclables | 60,000 |
| organics | 150,000 |
| residue | 290,000 |
| dry | 232,000 |
| liquids | 46,400 |
| saf range | 32,480 |

## FOAK to NOAK

Cost multiplier vs the incumbent's cost for each component (1.00 = incumbent).

| Component | FOAK | NOAK |
|---|---|---|
| plant capex | 1.47 | 1.00 |

## Cash flow

| Year | Phase | Revenue | Gross profit | Operating cost | EBIT | Capex | Cumulative cash | Cost vs incumbent |
|---|---|---|---|---|---|---|---|---|
| 1 | R&D | $0 | $0 | $20.0M | -$20.0M | $0 | -$20.0M | 1.47 |
| 2 | R&D | $0 | $0 | $20.0M | -$20.0M | $0 | -$40.0M | 1.47 |
| 3 | commercial | $0 | $0 | $10.0M | -$10.0M | $238.3M | -$288.3M | 1.47 |
| 4 | commercial | $0 | $0 | $10.0M | -$10.0M | $238.3M | -$536.6M | 1.47 |
| 5 | commercial | $46.5M | $9.0M | $11.4M | -$2.4M | $209.7M | -$748.7M | 1.29 |
| 6 | commercial | $91.9M | $37.8M | $12.8M | $25.0M | $209.7M | -$933.4M | 1.29 |
| 7 | commercial | $136.3M | $44.7M | $14.1M | $30.6M | $194.6M | -$1.10B | 1.20 |
| 8 | commercial | $179.8M | $71.5M | $15.4M | $56.1M | $379.1M | -$1.42B | 1.14 |
| 9 | commercial | $222.4M | $76.7M | $16.7M | $60.0M | $361.7M | -$1.72B | 1.09 |
| 10 | commercial | $308.3M | $108.4M | $19.2M | $89.2M | $348.4M | -$1.98B | 1.05 |
| 11 | commercial | $392.5M | $138.5M | $21.8M | $116.7M | $337.7M | -$2.20B | 1.02 |
| 12 | commercial | $475.2M | $167.0M | $24.3M | $142.8M | $328.8M | -$2.39B | 1.00 |
| 13 | commercial | $556.4M | $194.1M | $26.7M | $167.4M | $324.8M | -$2.55B | 1.00 |
| 14 | commercial | $636.3M | $219.9M | $29.1M | $190.8M | $324.8M | -$2.68B | 1.00 |
| 15 | commercial | $715.0M | $244.4M | $31.4M | $212.9M | $324.8M | -$2.79B | 1.00 |

Revenue in the final year by stream:

- saf: $321.4M (45%)
- coproducts: $88.7M (12%)
- gate_fees: $252.9M (35%)
- recyclables: $52.0M (7%)

## Break-evens

| Question | Answer | Base input |
|---|---|---|
| Annual decline in SAF premium for NPV = 0 | -0.00906 | 0.04 |
| Long-run SAF premium floor ($/t) for NPV = 0 | no crossing in range | 700 |
| Gasifier availability for NPV = 0 | no crossing in range | 0.85 |
| NOAK capex per t/yr dry gasifier feed for NPV = 0 | 946 | 1,400 |
| Gate fee for NPV = 0 | 123 | 70 |

## Scenarios

| Scenario | NPV | Final-year revenue | Peak cash need |
|---|---|---|---|
| No sorting (Fulcrum-like feed) | -$2.38B | $621.1M | $6.07B |
| Fossil-carbon fuel earns no SAF premium | -$919.4M | $683.4M | $2.97B |
| Fossil-carbon fuel earns the full SAF premium | -$654.5M | $746.6M | $2.61B |
| Low gate fee ($30/t) | -$1.38B | $570.5M | $3.51B |
| UK-level gate fee ($150/t) | $408.2M | $1.00B | $1.70B |
| SAF premium holds at today's level | -$228.1M | $852.2M | $2.23B |
| SAF premium falls 8%/yr | -$847.1M | $701.6M | $2.95B |

## Sensitivity (one input at a time)

![Tornado](tornado.png)

| Input | Low | NPV at low | High | NPV at high |
|---|---|---|---|---|
| `ft.capex_per_dry_t` | 900 | $80.3M | 2,200 | -$2.17B |
| `waste.gate_fee` | 30 | -$1.38B | 150 | $408.2M |
| `ft.fuel_yield` | 0.15 | -$1.21B | 0.25 | -$360.8M |
| `sort.cost` | 15 | -$555.9M | 60 | -$1.25B |
| `ft.availability` | 0.6 | -$1.30B | 0.92 | -$642.2M |
| `market.premium_decline` | 0.0 | -$228.1M | 0.1 | -$850.3M |
| `market.jet_price` | 600 | -$985.3M | 950 | -$471.0M |
| `ft.var_opex` | 50 | -$644.0M | 110 | -$1.07B |
| `sort.recyclables_share` | 0.08 | -$943.0M | 0.18 | -$552.7M |
| `sort.recyclables_value` | 40 | -$930.3M | 250 | -$553.9M |
| `learning.rate_capex` | 0.05 | -$637.0M | 0.2 | -$1.01B |
| `sort.organics_fee` | 0 | -$694.5M | 80 | -$1.06B |
| `sort.organics_share` | 0.2 | -$967.1M | 0.4 | -$606.7M |
| `learning.noak_experience` | 4 | -$652.3M | 15 | -$979.6M |
| `market.premium_floor` | 300 | -$850.4M | 1,100 | -$530.2M |

## Monte Carlo

2,000 draws, triangular distribution on every input with a range.

| P10 | P50 | P90 | P(NPV > 0) |
|---|---|---|---|
| -$1.87B | -$1.03B | -$150.1M | 7% |

![Monte Carlo](monte_carlo.png)

## Kill metrics

| Metric | Value | Threshold | Passes |
|---|---|---|---|
| NOAK MSP vs HEFA SAF price | 0.79 x (<=1 to win) | 1.00 | yes |
| NOAK MSP vs projected 2035 SAF price | 1.02 x (<=1 to win) | 1.00 | no |
| Cost of CO2e avoided at NOAK | 314.39 $/t (<=300) | 300.00 | no |
| Gasifier availability with sorted feed | 0.85 fraction (>=0.80) | 0.80 | yes |
| Revenue at full scale vs big-enough line | 0.71 x | 1.00 | no |
| Probability NPV > 0 | 7% | 50% | no |

## Scorecard

Economics is scored from P(NPV > 0); the rest are judgment scores set in the inputs file.

| Category | Weight | Score |
|---|---|---|
| impact | 20% | 4 |
| breakthrough | 20% | 4 |
| feasibility | 15% | 3 |
| economics | 15% | 1 |
| scalability | 10% | 3 |
| demand | 10% | 5 |
| white space | 5% | 3 |
| validation | 5% | 3 |
| **Weighted total** | | **3.30** |

## Notes

- Fuel from the fossil (plastic) share of the residue earns the policy.rcf_credit share of the SAF premium.
- Market check: 11 plants at maturity make 304 kt/yr of SAF-range fuel, 3.3% of the ~9.2 Mt/yr the EU mandate requires in 2035.
- One mature plant: 27.6 kt/yr SAF-range fuel (35% from fossil carbon), 11.8 kt/yr co-products.
- SAF price path: premium over jet $1,362/t in model year 1 (2027), $983/t in 2035, $769/t in year 15.
- NPV and IRR include the remaining-life operating cash of plants built within the 15-yr horizon (no new builds after it) while it stays positive; 26 tail years counted. NPV over the horizon alone: $-1,334M.
- Pre-tax, real 2026 USD; operating profit is before depreciation.

