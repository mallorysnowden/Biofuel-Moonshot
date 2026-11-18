"""Run every SAF configuration and write one apples-to-apples comparison table.

Usage: python scripts/compare_saf.py [--draws N]
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from run_tea import load_project_params  # noqa: E402
from tea import saf_engine as e  # noqa: E402
from tea.framework.report import money  # noqa: E402
from tea.framework.uncertainty import monte_carlo  # noqa: E402
from tea.inputs import base_values  # noqa: E402

CASES = [
    ("Trash refinery (sorted MSW, gasification + FT)", "saf_msw_ft", {}),
    ("Trash refinery, unsorted feed (Fulcrum-like)", "saf_msw_ft", {"sort.enabled": 0}),
    ("Sorted wet organics, HTL", "saf_htl", {}),
    ("Pongamia on degraded land, HEFA", "saf_pongamia", {}),
    ("Agave on semi-arid land, alcohol-to-jet", "saf_pongamia", "AGAVE"),
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--draws", type=int, default=1000)
    args = ap.parse_args()
    rows = []
    for label, project, override in CASES:
        mod = importlib.import_module(f"tea.{project}")
        params = load_project_params(ROOT / "inputs" / f"{project}.toml")
        if override == "AGAVE":
            override = mod.AGAVE
        v = {**base_values(params), **override}
        r = mod.run(v)
        mc = monte_carlo(params, v, lambda x: mod.run(x).npv, draws=args.draws)
        p_pos = sum(x > 0 for x in mc) / len(mc)
        m = e.msp(v, mod.plant_year)
        mat = e.mature(v, mod.plant_year)
        kills_passed = sum(k.passes for k in r.kill_metrics)
        rows.append([label, money(r.npv), f"{r.irr:.0%}" if r.irr is not None else "n/a", f"{p_pos:.0%}",
                     f"${m:,.0f}", f"${e.abatement_cost(v, m, v['ghg.saving']):,.0f}",
                     f"{(mat['saf'] + mat['saf_rcf']) / 1e3:,.0f}", money(r.peak_cash_need), money(r.full_scale_revenue),
                     f"{kills_passed}/{len(r.kill_metrics)}"])
    v0 = base_values(load_project_params(ROOT / "inputs" / "saf_msw_ft.toml"))
    head = ["Configuration", "NPV", "IRR", "P(NPV>0)", "NOAK MSP $/t", "$/t CO2e", "SAF kt/yr per plant",
            "Peak cash", "Year-15 revenue", "Kill metrics passed"]
    L = ["# SAF configurations compared", "",
         "Same EU market, finance, company and learning inputs for every case (`inputs/saf_market.toml`).", "",
         f"Benchmarks: HEFA SAF ${v0['market.hefa_price']:,.0f}/t; projected 2035 SAF price "
         f"${e.saf_price(v0, e.year_of(v0, 2035)):,.0f}/t; long-run SAF price "
         f"${v0['market.jet_price'] + v0['market.premium_floor']:,.0f}/t; fossil jet ${v0['market.jet_price']:,.0f}/t.", "",
         "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    L += ["| " + " | ".join(r) + " |" for r in rows]
    L += ["", f"Monte Carlo: {args.draws} draws per case, triangular on every input with a range.",
          "MSP = levelized SAF price at which one NOAK plant breaks even over its life at the company discount rate.",
          "See results/<project>/summary.md for each case's full report."]
    out = ROOT / "results" / "comparison.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
