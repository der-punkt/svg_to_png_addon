---
name: python-code-diagnostics
description: "Python-only: run ty and ruff diagnostics sequentially via an embedded CLI tool, analyze report outputs, apply focused Python code fixes, and re-run checks until diagnostics improve. Only use for Python projects with a src/ layout. Do not use for Go, Rust, JavaScript, or any other language."
metadata:
  author: "Christian Malek"
  version: "1.0.0"
---

# Python Code Diagnostics

## Use when

- The user asks to run ty and ruff diagnostics on a Python project.
- The user wants diagnostics-based Python code fixes.
- The workspace contains Python source files (the tool runs on the whole project, including `src/`, `tests/`, etc.).

## Do not use when

- The project is not Python (Go, Rust, JavaScript, TypeScript, etc.).
- The user requests review-only feedback without code edits.
- The user asks for unrelated release or deployment workflows.

## Inputs

- Workspace root is the project root (`.` is analysed, so `src/`, `tests/`, etc. are all included).
- uvx is available in PATH.
- `PYTHON_CODE_DIAGNOSTICS_SKILL_DIR` is optional and must point to the installed skill directory when set.

## Embedded CLI tool

- Tool location is resolved from the project installation, global OpenCode installation, or repository symlink location. Set `PYTHON_CODE_DIAGNOSTICS_SKILL_DIR` to override this resolution.
- Command:

```bash
if [[ -n "${PYTHON_CODE_DIAGNOSTICS_SKILL_DIR:-}" ]]; then
  SKILL_DIR="${PYTHON_CODE_DIAGNOSTICS_SKILL_DIR}"
else
  SKILL_DIR=""
  for candidate in \
    "$PWD/.agents/skills/python-code-diagnostics" \
    "$HOME/.config/opencode/skills/python-code-diagnostics" \
    "$HOME/.agents/skills/software-engineering/python-code-diagnostics" \
    "$HOME/.agents/skills/python-code-diagnostics"; do
    if [[ -f "$candidate/scripts/run_code_diagnostics.sh" ]]; then
      SKILL_DIR="$candidate"
      break
    fi
  done
fi

if [[ -z "$SKILL_DIR" || ! -f "$SKILL_DIR/scripts/run_code_diagnostics.sh" ]]; then
  printf 'Error: python-code-diagnostics skill directory not found. Set PYTHON_CODE_DIAGNOSTICS_SKILL_DIR.\n' >&2
  exit 1
fi

bash "$SKILL_DIR/scripts/run_code_diagnostics.sh"
```

## Workflow

The report files are the loop state. Each tool run overwrites them with the current findings. The exit code is the termination signal.

Repeat this loop until the tool exits with code 0:

1. Run the embedded tool command above from workspace root.
2. Check the exit code:
   - Exit 0 → both checks clean; the tool has already deleted the `code_diagnostics` folder. Stop.
   - Exit 1 → findings remain, continue.
3. Read the first 10 lines of code_diagnostics/ty_output.txt.
4. Read the first 10 lines of code_diagnostics/ruff_output.txt.
5. Fix the visible issues with this priority:
   - ty findings first (type errors, missing attributes, incompatible types)
   - ruff findings second (style, lint, unused imports)
   - findings in `tests/` are included and must be fixed too
6. Go back to step 1.

## Defaults

- Read report files in small chunks — never dump the full file into context.
- Apply minimal, focused code changes per iteration.
- Keep public APIs unchanged unless a fix requires otherwise.
- Do not create additional one-off shell scripts.

## Gotchas

- Some ty findings cascade: fixing a root-cause type error may remove several follow-on errors automatically. Prefer root-cause fixes.
- Ruff `--output-file` writes only the file path and rule, not line context. Use `read_file` on the reported file+line to get the code context before editing.

## Validation

- Success: tool exits with code 0 and both report files are empty or contain no findings.
- Partial success: diagnostics count is reduced; list remaining open findings explicitly.
- Failure: required prerequisites are missing or no safe fix is possible without breaking the API.

## Output format

After each iteration report:

1. Findings fixed (file, line, rule).
2. Findings still open (first 10, with rule name).
3. Next action.
