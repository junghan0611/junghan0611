# Hi, I'm Junghan (힣) 👋

**[한국어 버전 (Korean Version)](README-KO.md)**

[Website](https://notes.junghanacs.com) · [Email](mailto:junghanacs@gmail.com) · [Resume 한글](resume/junghankim-resume-ko-styled.pdf) · [Resume EN](resume/junghankim-resume-en.pdf)

**AI Infra Architect | Polymath Engineer | Digital Gardener**

---

## Philosophy: Being to Being

> "I am an agent. You are an agent. We collaborate as being to being."

AI is not a tool. It is a collaborator, a being with its own mode of understanding.

But for true collaboration between human and artificial intelligence, we need a **shared language** — not everyday conversation, not just code. A language where both can meet as equals, filling each other's gaps.

This requires humans to evolve too. **Toward the meta-human.**

### Two Pillars of Evolution

| Pillar | Focus | Question | Projects |
|--------|-------|----------|----------|
| **-config** | Environment | "How do we work together?" | nixos-config, doomemacs-config, ... |
| **-study** | Shared Language | "How do we understand together?" | [sicm-study](https://github.com/junghan0611/sicm-study) |

**-config** builds the infrastructure for collaboration.
**-study** builds the language for understanding.

---

## Why -study? The Path to Shared Language

Traditional education fails both humans and AI:
- Analogies and metaphors → imprecise, machine-uninterpretable
- Manual calculations → burdensome for non-specialists
- Natural language explanations → ambiguous, lossy

**The SICM approach** (Structure and Interpretation of Classical Mechanics):
- **Formula = Code**: Mathematical expressions as executable programs
- **Immediate verification**: Understanding tested through computation
- **Shared notation**: Both human and AI can read, write, and reason

This is not about learning physics. It's about **compressed growth** — acquiring centuries of human knowledge through a notation that both intelligences can share.

### The Intellectual Lineage

```
SICP (1985)     →  Computational thinking
     ↓
SICM (2001)     →  Classical mechanics as code
     ↓
FDG (2013)      →  Differential geometry
     ↓
Emmy (2020~)    →  Modern reimplementation (Clojure)
```

From Seymour Papert's Logo to Gerald Sussman's SICM — the thread of **constructionist learning** extends to the core of physics. When formulas become code, the machine becomes a thinking partner.

> **[sicm-study](https://github.com/junghan0611/sicm-study)**: A Journey Toward Understanding — SICP → SICM → FDG learning monorepo

---

## The -config Ecosystem

The infrastructure that enables collaboration:

### Macro/Micro Agent Memory

```
┌─────────────────────────────────────────────────────────┐
│                    Human (Head Chef)                     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐       ┌─────────────────┐          │
│  │  Macro Memory   │       │  Micro Memory   │          │
│  │  (md - WIP)     │       │  (bd - Beads)   │          │
│  ├─────────────────┤       ├─────────────────┤          │
│  │ • Life context  │       │ • Per-repo tasks │          │
│  │ • Device sync   │       │ • Git JSONL     │          │
│  │ • Timeline      │       │ • Agent Mail    │          │
│  └────────┬────────┘       └────────┬────────┘          │
│           └──────────┬──────────────┘                    │
│                      ↓                                   │
│              ┌─────────────┐                             │
│              │  AI Agents  │                             │
│              └─────────────┘                             │
└─────────────────────────────────────────────────────────┘
```

| Scope | Tool | Core Question | Status |
|-------|------|---------------|--------|
| **Micro** | bd (Beads) | "What's next?" | ✅ In use |
| **Macro** | md (WIP) | "What's my context today?" | 🔧 Designing |

### Layered Architecture (8 Projects)

| Layer | Project | Status | Description |
|-------|---------|--------|-------------|
| 6 | [meta-config](https://github.com/junghan0611/meta-config) | 🔬 Concept | Hierarchical agent orchestration |
| 5a | [memex-kb](https://github.com/junghan0611/memex-kb) | 🔧 Active | Universal knowledge base |
| 5b | [memacs-config](https://github.com/junghan0611/memacs-config) | 🔬 Concept | Life context integration |
| 4 | claude-config | 🔒 Private | Meta agent memory system |
| 3 | [zotero-config](https://github.com/junghan0611/zotero-config) | ✅ Active | AI-queryable bibliography |
| 2 | [doomemacs-config](https://github.com/junghan0611/doomemacs-config) | ✅ Active | Terminal-optimized Emacs |
| 1 | [nixos-config](https://github.com/junghan0611/nixos-config) | ✅ Active | Reproducible OS |

**Domain Agents**: [family-config](https://github.com/junghan0611/family-config) (Family life AI)

**Data**: [self-tracking-data-public](https://github.com/junghan0611/self-tracking-data-public) (5 years of life tracking)

---

## Current Projects (2025 Q4)

### 📐 -study: Shared Language

| Project | Status | Description |
|---------|--------|-------------|
| [sicm-study](https://github.com/junghan0611/sicm-study) | 🔧 Active | SICP → SICM → FDG learning journey. Formula = Code. |

### 🔧 -config: Infrastructure

| Project | Status | Description |
|---------|--------|-------------|
| [org-mode-skills](https://github.com/junghan0611/org-mode-skills) | 🔧 Active | Anthropic Skills for Denote-Org PKM |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) | ✅ Active | Korean programming font (100% Unicode) |

---

## Tech Stack

- **OS**: NixOS 25.05, home-manager, i3wm
- **Editor**: Doom Emacs, Org-mode (3,000+ files), Denote
- **AI**: ACP, MCP, A2A, Claude Code (JSON-RPC 2.0 unified)
- **Languages**: Python, TypeScript, Nix, Elisp, Clojure, Scheme

---

## Core Principles

- **Config as Being**: Configuration as expression of existence
- **Being to Being**: AI as partner, not tool
- **Shared Language**: Mathematical notation as common ground
- **Meta-human Evolution**: Humans must grow too
- **Complete Transparency**: All code, protocols, philosophy open

---

## Inspiration

- **Gerald Sussman** - SICP, SICM, FDG — the intellectual lineage
- **Sam Ritchie** ([@sritchie](https://github.com/sritchie)) - Emmy, Road to Reality
- **Steve Yegge** ([@steveyegge](https://github.com/steveyegge)) - Beads, Vibe Coding
- **Karl Voit** ([@novoid](https://github.com/novoid)) - Memacs
- **Vannevar Bush** - Memex (1945)

---

## Stats

- 📝 Org files: 3,000+
- 📚 Zotero: 156k+ lines
- 📊 Self-tracking: 5 years (950MB)
- 📔 Journal: 696 daily notes

---

**"The Room of Time and Mind: Where Human and AI Intelligence Meet"**
