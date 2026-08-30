# BUG-002 — Verify rounding behavior on small/frequent claims (dust amounts)

- **Project:** Mexico Staking (MEX)
- **Environment:** devnet, `mexicoweb-dev.up.railway.app`
- **Found by:** QA smoke pass (spotted in a Network-tab / history screenshot, not part of the original checklists)
- **Date:** 2026-08-21
- **Severity:** Medium (pending verification — could escalate to High if over-payment is confirmed)
- **Priority:** P2 — should be verified and closed out before real funds are involved
- **Status:** Open — needs investigation, currently only a suspicion from observed data

## Summary

The operations history shows multiple small, fractional claims on the same
day (e.g. `+0.001`, `+0.005` MEX). This is not itself a confirmed bug, but a
signal that rounding behavior on small reward amounts needs to be explicitly
verified. Two failure modes are possible and both need to be checked:

1. **Over-payment:** claiming very frequently in small increments could pay
   out more in total than the reward formula would produce for a single
   claim over the same time window (e.g. if each claim rounds up, or if
   per-claim minimums/fees aren't applied consistently).
2. **Under-payment / lost dust:** a claim that computes to an amount that
   rounds down to zero (below the token's smallest representable unit, or
   below a UI-enforced minimum) could silently discard the accrued reward
   instead of carrying it forward to the next claim.

## Steps to Reproduce / Investigate

1. Stake the minimum amount at the minimum lock tier so accrual per unit
   time is as small as possible.
2. Perform several claims in rapid succession within the same day (e.g.
   every few minutes) instead of one claim at the end of the day.
3. Record each claimed amount and timestamp from the operations history.
4. Separately, let the same-size position accrue for the equivalent total
   elapsed time and perform a single claim.
5. Compare: `sum(frequent small claims)` vs `single claim over same duration`.
6. Additionally, force a scenario where accrued rewards since the last claim
   are smaller than the smallest representable MEX unit (or smaller than any
   UI-enforced minimum claim amount) and attempt to claim.

## Expected Result

- `sum(frequent small claims)` should equal `single claim over same
  duration)` within the smallest representable unit of MEX — frequent
  claiming must not be a way to extract more value than the reward formula
  intends.
- A claim whose computed amount rounds down to zero should either:
  - be rejected/blocked (no-op, no wasted transaction fee), with the
    unclaimed accrual preserved and included in the next claim, or
  - be prevented client-side with a clear "nothing to claim yet" state,
    consistent with the on-chain accounting.
- In no case should accrued rewards be silently zeroed out and lost when a
  claim's rounding produces a zero-transfer amount.

## Actual Result (to be filled in after investigation)

- [ ] Confirmed whether frequent small claims sum to more than a single
      equivalent-duration claim (over-payment).
- [ ] Confirmed whether a near-zero claim discards the accrued remainder
      instead of carrying it forward (lost accrual).
- [ ] Recorded the exact reward formula / rounding rule used on-chain
      (round down, round to nearest, truncate to N decimals, etc.).

## Impact

- If over-payment is confirmed: users could farm extra MEX simply by
  claiming very frequently, which directly undermines token economics and
  the (currently unenforced) supply/cap assumptions in the PRD.
- If under-payment/lost-dust is confirmed: users lose small amounts of
  legitimately accrued rewards, which is a fairness/trust issue even if the
  absolute amounts are small, and could compound at scale across many users
  and many claims.

## Suggested Fix (pending confirmation of which failure mode applies)

1. Document the exact rounding rule for reward calculation and claiming
   on-chain (e.g. always round down at the token's decimal precision, carry
   any remainder in the position's accrued-but-unclaimed counter rather than
   resetting it to zero on each claim).
2. Add an explicit on-chain/unit test comparing `N` frequent small claims
   against `1` claim over the same total duration for the same stake amount,
   asserting they are equal within one base unit.
3. Consider a minimum-claim-amount guard in the UI (with a matching program
   check) to avoid users paying network fees for near-zero claims, as long as
   the underlying accrual is preserved rather than discarded.

## Evidence

Reported from an operations-history screenshot shared during the QA smoke
pass (see QA chat log, 2026-08-21), showing `+0.001` and `+0.005` MEX claim
entries on the same day. Attach the original screenshot and, once available,
the on-chain transaction signatures for the claims in question.
