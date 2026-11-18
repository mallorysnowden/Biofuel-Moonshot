"""Shared engine for the SAF moonshot TEAs.

Every configuration is a fleet of identical plants sold into the same EU SAF
market, so results compare apples to apples. A configuration only supplies
`plant_year(v, age)`: one NOAK plant's physical and cash flows in its age-th year
(age 0 = the year it is built). The engine adds:

- the fleet build schedule and Wright's-law learning on capex by plant count,
- the SAF price path (fossil jet + a premium that shrinks over time),
- company overheads, cash flow, NPV, minimum selling price (MSP) and kill metrics.

plant_year returns a dict with:
    saf          t/yr SAF that counts toward ReFuelEU (biogenic)
    saf_rcf      t/yr SAF-range fuel from fossil carbon (recycled carbon fuel)
    coproduct    t/yr naphtha/diesel co-products
    revenue      {stream: $/yr} other revenue (gate fees, recyclables, meal, credits)
    opex         {item: $/yr} operating costs
    capex        $ spent this year at NOAK cost
"""
from __future__ import annotations

from typing import Callable

from .finance import irr, npv
from .framework.learning import cost_multiplier
from .framework.result import FunctionalUnit, KillMetric, StandardResult, YearRow

PlantYear = Callable[[dict, int], dict]


# --- market ------------------------------------------------------------------

def saf_premium(v, t: int) -> float:
    """SAF premium over fossil jet ($/t) in model year t (t = 1 is the first model year).

    The premium shrinks each year as supply catches up, but not below a floor set by the cost of
    the marginal supply the rising mandate still needs.
    """
    years_since_2025 = v["market.years_2025_to_year1"] + t - 1
    decayed = v["market.saf_premium_2025"] * (1 - v["market.premium_decline"]) ** years_since_2025
    return max(decayed, min(v["market.premium_floor"], v["market.saf_premium_2025"]))


def saf_price(v, t: int) -> float:
    return v["market.jet_price"] + saf_premium(v, t)


def year_of(v, calendar_year: int) -> int:
    return calendar_year - 2025 - int(v["market.years_2025_to_year1"]) + 1


def coproduct_price(v) -> float:
    return v["market.jet_price"] * v["market.coproduct_factor"]


# --- plant economics -----------------------------------------------------------

def plant_cash(v, f: dict, t: int, capex_mult: float) -> tuple[dict, float, float]:
    """(revenue by stream, operating cost, capex) for one plant-year."""
    rev = {"saf": f["saf"] * saf_price(v, t)
                  + f["saf_rcf"] * (v["market.jet_price"] + v["policy.rcf_credit"] * saf_premium(v, t)),
           "coproducts": f["coproduct"] * coproduct_price(v)}
    for k, x in f["revenue"].items():
        rev[k] = rev.get(k, 0.0) + x
    return rev, sum(f["opex"].values()), f["capex"] * capex_mult


def msp(v, plant_year: PlantYear, capex_mult: float = 1.0) -> float:
    """Levelized SAF price ($/t, all SAF-range fuel) at which one plant breaks even over its life.

    Co-products are credited at the co-product price and other revenue (gate fees, recyclables,
    meal, credits) is credited as earned.
    """
    r = v["finance.company_discount_rate"]
    life = int(v["plant.life"]) + int(v.get("plant.build_years", 0))
    cost_pv = fuel_pv = 0.0
    for age in range(life + 1):
        f = plant_year(v, age)
        d = (1 + r) ** -(age + 1)
        credits = f["coproduct"] * coproduct_price(v) + sum(f["revenue"].values())
        cost_pv += d * (f["capex"] * capex_mult + sum(f["opex"].values()) - credits)
        fuel_pv += d * (f["saf"] + f["saf_rcf"])
    return cost_pv / fuel_pv if fuel_pv else float("inf")


def mature(v, plant_year: PlantYear) -> dict:
    return plant_year(v, int(v["plant.mature_age"]))


def abatement_cost(v, price: float, saving: float) -> float:
    """$/t CO2e avoided by a fuel at `price` that cuts life-cycle emissions by `saving` vs fossil jet."""
    avoided = v["ghg.fossil_jet"] * saving
    return (price - v["market.jet_price"]) / avoided if avoided else float("inf")


# --- company model -------------------------------------------------------------

def run(v, plant_year: PlantYear, project: str, extra_kills: list[KillMetric] | None = None,
        notes: list[str] | None = None, tables: list | None = None) -> StandardResult:
    horizon = int(v["finance.horizon"])
    rd = int(round(v["company.rd_years"]))
    sched = v["plant.schedule"]  # cumulative plants started by commercial year
    rate = v["finance.company_discount_rate"]
    noak_exp, lr = v["learning.noak_experience"], v["learning.rate_capex"]
    first_exp = v["learning.first_year_experience"]

    plants: list[tuple[int, float]] = []  # (build year, capex multiplier)
    rows: list[YearRow] = []
    cumulative = learning_investment = 0.0
    noak_year = None
    for t in range(1, horizon + 1):
        k = t - rd
        target = sched[min(k, len(sched)) - 1] if k >= 1 else 0
        while len(plants) < target:
            n = len(plants)  # plants already built
            mult = cost_multiplier(first_exp + n, noak_exp, 1.0, lr)
            plants.append((t, mult))
            if noak_year is None and first_exp + n >= noak_exp:
                noak_year = t
        streams: dict[str, float] = {}
        opex = capex = 0.0
        for built, mult in plants:
            f = plant_year(v, t - built)
            rev, op, cx = plant_cash(v, f, t, mult)
            for s, x in rev.items():
                streams[s] = streams.get(s, 0.0) + x
            opex += op
            capex += cx
            learning_investment += f["capex"] * (mult - 1)
        revenue = sum(streams.values())
        phase = "R&D" if k < 1 else "commercial"
        overhead = v["company.rd_opex"] if phase == "R&D" else v["company.corporate_opex"] + revenue * v["company.ga_share"]
        gross = revenue - opex
        ebit = gross - overhead
        cumulative += ebit - capex
        newest = plants[-1][1] if plants else cost_multiplier(first_exp, noak_exp, 1.0, lr)
        rows.append(YearRow(t, phase, revenue, opex, gross, overhead, ebit, cumulative, newest, streams, capex))

    cash = [r.ebit - r.capex for r in rows]
    # Plants keep running after the horizon; count their remaining operating cash (no new builds).
    tail = []
    if v.get("plant.count_remaining_life", 1):
        for t in range(horizon + 1, horizon + int(v["plant.life"]) + int(v.get("plant.build_years", 0)) + 1):
            rev_t = op_t = 0.0
            for built, mult in plants:
                rev, op, _ = plant_cash(v, plant_year(v, t - built), t, mult)
                rev_t += sum(rev.values())
                op_t += op
            c = rev_t - op_t - v["company.corporate_opex"] - rev_t * v["company.ga_share"]
            if c <= 0:  # same rule in all three finalist TEAs: stop when cash turns negative
                break
            tail.append(c)
    npv_horizon = npv(rate, cash)
    went_negative, breakeven_year = False, None
    for r in rows:
        if r.cumulative_cash < 0:
            went_negative = True
        elif went_negative and breakeven_year is None:
            breakeven_year = r.year

    m_noak = msp(v, plant_year)
    foak_mult = cost_multiplier(first_exp, noak_exp, 1.0, lr)
    m_foak = msp(v, plant_year, foak_mult)
    hefa = v["market.hefa_price"]
    p2035 = saf_price(v, year_of(v, 2035))
    saving = v["ghg.saving"]
    fus = [
        FunctionalUnit(
            "SAF supply cost (levelized over plant life)", "$/t fuel",
            {"Ours at NOAK (MSP)": m_noak, "Ours, first plant (FOAK MSP)": m_foak,
             "HEFA SAF market price (incumbent SAF)": hefa,
             "Projected SAF price in 2035 (this model)": p2035,
             "Fossil jet": v["market.jet_price"],
             "Fossil jet + ReFuelEU penalty": v["market.jet_price"] + v["market.penalty_multiple"] * (hefa - v["market.jet_price"])},
            "MSP credits co-products and other revenue. The penalty is at least twice the SAF-jet price gap per tonne missed.",
        ),
        FunctionalUnit(
            "Cost of CO2e avoided", "$/t CO2e",
            {"Ours at NOAK": abatement_cost(v, m_noak, saving),
             "HEFA SAF at market price": abatement_cost(v, hefa, v["ghg.saving_hefa"])},
            "Price premium over fossil jet divided by life-cycle CO2e avoided per tonne.",
        ),
    ]
    big = v["scale.big_enough_revenue"]
    kills = [
        KillMetric("NOAK MSP vs HEFA SAF price", m_noak / hefa, 1.0, "x (<=1 to win)", m_noak <= hefa,
                   "Must undercut the incumbent SAF, not fossil jet"),
        KillMetric("NOAK MSP vs projected 2035 SAF price", m_noak / p2035, 1.0, "x (<=1 to win)", m_noak <= p2035,
                   "The premium shrinks over time in this model"),
        KillMetric("Cost of CO2e avoided at NOAK", abatement_cost(v, m_noak, saving), 300.0, "$/t (<=300)",
                   abatement_cost(v, m_noak, saving) <= 300.0, "300 $/t threshold is a judgment"),
        *(extra_kills or []),
        KillMetric("Revenue at full scale vs big-enough line", rows[-1].revenue / big, 1.0, "x", rows[-1].revenue >= big),
    ]
    mat = mature(v, plant_year)
    fleet_saf = sum(mature(v, plant_year)["saf"] + mature(v, plant_year)["saf_rcf"] for _ in plants)
    mandate_2035 = v["market.eu_jet_demand"] * v["market.mandate_2035"]
    base_notes = [
        f"Market check: {len(plants)} plants at maturity make {fleet_saf / 1e3:,.0f} kt/yr of SAF-range fuel, "
        f"{fleet_saf / mandate_2035:.1%} of the ~{mandate_2035 / 1e6:.1f} Mt/yr the EU mandate requires in 2035.",
        f"One mature plant: {(mat['saf'] + mat['saf_rcf']) / 1e3:,.1f} kt/yr SAF-range fuel "
        f"({mat['saf_rcf'] / max(mat['saf'] + mat['saf_rcf'], 1):.0%} from fossil carbon), {mat['coproduct'] / 1e3:,.1f} kt/yr co-products.",
        f"SAF price path: premium over jet ${saf_premium(v, 1):,.0f}/t in model year 1 (2027), "
        f"${saf_premium(v, year_of(v, 2035)):,.0f}/t in 2035, ${saf_premium(v, horizon):,.0f}/t in year {horizon}.",
        f"NPV and IRR include the remaining-life operating cash of plants built within the {horizon}-yr horizon "
        f"(no new builds after it) while it stays positive; {len(tail)} tail years counted. "
        f"NPV over the horizon alone: ${npv_horizon / 1e6:,.0f}M.",
        "Pre-tax, real 2026 USD; operating profit is before depreciation.",
    ]
    return StandardResult(
        project=project,
        years=rows,
        npv=npv(rate, cash + tail),
        irr=irr(cash + tail),
        peak_cash_need=-min(0.0, min(r.cumulative_cash for r in rows)),
        breakeven_year=breakeven_year,
        full_scale_revenue=rows[-1].revenue,
        functional_units=fus,
        learning={"plant capex": (foak_mult, 1.0)},
        noak_year=noak_year,
        learning_investment=learning_investment,
        kill_metrics=kills,
        notes=(notes or []) + base_notes,
        tables=tables or [],
    )


def common_breakevens(v, run_fn, extra: list[tuple[str, float, float, str]]) -> list[dict]:
    from .framework.uncertainty import breakeven
    npv_of = lambda x: run_fn(x).npv  # noqa: E731
    items = [("market.premium_decline", -0.05, 0.5, "Annual decline in SAF premium for NPV = 0"),
             ("market.premium_floor", 0, 3000, "Long-run SAF premium floor ($/t) for NPV = 0")] + extra
    return [{"question": label, "input": key, "answer": breakeven(v, key, npv_of, 0.0, lo, hi), "base": v[key]}
            for key, lo, hi, label in items]


def common_scenarios() -> list[tuple[str, dict]]:
    return [
        ("SAF premium holds at today's level", {"market.premium_decline": 0.0}),
        ("SAF premium falls 8%/yr", {"market.premium_decline": 0.08}),
    ]
