import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_tea import load_project_params  # noqa: E402
from tea import saf_engine as e, saf_htl, saf_msw_ft, saf_pongamia  # noqa: E402
from tea.finance import crf  # noqa: E402
from tea.inputs import base_values  # noqa: E402


def load(project):
    return base_values(load_project_params(ROOT / "inputs" / f"{project}.toml"))


@pytest.fixture
def msw():
    return load("saf_msw_ft")


def test_include_merges_market_inputs(msw):
    assert msw["market.jet_price"] == 735 and msw["finance.eur_usd"] == 1.15


def test_premium_path_and_floor(msw):
    p0, d = msw["market.saf_premium_2025"], msw["market.premium_decline"]
    assert e.saf_premium(msw, 1) == pytest.approx(p0 * (1 - d) ** 2)  # model year 1 = 2027
    assert e.year_of(msw, 2035) == 9
    assert e.saf_premium(msw, 60) == msw["market.premium_floor"]
    assert e.saf_premium({**msw, "market.premium_floor": 5000}, 60) == p0  # floor never exceeds today's premium


def test_msp_by_hand(msw):
    v = {**msw, "plant.life": 20, "finance.company_discount_rate": 0.10}

    def plant(v_, age):
        on = 1 <= age <= 20
        return {"saf": 10.0 if on else 0.0, "saf_rcf": 0.0, "coproduct": 0.0, "revenue": {},
                "opex": {}, "capex": 1000.0 if age == 0 else 0.0}
    # capex at t=1 (age 0), fuel in t=2..21: MSP = 1000 * 1.1 / (10 * annuity factor)
    annuity = sum(1.1 ** -(a + 1) for a in range(1, 21))
    assert e.msp(v, plant) == pytest.approx(1000 * 1.1 ** -1 / (10 * annuity))


def test_msw_mass_balance_by_hand(msw):
    mb = saf_msw_ft.mass_balance(msw)
    residue = 500_000 * (1 - 0.12 - 0.30)
    assert mb["residue"] == pytest.approx(residue)
    assert mb["liquids"] == pytest.approx(residue * 0.8 * 0.20)
    assert mb["saf_range"] == pytest.approx(residue * 0.8 * 0.20 * 0.70)


def test_unsorted_feeds_everything_at_lower_availability(msw):
    v = {**msw, "sort.enabled": 0}
    mb = saf_msw_ft.mass_balance(v)
    assert mb["recyclables"] == mb["organics"] == 0
    assert saf_msw_ft.availability(v) == msw["ft.availability_unsorted"]
    assert e.msp(v, saf_msw_ft.plant_year) > e.msp(msw, saf_msw_ft.plant_year)


def test_biogenic_split(msw):
    f = saf_msw_ft.plant_year(msw, 2)
    assert f["saf"] / (f["saf"] + f["saf_rcf"]) == pytest.approx(msw["ft.biogenic_share"])


def test_fleet_and_learning(msw):
    r = saf_msw_ft.run(msw)
    b = -math.log2(1 - msw["learning.rate_capex"])
    assert r.learning["plant capex"][0] == pytest.approx(8 ** b)
    total_capex = sum(y.capex for y in r.years)
    noak_capex = saf_msw_ft.mass_balance(msw)["dry"] * msw["ft.capex_per_dry_t"]
    assert total_capex > msw["plant.schedule"][-1] * noak_capex  # learning premium on early plants


def test_tail_only_adds_operating_cash(msw):
    with_tail = saf_msw_ft.run(msw).npv
    horizon_only = saf_msw_ft.run({**msw, "plant.count_remaining_life": 0}).npv
    assert with_tail > horizon_only


def test_htl_mass_balance_by_hand():
    v = load("saf_htl")
    mb = saf_htl.mass_balance(v)
    assert mb["fuel"] == pytest.approx(300_000 * 0.25 * 0.40 * 0.80)
    assert saf_htl.plant_year(v, 2)["saf_rcf"] == 0


def test_pongamia_yield_ramp():
    v = load("saf_pongamia")
    assert saf_pongamia.yield_factor(v, 2) == 0
    assert saf_pongamia.yield_factor(v, 3) == pytest.approx(0.2)
    assert saf_pongamia.yield_factor(v, 5) == pytest.approx(0.2 + 0.8 * 2 / 4)
    assert saf_pongamia.yield_factor(v, 7) == 1.0
    f = saf_pongamia.plant_year(v, 8)
    assert f["saf"] == pytest.approx(30_000 * 2.0 * 0.83 * 0.60)


def test_pongamia_capex_timing():
    v = load("saf_pongamia")
    est = saf_pongamia.plant_year(v, 0)["capex"]
    conv = saf_pongamia.plant_year(v, 2)["capex"]
    assert est == pytest.approx(30_000 * 3000)
    assert conv == pytest.approx(30_000 * 2.0 * 0.83 * 2400)


def test_agave_yields_more_saf_per_ha():
    v = load("saf_pongamia")
    a = {**v, **saf_pongamia.AGAVE}
    per_ha = lambda x: saf_pongamia.mass_balance(x)["saf_range"] / x["crop.area_ha"]  # noqa: E731
    assert per_ha(a) == pytest.approx(5.85 * 0.60 * 0.83)
    assert per_ha(a) > per_ha(v)


def test_crf_consistency():
    assert crf(0.10, 25) == pytest.approx(0.10 / (1 - 1.10 ** -25))


def test_construction_years_before_output(msw):
    total = saf_msw_ft.mass_balance(msw)["dry"] * msw["ft.capex_per_dry_t"]
    y0, y1, y2 = (saf_msw_ft.plant_year(msw, a) for a in (0, 1, 2))
    assert y0["capex"] == pytest.approx(total / 2) and y1["capex"] == pytest.approx(total / 2)
    assert y0["saf"] == y1["saf"] == 0 and sum(y0["opex"].values()) == 0
    assert y2["capex"] == 0 and y2["saf"] > 0
    assert saf_msw_ft.plant_year(msw, 3)["saf"] == pytest.approx(y2["saf"] / msw["plant.first_year_factor"])
