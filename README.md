# Awesome Proactive Agents

**English** | [中文](README.zh-CN.md)

> **When should an always-on agent intervene?**
> A field map of proactive AI assistance: what signals an agent can watch, how it decides to act, what it does, what it remembers, and how we measure whether the intervention was worth it.

Most agent research asks *"can the agent do the task?"*. This list is organized around a different question: *"should the agent act right now, unprompted?"* — the timing problem that always-on assistants (smart glasses, MR headsets, ambient copilots) cannot avoid.

**Organizing thesis:** an intervention is a decision under uncertainty —
`intervene ⇔ E[benefit of acting] − E[cost of interrupting] > θ`
Every work below is placed by which part of that inequality it advances.

*Status: v0.1 skeleton · actively maintained · PRs welcome.*

---

## Taxonomy

```
                 ┌─────────────────────────────────────────────┐
                 │        PROACTIVE INTERVENTION PIPELINE      │
                 └─────────────────────────────────────────────┘

  1. SIGNALS          2. DECISION           3. ACTION          4. MEMORY
  what to watch       when to act           what to do         what it knows
  ───────────         ───────────           ──────────         ───────────
  gaze / eye-hand     rule-based            speak / display    session memory
  scene change        (script deviation)    GUI operation      episodic store
  temporal context    decision-theoretic    physical guidance  user profile
  user behavior       (benefit − cost)                         personal thresholds
        │                   │                    │                  │
        └───────────────────┴────────┬───────────┴──────────────────┘
                                     ▼
                 5. EVALUATION & SELF-IMPROVEMENT  (the loop)
                 was the intervention good? does the system get better?
                 offline: timing precision/recall · annoyance benchmarks
                 online:  accept / dismiss / "snooze 3 days" = reward events
                 → feedback re-tunes θ (the smallest possible RL)
```

---

## 1 · Signals — what can trigger an intervention

| Work | Venue / Date | Signal type | One line |
|---|---|---|---|
| [SIAgent](https://arxiv.org/abs/2603.00522) | arXiv 2026.02 | eye–hand coordination | Translates gaze + hand micro-actions into natural language, then LLM infers intent; 97.2% intent recognition over 60+ VR tasks (vs 93.1% gaze+pinch) |
| [YETI](https://arxiv.org/abs/2501.09355) | arXiv 2025.01 | scene change + task alignment | SSIM frame differencing detects scene shifts; alignment of user actions against expected task steps flags deviation |
| [VisionClaw](https://arxiv.org/abs/2604.03486) | arXiv 2026.04 | always-on egocentric stream | Always-on glasses agent that autonomously decides when to assist |
| [Egocentric Co-Pilot](https://arxiv.org/abs/2603.01104) | WWW 2026 | egocentric video | First-person co-pilot with web-native deployment |
| [Predicting Human Interruptibility with Sensors](https://dl.acm.org/doi/10.1145/1057237.1057243) | TOCHI 2005 (Fogarty et al.) | ambient sensors | Pre-LLM proof that cheap sensors predict interruptibility better than humans do |

*Open slot: temporal/calendar context signals in the LLM era — surprisingly under-explored.*

## 2 · Decision — when to act

The core of the field, and the layer with the deepest history. Two lineages that current MR papers rarely connect:

### Decision-theoretic lineage (2000s–2010s: notifications & attention management)

| Work | Venue / Date | Contribution |
|---|---|---|
| [Attention-Sensitive Alerting](https://arxiv.org/abs/1301.6707) | UAI 1999 (Horvitz, Jacobs, Hovel) | Framed alerting as expected-utility: cost of deferring vs cost of interrupting, under uncertainty about user attention |
| [Learning and Reasoning about Interruption](https://www.microsoft.com/en-us/research/publication/learning-and-reasoning-about-interruption/) | ICMI 2003 (Horvitz & Apacible) | Learned models of interruptability from desktop activity streams |
| [Beyond Interruptibility](https://dl.acm.org/doi/10.1145/3130956) | IMWUT 2017 (Pielot et al.) | Shifted the question from "can I interrupt?" to "is this an *opportune moment to engage*?"; 337-user field study, 5× lift from behavioral history |

### LLM-era proactivity (2024–)

| Work | Venue / Date | Decision mechanism |
|---|---|---|
| [Proactive Agent](https://arxiv.org/abs/2410.12361) | arXiv 2024.10 (THU) | Reward model trained on human accept/reject labels simulates user judgment; ProactiveBench (6,790 events), F1 66.47% |
| [YETI](https://arxiv.org/abs/2501.09355) | arXiv 2025.01 | Rule-based: deviation from known task script ⇒ intervene (no cost term) |
| [Proactive Assistant Dialogue Generation](https://arxiv.org/abs/2506.05904) | arXiv 2025.06 | When-to-speak from streaming egocentric video |
| [VisionClaw](https://arxiv.org/abs/2604.03486) | arXiv 2026.04 | Agent self-decides assistance moments on always-on glasses |

**The gap this list exists to expose:** the 1999–2017 lineage modeled the *cost* side rigorously but had no capable actor; the LLM era has capable actors but mostly detects "user needs help" without a cost term. Almost nobody has rebuilt the full `benefit − cost` decision with modern models in open-world (script-free) scenarios.

## 3 · Action — what the agent does once it decides

| Work | Venue / Date | Capability |
|---|---|---|
| [UI-TARS-2](https://arxiv.org/abs/2509.02544) | arXiv 2025.09 (ByteDance Seed) | Multi-turn RL GUI agent: data flywheel + hybrid environment (GUI + file system + terminal) + unified sandbox; OSWorld 47.5, AndroidWorld 73.3. Proves multi-turn RL works *when reward has ground truth (task completion)* |
| [Seed1.5-VL](https://arxiv.org/abs/2505.07062) | arXiv 2025.05 (ByteDance Seed) | 532M vision encoder + 20B-active MoE; SOTA on 38/60 public benchmarks incl. GUI/agent tasks |
| [Depth Anything 3](https://arxiv.org/abs/2511.10647) | arXiv 2025.11 (ByteDance Seed) | Any-view geometry from a single plain transformer with a depth-ray target; surpasses VGGT on pose + geometry. Spatial grounding for physical-world intervention |

*Placement rationale: perception/geometry/GUI-operation are the "hands" — mature building blocks. The bottleneck is layer 2, not layer 3.*

## 4 · Memory — what the agent knows about you

Timing decisions are personal: the same intervention is helpful for one user and noise for another. Cost models need memory.

| Work | Venue / Date | One line |
|---|---|---|
| [MemGPT](https://arxiv.org/abs/2310.08560) | arXiv 2023.10 | OS-style paged memory for LLMs (now Letta) |
| [Mem0](https://arxiv.org/abs/2504.19413) | arXiv 2025.04 | Production-oriented scalable long-term memory layer |
| [MemOS](https://arxiv.org/abs/2507.03724) | arXiv 2025.07 | Memory as a first-class OS resource: parametric / activation / plaintext, unified in MemCube |
| [SpeechLess](https://arxiv.org/abs/2602.00793) | arXiv 2026.02 | Personalized spatial memory assistant in AR — closest existing work to memory-conditioned intervention |

## 5 · Evaluation & Self-Improvement — closing the loop

The least standardized layer, and (per the thesis of this list) the one that gates everything else: without a reliable eval, an RL reward for intervention quality cannot even be defined.

### Benchmarks & datasets

| Resource | Venue / Date | What it measures |
|---|---|---|
| [HoloAssist](https://arxiv.org/abs/2309.17024) | ICCV 2023 (Microsoft) | 166h egocentric collaborative manipulation; benchmarks incl. **mistake detection & intervention type prediction** — the closest thing to a timing benchmark today |
| [Ego4D](https://arxiv.org/abs/2110.07058) | CVPR 2022 | 3,670h egocentric video; the substrate most proactive-assistant work builds on (see also EgoExo4D) |
| [ProactiveBench](https://arxiv.org/abs/2410.12361) | 2024.10 | 6,790 events with human accept/reject labels for proactive task prediction |
| [ProactiveEval](https://arxiv.org/abs/2508.20973) | arXiv 2025.08 | Unified evaluation framework for proactive *dialogue* agents |
| [ProAgentBench](https://arxiv.org/abs/2602.04482) | arXiv 2026.02 | Proactive assistance evaluation with real-world data |

### Surveys

| Work | Venue / Date | Use |
|---|---|---|
| [Egocentric Procedural AI Assistants](https://arxiv.org/abs/2511.13261) | arXiv 2025.11 | Benchmark roster and task landscape for procedural egocentric assistance |

### Online feedback & self-improvement

Every deployed proactive system already emits a reward stream, and most of it is discarded. Explicit user actions — accept, dismiss, "don't show this again", "snooze for 3 days" — are labeled preference data on `(context, intervention)` pairs. "Snooze for 3 days" is doubly informative: a strong negative reward on this intervention *and* a hard constraint the user writes directly into the policy.

Feedback itself has depth — the truer the signal, the harder the attribution:

| Level | Signal | Cost | Attribution |
|---|---|---|---|
| **L0 explicit** | accept / dismiss / snooze | free but sparse & biased | trivial |
| **L1 implicit behavioral** | did the user follow the suggestion; gaze dwell vs aversion; recovery time after interruption; undo | dense, no user effort | easy–moderate |
| **L2 outcome** | task completion delta, time saved, errors avoided | needs task instrumentation | delayed → credit assignment |
| **L3 long-term** | retention, trust, user disabling proactivity entirely (the ultimate negative reward) | population-level A/B only | hardest |

Three maturity levels observed in practice:

1. **Log only** — feedback collected, never used (most products today).
2. **Threshold adaptation** — per-user, per-context updates to θ; one parameter, bandit-style. The smallest possible RL, and probably where always-on assistants should start.
3. **Policy learning** — a learned reward model over interventions ([Proactive Agent](https://arxiv.org/abs/2410.12361) is the offline version of this).

The asymmetry that makes this hard: negative signals are cheap and abundant (every dismissal is one), while positive signals are weak and delayed — the user who *wasn't* annoyed says nothing, and the intervention that saves ten minutes tomorrow emits nothing today. This is why self-improvement is drawn inside the evaluation layer rather than as a sixth stage: the feedback edge is only as good as the measurement that defines it (`reward ⊆ eval`).

### Missing metrics (open)

- **Timing precision/recall**: of the moments an agent chose to intervene, how many were opportune? Of the opportune moments, how many were caught?
- **Annoyance / interruption cost**: acceptance rate alone is gameable (reward hacking via under- or over-triggering); a cost-side metric is needed.
- **Delayed benefit**: interventions whose value materializes later have no credit-assignment story.

---

## Cross-cutting comparison

| Work | Signal | Decision | Scenario | Eval loop |
|---|---|---|---|---|
| Horvitz 1999–2003 | desktop activity | expected utility (benefit − cost) | notifications, closed | user studies |
| Pielot 2017 | phone sensors + behavior history | learned opportune-moment classifier | mobile engagement | 337-user field study |
| Proactive Agent 2024 | event streams | learned reward model (accept/reject) | desktop tasks | ProactiveBench |
| YETI 2025 | SSIM + script alignment | rule: deviation ⇒ intervene, no cost term | scripted procedural AR | HoloAssist |
| VisionClaw 2026 | always-on egocentric | agent self-decision | open-world glasses | — |
| SIAgent 2026 | eye–hand | intent recognition (understand, not when-to-act) | VR tasks | 60+ task suite |
| UI-TARS-2 2025 | GUI state | task-completion reward (ground truth exists) | GUI/OS, closed | OSWorld etc. |

Reading the table by column: signals are getting richer, actors are getting stronger, but the **decision column still splits into "rules without cost terms" and "cost models without modern actors"** — and the eval column has no shared benchmark for timing quality in open-world scenarios.

## Open problems (survey seed)

1. **Reward without ground truth.** GUI agents have task completion as reward; intervention quality has no equivalent. What is the eval that makes an RL reward definable?
2. **The cost term.** Modern proactive works detect need; almost none model interruption cost. How does the 1999–2017 utility framing port to LLM actors?
3. **Script-free timing.** YETI-style deviation detection needs a task script. Open-world daily scenarios have none.
4. **Credit assignment for delayed benefit.** An intervention that saves the user ten minutes tomorrow gets no signal today.
5. **Personalized thresholds.** The same θ is wrong for different users, contexts, and times of day — timing policy must be memory-conditioned.
6. **Benchmark fragmentation.** HoloAssist's intervention-type prediction, ProactiveBench's accept/reject, ProactiveEval's dialogue framing measure different slices; none covers open-world MR intervention timing end to end.

---

## Contributing

One PR per work. Place it in the layer it primarily advances, add one honest line about what it does (not the abstract's claim), and if it belongs in the cross-cutting table, fill all four columns. Entries need a verifiable link (arXiv / DOI / official page).

## Maintainer

Tao An ([FIM Labs](https://fim.ai)) — building agent runtimes; this map is the outline of a survey in progress on intervention timing for always-on agents.

*License: CC0. Last verified: 2026-07.*
