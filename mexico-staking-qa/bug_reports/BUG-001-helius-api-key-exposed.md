# BUG-001 — Helius RPC API key exposed in plain text on the front end

- **Project:** Mexico Staking (MEX)
- **Environment:** devnet, `mexicoweb-dev.up.railway.app`
- **Found by:** QA smoke pass (spotted in a Network-tab screenshot, not part of the original checklists)
- **Date:** 2026-08-21
- **Severity:** Critical
- **Priority:** P1 — should be fixed before any mainnet-facing deployment
- **Status:** Open — described in chat only, formalized here

## Summary

Every RPC request made from the front end includes the Helius API key as a
plain-text query parameter (`?api-key=...`). The key is fully visible in the
browser's Network tab and in the request URL, so anyone with basic DevTools
access can copy it and reuse it outside the application.

## Steps to Reproduce

1. Open `mexicoweb-dev.up.railway.app` in a browser with DevTools open on the
   Network tab.
2. Connect a wallet and trigger any RPC-dependent action (load balances, load
   positions, load pool stats, submit a transaction).
3. Inspect any outgoing request to `*.helius-rpc.com` (or equivalent Helius
   endpoint).
4. Observe the full request URL, e.g.:
   `https://devnet.helius-rpc.com/?api-key=<REDACTED>`
5. Copy the `api-key` value out of the URL.

## Actual Result

The Helius API key is sent directly from the browser to Helius as a URL query
parameter on every RPC call. It is:
- Visible to anyone inspecting Network traffic (DevTools, browser extensions,
  proxy tools, corporate/ISP-level logging of full URLs).
- Trivially copyable and reusable by a third party outside of the
  application.

## Expected Result

The front end should never hold or transmit the raw provider API key. RPC
traffic should be routed through a backend proxy that:
- Holds the Helius API key server-side only (env var / secret manager).
- Accepts requests from the front end without the key embedded in the URL.
- Attaches the real Helius key server-side before forwarding upstream.
- Ideally applies its own rate limiting / auth per user or per session, so a
  single leaked front-end-facing endpoint can't be used to fully drain quota.

## Impact

- **Quota exhaustion / denial of service:** anyone can copy the key and issue
  their own requests against it, exhausting the plan's request quota and
  degrading or breaking the app for legitimate users.
- **Cost impact:** if the Helius plan is paid/metered, third-party usage of
  the leaked key directly costs the team money.
- **Mainnet risk (highest concern):** if the *same* Helius key (or a key on
  the same account/billing plan) is ever reused for a production/mainnet
  deployment, this becomes a production incident, not just a devnet
  inconvenience. Keys should be rotated and the proxy fix should land before
  any mainnet cutover.

## Suggested Fix

1. Introduce a lightweight backend proxy endpoint (e.g. `/api/rpc`) that the
   front end calls instead of Helius directly.
2. Move the Helius API key to a server-side-only environment variable; remove
   it from all front-end bundles/config.
3. Rotate the currently-exposed devnet key once the proxy is live (it should
   be treated as compromised).
4. Add a regression check (e.g. a simple grep/CI check or code review
   checklist item) to ensure no provider API key ever ships in client-side
   code or is appended as a URL query parameter from the browser.
5. Before mainnet: confirm the mainnet Helius key is provisioned separately
   from devnet and is never referenced from front-end code.

## Evidence

Reported from a Network-tab screenshot shared during the QA smoke pass (see
QA chat log, 2026-08-21). Attach the original screenshot / a fresh HAR export
here when available.
