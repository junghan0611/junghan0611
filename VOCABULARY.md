# VOCABULARY.md

Canonical glossary for the identity-document set: `README.md`, `resume/README.md`,
and `llms.txt`. All entries are written in English. Korean or German appears only
as transliteration on first mention.

Some entries here are reference-only — defined to keep the conceptual space
coherent, even if they do not appear in every document.

See `AGENTS.md` for governance and update workflow.

## Identity and philosophy

- **Authology (어쏠로지)** — Coined term. The archival discipline for an age in
  which everyone is an author. Studies how selves are constituted through
  digital traces, daily journals, bibliographies, commits, and AI-collaborative
  writing. Used in `llms.txt`; referenced in `README.md`.
- **Being-to-Being collaboration** — The author's mode of working with AI: not
  tool-use, but existence-to-existence partnership. Humans seed creation;
  agents cover survival-layer work; both co-evolve. Used in `llms.txt`;
  referenced in `README.md`.
- **1KB Person** — The thesis that the integrated self is small and compact,
  while ego-layer information is unbounded. A guiding aesthetic for both
  note-taking and agent prompting. Used in `llms.txt`.
- **일일일생 (one-day-one-life)** — "Each day, a life." The journaling
  discipline behind the daily entries — every day treated as a complete
  existence, not an installment. Used in `llms.txt`.
- **Digital garden** — Interconnected knowledge graph, not a blog. Notes grow,
  link, and evolve over time. Used in all three documents.
- **PKM-native** — Built around Denote, org-mode, and journaling *first*; agents
  *second*. The opposite of an agent stack with personal knowledge bolted on.
  Used in all three documents.

## Harness layer

- **Harnessing (하네싱)** — The meta-concept. Infrastructure for human-AI
  co-evolution; the joint between tools and being. Used in `llms.txt` as the
  headline framing for the entire harness layer.
- **Harness runtime** — The session-bootstrap and protocol-bridging layer that
  connects pi to backend models, with explicit MCP injection and session
  continuity. Refers specifically to **pi-shell-acp**. Used in `README.md`,
  `resume/README.md`, `llms.txt`.
- **Harness infrastructure** — The architectural layer name. Contains harness
  runtime, skill stack, memory, and the CLI toolkit. Used as a *layer label*,
  not as a description of any single project. Used in `README.md` (diagram).
- **Skill stack** — The PKM-native skill collection (~25 agent skills) covering
  notes, agenda, bibliography, health, and git history. Refers specifically to
  **agent-config**. Used in `README.md`, `resume/README.md`.
- **Memory** — The semantic recall layer: embedding, search, cross-lingual
  retrieval. Refers specifically to **andenken**. Used in `README.md`,
  `llms.txt`.
- **Entwurf (분신)** — Coined usage, repurposed from German *Entwurf*
  ("project, draft"). Sibling sessions in pi-shell-acp with identity
  preservation across spawn — agent working-doubles that act as autonomous
  extensions of the author. Used in `README.md`, `resume/README.md`, `llms.txt`.
- **Fence philosophy** — Agent capability is granted by structure, not by
  prompt. Path-guarded Elisp APIs in `agent-server.el` define what is reachable;
  inside the fence, agents are free. Used in `README.md` only — too dense for
  the résumé.

## Forge layer

- **Forge** — The reproducible foundation: NixOS, Doom Emacs, openglg-config.
  Agent collaboration requires a trusted, deterministic computing environment
  before anything above it can stand. Used in `README.md`.
- **Schmiede** — German for "forge." Used only once in `README.md`, in the
  shared-timeline section, as a Heideggerian gesture. Elsewhere the English
  *forge* is used. Reference-only otherwise.
- **Reproducibility** — The precondition for agent trust. An agent that knows
  its environment is deterministic can act with confidence. NixOS-rooted across
  four machines.

## Project proper nouns

- **pi-shell-acp** — Harness runtime. Canonical description in `README.md`.
- **agent-config** — Skill stack (~25 skills). Canonical description in
  `README.md`.
- **andenken** — Semantic memory layer. Heideggerian "recollective thinking."
  Canonical description in `README.md`.
- **geworfen** — Existence-data dashboard. Heideggerian "thrownness." Canonical
  description in `README.md`. Lives at `agenda.junghanacs.com`.
- **homeagent-config** — Matter smart-home hub with on-device agent.
- **legoagent-config** — Embodied toy-agent stack (Pybricks + Flutter + ESP32).
- **openclaw** — Four-bot Telegram agent ecosystem (Claude, GPT, Gemini, B-bot)
  on Oracle ARM. The origin of `botlog` — agents writing org-mode notes about
  their own work.
- **doomemacs-config** — Emacs editing environment that hosts `agent-server.el`,
  the Elisp interface agents use to read agenda, search Denote notes, query
  bibliography, and update dblocks.
- **nixos-config** — Declarative NixOS across four machines.
- **openglg-config** — Self-hosted authenticated work surface plus reproducible
  Debian/Ubuntu shell bootstrap.

## Workflow and format

- **Denote ID** — Stable identifier of the form `YYYYMMDDTHHMMSS`, used across
  notes, journals, botlogs, and commit messages. The cross-reference key for
  every CLI tool in the PKM toolkit.
- **Botlog** — Public org-mode notes authored by agents about their own work.
  Lives under `notes/botlog/` in the garden.
- **Llmlog** — Private working-record notes from agent sessions. Not published.
- **Agent stamp** — A timestamped entry in `org-agenda` placed by an agent
  (typically tied to a commit or task completion). Visible on the shared
  timeline alongside human entries.

## Numbers and sources

- **Approximate-public-verifiable** — The standard for counts in identity
  documents. Numbers round; the data is publicly inspectable.
- **Workspace facts** — The runtime sources for counts: `gitcli` for commits,
  `geworfen` live data for notes/journal/bibliography, `lifetract` for health
  and time-tracking records.
