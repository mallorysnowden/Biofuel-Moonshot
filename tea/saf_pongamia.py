"""Afforestation feedstock: pongamia trees on severely degraded land, pressed for oil, refined to SAF by HEFA.

Crops grown on severely degraded land are now Annex IX Part A feedstocks, so the fuel counts
toward ReFuelEU. Each "plant" is a plantation block plus its share of crushing and HEFA
capacity. Trees yield from year 3 and reach full yield around year 7, so early years carry
cost with little output. Agave (ethanol, then alcohol-to-jet) on semi-arid land is a scenario.
"""
from __future__ import annotations

from . import saf_engine as e
from .framework.result import KillMetric

PROJECT = "Afforestation: pongamia on degraded land to HEFA SAF"

AGAVE = {
    "crop.feed_yield": 5.85,           # t ethanol/ha-yr: 7,414 L/ha-yr x 0.789 kg/L (U. Sydney field study)
    "crop.first_yield_age": 5,
    "crop.full_yield_age": 6,
    "crop.establish_cost": 2500,
    "crop.om_cost": 800,
    "crop.process_cost": 0,
    "crop.meal_yield": 0,
    "conv.liquid_yield": 0.60,         # EASA alcohol-to-jet: 60% fuel conversion
    "conv.jet_share": 0.83,            # EASA alcohol-to-jet: 83% SAF selectivity
    "conv.capex_per_t": 4500,
    "conv.var_opex": 500,
}


def yield_factor(v, age: int) -> float:
    first, full = v["crop.first_yield_age"], v["crop.full_yield_age"]
    if age < first or age > v["plant.life"]:
        return 0.0
    if age >= full:
        return 1.0
    return 0.2 + 0.8 * (age - first) / max(full - first, 1)


def mass_balance(v) -> dict:
    """Mature yields for one plantation block."""
    area = v["crop.area_ha"]
    feed = area * v["crop.feed_yield"]
    liquids = feed * v["conv.liquid_yield"]
    return {"area_ha": area, "feed": feed, "liquids": liquids, "saf_range": liquids * v["conv.jet_share"],
            "meal": area * v["crop.meal_yield"]}


def plant_year(v, age: int) -> dict:
    mb = mass_balance(v)
    y = yield_factor(v, age)
    conv_capex = mb["liquids"] * v["conv.capex_per_t"]
    capex = (mb["area_ha"] * v["crop.establish_cost"] if age == 0 else 0.0) + \
            (conv_capex if age == v["crop.first_yield_age"] - 1 else 0.0)
    alive = age <= v["plant.life"]
    converting = alive and age >= v["crop.first_yield_age"]
    return {
        "saf": mb["saf_range"] * y,
        "saf_rcf": 0.0,
        "coproduct": mb["liquids"] * (1 - v["conv.jet_share"]) * y,
        "revenue": {"meal": mb["meal"] * y * v["crop.meal_price"],
                    "carbon_credits": mb["area_ha"] * v["crop.carbon_credit"] if alive else 0.0},
        "opex": {"plantation": mb["area_ha"] * (v["crop.om_cost"] + v["crop.land_cost"]) if alive else 0.0,
                 "processing": mb["feed"] * y * v["crop.process_cost"],
                 "conversion_variable": mb["liquids"] * y * v["conv.var_opex"],
                 "conversion_fixed": conv_capex * v["conv.fixed_share"] if converting else 0.0},
        "capex": capex,
    }


def run(v):
    mb = mass_balance(v)
    per_ha = mb["saf_range"] / mb["area_ha"]
    kills = [KillMetric("Mature SAF yield per hectare", per_ha, 1.0, "t SAF/ha-yr (>=1.0)", per_ha >= 1.0,
                        "1 t/ha-yr threshold is a judgment; 9 Mt/yr of SAF would need ~9 Mha at that yield")]
    table = ("Mature plantation block (t/yr)", ["Stream", "Value"],
             [[k.replace("_", " "), f"{x:,.0f}"] for k, x in mb.items()])
    return e.run(v, plant_year, PROJECT, kills, tables=[table], notes=[
        "Fuel from crops on severely degraded land counts as an Annex IX Part A feedstock under ReFuelEU.",
        f"Land check: {mb['area_ha'] / 1e3:,.0f} kha per block; SAF yield {per_ha:.2f} t/ha-yr at maturity."])


def breakevens(v):
    return e.common_breakevens(v, run, [
        ("crop.feed_yield", 0.2, 8.0, "Mature oil yield (t/ha-yr) for NPV = 0"),
        ("crop.establish_cost", 0, 20000, "Establishment cost per ha for NPV = 0"),
        ("crop.carbon_credit", -500, 2000, "Carbon credit per ha-yr for NPV = 0"),
    ])


def scenarios(v):
    return [
        ("Agave on semi-arid land, ethanol to alcohol-to-jet", AGAVE),
        ("Pongamia with carbon credits ($100/ha-yr)", {"crop.carbon_credit": 100}),
        ("Pongamia at Terviva-level oil yield (3 t/ha)", {"crop.feed_yield": 3.0}),
        *e.common_scenarios(),
    ]
