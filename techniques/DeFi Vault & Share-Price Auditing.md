# DeFi Vault & Share-Price Auditing

_Field playbook distilled from real authorized audits on the [Bug-Bounty-Knowledge](https://github.com/IsaiahDupree/Bug-Bounty-Knowledge) shelf: Polymarket V2 (Cantina), dreUSD (Sherlock — 2 confirmed Mediums), Veda boring-vault (Immunefi), Enzyme Onyx (Immunefi). For AUTHORIZED testing + responsible disclosure only._

**Scope:** ERC-4626 / ERC-7540 vaults, yield/rewards distributors, share-price accounting, fee handlers, cross-chain custody. Maps to OWASP Smart Contract Top 10, SWC, and Immunefi impact tiers.

---

## The 60-second disqualifier (run this FIRST on any vault)

> **"Is there a permissionless code path that turns a token *balance* into stored *share price*?"**

- **YES** → the inflation / donation / first-depositor class is LIVE. Dig here first. This is where dreUSD M-2 lived (`totalAssets()` summed vested rewards with `_decimalsOffset()==0`, so a 1-wei attacker could inflate and round a victim's deposit to 0 shares).
- **NO (NAV is admin-pushed / handler-gated)** → the entire inflation class is DEAD. A token donation just inflates NAV equally for all holders → donor subsidizes everyone → net loss, not an attack. Move EV elsewhere. This is what made Enzyme Onyx and Veda "hardened — no finding": `ValuationHandler` share value is set only by `onlyAdminOrOwner` (`updateShareValue` / `setAssetRatesThenUpdateShareValue`); `getSharePrice()` returns the stored value, never a live balance sum.

If you can't answer in 60 seconds, grep every state-mutating function that writes the share-price/exchange-rate storage var and list its access modifier. The answer falls out.

---

## What "good" looks like (defensive patterns — if you see ALL of these, the core is likely clean)

1. **Admin-pushed NAV, not live balance-derived** share price. Kills donation/inflation.
2. **All conversion math floors in the vault's favor** — deposits mint *fewer* shares, redeems pay *fewer* assets. Check every `mulDiv` / division rounding direction. (Veda: `+1` virtual offset in denominator, RAY-precision; Enzyme: every `ValueHelpersLib` fn floors.)
3. **Virtual shares / decimals offset > 0** (OZ ERC-4626 inflation mitigation) OR a `minimumMint` / `shares==0` revert guard.
4. **`updateExchangeRate` happens BEFORE pricing** within the same tx (no stale-rate sandwich window).
5. **Value-denominated fee accounting that is EXCLUDED from NAV** (`netValue = totalPositionsValue − totalFeesOwed`) → no double-count of unclaimed fees.
6. **`msg.sender` baked into the CREATE2 salt** for deterministic factories → defeats address-squatting/hijack of deterministic proxies (Enzyme `DeterministicBeaconFactory`: `keccak256(abi.encode(msg.sender, _salt))`).

---

## High-yield bug classes for vaults (ranked by realized payout odds)

| # | Class | Where it hides | Concrete tell |
|---|-------|----------------|---------------|
| 1 | **Share-price inflation / first-depositor** | `totalAssets()`, `convertToShares`, decimals offset | balance-derived NAV + 0 offset + no min-mint; 1-wei attacker rounds victim to 0 shares |
| 2 | **Rounding-direction drain** | every `mulDiv`/`/` in deposit/redeem/fee | a path that rounds in the *user's* favor, repeatable for profit |
| 3 | **View/effect asymmetry** | a `totalAssets()`-style view that counts X, but the claim/settle path returns 0 for X under some state (e.g. paused) | dreUSD M-1: `totalAssets` added `vestedAmount()` unconditionally, but `_claimVestedRewards()` returned 0 when distributor paused → overpay + DoS |
| 4 | **Access control on value-movers** | `mint`/`burn`/`withdraw`/`transfer`/`setRate`/`updateNAV` | any one reachable without the intended `onlyHandler`/`onlyAdmin` gate |
| 5 | **Async-queue free option (ERC-7540)** | cancel-after-`minRequestDuration` | user can avoid an unfavorable settlement; weigh against admin batching of NAV-update + execution |
| 6 | **Stale-NAV at execution** | "does not validate sharePrice timestamp" comments | exploitable only if NON-admin can execute at a stale NAV; if admin-only = trusted = OOS |
| 7 | **Cross-chain custody / message** | CCIP/bridge receivers, per-user wallets | forged/replayed source, wallet-squatting via deterministic address, cross-wallet drain |
| 8 | **Fee math** | HWM/hurdle, mgmt time-proration, entrance/exit burn | double-count, HWM reset abuse — but usually admin-flow-only = low odds |

---

## The "trusted roles = OOS" filter (avoid writing invalid reports)

Before writing up anything that requires the admin/owner/keeper to act maliciously or carelessly: **re-read the program's trust model.** In most vault programs, admin/owner/valuation-pusher roles are *trusted*. A "bug" that needs the admin to push a bad NAV, set a malicious fee asset, or execute at a stale price is **out of scope** — it's an operational responsibility, not a vulnerability. dreUSD's two Mediums survived precisely because they were triggerable by a *legitimate* PAUSER action / a normal `vault.deposit()` — no malicious admin required.

---

## Workflow (the rig)

1. **Scaffold:** clone in-scope source @ exact commit (gitignored), full recursive submodules, `forge build`, `slither` baseline.
2. **Map value-movers:** `grep -nE "function .*\b(external|public)\b"` every contract; tag each with its access modifier; flag every one that writes share-price/balance/supply.
3. **Run the 60-second disqualifier.** If inflation is dead, pivot to rounding + view/effect asymmetry + the async/cross-chain edges.
4. **Prove or kill with Foundry:** write the PoC as a forge test (local repro → forked-chain sim). One passing PoC beats twenty hypotheses. Invariant/fuzz suites (conservation, solvency, monotonic share price) both *find* drift and *document* "no bug, here's the ~900k transitions that prove it."
5. **Report:** lead with impact; separate CONFIRMED from SUSPECTED; Sherlock format needs a Medium/High label or it's invalid.

---

## Proof-of-Impact & CWE

- **Impact-first severity** (Immunefi): direct theft / permanent freeze / unauthorized mint-burn / insolvency / accounting corruption = Critical/High. A theoretical rounding dust with no profitable path = Low/Info, don't oversell.
- **Common CWEs:** CWE-682 (incorrect calculation / rounding), CWE-840 (business logic), CWE-284 (improper access control), CWE-841 (bad behavioral workflow — view/effect asymmetry), CWE-362 (race / front-run).
- **Evidence:** commit hash, chain ID, block number, addresses, the forge test command + output. Deterministic repro or it didn't happen.

---

## Standing discipline

A documented **"no bug found, here's the disqualifier that killed each class"** is a valid, valuable result — and it makes the *next* audit faster. Hardened/mature targets (Veda, Enzyme Onyx) burn time; **fresh time-boxed contests** are where the realized findings come from (dreUSD). One strong PoC-backed finding beats twenty weak leads.
