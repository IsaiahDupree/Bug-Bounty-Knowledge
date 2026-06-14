# Bug Bounty Discovery & Triage Methodology

_How to find work worth doing — the reproducible front of the funnel, distilled from real audit campaigns. For AUTHORIZED testing + responsible disclosure only._

> **North star: expected value per hour, not contests entered.** The single biggest EV lever, found empirically: **fresh time-boxed contests >> picked-over always-on programs.** A fresh Sherlock contest (dreUSD) yielded 2 confirmed Mediums; two mature always-on Immunefi programs in a row (Veda, Enzyme Onyx) yielded honest "hardened, no bug" verdicts — the obvious surfaces were already closed by prior audits. Tune discovery to surface **fresh, time-boxed scope the moment it's announced**, and be skeptical of mega always-on bounties.

A documented "no bug found, here's the disqualifier that killed each class" is a **valid result**. Never manufacture findings or submit weak/known leads — that burns reputation and gets you banned.

---

## 1. Platforms to monitor (and how to read them)

| Platform | Surface | How to read | Fit |
|---|---|---|---|
| **Sherlock — Contests** | time-boxed | public JSON API (`/contests`, paginated) | ⭐ primary |
| **Sherlock — Bug Bounties** | **always-on** (separate surface!) | public JSON API (`/bug_bounties`) | freshly-launched ones are higher EV |
| **Cantina** | time-boxed | public competitions API | ⭐ primary |
| **Code4rena** | time-boxed | public audits API (paginated) | ⭐ primary |
| **Immunefi** | always-on + boosts | public bounties JSON | always-on = low EV; **live competitions aren't in the public JSON** — watch the Competitions tab manually |
| **Codehawks / HackerOne / Bugcrowd / Intigriti** | mixed | API key / manual | web2 + manual path |

> Two distinct surfaces matter: time-boxed (a deadline) vs always-on (no deadline). A recently-launched **always-on** bounty (tag anything `live_since` < 60 days as **🆕 fresh**) is far less picked-over than a years-old one — rank fresh first. The three competitive-audit platforms (Sherlock + Cantina + Code4rena) are the core: fresh, well-scoped Solidity on a clock.

## 2. The discovery engine (read-only, never joins or submits)
One scheduled script polls every JSON API, normalizes each open opportunity, ranks it, and diffs against the last run to surface what's **NEW** and **UPCOMING**. Fire OS notifications on genuine signal only:
- **⏰ UPCOMING** — a contest was *announced*. Highest priority: read scope on day-zero, before the crowd.
- **🔔 NEW** — a new target appeared since the last run.

## 3. EV triage — the ranking
```
ev_score = ($rewards / nSLOC) × time_factor
```
- **reward density** (`$rewards / nSLOC`) — reward per line of *in-scope* code = best odds of a paid finding per hour. Where nSLOC is unknown, use a bounded reward proxy.
- **time_factor** — penalize <2 days left (×0.3), ease 2–5 days (×0.8), full for longer (×1.0), and slightly favor not-yet-started contests (×1.1 — full window ahead).

**Beyond the score, high-EV =** fresh product/first contest · toolchain fit (Solidity/Foundry — skip rig mismatches like Cairo/Rust unless you have the rig) · public repo at a pinned commit (clone & build immediately) · no KYC-to-participate · vault/share-price/accounting shaped (where your playbooks are sharpest).

**Disqualifiers (deprioritize):** mega always-on programs (most picked-over code on the internet) · already in judging/ended · scope you can't build (private repo, exotic chain, no commit pin).

## 4. The full pipeline — and the two human gates
```
 discover + triage ──► JOIN contest ──► scaffold rig ──► hunt + PoC ──► SUBMIT
   ✅ automated         🚫 human          ✅ automated      ⚙️ assisted     🚫 human
```
**Join and submit are deliberately manual:**
- **Join** = signing a wallet tx + accepting a legal rules-of-engagement / safe-harbor. Auto-signing a legal commitment is out of bounds.
- **Submit** = auto-filing unverified findings is spam → reputation damage + bans. Every program (and a sane policy) rewards verified, PoC-backed, high-signal reports. The human gate is where you choose severity correctly and catch the label/validity mistakes that would invalidate a submission.

## 5. The hunting toolkit (close the loop)
- **Knowledge MCP** (`kb_search` / `kb_get` / `kb_list` / `kb_index`) — query this Bug-Bounty-Knowledge base (and a trading base) for the target's shape. Start every audit with `kb_search` on the contract pattern. See [knowledge-mcp](https://github.com/IsaiahDupree/knowledge-mcp).
- **Playbook lenses** — [DeFi Vault & Share-Price Auditing](./DeFi%20Vault%20%26%20Share-Price%20Auditing.md) (the 60-second inflation disqualifier, ranked vault classes, trusted-roles=OOS filter) and [RWA Mint/Redeem Vault Auditing](./RWA%20Mint-Redeem%20Vault%20Auditing.md).
- **bbkit** — score confirmed findings with `bbkit.cvss` + `bbkit.severity`, write them up with `bbkit.report`.

---
_The discipline: optimize EV/hour, prefer fresh time-boxed scope, automate everything except the two legal/quality human gates, and treat a well-documented "no finding" as a real, reputation-preserving outcome._
