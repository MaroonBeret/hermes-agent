---
name: scrapling-safe-fetch
description: "Use when normal browser/curl/web extraction is blocked by Cloudflare or basic anti-bot checks on public documentation, article, or help-center pages. Prefer official APIs first, then use a reviewed Scrapling helper in an isolated environment."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [web, scraping, cloudflare, public-docs, help-center, scrapling]
    related_skills: [consumer-research-and-sourcing, blogwatcher]
---

# Scrapling Safe Fetch

## Overview

Use this skill when a public page needs to be read for research or troubleshooting, but ordinary `curl`, browser snapshots, or web extraction get blocked by Cloudflare/basic anti-bot interstitials. The goal is not stealthy account automation; it is a last-mile fetch path for public documentation, help centers, articles, and other non-authenticated pages.

The preferred order is:

1. Use first-party APIs or static sources when available.
2. Try normal fetch/extraction tools.
3. Use Scrapling only for public pages that remain blocked.
4. Keep the run isolated and non-sensitive: no personal browser profile, no user cookies, no saved dev cache, no exposed MCP server.

## When to Use

- Public documentation/help-center pages are behind a basic anti-bot/Cloudflare check.
- A site serves useful HTML but rejects plain `curl` or simple fetchers.
- You need a repeatable, auditable fallback before asking the user to manually copy text.
- You are researching public product docs, support articles, release notes, or blog posts.

Do **not** use for:

- Authenticated pages unless the user explicitly approves a credential/cookie workflow for that task.
- Pages containing private data, billing, admin dashboards, or user accounts.
- Circumventing paywalls, access controls, or site policies.
- Running arbitrary browser profiles, untrusted CDP endpoints, or Scrapling MCP exposed on the network.

## Security Review Summary

Scrapling 0.4.9 was reviewed from GitHub repository `D4Vinci/Scrapling` at commit `c0f012d6625528a756e3852bad9ae7500c223579` before adding this workflow.

Assessment: acceptable for public-page scraping in an isolated Python environment, with precautions.

Risks found:

- No malicious install-time hooks or hidden telemetry were found in the reviewed version.
- Browser/stealth fetchers execute or interact with target-site JavaScript; treat pages as untrusted.
- `scrapling install` may run Playwright install commands and system dependency installation; do not run blindly as root.
- Development cache can store response bodies, cookies, and headers; do not enable it for sensitive/authenticated pages.
- Spider checkpoints use pickle; never resume untrusted checkpoints.
- Scrapling MCP can bind to `0.0.0.0`; do not expose it.
- Avoid `real_chrome=True`, personal browser profiles, untrusted CDP URLs, and untrusted browser flags.

## Setup

Create an isolated environment outside the project tree:

```bash
python3 -m venv ~/.hermes/venvs/scrapling
~/.hermes/venvs/scrapling/bin/python -m pip install --upgrade pip
~/.hermes/venvs/scrapling/bin/python -m pip install 'scrapling==0.4.9'
```

If browser-backed fetchers are later needed, install browser dependencies deliberately and without root unless necessary. For ordinary public HTML pages, start with the lightweight `Fetcher` helper below.

## Helper Script

This skill ships a small helper at:

```bash
skills/research/scrapling-safe-fetch/scripts/scrapling_safe_fetch.py
```

Run it from a Hermes checkout with the isolated venv:

```bash
~/.hermes/venvs/scrapling/bin/python \
  skills/research/scrapling-safe-fetch/scripts/scrapling_safe_fetch.py \
  'https://example.com/page' --limit 12000
```

JSON output:

```bash
~/.hermes/venvs/scrapling/bin/python \
  skills/research/scrapling-safe-fetch/scripts/scrapling_safe_fetch.py \
  'https://example.com/page' --json --limit 12000
```

Disable Scrapling's synthetic Google referer when desired:

```bash
~/.hermes/venvs/scrapling/bin/python \
  skills/research/scrapling-safe-fetch/scripts/scrapling_safe_fetch.py \
  'https://example.com/page' --no-google-referer
```

## Fetching Rules

- Public pages only unless the user explicitly approves the authenticated workflow.
- Never use the user's personal browser profile.
- Never pass site credentials, cookies, bearer tokens, or admin URLs to this helper.
- Do not enable Scrapling development cache for sensitive pages.
- Do not start Scrapling MCP except bound to localhost and only with explicit user intent.
- Prefer first-party APIs when available. Example: for Zendesk Help Center sites, check the Help Center API before using browser-like fetching.
- Keep output bounded with `--limit` so blocked-page retries do not flood context.

## Verified Use Case

This workflow successfully fetched UniFi Help Center content after browser automation hit Cloudflare verification, including:

- `https://help.ui.com/hc/en-us/articles/18965560820247-Implementing-Network-and-Client-Isolation-in-UniFi`

The durable lesson from that incident: if normal docs fetching fails, proactively try safe alternate public-page retrieval paths before asking the user to paste docs manually.

## Common Pitfalls

1. **Stopping at the first blocked fetch.** Try first-party APIs and this safe public-page fallback before declaring a blocker.
2. **Using a personal Chrome profile.** This can leak cookies and account state. Do not use `real_chrome=True` or profile directories for this workflow.
3. **Letting caches collect sensitive data.** Keep Scrapling dev cache off unless the target is clearly public and non-sensitive.
4. **Running install commands as root.** Use an isolated user venv. Review browser/system dependency installs before running them.
5. **Exposing MCP.** If Scrapling MCP is ever needed, bind only to localhost and do not put it behind public or LAN exposure.
6. **Treating scraping as an API substitute.** Prefer official APIs and RSS/Atom feeds where available; scraping is the fallback.

## Verification Checklist

- [ ] Target page is public and non-sensitive.
- [ ] First-party API/static source was considered first.
- [ ] No credentials, cookies, personal browser profile, or untrusted CDP endpoint were used.
- [ ] Output was limited and inspected for useful article text, not just an interstitial.
- [ ] Any reusable discovery was added back to the appropriate skill or project guidance.
