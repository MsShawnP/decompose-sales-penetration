"""Canonical / locked-constant tests for the household panel.

Mirrors the cinderhaven-store-universe test_canonical.py pattern. Grows with each
Slice 1 sub-task; this file currently covers A1 (constants + calendar).
"""

import pandas as pd

import cinderhaven_household_panel as hp


class TestConstants:
    def test_seed_locked(self):
        assert hp.SEED == 42

    def test_household_count_locked(self):
        assert hp.N_HOUSEHOLDS == 5000

    def test_quarter_split_locked(self):
        assert hp.BURN_IN_QUARTERS == 4
        assert hp.ANALYSIS_QUARTERS == 8
        assert hp.TOTAL_QUARTERS == 12

    def test_panel_version_set(self):
        assert isinstance(hp.PANEL_VERSION, str) and hp.PANEL_VERSION

    def test_canonical_universe_reused(self):
        # Reused from the SSOT — must match the canonical universe exactly.
        assert len(hp.ALL_SKUS) == 50
        assert set(hp.PRODUCT_LINES.keys()) == {"AS", "PS", "SC", "DG", "SB"}
        assert len(hp.RETAILERS) == 6
        assert hp.DEMO_AS_OF_DATE == pd.Timestamp("2025-12-29")


class TestCalendar:
    def test_twelve_quarters(self):
        q = hp.get_quarters()
        assert len(q) == 12
        assert q["quarter_index"].tolist() == list(range(12))

    def test_burn_in_then_analysis(self):
        q = hp.get_quarters()
        assert (q["phase"] == "burn_in").sum() == 4
        assert (q["phase"] == "analysis").sum() == 8
        # burn-in strictly precedes the analysis window
        assert q.loc[q["is_analysis"], "quarter_index"].min() == 4

    def test_labels_and_pos_alignment(self):
        q = hp.get_quarters()
        assert q["label"].iloc[0] == "2023-Q1"
        assert q["label"].iloc[-1] == "2025-Q4"
        # analysis window aligns to the store-universe POS window (2024-2025)
        analysis = q[q["is_analysis"]]
        assert analysis["label"].iloc[0] == "2024-Q1"
        assert analysis["label"].iloc[-1] == "2025-Q4"
        assert hp.ANALYSIS_QUARTER_LABELS[0] == "2024-Q1"
        assert hp.BURN_IN_QUARTER_LABELS == ["2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4"]

    def test_dates_contiguous_and_non_overlapping(self):
        q = hp.get_quarters().sort_values("quarter_index").reset_index(drop=True)
        for i in range(len(q)):
            assert q.loc[i, "start_date"] < q.loc[i, "end_date"]
            if i > 0:
                # each quarter starts the day after the previous one ends
                assert q.loc[i, "start_date"] == q.loc[i - 1, "end_date"] + pd.Timedelta(days=1)

    def test_reproducible(self):
        pd.testing.assert_frame_equal(hp.get_quarters(), hp.get_quarters())


class TestHouseholds:
    def test_count_locked(self):
        assert len(hp.get_households()) == 5000

    def test_reproducible(self):
        pd.testing.assert_frame_equal(hp.get_households(), hp.get_households())

    def test_regions_are_canonical(self):
        h = hp.get_households()
        assert set(h["region"]) == set(hp.REGIONS)

    def test_latent_attrs_in_unit_range(self):
        h = hp.get_households()
        for col in ("price_sensitivity", "innovator_affinity"):
            assert h[col].between(0.0, 1.0).all(), f"{col} outside [0,1]"

    def test_propensity_right_skewed_and_overdispersed(self):
        x = hp.get_households()["base_propensity"].to_numpy()
        assert (x >= 0).all()
        m, s = x.mean(), x.std()
        skew = (((x - m) / s) ** 3).mean()  # Fisher-Pearson sample skewness
        assert skew > 1.0, f"propensity skew {skew:.2f} not right-skewed enough"
        assert x.var() / x.mean() > 1.0, "propensity should be overdispersed"

    def test_ids_unique_and_formatted(self):
        h = hp.get_households()
        assert h["household_id"].is_unique
        assert h["household_id"].iloc[0] == "HH-00001"
        assert h["household_id"].iloc[-1] == "HH-05000"
