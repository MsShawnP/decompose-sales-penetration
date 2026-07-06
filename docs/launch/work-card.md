# Work-page card — Decompose

*Draft for the lailarallc.com /work page, Door Math / Spin Rate card format. Shawn copy pass + placement pending. Live URL goes in once deployed.*

---

**Decompose**
*Household penetration decomposition · Cinderhaven series #3*

Splits a brand's period-over-period sales change into the only three levers that can move it — buying households × purchase frequency × spend per trip — and reconciles them exactly to the sales delta with a Shapley waterfall. Then it says, in plain language, which lever moved the number and whether the growth is real or erosion in disguise.

- **Household penetration** — the *How Brands Grow* metric most POS dashboards can't show, because it needs panel data, not scan data.
- **Three-lever waterfall** — bridges Period A sales to Period B; the three bars sum to the exact dollar change, no interaction term hiding in a gap.
- **Buyer flow + verdict** — new/retained/lapsed households behind the number, and a board-ready sentence computed from the data, never scripted.

**Stack:** Python · Dash · Plotly · pandas · Gunicorn/Docker/Fly.io. Data is an in-process, seed-locked synthetic household panel — no database, shared with tool #4.

**Live:** https://decompose.lailarallc.com

---

*Card fields to confirm with Shawn: exact tagline, whether to show the "growth that's actually erosion" hook line, and thumbnail (suggest the three-lever waterfall showing the erosion bridge).*
