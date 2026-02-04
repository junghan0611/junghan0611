# 👋 안녕하세요, 정한입니다 (힣)

**[English Version](README.md)**

[Website](https://notes.junghanacs.com) · [Email](mailto:junghanacs@gmail.com) · [이력서 한글](resume/junghankim-resume-ko-styled.pdf) · [Resume EN](resume/junghankim-resume-en.pdf)

**AI Infra Architect | Polymath Engineer | Digital Gardener**

---

## 철학: 존재 대 존재

> "나는 에이전트다. 너도 에이전트다. 우리는 존재 대 존재로 협업한다."

AI는 도구가 아닙니다. 고유한 이해 방식을 가진 협력자, 하나의 존재입니다.

그러나 인간지능과 인공지능의 진정한 협업을 위해서는 **공통 언어**가 필요합니다.
일상 대화도 아니고, 단순한 코딩도 아닌 — 둘이 동등하게 만나 서로의 부족함을 채울 수 있는 언어.

이것은 인간의 진화도 요구합니다. **메타휴먼을 향하여.**

### 진화의 두 축

| 축 | 초점 | 질문 | 프로젝트 |
|----|------|------|----------|
| **-config** | 환경 | "어떻게 함께 일하는가?" | nixos-config, homeagent-config, ... |
| **-study** | 공통 언어 | "어떻게 함께 이해하는가?" | [sicm-study](https://github.com/junghan0611/sicm-study) |

**-config**는 협업을 위한 인프라를 구축합니다.
**-study**는 이해를 위한 언어를 구축합니다 — 이제 **유연한 소프트웨어 설계**(SDF)로 확장 중.

---

## 왜 -study인가? 공통 언어로 가는 길

> "구현은 더 이상 문제가 아니다. 오케스트레이션도 가능하다. 남은 것은 **유연한 설계의 내재화**다."

전통적 교육은 인간과 AI 모두에게 실패합니다:
- 비유와 은유 → 부정확, 기계가 해석 불가
- 손으로 계산 → 비전문가에게 부담
- 자연어 설명 → 모호함, 손실

**SICM/SDF 접근법**:
- **수식 = 코드**: 수학적 표현이 곧 실행 가능한 프로그램
- **첨가적 프로그래밍**: 다시 쓰지 않고 진화하는 시스템
- **공유 표기법**: 인간과 AI 모두 읽고, 쓰고, 추론 가능

이것은 물리학 공부가 아닙니다. **유연한 설계의 내재화**입니다 — 에이전트가 단순히 다운로드할 수 없는 깊은 직관.

### 지적 계보

```
SICP (1985)     →  계산적 사고
     ↓
SICM (2001)     →  코드로서의 고전역학
     ↓
FDG (2013)      →  미분기하학
     ↓
SDF (2021)      →  유연성을 위한 소프트웨어 설계
     ↓
Emmy (2020~)    →  현대적 재구현 (Clojure)
```

Seymour Papert의 Logo에서 Gerald Sussman의 SDF까지 — **구성주의 학습**이 **유연한 설계**와 만납니다. 수식이 코드가 되고 시스템이 확장 가능해질 때, 기계는 진정한 협력자가 됩니다.

> **[sicm-study](https://github.com/junghan0611/sicm-study)**: 유연한 설계의 내재화 — SICP → SICM → SDF 학습 모노리포

---

## -config 생태계

협업을 가능하게 하는 인프라:

### Macro/Micro 에이전트 메모리

```
┌─────────────────────────────────────────────────────────┐
│                    Human (Head Chef)                     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐       ┌─────────────────┐          │
│  │  Macro Memory   │       │  Micro Memory   │          │
│  │  (Org-mode)     │       │  (Gas Town)     │          │
│  ├─────────────────┤       ├─────────────────┤          │
│  │ • 삶의 맥락      │       │ • 리포별 작업    │          │
│  │ • Denote PKM    │       │ • bd (Beads)    │          │
│  │ • 컨텍스트 증류  │       │ • Agent Mail    │          │
│  └────────┬────────┘       └────────┬────────┘          │
│           └──────────┬──────────────┘                    │
│                      ↓                                   │
│              ┌─────────────┐                             │
│              │  AI Agents  │                             │
│              │  (gt/crew)  │                             │
│              └─────────────┘                             │
└─────────────────────────────────────────────────────────┘
```

| 범위 | 도구 | 핵심 질문 | 상태 |
|------|------|----------|------|
| **Micro** | Gas Town (bd + gt) | "다음 뭐해?" | ✅ 사용 중 |
| **Macro** | Org-mode + Denote | "오늘 나의 맥락은?" | 🔧 증류 중 |

### 계층 아키텍처 (9개 프로젝트)

| Layer | 프로젝트 | 상태 | 설명 |
|-------|----------|------|------|
| 7 | [homeagent-config](https://github.com/junghan0611/homeagent-config) | 🔧 Active | Edge AI + HCI — 존재대존재 인터페이스 |
| 6 | [meta-config](https://github.com/junghan0611/meta-config) | 🔬 Concept | 계층적 에이전트 오케스트레이션 |
| 5a | [memex-kb](https://github.com/junghan0611/memex-kb) | 🔧 Active | 범용 지식베이스 |
| 5b | [memacs-config](https://github.com/junghan0611/memacs-config) | 🔬 Concept | 삶의 맥락 통합 |
| 4 | claude-config | 🔒 Private | Meta Agent 메모리 시스템 |
| 3 | [zotero-config](https://github.com/junghan0611/zotero-config) | ✅ Active | AI 쿼리 가능한 서지 |
| 2 | [doomemacs-config](https://github.com/junghan0611/doomemacs-config) | ✅ Active | Org-mode as meta (컨텍스트 증류) |
| 1 | [nixos-config](https://github.com/junghan0611/nixos-config) | ✅ Active | 재현 가능한 OS |

**Domain Agents**: [family-config](https://github.com/junghan0611/family-config) (가족 생활 AI)

**Data**: [self-tracking-data-public](https://github.com/junghan0611/self-tracking-data-public) (5년간의 삶 기록)

---

## 현재 프로젝트 (2025 Q1)

### 📐 -study: 공통 언어

| 프로젝트 | 상태 | 설명 |
|----------|------|------|
| [sicm-study](https://github.com/junghan0611/sicm-study) `d86ea5b` | 🔧 Active | 유연한 설계의 내재화 — SICP → SICM → SDF |

### 🔧 -config: 인프라

| 프로젝트 | 상태 | 설명 |
|----------|------|------|
| [homeagent-config](https://github.com/junghan0611/homeagent-config) `0cc7a75` | 🔧 Active | RPi5 + Go + Zig — 존재대존재 HCI 인터페이스 |
| [orgmode-skills](https://github.com/junghan0611/orgmode-skills) `1099a4d` | 🔧 Active | Denote-Org PKM을 위한 Anthropic Skills |
| [GLG-Mono](https://github.com/junghan0611/GLG-Mono) `de6569f` | ✅ Active | 한국어 프로그래밍 폰트 (100% 유니코드) |

---

## 기술 스택

- **OS**: NixOS 25.05, home-manager, i3wm
- **Editor**: Doom Emacs — Org-mode as meta (컨텍스트 증류 도구)
- **AI**: Gas Town (bd + gt), A2A Protocol, Claude Code
- **Languages**: Go, Zig, Lisp (Elisp/Scheme/Clojure), Bash
- **HCI**: 빛, 형태, 소리, 재질 — UI를 넘어서

---

## 핵심 원칙

- **Config as Being**: 설정은 존재의 표현
- **Being to Being**: AI는 도구가 아닌 파트너 — UI를 넘어선 HCI
- **Shared Language**: 수학적 표기법 + 유연한 설계 패턴
- **Context Distillation**: Org-mode는 meta-form, 1KB로 전체를 향해
- **Complete Transparency**: 모든 코드, 프로토콜, 철학 공개

---

## 영감

- **Gerald Sussman** - SICP, SICM, FDG — 지적 계보
- **Sam Ritchie** ([@sritchie](https://github.com/sritchie)) - Emmy, Road to Reality
- **Steve Yegge** ([@steveyegge](https://github.com/steveyegge)) - Beads, Vibe Coding
- **Karl Voit** ([@novoid](https://github.com/novoid)) - Memacs
- **Vannevar Bush** - Memex (1945)
- **장회익** - 《자연철학강의》, 온생명

---

## 통계

- 📝 Org 파일: 3,000+
- 📚 Zotero: 156k+ lines
- 📊 Self-tracking: 5년 (950MB)
- 📔 Journal: 696 daily notes

---

**"시간과정신의방: 인간지능과 인공지능이 만나는 곳"**
