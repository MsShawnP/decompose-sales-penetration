"""Three-lever decomposition math (Slice 2).

Decomposes a period-over-period sales change into the only three things that can move
it — buying households x purchase frequency x spend per trip — and produces a
plain-language "which lever" verdict.

The attribution is an exact **Shapley** decomposition: each lever's contribution is
its average marginal effect over all orderings of the three changes. For three
multiplicative factors the contributions sum EXACTLY to the sales delta (Shapley
efficiency), which is the reconciliation guarantee the whole tool rests on. Shapley is
used instead of single-order sequential substitution because the latter is
order-dependent (whichever lever is applied first absorbs the interaction terms),
which would mislead the verdict.

All inputs come from the panel's ``get_period_metrics`` — nothing is invented here.
"""

from dataclasses import dataclass

from cinderhaven_household_panel import get_period_metrics

LEVERS = ("buying_households", "frequency", "spend_per_trip")

# Direction-aware plain-language phrases for each lever, keyed by (lever, went_up).
_LEVER_PHRASES = {
    ("buying_households", True): "more households buying the brand",
    ("buying_households", False): "fewer households buying the brand",
    ("frequency", True): "buyers shopping more often",
    ("frequency", False): "buyers shopping less often",
    ("spend_per_trip", True): "higher spend per trip",
    ("spend_per_trip", False): "lower spend per trip",
}


def _lever_phrase(lever: str, contribution: float) -> str:
    return _LEVER_PHRASES[(lever, contribution >= 0)]
# Default: a lever must account for at least this share of the total gross movement to
# be named the single driver; otherwise the verdict hedges ("mixed").
DEFAULT_DOMINANCE_THRESHOLD = 0.5


@dataclass(frozen=True)
class Waterfall:
    period_a: str
    period_b: str
    sales_a: float
    sales_b: float
    delta: float
    contributions: dict          # lever -> $ contribution to the delta (sum == delta)
    product_line: str | None = None
    retailer_id: str | None = None

    @property
    def reconciles(self) -> bool:
        return abs(sum(self.contributions.values()) - self.delta) <= 1e-6


def _shapley_three_factor(a0, b0, c0, a1, b1, c1):
    """Exact Shapley contributions of A, B, C to the change in the product A*B*C.

    Coalition weights for n=3: empty/full sets weight 1/3, singletons 1/6.
    """
    da, db, dc = a1 - a0, b1 - b0, c1 - c0
    phi_a = (1 / 3) * da * b0 * c0 + (1 / 6) * da * b1 * c0 + (1 / 6) * da * b0 * c1 + (1 / 3) * da * b1 * c1
    phi_b = (1 / 3) * a0 * db * c0 + (1 / 6) * a1 * db * c0 + (1 / 6) * a0 * db * c1 + (1 / 3) * a1 * db * c1
    phi_c = (1 / 3) * a0 * b0 * dc + (1 / 6) * a1 * b0 * dc + (1 / 6) * a0 * b1 * dc + (1 / 3) * a1 * b1 * dc
    return phi_a, phi_b, phi_c


def three_lever_waterfall(period_a: str, period_b: str,
                          product_line=None, retailer_id=None) -> Waterfall:
    """Bridge sales from period_a to period_b across the three levers (exact)."""
    m = get_period_metrics(product_line, retailer_id).set_index("quarter_label")
    if period_a not in m.index or period_b not in m.index:
        raise KeyError(f"unknown period(s): {period_a!r}, {period_b!r}")
    a, b = m.loc[period_a], m.loc[period_b]
    phi_h, phi_f, phi_s = _shapley_three_factor(
        a["buying_households"], a["frequency"], a["spend_per_trip"],
        b["buying_households"], b["frequency"], b["spend_per_trip"],
    )
    sales_a = a["buying_households"] * a["frequency"] * a["spend_per_trip"]
    sales_b = b["buying_households"] * b["frequency"] * b["spend_per_trip"]
    return Waterfall(
        period_a=period_a,
        period_b=period_b,
        sales_a=float(sales_a),
        sales_b=float(sales_b),
        delta=float(sales_b - sales_a),
        contributions={
            "buying_households": float(phi_h),
            "frequency": float(phi_f),
            "spend_per_trip": float(phi_s),
        },
        product_line=product_line,
        retailer_id=retailer_id,
    )


def which_lever_verdict(wf: Waterfall, threshold: float = DEFAULT_DOMINANCE_THRESHOLD) -> dict:
    """Plain-language verdict naming the driving lever, or hedging when none dominates.

    Dominance is share of GROSS movement (sum of absolute contributions), so two
    levers that fight (one up, one down) don't manufacture a false "winner".
    """
    contribs = wf.contributions
    gross = sum(abs(v) for v in contribs.values())
    shares = {k: (abs(v) / gross if gross else 0.0) for k, v in contribs.items()}

    # Nothing moved (e.g. period_a == period_b): every contribution is exactly zero,
    # so gross == 0. Return a neutral verdict rather than falling through to the
    # "mixed" branch, which would falsely claim levers rose (a 0.0 contribution maps
    # to the "up" phrase and delta >= 0 reads as "rose").
    if gross == 0:
        return {
            "headline_lever": "none",
            "direction": "flat",
            "dominant": False,
            "shares": shares,
            "contributions": contribs,
            "sentence": f"Sales were unchanged between {wf.period_a} and {wf.period_b}.",
        }

    ranked = sorted(contribs, key=lambda k: abs(contribs[k]), reverse=True)
    top = ranked[0]

    dominant = gross > 0 and shares[top] >= threshold
    direction = "up" if wf.delta >= 0 else "down"
    moved = "rose" if wf.delta >= 0 else "fell"
    amount = f"${abs(wf.delta):,.0f}"

    if dominant:
        phrase = _lever_phrase(top, contribs[top])
        sentence = (
            f"Sales {moved} {amount} from {wf.period_a} to {wf.period_b}, "
            f"driven mainly by {phrase}."
        )
        headline = top
    else:
        a, b = ranked[0], ranked[1]
        sentence = (
            f"Sales {moved} {amount} from {wf.period_a} to {wf.period_b}, "
            f"with no single dominant lever — {_lever_phrase(a, contribs[a])} "
            f"and {_lever_phrase(b, contribs[b])} together."
        )
        headline = "mixed"

    return {
        "headline_lever": headline,
        "direction": direction,
        "dominant": dominant,
        "shares": shares,
        "contributions": contribs,
        "sentence": sentence,
    }
