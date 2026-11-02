# Home Assistant Add-on: SVG to PNG Converter

## Overview
This Home Assistant add-on provides a simple way to convert SVG images to PNG format using an integrated conversion service. The add-on runs a lightweight service inside a Docker container and exposes a custom service for easy integration with Home Assistant.

## Features
- Converts SVG images to PNG format.
- Integrates seamlessly with Home Assistant services.
- Uses **CairoSVG** for accurate and high-quality rendering.
- Works on multiple architectures (amd64, armv7, aarch64).

## Installation
### **Step 1: Add the Repository**
1. Open **Home Assistant**.
2. Navigate to **Settings** > **Add-ons** > **Add-on Store**.
3. Click the **three dots** in the top-right corner and select **Repositories**.
4. Add the following URL:
   ```
   https://github.com/der-punkt/svg_to_png_addon
   ```
5. Click **Add** and wait for the repository to load.

### **Step 2: Install the Add-on**
1. Locate **SVG to PNG Converter** in the add-on store.
2. Click **Install**.
3. Start the add-on with privileged access (required).

### **Step 3: Install the service**
1. Open your `configuration.yaml` file.
2. Add the service:
   ```
   svg_to_png:
   ```
3. Restart Home Assistant

## Usage
### **Calling the Service in Home Assistant**
Once installed, you can use the custom **service** to convert an SVG file.

#### **Service Name:**
```
svg_to_png.convert
```

#### **Service Data Example:**
```yaml
service: svg_to_png.convert
data:
  input_path: "/media/tmp/image.svg"
  output_path: "/media/tmp/image.png"
```

### **How It Works**
1. The Home Assistant service sends a request to the add-on.
2. The add-on runs `cairosvg` inside the Docker container to convert the file.
3. The PNG file is saved in the specified location.

## Logs & Debugging
To check the add-on logs:
```bash
ha addons logs svg_to_png
```
If you encounter issues, make sure:
- The file paths are correct.
- The add-on has sufficient permissions.
- Docker is running properly.

## AI Agent Development Environment

This repository ships the configuration used by AI coding agents (e.g. GitHub Copilot) so that agents working on the codebase follow a consistent engineering workflow. If you are only using the add-on, you can ignore this section.

### Layout

| Path | Purpose |
| ---- | ------- |
| `.agents/skills/` | Installed [agent skills](https://skills.sh) — modular workflow packages (spec → plan → implement → test → review → ship) that give agents structured engineering practices. Each skill lives in `.agents/skills/<name>/SKILL.md`. |
| `.github/agents/` | Custom agent definitions (`.agent.md`) for the Copilot agent framework — a tiered set of executor and reviewer agents. |
| `.github/ISSUE_TEMPLATE/` | GitHub issue templates (bug report, feature request). |
| `skills-lock.json` | Lock file pinning the exact source and content hash of every installed skill, so each machine starts from the same agent setup. |

### Agent tiers (`.github/agents/`)

The agents form an escalation chain plus independent reviewers:

| Agent | Role |
| ----- | ---- |
| `execution` | Tier 1 — clearly specified, locally scoped, mechanically verifiable work. Escalates to `reasoning` when judgment is required. |
| `reasoning` | Tier 2 — analysis, judgment, ambiguity resolution, and cross-component reasoning. Escalates to `advanced-reasoning` when a task remains unresolved. |
| `advanced-reasoning` | Tier 3 — exceptional work requiring deep system-level reasoning, or unresolved escalations from lower tiers. |
| `deepseek-review`, `qwen-review` | Read-only, adversarial reviewers that challenge plans, code, and technical claims before approval. They never edit files or run commands. |

Each `.agent.md` file declares its name, description, allowed tools, reasoning effort, model(s), and the agents it may delegate to (`agents:` field).

### Managing skills and `skills-lock.json`

Skills are installed with the skills CLI:

```bash
npx skills find [query]           # search the skills ecosystem
npx skills add <owner/repo@skill> # install a skill into .agents/skills/
npx skills update                 # update installed skills
```

`skills-lock.json` records, for each installed skill, its `source` (e.g. `addyosmani/agent-skills`), `sourceType`, `skillPath`, and the `computedHash` of the skill content. When you add, update, or remove skills, commit the changed files under `.agents/skills/` together with the updated lock file.

## Contributing
Feel free to contribute by submitting **pull requests** or opening **issues** on GitHub!

## Contributors
We thank the following contributors for their work on this add-on:
- [MatAhman](https://github.com/MatAhman) — Added fonts for improved Unicode SVG text rendering ([PR #3](https://github.com/der-punkt/svg_to_png_addon/pull/3))

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
⭐ **Enjoy using the SVG to PNG Converter?** Consider starring the repository on GitHub! ⭐

