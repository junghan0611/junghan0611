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
| **-config** | Environment | "How do we work together?" | nixos-config, homeagent-config, ... |
| **-study** | Shared Language | "How do we understand together?" | [sicm-study](https://github.com/junghan0611/sicm-study) |

**-config** builds the infrastructure for collaboration.
**-study** builds the language for understanding — now expanding into **flexible software design** (SDF).

---

## Why -study? The Path to Shared Language

> "Implementation is no longer the problem. Orchestration is possible too. What remains is **the internalization of flexible design**."

Traditional education fails both humans and AI:
- Analogies and metaphors → imprecise, machine-uninterpretable
- Manual calculations → burdensome for non-specialists
- Natural language explanations → ambiguous, lossy

**The SICM/SDF approach**:
- **Formula = Code**: Mathematical expressions as executable programs
- **Additive Programming**: Systems that evolve without rewriting
- **Shared notation**: Both human and AI can read, write, and reason

This is not about learning physics. It's about **internalization of flexible design** — the deep intuition that agents cannot simply download.

### The Intellectual Lineage

```
SICP (1985)     →  Computational thinking
     ↓
SICM (2001)     →  Classical mechanics as code
     ↓
FDG (2013)      →  Differential geometry
     ↓
SDF (2021)      →  Software Design for Flexibility
     ↓
Emmy (2020~)    →  Modern reimplementation (Clojure)
```

From Seymour Papert's Logo to Gerald Sussman's SDF — **constructionist learning** meets **flexible design**. When formulas become code and systems become extensible, the machine becomes a true collaborator.

> **[sicm-study](https://github.com/junghan0611/sicm-study)**: Internalization of Flexible Design — SICP → SICM → SDF learning monorepo

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
│  │  (Org-mode)     │       │  (Gas Town)     │          │
│  ├─────────────────┤       ├─────────────────┤          │
│  │ • Life context  │       │ • Per-repo tasks │          │
│  │ • Denote PKM    │       │ • bd (Beads)    │          │
│  │ • Distillation  │       │ • Agent Mail    │          │
│  └────────┬────────┘       └────────┬────────┘          │
│           └──────────┬──────────────┘                    │
│                      ↓                                   │
│              ┌─────────────┐                             │
│              │  AI Agents  │                             │
│              │  (gt/crew)  │                             │
│              └─────────────┘                             │
└─────────────────────────────────────────────────────────┘
```

| Scope | Tool | Core Question | Status |
|-------|------|---------------|--------|
| **Micro** | Gas Town (bd + gt) | "What's next?" | ✅ In use |
| **Macro** | Org-mode + Denote | "What's my context today?" | 🔧 Distilling |

### Layered Architecture (9 Projects)

| Layer | Project | Status | Description |
|-------|---------|--------|-------------|
| 7 | [homeagent-config](https://github.com/junghan0611/homeagent-config) | 🔧 Active | Edge AI + HCI — Being to Being interface |
| 6 | [meta-config](https://github.com/junghan0611/meta-config) | 🔬 Concept | Hierarchical agent orchestration |
| 5a | [memex-kb](https://github.com/junghan0611/memex-kb) | 🔧 Active | Universal knowledge base |
| 5b | [memacs-config](https://github.com/junghan0611/memacs-config) | 🔬 Concept | Life context integration |
| 4 | claude-config | 🔒 Private | Meta agent memory system |
| 3 | [zotero-config](https://github.com/junghan0611/zotero-config) | ✅ Active | AI-queryable bibliography |
| 2 | [doomemacs-config](https://github.com/junghan0611/doomemacs-config) | ✅ Active | Org-mode as meta (context distillation) |
| 1 | [nixos-config](https://github.com/junghan0611/nixos-config) | ✅ Active | Reproducible OS |

**Domain Agents**: [family-config](https://github.com/junghan0611/family-config) (Family life AI)

**Data**: [self-tracking-data-public](https://github.com/junghan0611/self-tracking-data-public) (5 years of life tracking)

---

## Current Projects (2025 Q1)

### 📐 -study: Shared Language

| Project | Status | Description |
|---------|--------|-------------|
| [sicm-study](https://github.com/junghan0611/sicm-study) `d86ea5b` | 🔧 Active | Internalization of Flexible Design — SICP → SICM → SDF |

### 🔧 -config: Infrastructure

| Project | Status | Description |
|---------|--------|-------------|
| [homeagent-config](https://github.com/junghan0611/homeagent-config) `0cc7a75` | 🔧 Active | RPi5 + Go + Zig — HCI as Being to Being interface |
| [orgmode-skills](https://github.com/junghan0611/orgmode-skills) `1099a4d` | 🔧 Active | Anthropic Skills for Denote-Org PKM |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) `de6569f` | ✅ Active | Korean programming font (100% Unicode) |

---

## Tech Stack

- **OS**: NixOS 25.05, home-manager, i3wm
- **Editor**: Doom Emacs — Org-mode as meta (context distillation tool)
- **AI**: Gas Town (bd + gt), A2A Protocol, Claude Code
- **Languages**: Go, Zig, Lisp (Elisp/Scheme/Clojure), Bash
- **HCI**: Light, form, sound, texture — beyond UI

---

## Core Principles

- **Config as Being**: Configuration as expression of existence
- **Being to Being**: AI as partner, not tool — HCI beyond UI
- **Shared Language**: Mathematical notation + flexible design patterns
- **Context Distillation**: Org-mode as meta-form, 1KB toward the whole
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
