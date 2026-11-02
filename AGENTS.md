# AGENTS.md

Guidance for AI coding agents (and humans) working in this repository.

## Project

Home Assistant add-on that converts SVG files to PNG. It consists of two parts:

- `addon/` — the add-on container: a Flask service (`convert.py`) using **CairoSVG** for conversion, plus fonts for Unicode SVG text rendering. Exposes `POST /convert` on port 5000. Also provides a CLI: `convert.py convert <input.svg> <output.png>`.
- `addon/custom_components/svg_to_png/` — the Home Assistant integration (domain `svg_to_png`) that registers the `svg_to_png.convert` service and posts the SVG file to the add-on.
- `repository.json` — the add-on store repository definition.

`run.sh` (add-on entrypoint) copies the custom component from the image into `/config/custom_components/svg_to_png/` on each start when the version changed.

## Commands

- Convert locally (CLI path): `python3 addon/convert.py convert <input.svg> <output.png>`
- Run the Flask server: `python3 addon/convert.py` (listens on 0.0.0.0:5000)
- Convert over HTTP: `curl -F "file=@input.svg" http://localhost:5000/convert > output.png`
- Build the add-on image: `docker build -t svg_to_png ./addon`
- Syntax check: `python3 -m py_compile addon/convert.py addon/custom_components/svg_to_png/__init__.py`

There is no test suite or linter configured. Verify behavior with the commands above.

## Conventions

- Python 3. Add-on dependencies: Flask + CairoSVG + fontconfig/DejaVu/Roboto (installed via `apk`); custom component needs only `requests`. Keep dependencies minimal; prefer stdlib.
- Use `logging` with a module-level logger (`logger` in `convert.py`, `_LOGGER` in the integration). No `print` in Python code. The emoji `echo` lines in `run.sh` are intentional startup status output.
- Keep the existing docstring style: functions document parameters, returns, and raised exceptions.
- `run.sh` runs under BusyBox (`#!/bin/sh`, Alpine-based `hassio-addons/base` image) — keep it POSIX sh, no bashisms.
- System packages in the Dockerfile are installed with `apk add --no-cache`; the `BUILD_FROM` base image arg must stay overridable.

## Versioning (important)

The add-on version must be bumped in **all four** places together:

1. `addon/config.yaml` → `version`
2. `addon/custom_components/svg_to_png/manifest.json` → `version`
3. `addon/run.sh` → `ADDON_VERSION`
4. `repository.json` → `addons[0].version`

`run.sh` compares `ADDON_VERSION` against `/config/custom_components/svg_to_png/.version` and only copies the integration when they differ — if any of the four drift, updated integration code will silently fail to propagate to existing installations.

## Boundaries

- Only `addon/` contents ship in the add-on image and to Home Assistant. `README.md`, `AGENTS.md`, `.github/`, `.agents/`, and `skills-lock.json` are repository tooling — never copy them into the image or the integration.
- The add-on requires the `config:rw` mapping in `addon/config.yaml` (it writes the integration to `/config`). Do not remove or weaken it.
- `.github/agents/*.agent.md` defines the tiered agent configuration (executors `execution` → `reasoning` → `advanced-reasoning`; read-only reviewers `deepseek-review`, `qwen-review`). Do not rename tiers or change their models without an explicit request.
- `.agents/skills/` and `skills-lock.json` pin the installed agent skills. If skills are added, updated, or removed, commit the lock file in the same change.

## Workflow skills

`.agents/skills/` contains installed engineering workflow skills (spec → plan → implement → test → review → ship). See the `using-agent-skills` skill for the phase→skill mapping.
