"""Trash refinery: Materra-style molecular sorting of residual MSW, then gasification + Fischer-Tropsch SAF.

Sorting splits each tonne of residual waste three ways: recyclables (sold), wet organics
(sent to anaerobic digestion at a fee), and a dry residue of known chemistry that feeds the
gasifier. The hypothesis is that a controlled gasifier diet raises plant availability above
what unsorted plants like Fulcrum's Sierra achieved.
"""
from __future__ import annotations

from . import saf_engine as e
from .framework.result import KillMetric

PROJECT = "Trash refinery: sorted MSW to gasification + Fischer-Tropsch SAF"


def mass_balance(v) -> dict:
    feed = v["plant.feed_t"]
    recyc = feed * v["sort.recyclables_share"] * v["sort.enabled"]
    organics = feed * v["sort.organics_share"] * v["sort.enabled"]
    residue = feed - recyc - organics
    dry = residue * (1 - v["ft.residue_moisture"])
    liquids = dry * v["ft.fuel_yield"]
    return {"feed": feed, "recyclables": recyc, "organics": organics, "residue": residue, "dry": dry,
            "liquids": liquids, "saf_range": liquids * v["ft.saf_selectivity"]}


def availability(v) -> float:
    return v["ft.availability"] if v["sort.enabled"] else v["ft.availability_unsorted"]


def plant_year(v, age: int) -> dict:
    mb = mass_balance(v)
    capex = mb["dry"] * v["ft.capex_per_dry_t"] if age == 0 else 0.0
    a = availability(v) * (v["plant.first_year_factor"] if age == 0 else 1.0)
    if age > v["plant.life"]:
        a = 0.0
    saf = mb["saf_range"] * a
    bio = v["ft.biogenic_share"]
    feed = mb["feed"] * a
    return {
        "saf": saf * bio,
        "saf_rcf": saf * (1 - bio),
        "coproduct": mb["liquids"] * (1 - v["ft.saf_selectivity"]) * a,
        "revenue": {"gate_fees": feed * v["waste.gate_fee"],
                    "recyclables": mb["recyclables"] * a * v["sort.recyclables_value"]},
        "opex": {"sorting": feed * v["sort.cost"] * v["sort.enabled"] + feed * v["ft.prep_cost"],
                 "organics_disposal": mb["organics"] * a * v["sort.organics_fee"],
                 "variable": mb["dry"] * a * v["ft.var_opex"],
                 "fixed": mb["dry"] * v["ft.capex_per_dry_t"] * v["ft.fixed_share"] if age <= v["plant.life"] else 0.0},
        "capex": capex,
    }


def run(v):
    mb = mass_balance(v)
    kills = [KillMetric("Gasifier availability with sorted feed", availability(v), 0.80, "fraction (>=0.80)",
                        availability(v) >= 0.80, "The core hypothesis: a controlled diet fixes Fulcrum's failure mode")]
    table = ("Mass balance per plant (t/yr at 100% availability)", ["Stream", "t/yr"],
             [[k.replace("_", " "), f"{x:,.0f}"] for k, x in mb.items()])
    return e.run(v, plant_year, PROJECT, kills, tables=[table], notes=[
        "Fuel from the fossil (plastic) share of the residue earns the policy.rcf_credit share of the SAF premium."])


def breakevens(v):
    return e.common_breakevens(v, run, [
        ("ft.availability", 0.3, 0.98, "Gasifier availability for NPV = 0"),
        ("ft.capex_per_dry_t", 100, 6000, "NOAK capex per t/yr dry gasifier feed for NPV = 0"),
        ("waste.gate_fee", -100, 300, "Gate fee for NPV = 0"),
    ])


def scenarios(v):
    return [
        ("No sorting (Fulcrum-like feed)", {"sort.enabled": 0}),
        ("Fossil-carbon fuel earns no SAF premium", {"policy.rcf_credit": 0.0}),
        ("Fossil-carbon fuel earns the full SAF premium", {"policy.rcf_credit": 1.0}),
        ("Low gate fee ($30/t)", {"waste.gate_fee": 30}),
        ("UK-level gate fee ($150/t)", {"waste.gate_fee": 150}),
        *e.common_scenarios(),
    ]
