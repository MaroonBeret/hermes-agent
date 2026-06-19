#!/usr/bin/env python3
"""Fetch a public page with Scrapling and extract readable text.

Designed for public documentation/help-center/article pages only: no user
browser profile, no credentials, no cookies supplied, no development cache, and
no MCP server.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape


def strip_html(html: str) -> str:
    html = re.sub(r"(?is)<script[^>]*>.*?</script>|<style[^>]*>.*?</style>", " ", html)
    html = re.sub(r"(?is)<(br|p|li|h[1-6]|div|section|article)[^>]*>", "\n", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a public page with Scrapling and extract readable text")
    parser.add_argument("url")
    parser.add_argument("--json", action="store_true", help="emit JSON with status, url, title, text")
    parser.add_argument("--limit", type=int, default=20000)
    parser.add_argument("--no-google-referer", action="store_true", help="disable Scrapling's synthetic Google referer")
    args = parser.parse_args()

    try:
        from scrapling.fetchers import Fetcher
    except Exception as exc:  # pragma: no cover - depends on optional package
        print(f"ERROR: Scrapling import failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    try:
        page = Fetcher.get(
            args.url,
            stealthy_headers=True,
            impersonate="chrome",
            follow_redirects=True,
            timeout=25,
            google_search=not args.no_google_referer,
        )
    except Exception as exc:
        print(f"ERROR: fetch failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    body = getattr(page, "body", b"")
    if isinstance(body, bytes):
        html = body.decode(getattr(page, "encoding", None) or "utf-8", errors="replace")
    else:
        html = str(body or getattr(page, "html_content", "") or getattr(page, "text", ""))

    title = ""
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    if match:
        title = re.sub(r"\s+", " ", strip_html(match.group(1))).strip()

    # Prefer common article containers when present.
    article = html
    for pattern in [
        r'(?is)<article[^>]*>(.*?)</article>',
        r'(?is)<div[^>]+class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>',
        r"(?is)<section[^>]+class='[^']*article[^']*'[^>]*>(.*?)</section>",
    ]:
        match = re.search(pattern, html)
        if match:
            article = match.group(1)
            break

    text = strip_html(article)[: args.limit]
    result = {
        "status": getattr(page, "status", None),
        "url": getattr(page, "url", args.url),
        "title": title,
        "text": text,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"URL: {result['url']}\nStatus: {result['status']}\nTitle: {title}\n\n{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
