#!/usr/bin/env bash
# This script runs ty and ruff diagnostics and stores their reports in a dedicated folder.
# It fails if any check reports issues and removes the reports folder only when all checks pass.

set -u -o pipefail

if ! command -v uvx >/dev/null 2>&1; then
  echo "Error: 'uvx' is not installed or not in PATH." >&2
  exit 1
fi

reports_dir="${REPORTS_DIR:-code_diagnostics}"
mkdir -p "$reports_dir"

# Keep reports out of Git by placing a .gitignore inside the folder itself
if [[ ! -f "$reports_dir/.gitignore" ]]; then
  echo "*" > "$reports_dir/.gitignore"
fi

echo "Running ty check..."
ty_status=0
uvx ty check --output-format full . > "$reports_dir/ty_output.txt" || ty_status=$?

echo "Running ruff check..."
ruff_status=0
uvx ruff check . --cache-dir "$reports_dir/.ruff_cache" --output-file "$reports_dir/ruff_output.txt" || ruff_status=$?

echo "Done. Reports written to '$reports_dir'."

if [[ $ty_status -ne 0 || $ruff_status -ne 0 ]]; then
  echo "At least one check reported issues (ty=$ty_status, ruff=$ruff_status)." >&2
  exit 1
fi

rm -rf "$reports_dir"
echo "All checks passed. Removed '$reports_dir'."
