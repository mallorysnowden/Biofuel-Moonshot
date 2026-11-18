# SAF configurations compared

Same EU market, finance, company and learning inputs for every case (`inputs/saf_market.toml`).

Benchmarks: HEFA SAF $2,214/t; projected 2035 SAF price $1,718/t; long-run SAF price $1,435/t; fossil jet $735/t.

| Configuration | NPV | IRR | P(NPV>0) | NOAK MSP $/t | $/t CO2e | SAF kt/yr per plant | Peak cash | Year-15 revenue | Kill metrics passed |
|---|---|---|---|---|---|---|---|---|---|
| Trash refinery (sorted MSW, gasification + FT) | -$786.9M | 4% | 7% | $1,756 | $314 | 28 | $2.79B | $715.0M | 2/5 |
| Trash refinery, unsorted feed (Fulcrum-like) | -$2.38B | -4% | 0% | $3,025 | $705 | 31 | $6.07B | $621.1M | 0/5 |
| Sorted wet organics, HTL | -$917.0M | -6% | 0% | $3,274 | $834 | 10 | $2.22B | $250.2M | 1/5 |
| Pongamia on degraded land, HEFA | -$413.6M | 7% | 3% | $1,648 | $321 | 30 | $2.35B | $501.1M | 2/5 |
| Agave on semi-arid land, alcohol-to-jet | -$1.62B | 1% | 2% | $2,136 | $493 | 87 | $5.59B | $765.7M | 2/5 |

Monte Carlo: 2000 draws per case, triangular on every input with a range.
MSP = levelized SAF price at which one NOAK plant breaks even over its life at the company discount rate.
See results/<project>/summary.md for each case's full report.
