#!/usr/bin/env bash
set -u

# Fast preflight for GitHub CLI usage.
# Exit code:
#   0 = API reachable and status page not degraded
#   1 = API unreachable
#   2 = Status page reports degraded/incident
#   3 = Missing dependency (curl)

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required but not installed."
  exit 3
fi

api_url="https://api.github.com/rate_limit"
status_url="https://www.githubstatus.com/api/v2/status.json"

echo "Checking GitHub API reachability..."
api_code="$(curl -sS -o /dev/null -w "%{http_code}" --max-time 8 "$api_url" 2>/dev/null || true)"

if [[ -z "$api_code" || "$api_code" == "000" ]]; then
  echo "FAIL: Cannot reach api.github.com"
  exit 1
fi

if [[ "$api_code" != "200" && "$api_code" != "403" ]]; then
  echo "WARN: api.github.com returned HTTP $api_code"
else
  echo "OK: api.github.com reachable (HTTP $api_code)"
fi

echo "Checking GitHub Status..."
status_json="$(curl -sS --max-time 8 "$status_url" 2>/dev/null || true)"
indicator="$(printf "%s" "$status_json" | sed -n 's/.*"indicator":"\([^"]*\)".*/\1/p')"
description="$(printf "%s" "$status_json" | sed -n 's/.*"description":"\([^"]*\)".*/\1/p')"

if [[ -z "$indicator" ]]; then
  echo "WARN: Could not read githubstatus response"
  exit 0
fi

echo "Status: $description ($indicator)"

if [[ "$indicator" == "none" ]]; then
  exit 0
fi

echo "WARN: GitHub status is not fully operational."
exit 2
