"""Sorted wet organics (food waste) to hydrothermal liquefaction (HTL), then biocrude upgrading to SAF.

HTL handles wet feed without drying, which suits the food-waste fraction that gasifiers
struggle with. The same molecular sorting line that feeds the gasifier case separates the
organics; source-separated food waste is a scenario.
"""
from __future__ import annotations

from . import saf_engine as e
from .framework.result import KillMetric

PROJECT = "Sorted wet organics to hydrothermal liquefaction SAF"


def mass_balance(v) -> dict:
    feed = v["plant.feed_t"]
    dry = feed * (1 - v["htl.moisture"])
    biocrude = dry * v["htl.biocrude_yield"]
    fuel = biocrude * v["htl.upgrade_yield"]
    return {"feed": feed, "dry": dry, "biocrude": biocrude, "fuel": fuel, "saf_range": fuel * v["htl.jet_share"]}


def plant_year(v, age: int) -> dict:
    mb = mass_balance(v)
    by = int(v["plant.build_years"])
    op = age - by  # years since start-up
    running = 0 <= op < v["plant.life"]
    a = v["htl.availability"] * (v["plant.first_year_factor"] if op == 0 else 1.0) if running else 0.0
    feed = mb["feed"] * a
    return {
        "saf": mb["saf_range"] * a,
        "saf_rcf": 0.0,
        "coproduct": mb["fuel"] * (1 - v["htl.jet_share"]) * a,
        "revenue": {"gate_fees": feed * v["waste.gate_fee"]},
        "opex": {"sorting": feed * v["sort.cost"],
                 "variable": mb["fuel"] * a * v["htl.var_opex"],
                 "fixed": mb["feed"] * v["htl.capex_per_wet_t"] * v["htl.fixed_share"] if running else 0.0},
        "capex": mb["feed"] * v["htl.capex_per_wet_t"] / by if age < by else 0.0,
    }


def run(v):
    mb = mass_balance(v)
    y = v["htl.biocrude_yield"]
    kills = [KillMetric("Biocrude yield on dry food waste", y, 0.40, "t/t dry (>=0.40)", y >= 0.40,
                        "PNNL sets >0.44 as a target for sludge; food waste varies with protein and ash")]
    table = ("Mass balance per plant (t/yr at 100% availability)", ["Stream", "t/yr"],
             [[k.replace("_", " "), f"{x:,.0f}"] for k, x in mb.items()])
    return e.run(v, plant_year, PROJECT, kills, tables=[table],
                 notes=["All carbon is biogenic, so all SAF-range fuel counts toward ReFuelEU."])


def breakevens(v):
    return e.common_breakevens(v, run, [
        ("htl.biocrude_yield", 0.1, 0.7, "Biocrude yield for NPV = 0"),
        ("htl.capex_per_wet_t", 20, 3000, "NOAK capex per t/yr wet feed for NPV = 0"),
        ("waste.gate_fee", -100, 300, "Gate fee for NPV = 0"),
    ])


def scenarios(v):
    return [
        ("Source-separated food waste (no sorting cost)", {"sort.cost": 0}),
        ("Higher jet cut (65%)", {"htl.jet_share": 0.65}),
        ("Food waste gate fee $60/t (composting-level)", {"waste.gate_fee": 60}),
        *e.common_scenarios(),
    ]
