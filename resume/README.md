# Junghan Kim

**PKM-AI Harness Engineer · From Embedded Systems to Shared Agent Work Surfaces**

[junghanacs@gmail.com](mailto:junghanacs@gmail.com) · [github.com/junghan0611](https://github.com/junghan0611) · [notes.junghanacs.com](https://notes.junghanacs.com) · [linkedin.com/in/junghan-kim-1489a4306](https://www.linkedin.com/in/junghan-kim-1489a4306)

---

## Summary

Engineer working across embedded systems, knowledge infrastructure, and AI agent collaboration. Current focus: PKM-native harnesses for long-term human-AI work, including shared memory, shared timelines, delegation interfaces, and reproducible work surfaces. Building these ideas in public through pi-shell-acp, agent-config, and a semantic digital garden, while continuing hands-on work across Go, Clojure, Zig, C, TypeScript, Nix, and Elisp.

---

## Career

### GoQual Inc. — Full Stack Architect

*2025.06 ~ Present*

#### On-Device AI Smart Home Hub (2025.09 ~ Present)

**HomeAgent** — Open-source Matter smart home hub with on-device AI agent.

- Designed and built a Go-based Matter hub running on RPi5 + Hailo-8 NPU (Yocto) and RK3576 (Android) from a single codebase, with Flutter as the app shell
- Explored local-first AI control loops for smart-home interaction, including on-device intent handling and model preparation workflows
- Implemented BLE commissioning for Matter/Thread devices via matterjs bridge, supporting 5 device types with OTBR integration
- Managed 3-agent parallel development sessions: 24 commits/day, 163 tests passing, zero file conflicts — human as PM
- Cross-platform: 96% code sharing between Linux and Android deployments

**SKS Hub** — Production Zigbee gateway firmware in Zig.

- Rewrote legacy C Zigbee SDK integration using Zig's type-safe FFI layer
- Built deterministic state machine architecture (single `HubState`, pure `transition()` functions)
- Aging test automation (24-hour stability verification) with Claude as pair programmer
- **198 commits in 30 days** across device driver, protocol, and cloud integration layers

#### AI Infrastructure & Knowledge Base (2025.06 ~ 2025.09)

- Built GPU cluster infrastructure: 3× RTX 5080, NixOS 25.11, 10G network, 17 Docker services
- Designed hierarchical AI agent system with n8n (40+ node workflows) + Supabase pgvector (2,945 document embeddings)
- Created data pipelines: Airbyte connectors for Channel.io, Notion, JIRA → PostgreSQL JSONB
- Deployed internal portal with Cloudflare Zero Trust

#### Agent Infrastructure & Tooling (2025.08 ~ Present)

- Built **pi-shell-acp**: ACP-based harness runtime for pi, connecting Codex and Claude Code with session continuity, explicit MCP injection, and entwurf sibling orchestration
- Built **agent-config**: PKM-native skill stack — 25 agent skills over notes, agenda, bibliography, health, and git history
- Designed 3-layer cross-lingual retrieval: embedding vectors + Denote dblock graph + personal vocabulary ontology (dictcli)
- Created agent-queryable CLI tools for life data and reasoning: denotecli, dictcli, gitcli, lifetract, bibcli, and **abductcli**
- Deployed **openclaw**: 4-bot Telegram agent ecosystem (Claude, GPT, Gemini) on Oracle ARM via Docker with org-mode memory search

### Self-Development & Parenting

*2022 ~ Present*

- Built and published Digital Garden with 2,174 pages ([notes.junghanacs.com](https://notes.junghanacs.com))
- Developed 10 interconnected open-source -config projects spanning NixOS, Doom Emacs, smart home, toy agents, self-hosting, and knowledge infrastructure
- Started **legoagent-config** (Pybricks + Flutter + ESP32 embodied toy-agent experiments) and **openglg-config** (self-hosted server + reproducible shell in one fork)
- Shaped a PKM-native public semantic garden — notes, bibliography, botlogs, and timeline data as shared interface surfaces for AI systems
- Created GLG-Mono: Korean programming font merging IBM Plex Mono + Sans KR with full Unicode coverage
- 5 years of quantified self-tracking data (Samsung Health + aTimeLogger), all version-controlled

### Sungkyunkwan University — Distributed Computing Lab

*2018 ~ 2021*

- Research on non-volatile memory filesystems and NUMA lock performance in virtualized environments
- Virginia Tech COSMOSS Lab exchange researcher (2019.07 ~ 2020.03)
- Publications: [notes.junghanacs.com/notes/20250317T150522](https://notes.junghanacs.com/notes/20250317T150522)

### NEMO-UX — Co-founder

*2013 ~ 2017*

- Built Linux-based large-format touch display OS for commercial/education markets
- Full embedded product lifecycle: hardware integration, OS customization, app development, mass production

---

## Education

- **Sungkyunkwan University** — Ph.D. coursework completed, Computer Science (2010 ~ 2012)
- **Sungkyunkwan University** — M.S. Computer Science (2008 ~ 2010)
- **Sejong University** — B.S. Computer Science (2004 ~ 2008)

---

## Open Source Ecosystem

| Project | Description | Tech |
|---------|-------------|------|
| [pi-shell-acp](https://github.com/junghan0611/pi-shell-acp) | ACP harness runtime for pi — Codex/Claude Code, MCP, session continuity | TypeScript |
| [agent-config](https://github.com/junghan0611/agent-config) | PKM-native memory and harness stack with 25 agent skills | TS |
| [andenken](https://github.com/junghan0611/andenken) | Recollective semantic memory (Gemini Embedding 2 · LanceDB) | TS · GraalVM |
| [homeagent-config](https://github.com/junghan0611/homeagent-config) | Matter smart home hub with on-device sLLM | Go · Flutter · Yocto |
| [legoagent-config](https://github.com/junghan0611/legoagent-config) | Embodied toy-agent stack with Pybricks, Flutter, and ESP32 | Pybricks · Flutter · ESP32 |
| [geworfen](https://github.com/junghan0611/geworfen) | Public timeline and existence-data WebTUI for the semantic garden | Clojure · GraalVM |
| [denotecli](https://github.com/junghan0611/denotecli) | Denote-Org skills for AI agents | Go |
| [durable-iot-migrate](https://github.com/junghan0611/durable-iot-migrate) | IoT platform migration with Temporal + Saga | Clojure |
| [dictcli](https://github.com/junghan0611/dictcli) | Personal vocabulary graph — 3,900+ triples, 2,400+ Korean↔English mappings | Clojure · GraalVM |
| [proxycli](https://github.com/junghan0611/proxycli) | CLI-to-OpenAI API proxy — Clojure/GraalVM native, Python→Clojure 92% reduction | Clojure · GraalVM |
| [abductcli](https://github.com/junghan0611/abductcli) | Quantitative abductive reasoning engine — anomaly → signal → memo → evaluation | Clojure |
| [nixos-config](https://github.com/junghan0611/nixos-config) | Declarative NixOS across 4 machines | Nix |
| [openglg-config](https://github.com/junghan0611/openglg-config) | Self-hosted authenticated work surface plus reproducible Debian/Ubuntu shell bootstrap | Docker · Nix |
| [doomemacs-config](https://github.com/junghan0611/doomemacs-config) | Emacs agent-server + shared org-agenda | Elisp |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) | Korean monospace font, 100% Unicode | FontForge |
| [sicm-study](https://github.com/junghan0611/sicm-study) | SICP → SICM → SDF flexible design study | Scheme · Clojure |

---

## Technical Stack

| Domain             | Technologies                                                                    |
|--------------------|---------------------------------------------------------------------------------|
| **Languages**      | Go · Clojure · Zig · C · Elisp · Nix · Bash · TypeScript                 |
| **AI/ML**          | Gemini Embedding 2 · LanceDB · semantic retrieval · sLLM workflows · Ollama |
| **IoT**            | Matter · Thread · Zigbee · MQTT · OTBR · Yocto · Flutter                  |
| **Infrastructure** | NixOS · Docker · GraalVM · GPU cluster                                       |
| **Knowledge**      | Emacs/Org-mode · Denote · BibLaTeX · Pandoc · semantic digital garden       |
| **Protocols**      | ACP · MCP · emacsclient · SSE · JSON-RPC 2.0 · REST · A2A                 |

---

## Awards

- **Prime Minister's Award** — Korea Software Competition, 2010
  - Mobile Virtualization Software (SKKU, advisor: Prof. Youngik Eom)

---

## By the Numbers

| Metric | Value |
|--------|-------|
| Org-mode notes | 3,400+ |
| Bibliography entries | 8,200+ |
| Total commits | 8,500+ |
| Recent commits (90 days, personal + work) | 2,900+ |
| Daily journal | 1,500+ days |
| Published digital garden | 2,200+ pages |
| Health tracking records | 4,400+ |
| Agent skills built | 25 |

---

*Last updated: 2026-04-27 · Suwon, South Korea*
