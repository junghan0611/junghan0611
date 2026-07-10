# Junghan Kim

**PKM-AI Harness Engineer · From Embedded Systems to Shared Agent Work Surfaces**

[junghanacs@gmail.com](mailto:junghanacs@gmail.com) · [github.com/junghan0611](https://github.com/junghan0611) · [notes.junghanacs.com](https://notes.junghanacs.com) · [linkedin.com/in/junghan-kim-1489a4306](https://www.linkedin.com/in/junghan-kim-1489a4306)

*Published online as Junghan Kim (김정한), GLG, GLGMAN, 힣, 힣맨, and 정한. One person. Much of the work below is public and searchable under those names.*

---

## How to read this résumé

This is a comprehensive résumé, not a target-specific cut. The independent work is part of the same body of evidence as the company work: ideas are built in public, then load-tested in production settings.

The manifesto at [github.com/junghan0611](https://github.com/junghan0611) is the longer version; this file compresses it into career evidence. The through-line is the vertical from embedded product work to shared agent work surfaces.

---

## Summary

I work from the firmware up to the agent loop. On one end: a Zigbee hub written in Zig, now shipping in mass production, with the server and the app I built on top of it. On the other end: a dispatch substrate that lets agent harnesses address one another, published on npm. The same person did both, and the middle is not empty — it is a reproducible NixOS/Emacs environment where humans and agents share memory, a timeline, and a set of boundaries.

This is not "full stack" in the front-end/back-end sense. It is depth across a vertical: silicon, protocol, service, interface, agent.

Current focus: PKM-native harnesses for long-term human-AI work, and standing up agents that attach to the person who owns a domain. Hands-on across Go, Clojure, Zig, C, TypeScript, Nix, and Elisp.

**Public evidence.** Agent claims are easy to fake, so each is anchored to open code: [entwurf](https://github.com/junghan0611/entwurf) for the agent loop, [homeagent-config](https://github.com/junghan0611/homeagent-config) for the embedded layer, [nixos-config](https://github.com/junghan0611/nixos-config) and [doomemacs-config](https://github.com/junghan0611/doomemacs-config) for the foundation. Company work below is closed-source; read it next to those.

---

## Career

### GoQual Inc. — Full Stack Architect

*2025.06 ~ Present*

#### Smart Home Hub — Firmware to Product (2025.12 ~ Present)

**SKS Hub** — Zigbee/Wi-Fi gateway firmware in Zig. **Shipped to mass production.**

- Rewrote a legacy C Zigbee SDK integration behind Zig's type-safe FFI layer
- Built a deterministic state machine architecture (single `HubState`, pure `transition()` functions)
- **198 commits in 30 days** across device driver, protocol, and cloud integration layers
- Aging test automation (24-hour stability verification) with Claude as pair programmer

**Productization on top of it** — the parts the original contract did not cover:

- Built the **server (Go)** and the **companion app (Flutter)** myself, extending a firmware deliverable into a whole product
- Designed one protocol served by **two interchangeable backends**: AWS IoT for connected deployments, and a local backend for closed networks — the firmware ships unmodified in both
- Multi-hub fan-out, verified on real hardware (one server, two live hubs, end-to-end)
- Mutual-TLS local broker, shadow mirroring with monotonic versioning, loopback event streaming

**Next-generation hub** — overcoming the constraints the shipped hub was built under:

- Port target moved from ARMv7/glibc with a vendor sysroot to **RISC-V (SG2000), statically linked musl**
- Extracted a **board HAL**, so the pure hub core no longer knows what board it runs on — the shipped hub becomes one backend among several
- Delegated the Zigbee transport from a directly driven radio to **Zigbee2MQTT (EFR32MG24)**
- Went **device-agnostic**: dropped seven hardcoded device-type handlers (an artifact of a 64MB RAM board) and let the device model pass through as a generic entity

#### On-Device AI Smart Home Hub (2025.09 ~ Present)

**HomeAgent** — Open-source Matter smart home hub with an on-device AI agent.

- Designed and built a Go-based Matter hub running on RPi5 + Hailo-8 NPU (Yocto) and RK3576 (Android) from a single codebase, with Flutter as the app shell
- Explored local-first AI control loops, including on-device intent handling and model preparation workflows
- Implemented BLE commissioning for Matter/Thread devices via a matterjs bridge, 5 device types, OTBR integration
- Managed 3-agent parallel development sessions: 24 commits/day, 163 tests passing, zero file conflicts — human as PM
- Cross-platform: 96% code sharing between Linux and Android deployments

**Matter wallpad (customer engagement)** — RK3576 + Android 15, ESP32-H2 as Thread RCP, AOSP-native CHIP C++ SDK with `ot-daemon`. Delivered as a versioned Android SDK (AAR) to the customer's own namespace.

**National R&D (IITP, 2025 ~ 2028)** — intelligent-home program with an AI SoC vendor. Our scope: sLLM-driven voice control, Matter integration, and porting the NPU workload across accelerator families. Currently in year two.

#### Domain-Owner Agents (2026.05 ~ Present)

The request I keep receiving from other teams is not "build me a dashboard." It is "make this run without me." So I do not build dashboards. I stand up an agent and attach it to the person who owns the domain.

- **VOC workbench** — a quantitative-abduction tool over daily customer-support data: fixes the units, periods, and inclusion policy of every number; makes evidence traceable down to a single conversation id; detects signals that differ from baseline; and leaves the residue that becomes next cycle's hypothesis. This is the production body of my open-source [abductcli](https://github.com/junghan0611/abductcli) experiment.
- **Incident workbench** — read-only evidence tool that reads live from real sources and aligns everything on a single KST time axis, rather than storing dumps. Chains the VOC → device → runtime trail.
- **Chief-of-staff agent** — a working surface that carries my own company portfolio: tracks, owners, decisions, ledger.
- **Forge connector** — agents turning conversations into durable, reviewable work items on self-hosted Forgejo. Public: [forge-config](https://github.com/junghan0611/forge-config)
- **Product security response (PSIRT)** — intake, reproduction, impact assessment, vendor escalation, and regulator/customer response for externally reported vulnerabilities

#### AI Infrastructure & Knowledge Base (2025.06 ~ 2025.09)

- Built GPU cluster infrastructure: 3× RTX 5080, NixOS 25.11, 10G network, 17 Docker services
- Designed a hierarchical AI agent system with n8n (40+ node workflows) + Supabase pgvector (2,945 document embeddings)
- Data pipelines: Airbyte connectors for Channel.io, Notion, JIRA → PostgreSQL JSONB
- Internal portal behind Cloudflare Zero Trust

#### Agent Infrastructure & Tooling (2025.08 ~ Present)

- Built **entwurf**: a garden-citizen dispatch substrate — agent harnesses (Claude Code, Codex, Antigravity, pi) address one another by id without owning each other's transcript, auth, or runtime. Published on npm.
- Built **agent-config**: PKM-native skill stack — 40+ agent skills over notes, agenda, bibliography, health, and git history
- Designed 3-layer cross-lingual retrieval: embedding vectors + Denote dblock graph + a personal vocabulary ontology (dictcli)
- Created agent-queryable CLI tools for life data and reasoning: denotecli, dictcli, gitcli, lifetract, bibcli, abductcli
- Deployed a 4-bot Telegram agent ecosystem (Claude, GPT, Gemini) on Oracle ARM via Docker with org-mode memory search

### Independent Work — Where the Ideas Come From

*2022 ~ Present*

- Built and published a digital garden of 2,200+ pages ([notes.junghanacs.com](https://notes.junghanacs.com)), backed by 3,500+ org-mode notes and 1,500+ consecutive days of journaling
- Built **memex-kb**, a document toolchain that makes Korean content machine-legible: `hwpx2org` for the Korean word processor format no toolchain wants to touch, `scanpdf2org` with vision transcription for scanned paper, `epub2org` / `html2epub`, `org2odtdoc` for the round trip back into office formats, `textlint-ko` for Korean prose linting, and a proposal pipeline. Org-mode is the meta-document everything passes through. **Every Korean organization hits this wall; I have a toolchain for it.**
- Designed **ROSSE** — the IndieWeb POSSE pattern inverted. Raw writing is struck outside where polish cannot reach it, recovered and converged in the garden, then syndicated back to every surface. memex-kb is the machinery this runs on.
- Developed 10+ interconnected open-source `-config` projects spanning NixOS, Doom Emacs, smart home, toy agents, self-hosting, and knowledge infrastructure
- Shaped a PKM-native public semantic garden — notes, bibliography, botlogs, and timeline data as shared interface surfaces for AI systems
- Run a 4-bot agent ecosystem continuously as an **exoself** rather than as per-project sessions — the reason its configuration repository stays private is that the bots' memory lives inside it
- Created GLG-Mono: a Korean programming font merging IBM Plex Mono + Sans KR with full Unicode coverage
- Quantified self-tracking since 2017 (Samsung Health + aTimeLogger), all version-controlled

### Sungkyunkwan University — Distributed Computing Lab

*2018 ~ 2021*

- Research on non-volatile memory filesystems and NUMA lock performance in virtualized environments
- Virginia Tech COSMOSS Lab exchange researcher (2019.07 ~ 2020.03)
- Publications: [notes.junghanacs.com/notes/20250317T150522](https://notes.junghanacs.com/notes/20250317T150522)

### NEMO-UX — Co-founder

*2013 ~ 2017*

- Built a Linux-based large-format touch display OS for commercial/education markets
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
| [entwurf](https://github.com/junghan0611/entwurf) | Garden-citizen dispatch substrate — agent harnesses address one another by id; meta-bridge, ACP plugin, npm | TypeScript |
| [homeagent-config](https://github.com/junghan0611/homeagent-config) | Matter smart home hub with on-device sLLM — single Go binary, RPi5 + Hailo-8 NPU and RK3576 Android | Go · Flutter · Yocto |
| [agent-config](https://github.com/junghan0611/agent-config) | PKM-native memory and harness stack, 40+ agent skills | TypeScript |
| [andenken](https://github.com/junghan0611/andenken) | Recollective semantic memory (embedding + LanceDB, cross-lingual) | TS · GraalVM |
| [geworfen](https://github.com/junghan0611/geworfen) | Public timeline and existence-data WebTUI for the semantic garden | Clojure · GraalVM |
| [nixos-config](https://github.com/junghan0611/nixos-config) | Declarative NixOS across 4 machines, 17+ Docker services | Nix |
| [doomemacs-config](https://github.com/junghan0611/doomemacs-config) | Emacs agent-server + shared org-agenda, path-guarded Elisp APIs | Elisp |
| [forge-config](https://github.com/junghan0611/forge-config) | Forgejo connector — agents leaving durable traces on code work items | TypeScript |
| [memex-kb](https://github.com/junghan0611/memex-kb) | Korean document toolchain — HWPX/scanned PDF/EPUB → Org → office formats, with Org as the meta-document | Nix · Python · Elisp |
| [abductcli](https://github.com/junghan0611/abductcli) | Quantitative abductive reasoning — anomaly → signal → memo → evaluation | Clojure |
| [dictcli](https://github.com/junghan0611/dictcli) | Personal vocabulary graph — 3,900+ triples, 2,400+ Korean↔English mappings | Clojure · GraalVM |
| [denotecli](https://github.com/junghan0611/denotecli) | Denote-Org query skills for AI agents | Go |
| [durable-iot-migrate](https://github.com/junghan0611/durable-iot-migrate) | IoT platform migration with Temporal + Saga — 62% less code than Go | Clojure |
| [openglg-config](https://github.com/junghan0611/openglg-config) | Self-hosted authenticated work surface plus reproducible shell bootstrap | Docker · Nix |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) | Korean monospace font, 100% Unicode | FontForge |
| [sicm-study](https://github.com/junghan0611/sicm-study) | SICP → SICM → SDF flexible design study | Scheme · Clojure |

---

## Technical Stack

| Domain             | Technologies                                                                    |
|--------------------|---------------------------------------------------------------------------------|
| **Languages**      | Go · Clojure · Zig · C · Elisp · Nix · Bash · TypeScript                 |
| **Embedded**       | ARM Linux · RISC-V · Yocto · static musl · board HAL · mTLS               |
| **IoT**            | Matter · Thread · Zigbee · Zigbee2MQTT · MQTT · OTBR · AWS IoT           |
| **AI/ML**          | Embedding retrieval · LanceDB · sLLM workflows · NPU deployment · Ollama   |
| **Infrastructure** | NixOS · Docker · GraalVM · GPU cluster                                       |
| **Knowledge**      | Emacs/Org-mode · Denote · BibLaTeX · Pandoc · semantic digital garden       |
| **Protocols**      | ACP · MCP · A2A · emacsclient · SSE · JSON-RPC 2.0 · REST                 |

---

## Awards

- **Prime Minister's Award** — Korea Software Competition, 2010
  - Mobile Virtualization Software (SKKU, advisor: Prof. Youngik Eom)

---

## By the Numbers

| Metric | Value |
|--------|-------|
| Org-mode notes | 3,500+ |
| Bibliography entries | 8,200+ |
| Total commits | 8,500+ |
| Daily journal | 1,500+ days |
| Published digital garden | 2,200+ pages |
| Health tracking days | 2,500+ |
| Agent skills built | 40+ |

*Rounded down from live data at [`agenda.junghanacs.com/api/stats`](https://agenda.junghanacs.com/api/stats), which serves these counts straight from the working corpus. Measured 2026-07-10.*

---

*Last updated: 2026-07-10 · Suwon, South Korea*
