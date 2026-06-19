# Claude Code Guidance for Hermes Agent

Claude Code should treat this repository as the shared source of durable agent knowledge for Hermes-related work.

## Start Here

1. Read `AGENTS.md` for the full Hermes Agent development guide.
2. Check `skills/` for reusable procedures before inventing a workflow.
3. If a task hits a non-trivial blocker and you find a reusable fix, update the relevant `SKILL.md` or add a focused reference/script under that skill.
4. Commit durable workflow improvements on the active fork/local branch; do not push to `upstream` unless Omer explicitly asks.

## Web Scraping / Blocked Public Pages

For public documentation, help-center, or article pages blocked by basic anti-bot/Cloudflare checks, use the built-in skill:

- `skills/research/scrapling-safe-fetch/SKILL.md`
- helper script: `skills/research/scrapling-safe-fetch/scripts/scrapling_safe_fetch.py`

Important rules from that skill:

- Prefer first-party APIs/static sources first.
- Use Scrapling only for public, non-sensitive pages.
- Never use personal browser profiles, user cookies, credentials, untrusted CDP endpoints, or exposed MCP servers.
- Keep fetched output bounded and inspect it for real article text, not just an interstitial.

## How Hermes and Claude Learn From Each Other

- **Shared repo skills:** reusable procedures belong in `skills/<category>/<name>/SKILL.md` and should be committed. Hermes can load them as skills; Claude can read them directly from the repo.
- **Repo guidance:** cross-agent operating rules belong here in `CLAUDE.md` and/or `AGENTS.md`.
- **Local runtime knowledge:** user-specific or host-specific facts belong in Hermes memory, not in public/shared skills.
- **No silent one-off fixes:** when a workaround is broadly useful, convert it into a skill/reference/script so the other agent can reuse it next time.
