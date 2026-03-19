# Junghan Kim

**Full Stack Polymath Engineer · From Embedded to On-Device AI**

[junghanacs@gmail.com](mailto:junghanacs@gmail.com) · [github.com/junghan0611](https://github.com/junghan0611) · [notes.junghanacs.com](https://notes.junghanacs.com) · [linkedin.com/in/junghan-kim-1489a4306](https://www.linkedin.com/in/junghan-kim-1489a4306)

---

## Summary

Full-stack engineer with experience spanning Linux kernel research, embedded IoT product development, and AI agent infrastructure. Currently building on-device AI systems for smart home hubs and designing semantic memory architecture for multi-agent collaboration. Work across Go, Clojure, Zig, C, and Elisp — from ARM boards to GPU clusters.

---

## Career

### GoQual Inc. — Full Stack Architect

*2025.06 ~ Present*

#### On-Device AI Smart Home Hub (2025.09 ~ Present)

**HomeAgent** — Open-source Matter smart home hub with on-device AI agent.

- Designed and built a Go-based Matter hub running on RPi5 (Yocto) and RK3576 (Android) from a single codebase, with Flutter as the app shell
- Fine-tuned Qwen3-0.6B via LoRA for IoT intent recognition: action accuracy 59.6% → **100%**, quantized to 379MB GGUF, **4-second inference on ARM**
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

#### Agent Memory & Tooling (2025.08 ~ Present)

- Built **agent-config**: semantic memory infrastructure with Gemini Embedding 2 + LanceDB, serving 25 agent skills
- Designed 3-layer cross-lingual search: embedding vectors + Denote dblock graph + personal vocabulary ontology (dictcli)
- Created 5 CLI tools for agent-queryable life data: denotecli (3,300 org files), dictcli (1,004 triples), gitcli (8,557 commits), lifetract (4,489 health records), bibcli (8,208 bibliography entries)
- Deployed 4-bot Telegram agent ecosystem (Claude, GPT, Gemini) on Oracle ARM via Docker with org-mode memory search

### Self-Development & Parenting

*2022 ~ 2025*

- Built and published Digital Garden with 2,174 pages ([notes.junghanacs.com](https://notes.junghanacs.com))
- Developed 8 interconnected open-source -config projects (NixOS, Doom Emacs, Zotero, knowledge base)
- Created GLG-Mono: Korean programming font merging IBM Plex Mono + Sans KR with full Unicode coverage
- 5 years of quantified self-tracking data (Samsung Health + aTimeLogger), all version-controlled

### Sungkyunkwan University — Distributed Computing Lab

*2018 ~ 2021*

- Research on non-volatile memory filesystems and NUMA lock performance in virtualized environments
- Virginia Tech COSMOSS Lab exchange researcher (2019.07 ~ 2020.03)
- Publications: [notes.junghanacs.com/notes/20250317T150522](https://notes.junghanacs.com/notes/20250317T150522)

### NEMO-UX — Co-founder & CTO

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
| [agent-config](https://github.com/junghan0611/agent-config) | 25 agent skills + configuration | TS |
| [andenken](https://github.com/junghan0611/andenken) | Recollective semantic memory (Gemini Embedding 2 · LanceDB) | TS · GraalVM |
| [homeagent-config](https://github.com/junghan0611/homeagent-config) | Matter smart home hub with on-device sLLM | Go · Flutter · Yocto |
| [geworfen](https://github.com/junghan0611/geworfen) | Existence data WebTUI viewer | Clojure · GraalVM |
| [denotecli](https://github.com/junghan0611/denotecli) | Denote-Org skills for AI agents | Go |
| [durable-iot-migrate](https://github.com/junghan0611/durable-iot-migrate) | IoT platform migration with Temporal + Saga | Clojure |
| [dictcli](https://github.com/junghan0611/dictcli) | Personal vocabulary graph (Korean↔English↔German) | Clojure · SQLite |
| [proxycli](https://github.com/junghan0611/proxycli) | CLI-to-OpenAI API proxy — Clojure/GraalVM native, Python→Clojure 92% reduction | Clojure · GraalVM |
| [nixos-config](https://github.com/junghan0611/nixos-config) | Declarative NixOS across 4 machines | Nix |
| [doomemacs-config](https://github.com/junghan0611/doomemacs-config) | Emacs agent-server + shared org-agenda | Elisp |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) | Korean monospace font, 100% Unicode | FontForge |
| [sicm-study](https://github.com/junghan0611/sicm-study) | SICP → SICM → SDF flexible design study | Scheme · Clojure |

---

## Technical Stack

| Domain | Technologies |
|--------|-------------|
| **Languages** | Go · Clojure · Zig · C · Elisp · Nix · Bash · TypeScript |
| **AI/ML** | sLLM fine-tuning (LoRA/GGUF) · Gemini Embedding 2 · LanceDB · Ollama · OpenRouter |
| **IoT** | Matter · Thread · Zigbee 3.0 · MQTT · OTBR · Yocto · Flutter |
| **Infrastructure** | NixOS · Docker · GraalVM · GPU cluster (CUDA) |
| **Knowledge** | Emacs/Org-mode · Denote · BibLaTeX · Pandoc |
| **Protocols** | emacsclient · SSE · JSON-RPC 2.0 · REST · A2A |

---

## Awards

- **Prime Minister's Award** — Korea Software Competition, 2010
  - Mobile Virtualization Software (SKKU, advisor: Prof. Youngik Eom)

---

## By the Numbers

| Metric | Value |
|--------|-------|
| Commits (30 days, 2026 Q1) | 1,092 |
| Active repos (30 days) | 31 |
| Org-mode notes | 3,295 |
| Bibliography entries | 8,208 |
| Total commits | 8,557 |
| Daily journal | 718 days |
| Published digital garden | 2,174 pages |
| Health tracking records | 4,489 |
| Agent skills built | 25 |

---

*Last updated: 2026-03-20 · Suwon, South Korea*
