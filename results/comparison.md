# SAF configurations compared

Same EU market, finance, company and learning inputs for every case (`inputs/saf_market.toml`).

Benchmarks: HEFA SAF $2,214/t; projected 2035 SAF price $1,718/t; long-run SAF price $1,435/t; fossil jet $735/t.

| Configuration | NPV | IRR | P(NPV>0) | NOAK MSP $/t | $/t CO2e | SAF kt/yr per plant | Peak cash | Year-15 revenue | Kill metrics passed |
|---|---|---|---|---|---|---|---|---|---|
| Trash refinery (sorted MSW, gasification + FT) | -$612.2M | 5% | 11% | $1,552 | $251 | 28 | $2.29B | $883.2M | 4/5 |
| Trash refinery, unsorted feed (Fulcrum-like) | -$2.38B | -4% | 1% | $2,709 | $608 | 31 | $5.92B | $767.3M | 0/5 |
| Sorted wet organics, HTL | -$918.0M | n/a | 0% | $2,947 | $726 | 10 | $2.17B | $309.1M | 1/5 |
| Pongamia on degraded land, HEFA | -$390.7M | 7% | 4% | $1,648 | $321 | 30 | $2.33B | $501.1M | 2/5 |
| Agave on semi-arid land, alcohol-to-jet | -$1.59B | 1% | 3% | $2,136 | $493 | 87 | $5.56B | $765.7M | 2/5 |

Monte Carlo: 1000 draws per case, triangular on every input with a range.
MSP = levelized SAF price at which one NOAK plant breaks even over its life at the company discount rate.
See results/<project>/summary.md for each case's full report.
