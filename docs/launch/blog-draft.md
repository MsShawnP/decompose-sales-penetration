# The one your dashboard isn't showing you

*Launch/reveal post for Decompose (Cinderhaven sales-penetration tool #3). Draft — Shawn copy pass pending. Placement: lailara-website blog, as the payoff to the live "Penetration Means Three Things" post.*

---

Sales went up 4%. The board is pleased. Nobody in the room can tell you why, and the dashboard on the wall can't either — because the dashboard is measuring the wrong kind of penetration.

"Penetration" means three different things, and a scan-data dashboard shows you two of them: how many stores carry you, and how much shelf you hold. The third meaning — the share of *households* that actually bought you — is the one that predicts whether this year's growth survives into next year. It needs panel data, not scan data, which is why most brands never see it.

Decompose shows it. And then it does something more useful: it splits your sales change into the only three things that can move it.

## Sales is a product of three levers

$$\text{Sales} = \text{buying households} \times \text{purchase frequency} \times \text{spend per trip}$$

More households buy you. Your buyers come back more often. Or they spend more each trip. That's the whole list. Every sales change — up or down — is some combination of those three, and nothing else.

Decompose takes two periods, computes each lever for both, and bridges the gap between them with a waterfall that reconciles *exactly* to the sales change. Not approximately. The three bars sum to the dollar delta, because the attribution is an exact Shapley decomposition — each lever gets credited its average marginal effect across every order the three changes could have happened in. No interaction term hides in a rounding gap.

## Growth that's actually erosion

Here is the Cinderhaven demo brand, comparing its two most recent like quarters. Sales are *up* $1,954. Good news, on the surface.

The waterfall says otherwise:

- **Buying households: −$2,459.** Fewer households bought the brand at all. Penetration fell 2.2 points.
- **Purchase frequency: −$3,597.** The households who stayed came back less often.
- **Spend per trip: +$8,010.** Prices went up, and the buyers who remained absorbed it.

Two levers are bleeding. One lever — price — is carrying the entire number and then some. Sales rose, but the brand is being held up by a smaller, more loyal, higher-spending core while its base quietly shrinks. That is not growth. That is erosion wearing growth's clothes, and it is exactly the pattern a scan-data dashboard reports as a good quarter.

The verdict Decompose writes for that comparison, in plain language a CFO can't misread: *"Sales rose $1,954 from 2024-Q4 to 2025-Q4, driven mainly by higher spend per trip."* Drive the same number with new households instead of price, and the verdict — computed from the data, never scripted — reads differently.

## Which lever do you pull next

The tool doesn't stop at what happened. Underneath the waterfall it shows the household flow behind the penetration number — new, retained, and lapsed buyers, quarter over quarter — so you can see whether you're replacing the households you lose or just squeezing the ones who stay. When price is doing all the work, that's the tell that the next move isn't another price increase; it's winning households back before the base gets too small to hold the number up.

## Honest by construction

The Cinderhaven data is synthetic — a stand-in ~$25M specialty food brand. The *method* is real, and so is the discipline behind it: the erosion window in the demo isn't scripted in. The panel is generated with realistic mechanics (prices rise, price-sensitive households buy less, some lapse), and the decline is then *computed* from the resulting transactions. The tool finds the story; it doesn't assert it. Point it at a period where new households drove the gain and it will say so instead.

That's the point of decomposing penetration into three levers: it takes "sales moved" — which tells you nothing — and turns it into "sales moved *because of this*, so pull *that*." The dashboard was never going to show you which one. This does.

---

*Decompose is tool #3 in the Cinderhaven sales-penetration series (Door Math · Spin Rate · **Decompose** · Leaky Bucket · Void Finder). Built on synthetic data; methodology and deliverables are real.*
