# VOCABULARY.md

Canonical glossary for the identity-document set: `README.md`, `resume/README.md`,
and `llms.txt`. All entries are written in English. Korean or German appears only
as transliteration on first mention.

Some entries here are reference-only — defined to keep the conceptual space
coherent, even if they do not appear in every document.

See `AGENTS.md` for governance and update workflow.

## Identity and philosophy

- **Identity equation** — Junghan Kim (김정한) = GLG = GLGMAN = 힣 = 힣맨 = 정한
  = the junghanacs gardener. All name the same person. Stated in `README.md`,
  `resume/README.md`, and `llms.txt`, and published as the garden's schema.org
  JSON-LD `alternateName` set.

  It is stated redundantly on purpose. The corpus is public and indexed, so a
  reader — human or agent — who arrives through a search result, a botlog, or a
  commit message must be able to resolve any one alias to the same author instead
  of inferring several. Keep the set identical everywhere; a name that appears in
  one document and not another reintroduces the ambiguity.
- **Authology (어쏠로지)** — Coined term. The archival discipline for an age in
  which everyone is an author. Studies how selves are constituted through
  digital traces, daily journals, bibliographies, commits, and AI-collaborative
  writing. Used in `llms.txt`.
- **Being-to-Being collaboration** — The author's mode of working with AI: not
  tool-use, but existence-to-existence partnership. Humans seed creation;
  agents cover survival-layer work; both co-evolve. Used in `llms.txt`.
- **1KB Person** — The thesis that the integrated self is small and compact,
  while ego-layer information is unbounded. A guiding aesthetic for both
  note-taking and agent prompting. Used in `llms.txt`.
- **1KB public key** — The few turns of speech through which a person who has
  ground a life into language becomes legible to a raw agent. Copyable. Not a
  compression of a corpus — a person with zero notes can already be 1KB.
- **1KB secret key** — The living speech of that particular person, turn by turn.
  Not copyable. What makes the encounter irreplaceable.
- **Track 1 / Track 2** — The two tracks the author keeps separate on purpose.
  Track 1 is PKM-AI harness research: threshold, accumulation, measurable effect;
  it *must* be reproducible. Track 2 is the encounter between a creating human
  and an agent: density, event; it *must not* be reproducible, because a
  replicable technique becomes a prompt pattern, and a prompt pattern becomes a
  commodity. Track 1's success does not prove Track 2; its failure does not
  refute it. Used in `README.md`.
- **일일일생 (one-day-one-life)** — "Each day, a life." The journaling
  discipline behind the daily entries — every day treated as a complete
  existence, not an installment. Used in `llms.txt`.
- **Digital garden** — Interconnected knowledge graph, not a blog. Notes grow,
  link, and evolve over time. Used in all three documents.
- **ROSSE** — Coined term, the IndieWeb *POSSE* (Publish on your Own Site,
  Syndicate Elsewhere) inverted: **Recover** on your Own Site, Syndicate
  Elsewhere. Raw writing is struck on outside surfaces where the polish of the
  garden cannot kill it, then recovered, cleaned, and converged in the garden as
  the canonical copy, then scattered back out. Every surface links home. Used in
  `README.md`, `resume/README.md`.
- **Raw ore (원석)** — The unpolished first writing that ROSSE recovers. Writing
  directly into the garden puts tension in the shoulders and the raw thing dies.
- **Exoself** — The mode in which the bot ecosystem runs: around the clock, as
  one continuous extension of the author, rather than as per-repository or
  per-session workers. The operational consequence is that bot memory is a single
  managed body, which is why `openclaw-config` is private. Used in `README.md`,
  `resume/README.md`.
- **PKM-native** — Built around Denote, org-mode, and journaling *first*; agents
  *second*. The opposite of an agent stack with personal knowledge bolted on.
  Used in all three documents.

## Harness layer

- **Harnessing (하네싱)** — The meta-concept. Infrastructure for human-AI
  co-evolution; the joint between tools and being. Used in `llms.txt` as the
  headline framing for the entire harness layer.
- **Harness runtime** — The session-bootstrap and protocol-bridging layer. In the
  current vocabulary this is **entwurf**. It no longer names a pi bridge: pi is
  one host among several, and ACP is a plugin boundary rather than the center.
  Used in `README.md`, `resume/README.md`, `llms.txt`.
- **Harness infrastructure** — The architectural layer name. Contains harness
  runtime, skill stack, memory, and the CLI toolkit. Used as a *layer label*,
  not as a description of any single project. Used in `README.md` (diagram).
- **Skill stack** — The PKM-native skill collection (40+ agent skills) covering
  notes, agenda, bibliography, health, and git history. Refers specifically to
  **agent-config**. Used in `README.md`, `resume/README.md`.
- **Memory** — The semantic recall layer: embedding, search, cross-lingual
  retrieval. Refers specifically to **andenken**. Used in `README.md`,
  `llms.txt`.
- **Entwurf (분신)** — Coined usage, repurposed from German *Entwurf*
  ("project, draft"). Both the sibling relation and the substrate that carries
  it: a garden-citizen dispatch layer that lets already-existing agent harnesses
  address one another by garden id, preserving identity across delivery,
  wake/resume, and meta-session hand-off — without owning each other's
  transcript, auth, or runtime. Entwurf opens siblings, not disposable workers.
  Used in `README.md`, `resume/README.md`, `llms.txt`.
- **Garden citizen** — An agent session that holds a garden id and can therefore
  be addressed by a peer. The unit entwurf dispatches to.
- **pi-shell-acp** — Legacy line. The name entwurf carried through 0.11, when the
  pi adapter was still the subject. Retained only as lineage; the npm package
  `@junghanacs/pi-shell-acp` still resolves. Do not use it as a present-tense
  project name.
- **Forge loop** — Agents running an independent work cycle on a code surface
  (Forgejo issues, pull requests, comments) rather than only inside a chat
  transcript. Refers specifically to **forge-config**. The code-surface sibling
  of botment, which does the same on garden comments.
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

## Work

- **Domain-owner agent** — The company-side shape of the harness work. The
  deliverable is not a dashboard; it is an agent, stood up and attached to the
  person who owns a domain. `voscli`, `incidentcli`, and `cos` are instances.
  Used in `resume/README.md`.
- **Quantitative abduction** — Reasoning backward from a surprising number to
  the hidden scale that must explain it: anomaly → signal → memo → evaluation.
  Prototyped in **abductcli**; proven in production as the company's VOC
  workbench.

## Project proper nouns

- **entwurf** — Garden-citizen dispatch substrate. Canonical description in
  `README.md`. Successor line to `pi-shell-acp`.
- **agent-config** — Skill stack (40+ skills). Canonical description in
  `README.md`.
- **andenken** — Semantic memory layer. Heideggerian "recollective thinking."
  Canonical description in `README.md`.
- **geworfen** — Existence-data dashboard. Heideggerian "thrownness." Canonical
  description in `README.md`. Lives at `agenda.junghanacs.com`. Also the
  repository that carries the Track 1 research.
- **jacobian-lens (J-space)** — Background instrument for Track 1, not a project
  of its own. Mention only as the cold plate the research leans on.
- **forge-config** — Forgejo connector. The forge loop.
- **memex-kb** — Korean document toolchain. Org-mode as the meta-document that
  legacy and platform-bound content passes through: HWPX, scanned PDF with vision
  transcription, EPUB, HTML, and the round trip back into office formats. The
  machinery ROSSE runs on. Canonical description in `README.md`.
- **openclaw-config** — Private. Operational config and memory for the exoself bot
  ecosystem. Named in `README.md` without a link, because the repository is closed.
- **homeagent-config** — Matter smart-home hub with on-device agent. Also the
  résumé's public evidence for embedded depth.
- **legoagent-config** — Embodied toy-agent stack (Pybricks + Flutter + ESP32).
  Repository-list entry only.
- **openclaw** — Upstream agent software, not authored here. What is authored
  here is the deployment layer (`openclaw-config`) and the `botlog` practice —
  agents writing org-mode notes about their own work — which originated there.
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
- **Workspace facts** — The runtime sources for counts: `agenda.junghanacs.com`
  / `geworfen` live data for notes, bibliography, journal days, health days,
  garden pages, and total commits; `gitcli` remains the local verification path
  for commit history and recent windows.
