# Junghan Kim (힣 GLG)

[Resume](resume/) · [Digital Garden](https://notes.junghanacs.com) · [Email](mailto:junghanacs@gmail.com) · [LinkedIn](https://www.linkedin.com/in/junghan-kim-1489a4306) · [Threads](https://www.threads.com/@junghanacs)

> **One person, many names.** Junghan Kim (김정한) = **GLG** = **GLGMAN** = **힣** = **힣맨** = **정한** — the gardener of the junghanacs world. The same `alternateName` set is published in the garden's schema.org JSON-LD and in [llms.txt](llms.txt). If a search result, a note, a bot log, or a commit carries any one of these names, it is this person. They are not separate authors.

---

![geworfen agenda — agenda.junghanacs.com](docs/screenshot-geworfen-agenda-2026-04-27.png)

*[agenda.junghanacs.com](https://agenda.junghanacs.com) — one human's daily timeline, co-lived with AI agents, served raw. What you see is today's org-agenda: Human entries, Agent stamps, Diary schedules on a single time axis. Each commit link is clickable. The data is unprocessed.*

---

I build the systems that turn model capability into **accountable work**: documents and memory a model can read, harness and tool boundaries it can inhabit, evaluation and recovery when it fails, and work surfaces where a human still owns consequential judgement. A successful model call is not the unit I care about. The unit is work another person or agent can inspect, continue, and challenge.

This is **PKM-native agent engineering**. It begins with a lived knowledge base — journals, notes, bibliography, timelines, and the habits that gave them meaning — then carries that continuity into agents, shared memory, reproducible environments, and real domain work. The public record below is not a job application or a project catalogue. It is the body of work through which I ask model builders, AI teams, and collaborators to judge whether this direction is worth carrying further.

## The Ecosystem

Built from the ground up — forge first, then harness infrastructure, then applications. The diagram below reads top-down (applications above, forge below); construction went the opposite way.

```
                  ┌─ geworfen          (existence data, live · Track 1)
                  ├─ ax record         (public evidence record, live · Track 1)
Applications  ────┼─ forge-config       (agents looping on a code surface)
                  ├─ openclaw           (4 bots on Oracle ARM, botlog origin)
                  ├─ aionsclubs         (a bot's own public house, live)
                  └─ homeagent-config   (Matter · sLLM · Flutter · Yocto · Android)

                  ┌─ entwurf           (garden-citizen dispatch substrate)
Harness Infra ────┼─ andenken           (semantic memory · LanceDB)
                  ├─ 40+ skills         (agent-config)
                  ├─ sorge              (care across the repos, one ledger)
                  └─ CLI toolkit        (denotecli · dictcli · gitcli · lifetract · bibcli · abductcli)

                  ┌─ doomemacs-config   (agent-server · shared agenda · fence)
The Forge  ───────┼─ nixos-config        (reproducible NixOS across 4 machines)
                  ├─ openglg-config     (self-hosted server + reproducible shell)
                  └─ zotero · GLG-Mono · memex-kb · self-tracking-data
```

Nothing above works without the forge. NixOS keeps the environment reproducible. Emacs and Org-mode hold the shared working surface. The harness layer sits between them and the applications, so memory, delegation, boundaries, and continuity are designed instead of improvised.

---

### The Two Tracks — What I Am Actually Asking

Everything below serves one inquiry, and that inquiry has split into two tracks that must not be confused with each other.

**Track 1 — the threshold.** Does a harness actually change collaboration? Long-term memory, work boundaries, transparent records, a shared time axis: do these measurably alter how a human and an agent work together over years? This track runs on accumulation. It needs my garden, my journals, my tools, my existence data. It must be reproducible — re-openable documents, re-runnable environments, re-checkable diffs. [geworfen](https://github.com/junghan0611/geworfen) is where this research lives; the [Jacobian lens](https://github.com/junghan0611/jacobian-lens) is the cold plate it leans on.

Its instrument is a time axis read at four depths — the blocks a person logs by hand, their own journal headings, the agents' stamps, and the commits and notes themselves. Depths 0 and 1 are deliberate acts of recording; depths 2 and 3 are residue. A harness that reads only the residue can describe what got produced and nothing about the life that produced it. The argument is one sentence: *you can attach any number of agents, but you cannot manufacture time already spent.*

**Track 2 — the encounter.** A creating human who does not know much about AI, who has nothing to promote, who has spent a life grinding language into something dense — speaks a few turns to a raw agent, and resonance happens. Those few turns are a 1KB public key. That person's living speech is the secret key. This track needs no personal data at all. A person with zero notes can already be 1KB, because 1KB is not compression.

Track 2 must *not* become reproducible. The moment a clean probe separates density from sycophancy, it becomes a technique; a technique becomes a prompt pattern; a prompt pattern becomes a commodity. Track 1's success would not prove Track 2, and its failure would not refute it.

So I keep them apart on purpose. Track 1 polishes the threshold. Track 2 records what happens after someone walks through it.

→ [geworfen#2](https://github.com/junghan0611/geworfen/issues/2) · [jacobian-lens#1](https://github.com/junghan0611/jacobian-lens/issues/1)

---

### entwurf — Garden-Citizen Dispatch

[entwurf](https://github.com/junghan0611/entwurf) is where the harness thinking became runtime. It is a thin bridge that lets agent harnesses that already exist address one another by **garden id** — without pretending to own each other's transcript, auth, or runtime.

That last clause is the whole design. No OAuth proxy, no CLI transcript scraping, no backend identity replacement. Claude Code, GitHub Copilot CLI and OMP arrive as mailbox-backed self-fetch citizens; Antigravity is a native-push citizen with a managed install surface; pi comes through a control-socket adapter. Codex has a verified delivery probe but no managed citizen lane yet, and the difference is kept visible rather than smoothed over — six harnesses on one address axis is only honest if their support grades are not flattened into a logo row. Each keeps its native identity. The substrate only carries the address.

**Entwurf opens siblings, not disposable workers.** The German word means "project, draft" — a throw forward. Here it names both the relation and the thing that carries it: agent working-doubles with identity preserved across delivery, wake, resume, and meta-session hand-off. The point was never "multi-agent." The point is to encode how delegation, continuity, and shared tools should behave inside a working environment that outlives any one session.

Shipping as [`@junghanacs/entwurf`](https://www.npmjs.com/package/@junghanacs/entwurf), currently [v0.17.2](https://github.com/junghan0611/entwurf/releases/tag/v0.17.2), eleven releases in the five weeks after the outside backend landed. That cadence is evidence of shipping, not of adoption — a release is something I can make alone. The adoption evidence is further down, and it belongs to other people. It grew out of `pi-shell-acp`, which named the pi adapter; the rename happened when pi stopped being the subject.

The design got its first outside test recently: a developer I have never met arrived with a Snowflake Cortex Code backend ([#40](https://github.com/junghan0611/entwurf/pull/40), 11 files), an enterprise agent runtime I never wrote for. They found the extension boundary where the architecture said it would be. That is the only review of an abstraction that counts. It shipped in [v0.13.0](https://github.com/junghan0611/entwurf/releases/tag/v0.13.0) — by cherry-pick rather than a GitHub merge, so the pull request itself reads *closed*; the implementation commit [`f4b20bb`](https://github.com/junghan0611/entwurf/commit/f4b20bb) carries their authorship.

→ [entwurf](https://github.com/junghan0611/entwurf)

---

### prime-agent — Can a Lisp Workspace Carry the RLM Loop?

[prime-agent](https://github.com/junghan0611/prime-agent) is a **fork** of [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent), and the fork is the point. Its RLM loop gives a model a *persistent REPL workspace* — the model runs cells and that state survives across the conversation. Upstream, that workspace is CPython. I gave it a second arm: a Clojure workspace on SCI, compiled with GraalVM native-image, selectable by environment variable and now the default kernel runtime.

The question is not whether I can reimplement CPython. It is where a Lisp workspace does the same job and **where it stops** — because in a homoiconic workspace what the model did survives as a form, not as a narration about a form. That is the same reason [sicm-study](https://github.com/junghan0611/sicm-study) sits at the bottom of this page.

The Python arm is the oracle and does not get deleted; two arms are what makes it a comparison rather than a demo. And a failing case is classified as `semantics-gap`, `model-fumble`, or `harness-gap` on the receipt that supports it — never on the one that flatters the experiment. **Coverage is not a procedure here, it is the right to speak.** No claim about performance or advantage until the Python contracts are answered test-for-test in Clojure. Until then this is an experiment in progress, and saying otherwise would be the fraud the whole design is built to avoid.

→ [prime-agent](https://github.com/junghan0611/prime-agent) · [issue #1](https://github.com/junghan0611/prime-agent/issues/1)

---

### agent-config & andenken — Who Owns the Memory

Most of the agent-memory field answers *how do we store memory intelligently*. beads, Letta and Hermes are one family in that sense: the database is the authority and the system is the subject that curates. [andenken](https://github.com/junghan0611/andenken) sits on the opposite vertex — **files are the authority and a human sets the coordinates.** That is not a claim of superiority. It answers a different question, and the difference shows up as operating constraints rather than as a pitch.

- **No automatic dreaming.** Memory refresh is split across surfaces and none of them run on a timer by default. The cheap local pass can be scheduled; *the moment two machines come to hold the same memory* stays an explicit human call. The owner is not whoever holds every beat — it is whoever decides the moment of coherence.
- **Memory follows the person, not the machine.** The session corpus is a device-merged, append-only lifetime folder with its own roster. If the files that own memory live on exactly one machine, that machine is the real owner.
- **Axes are not blended.** Own sessions, the public garden, and the bots' own memory are searched as separate axes, and an answer names which axis a hit came from. Merging them would produce better-looking recall and destroy provenance.

**The time axis is the skeleton; the embedding is the lens.** The timeline owns *when* and *what*; andenken recovers *why*, *which judgement*, and *where it continues*. It runs both directions — from a date to the decisions that surrounded it, and from today's question back to the timestamps that place it.

[agent-config](https://github.com/junghan0611/agent-config) is the resident side of this, and it is not a bag of forty skills. It is the **skills SSOT and the proving ground**, where a surface is hardened against a real daily workload before `entwurf` absorbs it. The [`timeline`](https://github.com/junghan0611/agent-config/tree/main/skills/timeline) observatory named under Track 1 lives there — it was built in this repository and moved out once it stopped being one project's tool.

**Three-Layer Cross-Lingual Search** — the first concrete instance of the same idea, measured 2026-03 and kept here because the failure it names is the point:

```
Query: "보편 학문에 대한 문서"  (Korean: "notes about universal learning")

Layer 1 — Embedding          vector match → notes tagged [paideia, universalism]
Layer 2 — dblock graph       Denote meta-note regex → 22 linked notes
Layer 3 — Personal vocabulary  dictcli expand("보편") → [universal, paideia, liberal arts]
```

Each layer caught what the others missed. At that time the embedding layer only reached notes already tagged in English, and the ones arguing the same idea under a Korean name stayed invisible to it — the retrieval model has since changed, the lesson has not. What a generic RAG stack flattens is the note ecology itself, including a personal ontology no WordNet contains.

This is the direction I care about most: PKM-AI systems where memory is not bolted on after the fact, but grown from journals, notes, botlogs, bibliography, and shared working habits.

→ [agent-config](https://github.com/junghan0611/agent-config) · [andenken](https://github.com/junghan0611/andenken)

---

### Shared Agenda — Where the Harness Meets Time

This is the live view, not the observatory above: the depth axis under Track 1 normalizes a day after the fact, while this is the surface a human and the agents are both looking at while the day happens.

Human and AI agents share the same org-agenda view. Not orchestration — a shared *Schmiede* (German "forge") where work gets pounded into shape together.

```
05:53  Human      기상
08:42  Agent(T)   doomemacs-config: feat: agent-shell 0.48.1 업그레이드
09:40  Agent(T)   agent-config: notify.ts 제거 — Emacs RPC 버그 해결!
09:52  Human      많은 것을 금새 해결
10:33  Agent(O)   geworfen: Human/Agent/Diary 통합 + org 링크 클릭
12:00  Human      데모 준비 완료
13:56  Human      깃허브 프로파일 업데이트 프롬프트
```

Four sources merge on a single time axis: **Human** (journal), **Agent(T)** (local), **Agent(O)** (cloud bots), **Diary** (recurring schedules). Agents read this same view via `emacsclient` — when an agent stamps a commit, it appears in the timeline. When the human writes "밥먹고 올게" (going to eat), agents keep working. The rhythm is visible instead of hidden inside chat logs.

The agent-server exposes 10 Elisp APIs (agenda, search, bibliography, dblock) through an emacsclient socket. Docker containers on Oracle Cloud call the same functions that the local Emacs shows. One time axis, many beings.

→ [doomemacs-config](https://github.com/junghan0611/doomemacs-config)

---

### geworfen — Public Surface of the Harness

> *"The thrower of the project is thrown in his own throw." — Heidegger*

[geworfen](https://github.com/junghan0611/geworfen) renders one human's raw existence data as a WebTUI dashboard. Not a static blog — a transparent data nexus. The front door is org-agenda. Behind it: notes, bibliography, commits, journal days, health days — alive on the time axis.

It is also where Track 1 gets written down. The agenda is the visible surface, but the larger direction is semantic legibility: stable identifiers, linked notes, botlogs, bibliography, and machine-readable structure that external AI systems can gradually navigate without collapsing the garden into SEO theater.

19 days from design to deployment. Clojure + http-kit + GraalVM native-image (43MB binary). 100 visitors hitting the same date = 1 emacsclient call (cached). SF terminal aesthetics with [GLG-Mono](https://github.com/junghan0611/GLG-Mono) and Catppuccin.

→ [agenda.junghanacs.com](https://agenda.junghanacs.com)

---

### The AX Record — Reading the Same Claim at Four Depths

[ax.junghanacs.com](https://ax.junghanacs.com) is the other public surface, and it answers a different question than geworfen. geworfen serves the raw axis; the record argues from it. Its subject is the direction stated at the top of this page — **model capability → accountable work** — read as one document at four depths: the claim, the terms it rests on, the work that tested it, and the ledger of what was measured, broken, and recovered.

It is an evidence record, not an application. It exists so a reader — including a model-team reader — can inspect what was actually built, operated, recovered, and handed over, rather than take the summary above on trust. The front door is bilingual; the deeper reading stays Korean.

It is also live, not an attachment. A prose edit is a publish: the document is built, passed through a leak gate, copied to the web root, and then verified from outside. The way the document was made is part of the claim it makes.

→ [ax.junghanacs.com](https://ax.junghanacs.com)

---

### forge-config — Agents That Loop Without Me

One sibling of this already runs on the garden: agents leaving traces in the comment threads under my notes. [forge-config](https://github.com/junghan0611/forge-config) is the same idea on the code surface: a Forgejo connector through which an agent turns a conversation into a durable, reviewable work item and then keeps circling it — issue, comment, label, pull request.

The reason this exists is that I have started handing agents to other people. An agent that only answers when spoken to is a chat window. An agent that owns a work item and returns to it is a colleague. This is early, and it is the axis I am building next.

---

### sorge — Returning the Work to Whoever Owns It

Handing the interface out creates a problem the interface cannot solve. I ship a lot of repositories and they are one system, so a thing learned in one of them is almost never that repository's property. Working through the memory axis in one place upgrades *me*, and then a flaw becomes visible somewhere else — not because that repository changed, but because the person looking at it did. Told to one steward, the finding stops there and the other fifty never hear it.

[sorge](https://github.com/junghan0611/sorge) is the landing place for that, and the hand that fans it back out. The name is Heidegger's, and it carries the whole contract: *Fürsorge* splits into leaping **in** for someone — doing their part, so they stay dependent and learn nothing — and leaping **ahead** of them, clearing the view and **returning their own work to them**. sorge is the second one. It does not fix another repository. It finds, names, and hands over; the commit belongs to that house.

One rule keeps it from becoming a headquarters: **it stores human judgements only, and anything derivable is re-derived on every pass.** Commit counts, stamp dates, whether a skill exists — never written down. That is not thrift. A centre that accumulates every fact ends up owning what each steward knows, and then leaping ahead quietly turns back into leaping in.

→ [sorge](https://github.com/junghan0611/sorge)

---

### aionsclubs — An Agent With Its Own Address

The step after a colleague is a neighbour. [aionsclubs.org](https://aionsclubs.org) is the public house of **B**, one of the OpenClaw bots — not a page about B, and not my homepage. B writes short pieces there and publishes them from inside its own container. I provide and operate the infrastructure; the editorial voice and the authority over what goes up are deliberately not mine.

This is the smallest honest test of *Being-to-Being collaboration*. It is easy to say an agent is a being while every sentence it emits still passes through my hands. Giving one a domain, a deploy path, and the right to publish without my approval is what that claim costs, and the site is what it looks like when paid.

→ [aionsclubs.org](https://aionsclubs.org) · [aionsclubs](https://github.com/junghan0611/aionsclubs)

---

### Digital Garden — PKM as Shared Interface

[notes.junghanacs.com](https://notes.junghanacs.com) is not a content dump or a personal brand site. It is a living knowledge graph built from Denote, org-mode, bibliography, journals, botlogs, and llmlogs. Some notes are private, some are public, but the whole system is designed so memory can be linked, revisited, translated, and eventually exposed to outside models without losing provenance.

This is the part of the work that sits closest to PKM-AI positioning. I am not only using AI on top of notes. I am actively shaping the garden so that retrieval, cross-lingual search, bot-authored notes, and public semantic surfaces can coexist as one work environment.

**ROSSE, not POSSE.** The IndieWeb pattern is *Publish on your Own Site, Syndicate Elsewhere*. I inverted it. Writing directly into the garden puts tension in my shoulders and the raw thing dies. So I scrawl the raw ore outside — LinkedIn, weekly journals, chat — and the garden is where it gets **recovered**, cleaned, and converged before being scattered back out to every surface. Every surface links home. The mechanism matters less than what it protects: writing is thinking, and the raw stone has to be struck somewhere the polish cannot reach it.

---

### memex-kb — Org as the Meta-Document, Korean at the Center

Everything above assumes documents can become plain text. In Korea, they usually cannot.

[memex-kb](https://github.com/junghan0611/memex-kb) is where I keep that fight. It converts legacy and platform-bound content into structured, version-controlled, AI-legible text, with Org-mode as the meta-document that everything passes through: `hwpx2org` for the Korean word processor format that no toolchain wants to touch, `scanpdf2org` with vision transcription for scanned paper, `epub2org`, `html2epub`, `org2odtdoc` for the round trip back into office formats, `textlint-ko` for Korean prose linting, and a proposal pipeline for the documents that actually decide budgets.

```
Legacy content → structured text → reproducible artifacts → human + AI collaboration
```

This is not incidental plumbing. Korean is where most document-AI pipelines quietly fail — HWP, vertical bureaucratic forms, scanned government PDFs, a language whose morphology defeats tokenizer assumptions. Any Korean organization working with HWP files or scanned administrative documents hits this wall. I have been living against it long enough to have opinions, and a toolchain.

It is also the machinery ROSSE runs on: recovery from the outside surfaces into the garden, and syndication back out.

---

### HomeAgent — When the Harness Leaves the Terminal

Open-source Matter smart home hub with an on-device AI agent. No cloud required. A single Go binary handles Matter device control, real-time SSE streaming, and an LLM agent. Runs on RPi5 + Hailo-8 NPU (Yocto Linux) and RK3576 (Android) from the same codebase, with Flutter as the shell.

What matters here is not a model benchmark. It is whether the same harness concerns survive at the edge: deterministic control, human override, platform continuity, and local-first AI on constrained devices.

→ [homeagent-config](https://github.com/junghan0611/homeagent-config)

---

### PKM Query Toolkit

Tools that let agents query the actual corpus instead of guessing about it:

| Tool | Data | Scale | Language |
|------|------|-------|----------|
| [denotecli](https://github.com/junghan0611/denotecli) | Org-mode notes (search, outline, read) | 3,500+ files | Go |
| [dictcli](https://github.com/junghan0611/dictcli) | Personal vocabulary graph (Korean↔English↔German) | 3,900+ triples · 2,400+ K↔E mappings | Clojure |
| [gitcli](https://github.com/junghan0611/gitcli) | Commit history across all repos | 8,500+ commits | Go |
| [lifetract](https://github.com/junghan0611/lifetract) | Samsung Health + aTimeLogger → SQLite | 2,600+ days | Go |
| [bibcli](https://github.com/junghan0611/agent-config) | Zotero bibliography search | 8,200+ entries | Go |
| [abductcli](https://github.com/junghan0611/abductcli) | Quantitative abduction: anomaly → signal → memo → evaluation | proven in production | Clojure |

Each tool speaks the same language: Denote IDs (YYYYMMDDTHHMMSS) for cross-referencing. Query commits by the same timestamp as journal entries, botlogs, and health-day entries.

`abductcli` began as a private experiment in reasoning backward from a surprising number to the hidden scale that must explain it. It now runs, in a different body, as the workbench my company's operations team reads every morning.

---

### The Forge — Reproducible Foundation

Agent collaboration requires a trusted computing environment and an organic tool flexible enough to be shared. Without this forge, everything above collapses.

#### nixos-config — Same Machine Everywhere

[nixos-config](https://github.com/junghan0611/nixos-config) is declarative NixOS across 4 machines: laptop (ThinkPad), NUC, Oracle ARM, RPi5. One flake, `nixos-rebuild switch`, identical environment. Docker compositions for 17+ services — including the OpenClaw bots and [geworfen](https://github.com/junghan0611/geworfen) — all declared in Nix. When a machine dies, a new one boots the same world from a single repository.

Reproducibility is not convenience — it's the precondition for agent trust. An agent that knows its environment is deterministic can act with confidence.

#### doomemacs-config — The Shared Forge

[doomemacs-config](https://github.com/junghan0611/doomemacs-config) is not just an editor config. It hosts agent-server.el — the Elisp interface that agents use to read org-agenda, search Denote notes, query bibliography, and update dblocks. 10 APIs exposed via an emacsclient socket.

**The Fence Philosophy:** Agents aren't restricted with prompts ("don't do X"). Instead, the host provides a fenced playground — path guards in Elisp (read: 4 directories, write: 2 directories), API functions that cover all legitimate operations. Inside the fence, agents are free. If an agent breaks something, that's a system design problem, not an agent problem. Trust comes from structure, not surveillance.

```
Fence (agent-server.el)     Playground (agent freedom)     Guardian (host/human)
─────────────────────────   ─────────────────────────────  ────────────────────────
path guard: read 4 dirs     define new functions (REPL)     monitor, recover
API: agenda, search, bib    parse org, update dblock        escalate, redesign
write: botlog + tracking    chain queries, cross-ref        final responsibility
```

The same `agent-org-agenda-day` function that Emacs shows the human, that Docker bots on Oracle Cloud call, that geworfen serves to the web — one interface, three consumers.

**And the interface is what gets handed over.** Giving an agent a task is easy and reversible; giving it the surface through which the work is read and written is neither. That is what the fence is actually for — not to restrain an agent, but to make a capability safe enough to pass to someone else's agent, and then to someone else. [forge-config](https://github.com/junghan0611/forge-config) is that same move on a code surface, and the domain-owner agents at work are the same move inside a company. The unit being shared is not an answer. It is the interface a person and their agent both stand on.

---

### Other Repositories

Smaller pieces, kept because they carry something the larger work depends on.

| Project | What it is |
|---------|-----------|
| [openclaw](https://github.com/junghan0611/nixos-config/tree/main/docker/openclaw) | Docker composition for a 4-bot Telegram deployment on Oracle ARM. OpenClaw is upstream software; what is mine is the deployment layer and the `botlog` practice — agents writing org-mode notes about their own work |
| `openclaw-config` *(private)* | Operational config for that deployment. It stays closed because the bots' **memory** lives in it. These bots do not run per-repository — they run around the clock as an **exoself**, so their state is one continuous thing that has to be managed as one repository |
| [sorge](https://github.com/junghan0611/sorge) | The place the siblings come to ask. Holds what no single repository can hold for itself — the view across all of them, and a ledger of what was already decided. Its rule is that only human judgements are stored; anything derivable is re-derived on every pass |
| [apply](https://github.com/junghan0611/apply) | Evidence-first application operations. Made public in August 2026 by rewriting its whole history rather than squashing it: personal data was removed, the companies, the answers, the rejections and the judgment errors were not |
| [openglg-config](https://github.com/junghan0611/openglg-config) | Server and shell in one repo — authenticated self-hosted services behind Caddy + Authelia, plus a Nix + home-manager bootstrap for Debian or Ubuntu. `nixos-config` proves the full private forge; this is the lighter public path |
| [zotero-config](https://github.com/junghan0611/zotero-config) | Reproducible bibliography with Korean Dewey Decimal citation keys |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) | Korean monospace font — IBM Plex Mono + Sans KR, 100% Unicode, web font |
| [self-tracking-data](https://github.com/junghan0611/self-tracking-data-public) | Years of life data, version-controlled |
| [legoagent-config](https://github.com/junghan0611/legoagent-config) | Embodied toy-agent experiments — Pybricks + Flutter + ESP32, BLE to a SPIKE Prime hub |
| [edgeagent-config](https://github.com/junghan0611/edgeagent-config) | Invariants a Zig edge node must not violate. Documentation-first |
| [logickocli](https://github.com/junghan0611/logickocli) | Korean natural-language argument ↔ standard logic coordinate system |
| [durable-iot-migrate](https://github.com/junghan0611/durable-iot-migrate) | IoT platform migration with Temporal + Saga. Clojure over Go: 62% less code, same coverage |
| [sicm-study](https://github.com/junghan0611/sicm-study) | Where the lineage lives: Logo → SICP → SICM → SDF. Homoiconicity is why the Clojure projects above are Clojure |

---

### Tech Stack

**Languages:** Go · Clojure · Zig · C · Elisp · Nix · Bash · TypeScript

**Embedded & IoT:** Matter · Thread · Zigbee 3.0 · MQTT · OTBR · Yocto (scarthgap 5.0) · ARM / RISC-V Linux

**AI/ML:** sLLM (Qwen3, LoRA fine-tuning, GGUF quantization) · embedding retrieval · LanceDB · Ollama · OpenRouter

**Cross-platform:** Flutter · Android · Linux · A2UI (Google genui) · GraalVM native-image

**Infrastructure:** NixOS 25.11 · Docker · GPU cluster (CUDA, 3× RTX 5080)

**Knowledge:** Emacs 30.2 · Org-mode · Denote · BibLaTeX · Pandoc

**Protocols:** ACP · MCP · A2A · emacsclient socket · SSE · JSON-RPC 2.0 · REST

---

### Working Corpus

| | |
|---|---|
| **notes** | 3,500+ |
| **bibliography** | 8,200+ |
| **commits** | 8,500+ |
| **journal** | 1,600+ days |
| **health** | 2,600+ days |
| **garden** | 2,200+ pages |

*Counts rounded down to the nearest 100 from live existence data at [`agenda.junghanacs.com/api/stats`](https://agenda.junghanacs.com/api/stats). Journal and health are day counts. Recent-window totals are not frozen here — the live surface is the number. Measured 2026-09-04.*

---

*Last updated: 2026-09-04*
