# RWA Mint/Redeem Vault Auditing

_Field lens distilled from a real authorized audit (Midas — Sherlock always-on, RWA mint/redeem). Sibling to [DeFi Vault & Share-Price Auditing](./DeFi%20Vault%20%26%20Share-Price%20Auditing.md). For AUTHORIZED testing + responsible disclosure only. This was a **hardened, no-finding** review — the value here is the lens and the disqualifiers, not an exploit._

**Scope shape:** tokenized real-world-asset systems where users `mint` a yield-bearing token against a stablecoin/RWA and `redeem` back, priced by an admin/oracle NAV (mTBILL/mBASIS-style). Maps to ERC-4626-adjacent accounting + oracle + role design.

---

## The 60-second disqualifier (run FIRST — same question as the vault playbook, RWA variant)

> **"Is the redeem/share price derived from a token *balance*, or *pushed* by an admin/oracle?"**

- **Balance-derived** → the inflation / donation / first-depositor class is LIVE (see the vault playbook). Dig here.
- **Admin/oracle-pushed NAV** → **the entire inflation class is DEAD.** The dreUSD-M2 / Enzyme inflation surface does not apply. In Midas the NAV came from a `CustomAggregatorV3CompatibleFeed` (feed admins post the price; `*Growth` variants add bounded linear interest between rounds), wrapped by a `DataFeed` that enforces Chainlink staleness (`healthyDiff`) + `[minExpectedAnswer, maxExpectedAnswer]` bounds on every read. No user manipulation path → move EV elsewhere.

If NAV is pushed, the inflation lane is closed. Spend your hours on the **flow math**, not the price.

## Where the bugs actually live in mint/redeem RWA (ranked by EV)

1. **Redeem/deposit flow math — instant vs request.** The `amountOut = amountMTokenWithoutFee × mTokenRate / tokenOutRate` (and inverse) is where rounding, fee order, and slippage interact. Check:
   - **`minReceiveAmount` slippage guard** enforced on the *actually-delivered* amount (not a pre-fee figure).
   - **Request flow rate-lock:** rates stored at request time, admin approves at a new rate — is the move bounded by a `variationTolerance`? Is the non-`safe` `approveRequest` `onlyAdmin` (trusted = out of scope) vs a `safe*` path that bounds the rate delta?
   - **Batch approval** that skips under-funded requests (`_validateLiquidity`) without reverting the whole batch — does the skip leak value or double-count limits?
2. **Integration variants = freshest code = best odds.** `RedemptionVaultWith{Swapper,BUIDL,Aave,Morpho,USTB}` / `DepositVaultWith{...}`. These wrap an external protocol — audit the **external-call assumptions**: slippage, who bears the loss, reentrancy across the external call (is `tokenOut` transfer last?), and conservation at oracle rates. The *Swapper* fallback (swap net mToken1→mToken2 via a trusted LP, redeem through a second vault) is the novel surface: confirm the inner redeem enforces the **same `minReceiveAmount`** so the fallback can't silently deliver below the user's floor.
3. **Decimal/rounding drain.** Look for a **strict round-trip equality** guard (`require(amount == convertFromBase18(amount).convertToBase18())`, "invalid rounding") — a system that *reverts* rather than silently dropping dust has no rounding-drain surface. Its absence is the bug; its presence is a closed lane.
4. **Stablecoin 1:1 shortcuts.** A hardcoded `STABLECOIN_RATE = 1e18` is only safe if the code *still* calls the feed health + min/max peg check first (reverts on a hard depeg out of bounds) before returning 1:1. A 1:1 that skips the feed entirely is a depeg-mispricing finding.
5. **Limits & allowances.** Daily instant limit + per-token allowance (`MAX_UINT` = unlimited) + greenlist/blacklist/sanctions gating — check the *update* order vs the transfer (TOCTOU), and whether gross vs net is limited consistently.

## What "good" looks like (if you see ALL of these, the core is likely clean — bank it as no-finding)
- NAV is admin/oracle-pushed with staleness + min/max bounds and `onlyUp`/`maxAnswerDeviation` on writes.
- Mint/burn is role-gated to the vaults; token is pausable + blacklist-gated on transfer.
- Fee is floor-division, capped at 100%, waived-accounts → 0; conversion reverts on rounding mismatch.
- Request flows lock rates and bound the admin re-price by a tolerance; `tokenOut` transfer is last.
- Swapper/integration fallbacks propagate the user's `minReceiveAmount` and round in the user's favor.

## The trusted-roles = out-of-scope filter (carry over from the vault playbook)
Almost every "admin can set a bad rate / drain via privileged call" lead is **out of scope** — competitive-audit rules treat trusted roles as trusted. Before writing a finding on an `onlyAdmin` path, confirm the program's in-scope-roles list. The EV is in **permissionless** user-reachable paths only.

---
_Hardened-no-finding is a valid, reputation-preserving result. Score any confirmed finding with `bbkit.cvss` + `bbkit.severity` and write it up with `bbkit.report`._
