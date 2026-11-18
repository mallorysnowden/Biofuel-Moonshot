# Biofuel moonshot TEA

Techno-economic analysis of sustainable aviation fuel (SAF) moonshots sold into the
EU ReFuelEU market, on the standard TEA framework shared with the thermosyphon and
prefab-homes repos (NOAK costs, Wright's-law learning, BAU comparison, tornado,
Monte Carlo, break-evens, kill metrics, scorecard).

Three supply configurations sell into the same market with the same finance, company
and learning inputs (`inputs/saf_market.toml`), so they compare apples to apples:

| Model | Configuration |
|---|---|
| `tea/saf_msw_ft.py` | **Trash refinery.** Materra-style molecular sorting of residual MSW into recyclables, wet organics and a dry residue that feeds gasification + Fischer-Tropsch |
| `tea/saf_htl.py` | Sorted wet organics to hydrothermal liquefaction (HTL) and upgrading |
| `tea/saf_pongamia.py` | Pongamia on severely degraded land to HEFA (agave + alcohol-to-jet as a scenario) |

## Run it

```bash
pip install -r requirements.txt
python scripts/run_tea.py saf_msw_ft        # also saf_htl, saf_pongamia
python scripts/compare_saf.py               # writes results/comparison.md
python -m pytest
```

## Results (base case)

| Configuration | NPV | IRR | P(NPV>0) | NOAK MSP $/t | $/t CO2e | Kill metrics passed |
|---|---|---|---|---|---|---|
| Trash refinery (sorted MSW, gasification + FT) | -$787M | 4% | 7% | $1,756 | $314 | 2/5 |
| Trash refinery, unsorted feed (Fulcrum-like) | -$2.38B | -4% | 0% | $3,025 | $705 | 0/5 |
| Sorted wet organics, HTL | -$917M | -6% | 0% | $3,274 | $834 | 1/5 |
| Pongamia on degraded land, HEFA | -$414M | 7% | 3% | $1,648 | $321 | 2/5 |
| Agave on semi-arid land, alcohol-to-jet | -$1.62B | 1% | 2% | $2,136 | $493 | 2/5 |

Benchmarks: HEFA SAF $2,214/t (EASA 2025), projected 2035 SAF price $1,718/t,
long-run SAF price $1,435/t (fossil jet $735 + a $700 premium floor), fossil jet $735/t.
MSP is the levelized SAF price at which one NOAK plant breaks even over its life at 10%,
including two years of construction before start-up.

**What it says**

1. **The trash refinery is the strongest waste configuration, and sorting is the reason.**
   Sorting cuts the MSP from $3,025/t to $1,756/t, 21% below today's HEFA price.
   That gap is the Fulcrum lesson quantified: a controlled gasifier diet lifts
   availability and lets recyclables and organics leave before the gasifier.
2. **No configuration clears a 10% return at base.** The trash refinery's MSP sits
   above both the projected 2035 price and the long-run price. The decisive inputs are
   market and siting, not chemistry:
   - Gate fee: break-even at ~$123/t (EU average ~$70); at UK-level fees ($150/t) NPV is +$408M.
   - NOAK capex: break-even at ~$946 per t/yr of dry feed (base $1,400).
   - Even if the 2025 premium held flat, NPV is −$228M.
3. **HTL fails on scale and cost.** One plant makes only ~10 kt/yr SAF; HTL fuel skews to diesel.
4. **Pongamia has the lowest MSP but is land- and time-bound.** MSP $1,648/t; trees take
   7 years to full yield; needs ~3.8 t oil/ha (base 2.0) or ~$305/ha-yr carbon credits to
   break even. Agave yields ~2.9x more SAF per hectare but alcohol-to-jet conversion costs more.

## Consistency audit (Nov 2026)

Aligned with the thermosyphon and prefab-homes TEAs:

- **Construction time (correction):** gasifier and HTL plants now spend two years in
  construction before start-up. Previously they produced in their build year, which
  understated MSP by ~$200/t.
- **G&A:** raised from 2% to the shared 3% of revenue.
- **Shared remaining-life rule:** after the horizon, built plants run out their life
  with no new builds, counted only while cash stays positive.

## Caveats

- Pre-tax, real 2026 USD. NPV counts the remaining life of plants built within the
  15-year horizon (no new builds after, only while cash stays positive); each report
  also shows the horizon-only NPV.
- Whether fuel from the fossil (plastic) fraction earns the SAF premium as "recycled
  carbon aviation fuel" is unverified; `policy.rcf_credit` = 0.5 in base, 0 and 1 as scenarios.
- Capex, yields and the premium path are mostly assumptions with ranges; sources are in
  each inputs file and `results/<project>/inputs_used.csv`.
- The fossil-jet life-cycle comparator (94 g CO2e/MJ) is from memory.

## Layout

```
inputs/          conventions.toml, saf_market.toml (shared), one file per configuration
tea/saf_engine.py   fleet, learning, SAF price path, MSP, kill metrics (shared)
tea/saf_*.py        configuration plant models
scripts/run_tea.py, scripts/compare_saf.py
results/            per-configuration reports and comparison.md
```
