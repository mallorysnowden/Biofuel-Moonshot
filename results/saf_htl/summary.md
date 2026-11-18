# Sorted wet organics to hydrothermal liquefaction SAF: TEA results

## Conventions

- Real 2026 US dollars (pre-tax). Canadian and euro figures converted at the fx rates below.
- Unit costs are entered at NOAK (Nth of a kind). The cost of getting there is shown separately with Wright's-law learning curves.
- **Boundary:** Wet organic waste at the gate to SAF and co-products at the plant gate. Excludes collection.
- **Functional units:** Levelized SAF supply cost ($/t fuel); cost of CO2e avoided ($/t).
- Company discount rate 10%, customer discount rate 8%, horizon 15 years.

## Headline

| Metric | Value |
|---|---|
| NPV | -$918.0M |
| IRR | n/a |
| Probability NPV > 0 (Monte Carlo) | 0% |
| Peak cash need | $2.17B |
| Cash breakeven year | not within horizon |
| Revenue in final year | $309.1M |
| NOAK reached in year | 12 |
| Extra cost paid while learning (FOAK to NOAK) | $242.6M |
| NPV if costs started at NOAK (no learning period) | -$771.0M |

## Customer cost vs BAU

**SAF supply cost (levelized over plant life)** ($/t fuel)

| Option | Value | vs ours |
|---|---|---|
| Ours at NOAK (MSP) | $2,947 | 1.00x |
| Ours, first plant (FOAK MSP) | $3,866 | 1.31x |
| HEFA SAF market price (incumbent SAF) | $2,214 | 0.75x |
| Projected SAF price in 2035 (this model) | $1,718 | 0.58x |
| Fossil jet | $735 | 0.25x |
| Fossil jet + ReFuelEU penalty | $3,693 | 1.25x |

MSP credits co-products and other revenue. The penalty is at least twice the SAF-jet price gap per tonne missed.

**Cost of CO2e avoided** ($/t CO2e)

| Option | Value | vs ours |
|---|---|---|
| Ours at NOAK | $726 | 1.00x |
| HEFA SAF at market price | $455 | 0.63x |

Price premium over fossil jet divided by life-cycle CO2e avoided per tonne.

**Mass balance per plant (t/yr at 100% availability)**

| Stream | t/yr |
|---|---|
| feed | 300,000 |
| dry | 75,000 |
| biocrude | 30,000 |
| fuel | 24,000 |
| saf range | 12,000 |

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
| 3 | commercial | $17.2M | -$313,596 | $10.3M | -$10.7M | $281.7M | -$332.4M | 1.47 |
| 4 | commercial | $33.9M | $10.4M | $10.7M | -$297,080 | $0 | -$332.7M | 1.47 |
| 5 | commercial | $50.1M | $9.1M | $11.0M | -$1.9M | $247.9M | -$582.6M | 1.29 |
| 6 | commercial | $65.8M | $18.8M | $11.3M | $7.5M | $0 | -$575.0M | 1.29 |
| 7 | commercial | $81.2M | $16.6M | $11.6M | $5.0M | $230.1M | -$800.1M | 1.20 |
| 8 | commercial | $112.1M | $24.1M | $12.2M | $11.8M | $218.2M | -$1.01B | 1.14 |
| 9 | commercial | $142.3M | $30.7M | $12.8M | $17.9M | $209.4M | -$1.20B | 1.09 |
| 10 | commercial | $171.7M | $36.6M | $13.4M | $23.2M | $202.5M | -$1.38B | 1.05 |
| 11 | commercial | $200.4M | $41.9M | $14.0M | $27.8M | $196.8M | -$1.55B | 1.02 |
| 12 | commercial | $228.5M | $46.4M | $14.6M | $31.8M | $192.0M | -$1.71B | 1.00 |
| 13 | commercial | $255.9M | $50.4M | $15.1M | $35.2M | $192.0M | -$1.86B | 1.00 |
| 14 | commercial | $282.8M | $53.7M | $15.7M | $38.1M | $192.0M | -$2.02B | 1.00 |
| 15 | commercial | $309.1M | $56.5M | $16.2M | $40.4M | $192.0M | -$2.17B | 1.00 |

Revenue in the final year by stream:

- saf: $161.1M (52%)
- coproducts: $94.5M (31%)
- gate_fees: $53.5M (17%)

## Break-evens

| Question | Answer | Base input |
|---|---|---|
| Annual decline in SAF premium for NPV = 0 | -0.0369 | 0.04 |
| Long-run SAF premium floor ($/t) for NPV = 0 | no crossing in range | 700 |
| Biocrude yield for NPV = 0 | no crossing in range | 0.4 |
| NOAK capex per t/yr wet feed for NPV = 0 | 266 | 640 |
| Gate fee for NPV = 0 | 103 | 20 |

## Scenarios

| Scenario | NPV | Final-year revenue | Peak cash need |
|---|---|---|---|
| Source-separated food waste (no sorting cost) | -$748.6M | $309.1M | $1.93B |
| Higher jet cut (65%) | -$828.8M | $329.1M | $2.03B |
| Food waste gate fee $60/t (composting-level) | -$475.4M | $416.2M | $1.53B |
| SAF premium holds at today's level | -$626.0M | $385.0M | $1.80B |
| SAF premium falls 8%/yr | -$963.1M | $301.7M | $2.28B |

## Sensitivity (one input at a time)

![Tornado](tornado.png)

| Input | Low | NPV at low | High | NPV at high |
|---|---|---|---|---|
| `htl.capex_per_wet_t` | 400 | -$328.7M | 1,125 | -$2.11B |
| `waste.gate_fee` | 0 | -$1.14B | 70 | -$364.8M |
| `sort.cost` | 0 | -$748.6M | 40 | -$1.20B |
| `htl.biocrude_yield` | 0.25 | -$1.19B | 0.5 | -$738.8M |
| `htl.var_opex` | 250 | -$782.5M | 650 | -$1.14B |
| `htl.moisture` | 0.7 | -$774.7M | 0.82 | -$1.12B |
| `market.premium_decline` | 0.0 | -$626.0M | 0.1 | -$967.3M |
| `market.jet_price` | 600 | -$1.05B | 950 | -$708.6M |
| `finance.company_discount_rate` | 0.08 | -$1.03B | 0.15 | -$697.3M |
| `htl.availability` | 0.65 | -$1.10B | 0.92 | -$854.7M |
| `learning.rate_capex` | 0.05 | -$825.1M | 0.2 | -$1.06B |
| `htl.jet_share` | 0.3 | -$1.04B | 0.65 | -$828.8M |
| `learning.noak_experience` | 4 | -$834.6M | 15 | -$1.04B |
| `market.coproduct_factor` | 1.0 | -$983.0M | 1.5 | -$820.4M |
| `htl.upgrade_yield` | 0.7 | -$1.01B | 0.88 | -$846.3M |

## Monte Carlo

1,000 draws, triangular distribution on every input with a range.

| P10 | P50 | P90 | P(NPV > 0) |
|---|---|---|---|
| -$1.71B | -$1.05B | -$565.8M | 0% |

![Monte Carlo](monte_carlo.png)

## Kill metrics

| Metric | Value | Threshold | Passes |
|---|---|---|---|
| NOAK MSP vs HEFA SAF price | 1.33 x (<=1 to win) | 1.00 | no |
| NOAK MSP vs projected 2035 SAF price | 1.72 x (<=1 to win) | 1.00 | no |
| Cost of CO2e avoided at NOAK | 726.39 $/t (<=300) | 300.00 | no |
| Biocrude yield on dry food waste | 0.40 t/t dry (>=0.40) | 0.40 | yes |
| Revenue at full scale vs big-enough line | 0.31 x | 1.00 | no |
| Probability NPV > 0 | 0% | 50% | no |

## Scorecard

Economics is scored from P(NPV > 0); the rest are judgment scores set in the inputs file.

| Category | Weight | Score |
|---|---|---|
| impact | 20% | 3 |
| breakthrough | 20% | 3 |
| feasibility | 15% | 3 |
| economics | 15% | 1 |
| scalability | 10% | 3 |
| demand | 10% | 5 |
| white space | 5% | 3 |
| validation | 5% | 3 |
| **Weighted total** | | **2.90** |

## Notes

- All carbon is biogenic, so all SAF-range fuel counts toward ReFuelEU.
- Market check: 11 plants at maturity make 112 kt/yr of SAF-range fuel, 1.2% of the ~9.2 Mt/yr the EU mandate requires in 2035.
- One mature plant: 10.2 kt/yr SAF-range fuel (0% from fossil carbon), 10.2 kt/yr co-products.
- SAF price path: premium over jet $1,362/t in model year 1 (2027), $983/t in 2035, $769/t in year 15.
- NPV and IRR include the remaining-life operating cash of plants built within the 15-yr horizon (no new builds after it). NPV over the horizon alone: $-1,000M.
- Pre-tax, real 2026 USD; operating profit is before depreciation.

