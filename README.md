# Awesome Proactive Agents

**English** | [中文](README.zh-CN.md)

> **When should an always-on agent intervene?**
> A field map of proactive AI assistance: what signals an agent can watch, how it decides to act, what it does, what it remembers, and how we measure whether the intervention was worth it.

Most agent research asks *"can the agent do the task?"*. This list is organized around a different question: *"should the agent act right now, unprompted?"* That is the timing problem always-on assistants (smart glasses, MR headsets, ambient copilots) cannot avoid.

**Organizing thesis:** an intervention is a decision under uncertainty.
`intervene ⇔ E[benefit of acting] − E[cost of interrupting] > θ`
Every work below is placed by which part of that inequality it advances.

*Status: v0.2 · actively maintained · PRs welcome.*

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

## 1 · Signals: what can trigger an intervention

| Work | Venue / Date | Signal type | One line |
|---|---|---|---|
| [SIAgent](https://arxiv.org/abs/2603.00522) | arXiv 2026.02 | eye–hand coordination | Translates gaze + hand micro-actions into natural language, then LLM infers intent; 97.2% intent recognition over 60+ VR tasks (vs 93.1% gaze+pinch) |
| [YETI](https://arxiv.org/abs/2501.09355) | arXiv 2025.01 | scene change + task alignment | SSIM frame differencing detects scene shifts; alignment of user actions against expected task steps flags deviation |
| [VisionClaw](https://arxiv.org/abs/2604.03486) | arXiv 2026.04 | always-on egocentric stream | Glasses agent with always-on *perception* but strictly reactive *action*: the stream grounds requests, never initiates; proactivity is named future work (§8). Corrected from the abstract's framing after full-text read |
| [Egocentric Co-Pilot](https://arxiv.org/abs/2603.01104) | WWW 2026 | egocentric video | First-person co-pilot with web-native deployment |
| [ProAgent](https://arxiv.org/abs/2512.06721) | arXiv 2025.12 | tiered daily-life sensing | Cheap cues always on, rich perception only when warranted, fused with stored preferences; deployed on AR glasses: +27.7% proactive prediction accuracy, −20.5% false detections (n=20) |
| [StreamGaze](https://arxiv.org/abs/2512.01707) | arXiv 2025.12 | gaze on streaming video | Whether gaze predicts *what happens next* (anticipation), not just current intent; past/present/proactive task families, 8,521 QA pairs |
| [TicToc: "Temporally Blind"](https://arxiv.org/abs/2510.23853) | ACL 2026 Findings | elapsed time itself | 76 scenarios testing whether tool-use decisions match human time perception; **no model exceeds 65% alignment even when handed explicit timestamps** |
| [Predicting Human Interruptibility with Sensors](https://dl.acm.org/doi/10.1145/1057237.1057243) | TOCHI 2005 (Fogarty et al.) | ambient sensors | Pre-LLM proof that cheap sensors predict interruptibility better than humans do |

*Update 2026-07: the temporal-context slot is no longer empty. It is failing. Agents stay temporally blind even with timestamps in hand (TicToc), which is a stronger finding than absence.*

## 2 · Decision: when to act

The core of the field, and the layer with the deepest history. Two lineages that current MR papers rarely connect:

### Decision-theoretic lineage (2000s–2010s: notifications & attention management)

| Work | Venue / Date | Contribution |
|---|---|---|
| [Attention-Sensitive Alerting](https://arxiv.org/abs/1301.6707) | UAI 1999 (Horvitz, Jacobs, Hovel) | Framed alerting as expected-utility: cost of deferring vs cost of interrupting, under uncertainty about user attention; waiting is a first-class action with a computable value |
| [Principles of Mixed-Initiative UI](https://doi.org/10.1145/302979.303030) | CHI 1999 (Horvitz) | The decision geometry: the action threshold *rises with the user's depth of focus*, and adding dialog as a third action yields a three-way policy (stay silent / ask / act), 25 years before assistants rediscovered the clarifying question as a UX pattern |
| [Four Methods for Coordinating Interruption](https://doi.org/10.1207/S15327051HCI1701_2) | HCI 2002 (McFarlane) | Timing is a *coordination* choice: immediate / negotiated / mediated / scheduled, compared in a 36-participant dual-task study. Negotiated (announce, let the user pick the moment) won most design goals. Modern proactive papers almost never run that baseline |
| [Learning and Reasoning about Interruption](https://www.microsoft.com/en-us/research/publication/learning-and-reasoning-about-interruption/) | ICMI 2003 (Horvitz & Apacible) | Learned interruption cost **in dollars** (willingness-to-pay) from desktop/calendar/audio streams, and *forecast* the next cheaply-interruptible window; models transferred across users scored below majority-class guessing: the standing warning against population-level timing policies |
| [Task Structure Predicts Cost of Interruption](https://doi.org/10.1145/1124772.1124882) | CHI 2006 (Iqbal & Bailey) | Interruption cost from task structure alone, no sensors: three plan features predict a 3.7× spread in resumption lag (464 → 1,702 ms), a price legible offline from exactly the task decomposition modern script-following agents already hold |
| [Disruption and Recovery of Computing Tasks](https://doi.org/10.1145/1240624.1240730) | CHI 2007 (Iqbal & Horvitz) | The field-measured magnitude, over 27 workers and 2,267 logged hours: a ~20-minute disruption arc per alert, and 27% of suspended windows unresumed after two hours. Any model pricing an interruption at the duration of its response is off by two orders of magnitude |
| [InterruptMe](https://doi.org/10.1145/2632048.2632062) | UbiComp 2014 (Pejović & Musolesi) | Interruption cost is **path-dependent**: sentiment toward a notification more than halves after eight others in the prior two hours, so a context-driven gate that fires back-to-back is *worse than random* on interruptibility exhaustion |
| [Beyond Interruptibility](https://dl.acm.org/doi/10.1145/3130956) | IMWUT 2017 (Pielot et al.) | Shifted the question from "can I interrupt?" to "is this an *opportune moment to engage*?"; 337-user field study, 5× lift from behavioral history |
| [Attention Management Systems: a Survey](https://arxiv.org/abs/1806.06771) | IMWUT 2018 (Anderson et al.) | The field's self-portrait at its pre-LLM peak. Attention fragmentation, breakpoints, deferral: the vocabulary the cost term lives in |
| [JITAI: Just-in-Time Adaptive Interventions](https://doi.org/10.1007/s12160-016-9830-8) | Ann. Behav. Med. 2018 (Nahum-Shani et al.) | Mobile health's timing formalism: decision points, tailoring variables, an explicit *provide nothing* action, and burden/fatigue as named first-class costs, but thresholds are theory-set free parameters and neither expectation is estimated |
| [Adaptive Notification Scheduling in Production](https://doi.org/10.1145/3292500.3330732) | KDD 2019 (Okoshi et al.) | Breakpoint-based deferral: 382,518-user deployment study (up to +60.7% click rate), then enabled for **all 10M+ Android users** of Yahoo! JAPAN's app, the lineage's population-scale proof |
| [Opportune Moments in VR](https://doi.org/10.1145/3491102.3517529) | CHI 2022 (Chen et al.) | Interruptibility prediction crossed into the headset four years before the proactive-MR wave, which has ignored it |

### LLM-era proactivity (2024–)

| Work | Venue / Date | Decision mechanism |
|---|---|---|
| [Proactive Agent](https://arxiv.org/abs/2410.12361) | arXiv 2024.10 (THU) | Reward model trained on human accept/reject labels simulates user judgment; ProactiveBench (6,790 events), F1 66.47% |
| [YETI](https://arxiv.org/abs/2501.09355) | arXiv 2025.01 | Rule-based: deviation from known task script ⇒ intervene (no cost term) |
| [Proactive Assistant Dialogue Generation](https://arxiv.org/abs/2506.05904) | arXiv 2025.06 | When-to-speak from streaming egocentric video |
| [VisionClaw](https://arxiv.org/abs/2604.03486) | arXiv 2026.04 | None: always-on perception, user-initiated action only. The most deployable 2026 system solves timing by not having it, and the human stays the gate |
| [PRISM](https://arxiv.org/abs/2602.01532) | arXiv 2026.02 | Intervenes when calibrated P(user acceptance) exceeds a threshold **derived from asymmetric costs of missed help vs false alarms**; −22.78% false alarms, +20.14% F1 on ProactiveBench. The closest rebuild of the utility decision so far |
| [Wake/Anchor without an LLM](https://arxiv.org/abs/2605.30152) | arXiv 2026.05 | Temporal-graph encoder emits per-event trigger probability; the LLM is called only *after* the trigger fires (4–7× faster on servers, ~220 MiB). The decision layer may not be an LLM problem at all |
| [Pro²Assist](https://arxiv.org/abs/2605.04227) | arXiv 2026.05 | Step-aware AR assistance over long-horizon procedures; reports **timing accuracy** as a headline metric (up to 2.29× baselines) |

**The gap this list exists to expose (updated 2026-07):** the 1999–2017 lineage modeled the *cost* side rigorously but had no capable actor. The LLM era has capable actors and is only now rediscovering the cost term, in fragments: PRISM prices false alarms, [Precision Proactivity](https://arxiv.org/abs/2505.10742) measures cognitive load, [EgoSocial](https://arxiv.org/abs/2510.13105) names social violation, gating papers price compute. Nobody has unified these fragments into one θ, and none of them inherits the 1999–2017 formalisms. Note also that three independent 2026 papers (PRISM's deliberation gate, the temporal-graph trigger, [pre-reasoning perception](https://arxiv.org/abs/2606.03236)) converge on a **cheap-gate / expensive-actor** architecture, a convergence the field itself has not yet remarked on.

## 3 · Action: what the agent does once it decides

| Work | Venue / Date | Capability |
|---|---|---|
| [UI-TARS-2](https://arxiv.org/abs/2509.02544) | arXiv 2025.09 (ByteDance Seed) | Multi-turn RL GUI agent: data flywheel + hybrid environment (GUI + file system + terminal) + unified sandbox; OSWorld 47.5, AndroidWorld 73.3. Proves multi-turn RL works *when reward has ground truth (task completion)* |
| [Seed1.5-VL](https://arxiv.org/abs/2505.07062) | arXiv 2025.05 (ByteDance Seed) | 532M vision encoder + 20B-active MoE; SOTA on 38/60 public benchmarks incl. GUI/agent tasks |
| [Depth Anything 3](https://arxiv.org/abs/2511.10647) | arXiv 2025.11 (ByteDance Seed) | Any-view geometry from a single plain transformer with a depth-ray target; surpasses VGGT on pose + geometry. Spatial grounding for physical-world intervention |
| [Full-Duplex-Bench](https://arxiv.org/abs/2503.04721) | ASRU 2025 | Millisecond-scale when-to-speak from the speech community: pause handling, turn-taking, **backchanneling**, barge-in. Backchanneling is the missing *graduated* action: intervention is not binary (silence / full interruption) but a menu of escalating costs |

*Placement rationale: perception/geometry/GUI-operation are the "hands", mature building blocks. The bottleneck is layer 2, not layer 3.*

## 4 · Memory: what the agent knows about you

Timing decisions are personal: the same intervention is helpful for one user and noise for another. Cost models need memory.

| Work | Venue / Date | One line |
|---|---|---|
| [MemGPT](https://arxiv.org/abs/2310.08560) | arXiv 2023.10 | OS-style paged memory for LLMs (now Letta) |
| [Mem0](https://arxiv.org/abs/2504.19413) | arXiv 2025.04 | Production-oriented scalable long-term memory layer |
| [MemOS](https://arxiv.org/abs/2507.03724) | arXiv 2025.07 | Memory as a first-class OS resource: parametric / activation / plaintext, unified in MemCube |
| [SpeechLess](https://arxiv.org/abs/2602.00793) | arXiv 2026.02 | Personalized spatial memory assistant in AR, the closest existing work to memory-conditioned intervention |
| [Sensing What Surveys Miss](https://arxiv.org/abs/2602.00880) | CHI 2026 | Physiological signals + **per-user dynamic thresholds** for when to fire LLM support; the rare study that ablates timing itself (well-timed vs misaligned vs random; well-timed: +21% accuracy). Personalized θ, implemented |

## 5 · Evaluation & Self-Improvement: closing the loop

The least standardized layer, and (per the thesis of this list) the one that gates everything else: without a reliable eval, an RL reward for intervention quality cannot even be defined.

### Benchmarks & datasets

| Resource | Venue / Date | What it measures |
|---|---|---|
| [HoloAssist](https://arxiv.org/abs/2309.17024) | ICCV 2023 (Microsoft) | 166h egocentric collaborative manipulation; benchmarks incl. **mistake detection & intervention type prediction**, the closest thing to a timing benchmark today |
| [Ego4D](https://arxiv.org/abs/2110.07058) | CVPR 2022 | 3,670h egocentric video; the substrate most proactive-assistant work builds on (see also EgoExo4D) |
| [ProactiveBench](https://arxiv.org/abs/2410.12361) | 2024.10 | 6,790 events with human accept/reject labels for proactive task prediction |
| [ProactiveEval](https://arxiv.org/abs/2508.20973) | arXiv 2025.08 | Unified evaluation framework for proactive *dialogue* agents |
| [ProAgentBench](https://arxiv.org/abs/2602.04482) | arXiv 2026.02 | Proactive assistance evaluation with real-world data |
| [EgoSocial](https://arxiv.org/abs/2510.13105) | arXiv 2025.10 | 13,500 egocentric social video-question pairs where **intervention timing is the metric itself**: Gemini 2.5 Pro scores 14.4%. Also names a cost this map lacked: social violation |
| [ProactiveVideoQA](https://arxiv.org/abs/2507.09313) | arXiv 2025.07 | **PAUC**: a published, human-validated metric for response *timing dynamics* (not just content). Its opening: no cost term |
| [EgoProactive / Pro²Bench](https://arxiv.org/abs/2606.04970) | arXiv 2026.06 (Meta) | Out-of-Plan annotations make *leaving the script* a first-class, recoverable event; unifies five benchmarks under one proactive-guidance schema |
| [Precision Proactivity](https://arxiv.org/abs/2505.10742) | arXiv 2025.05 | 1,178 observations of real professional work: **AI-initiated task switching is the strongest predictor of performance decline**, the empirical price tag the LLM-era cost term was missing |

### Surveys

| Work | Venue / Date | Use |
|---|---|---|
| [Egocentric Procedural AI Assistants](https://arxiv.org/abs/2511.13261) | arXiv 2025.11 | Benchmark roster and task landscape for procedural egocentric assistance |
| [Proactive Conversational AI](https://doi.org/10.1145/3715097) | ACM TOIS 2025 (Deng et al.) | The dialogue-side survey: *what to say and toward what goal once speaking is licensed*. This map covers whether to speak at all. Cite it, then draw the line |
| [Anticipatory Mobile Computing](https://doi.org/10.1145/2693843) | ACM CSUR 2015 (Pejović & Musolesi) | The closest prior survey: one subsection on opportune moments inside a broader treatment of mobile sensing and context prediction. Neither organizes the literature around a decision rule nor prices the intervention, and it predates always-on LLM assistants entirely |

### Online feedback & self-improvement

Every deployed proactive system already emits a reward stream, and most of it is discarded. Explicit user actions (accept, dismiss, "don't show this again", "snooze for 3 days") are labeled preference data on `(context, intervention)` pairs. "Snooze for 3 days" is doubly informative: a strong negative reward on this intervention *and* a hard constraint the user writes directly into the policy.

Feedback itself has depth. The truer the signal, the harder the attribution:

| Level | Signal | Cost | Attribution |
|---|---|---|---|
| **L0 explicit** | accept / dismiss / snooze | free but sparse & biased | trivial |
| **L1 implicit behavioral** | did the user follow the suggestion; gaze dwell vs aversion; recovery time after interruption; undo | dense, no user effort | easy–moderate |
| **L2 outcome** | task completion delta, time saved, errors avoided | needs task instrumentation | delayed → credit assignment |
| **L3 long-term** | retention, trust, user disabling proactivity entirely (the ultimate negative reward) | population-level A/B only | hardest |

Three maturity levels observed in practice:

1. **Log only**: feedback collected, never used (most products today).
2. **Threshold adaptation**: per-user, per-context updates to θ; one parameter, bandit-style. The smallest possible RL, and probably where always-on assistants should start.
3. **Policy learning**: a learned reward model over interventions ([Proactive Agent](https://arxiv.org/abs/2410.12361) is the offline version of this).

The asymmetry that makes this hard: negative signals are cheap and abundant (every dismissal is one), while positive signals are weak and delayed. The user who *wasn't* annoyed says nothing, and the intervention that saves ten minutes tomorrow emits nothing today. This is why self-improvement is drawn inside the evaluation layer rather than as a sixth stage: the feedback edge is only as good as the measurement that defines it (`reward ⊆ eval`).

### Missing metrics (open)

- **Timing precision/recall with a cost term**: PAUC (ProactiveVideoQA) is a first published attempt at scoring timing dynamics, but a metric that rewards catching opportune moments without pricing false interruptions is still half a metric.
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
| VisionClaw 2026 | always-on egocentric | none (user-initiated; proactivity = future work) | open-world glasses | n/a |
| SIAgent 2026 | eye–hand | intent recognition (understand, not when-to-act) | VR tasks | 60+ task suite |
| UI-TARS-2 2025 | GUI state | task-completion reward (ground truth exists) | GUI/OS, closed | OSWorld etc. |
| PRISM 2026 | event streams | calibrated P(accept) vs asymmetric-cost threshold | desktop tasks | ProactiveBench |

Reading the table by column: signals are getting richer, actors are getting stronger, but the **decision column still splits into "rules without cost terms" and "cost models without modern actors"**. PRISM is the first visible bridge, and it prices only false alarms, in a desktop setting. The eval column still has no shared benchmark for timing quality in open-world scenarios (EgoSocial comes closest, for the social slice).

## Open problems (survey seed)

1. **Reward without ground truth.** GUI agents have task completion as reward; intervention quality has no equivalent. What is the eval that makes an RL reward definable?
2. **The cost term.** As of 2026 the honest framing is no longer "nobody models cost" but "cost is modeled in fragments": false-alarm rate (PRISM), cognitive load (Precision Proactivity), social violation (EgoSocial), compute (gating papers). Nobody has unified the fragments into one θ or inherited the 1999–2017 utility formalisms.
3. **Script-free timing.** YETI-style deviation detection needs a task script. Open-world daily scenarios have none.
4. **Credit assignment for delayed benefit.** An intervention that saves the user ten minutes tomorrow gets no signal today.
5. **Personalized thresholds.** The same θ is wrong for different users, contexts, and times of day, so timing policy must be memory-conditioned.
6. **Benchmark fragmentation.** HoloAssist's intervention-type prediction, ProactiveBench's accept/reject, ProactiveEval's dialogue framing, EgoSocial's social timing, PAUC's timing dynamics measure different slices; Pro²Bench's five-benchmark unification is a first step but stays script-anchored. None covers open-world MR intervention timing end to end.

---

## Contributing

One PR per work. Place it in the layer it primarily advances, add one honest line about what it does (not the abstract's claim), and if it belongs in the cross-cutting table, fill all four columns. Entries need a verifiable link (arXiv / DOI / official page).

## Maintainer

Tao An ([FIM Labs](https://fim.ai), Singapore), building agent runtimes. This map is the outline of a survey in progress on intervention timing for always-on agents.

*License: CC0. Last verified: 2026-07.*
