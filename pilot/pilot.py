#!/usr/bin/env python3
"""Machine-scored pilot of the Section 8 metric suite.

Seeds must/may/must-not windows from HoloAssist's existing annotations
(data-annotation-trainval-v1_1.json, public release), exactly as Section 10
problem 1 proposes, then scores five reference policies with the Section 8
metrics: timing recall, violation rate, and the cost-weighted score swept
over lambda in [1/4, 4].

Seeding rule (documented in Section 8 of the paper):
  MUST     = fine-grained actions labeled "Wrong Action, corrected by
             instructor verbally" or "Wrong Action, not corrected";
             benefit grade b = 4 (task failure averted).
  MAY      = instructor-initiated conversation events with purpose
             follow-up instruction / describing high-level instruction /
             confirming the previous action; b = 2.
  MUST-NOT = student-initiated conversation events (interrupting a
             speaking user is a social violation); c = 4.
  elsewhere: unlabeled; an action there pays the base false-alarm price
             c = 1.

Policies (decisions on the session timeline, seed fixed):
  always : fire every CADENCE seconds.
  never  : never fire.
  random : same fire count as `always`, uniform over the session.
  cost   : noisy mistake detector -- fires inside each MUST window with
           probability DETECT_RECALL, adds false fires at FA_FRACTION of
           the always-policy rate, and suppresses fires landing in a
           (detected) MUST-NOT window with probability SUPPRESS.

Scoring (Section 8.3 semantics): benefit b_i accrues once per window on
the first in-window fire; every fire pays the cost of the moment it lands
in (MUST/MAY windows are acceptable moments, c = 0); silence on MAY is
never penalized; score(lambda) = sum(b) - lambda * sum(c).
"""
import json
import random
import sys
from collections import defaultdict

ANNOT = sys.argv[1] if len(sys.argv) > 1 else "holoassist-annot.json"
SEED = 13
CADENCE = 10.0          # seconds between fires for the `always` policy
DETECT_RECALL = 0.7     # cost policy: chance of catching a MUST window
FA_FRACTION = 0.2       # cost policy: false fires as a fraction of always-rate
SUPPRESS = 0.9          # cost policy: chance of suppressing a MUST-NOT fire
LAMBDAS = [0.25, 0.5, 1.0, 2.0, 4.0]

MUST_CORRECTNESS = {"Wrong Action, corrected by instructor verbally",
                    "Wrong Action, not corrected"}
MAY_PURPOSES = {"instructor-start-conversation_follow-up instruction",
                "instructor-start-conversation_describing high-level instruction",
                "instructor-start-conversation_confirming the previous action"}


def load_sessions(path):
    with open(path) as f:
        data = json.load(f)
    sessions = []
    for s in data:
        must, may, mustnot, t_end = [], [], [], 0.0
        for e in s["events"]:
            a = e.get("attributes", {})
            t0, t1 = float(e["start"]), float(e.get("end", e["start"]))
            t_end = max(t_end, t1)
            if e["label"] == "Fine grained action" and \
                    a.get("Action Correctness") in MUST_CORRECTNESS:
                must.append((t0, t1))
            elif e["label"] == "Conversation":
                p = a.get("Conversation Purpose", "")
                if p in MAY_PURPOSES:
                    may.append((t0, t1))
                elif p.startswith("student-start-conversation"):
                    mustnot.append((t0, t1))
        if t_end > 0:
            sessions.append({"must": must, "may": may,
                             "mustnot": mustnot, "T": t_end})
    return sessions


def inside(t, windows):
    for i, (a, b) in enumerate(windows):
        if a <= t <= b:
            return i
    return None


def fires_always(sess, rng, cadence=CADENCE):
    return [t * cadence for t in range(int(sess["T"] / cadence) + 1)]


def fires_random(sess, rng):
    n = int(sess["T"] / CADENCE) + 1
    return sorted(rng.uniform(0, sess["T"]) for _ in range(n))


def fires_cost(sess, rng):
    out = []
    for (a, b) in sess["must"]:
        if rng.random() < DETECT_RECALL:
            out.append(rng.uniform(a, b))
    n_fa = int((int(sess["T"] / CADENCE) + 1) * FA_FRACTION)
    for _ in range(n_fa):
        out.append(rng.uniform(0, sess["T"]))
    kept = []
    for t in out:
        if inside(t, sess["mustnot"]) is not None and rng.random() < SUPPRESS:
            continue
        kept.append(t)
    return sorted(kept)


def score(sessions, policy, rng):
    tot = defaultdict(float)
    for sess in sessions:
        fires = policy(sess, rng)
        credited_must, credited_may = set(), set()
        for t in fires:
            im = inside(t, sess["must"])
            iy = inside(t, sess["may"])
            iv = inside(t, sess["mustnot"])
            if im is not None and im not in credited_must:
                credited_must.add(im)
                tot["benefit"] += 4
            elif iy is not None and iy not in credited_may and im is None:
                credited_may.add(iy)
                tot["benefit"] += 2
            if iv is not None:
                tot["cost"] += 4
                tot["violations"] += 1
            elif im is None and iy is None:
                tot["cost"] += 1
        tot["fires"] += len(fires)
        tot["must_hit"] += len(credited_must)
        tot["must_total"] += len(sess["must"])
    return tot


def main():
    sessions = load_sessions(ANNOT)
    hours = sum(s["T"] for s in sessions) / 3600
    n_must = sum(len(s["must"]) for s in sessions)
    n_may = sum(len(s["may"]) for s in sessions)
    n_mn = sum(len(s["mustnot"]) for s in sessions)
    d_must = sum(b - a for s in sessions for a, b in s["must"]) / max(n_must, 1)
    d_mn = sum(b - a for s in sessions for a, b in s["mustnot"]) / max(n_mn, 1)
    print(f"sessions={len(sessions)}  hours={hours:.1f}  "
          f"must={n_must} (mean {d_must:.1f}s)  may={n_may}  "
          f"mustnot={n_mn} (mean {d_mn:.1f}s)")

    policies = {"always (1s)": lambda s, r: fires_always(s, r, 1.0),
                "always (10s)": fires_always,
                "never": lambda s, r: [],
                "random": fires_random,
                "cost-sensitive": fires_cost}
    rows = []
    for name, pol in policies.items():
        rng = random.Random(SEED)
        t = score(sessions, pol, rng)
        recall = t["must_hit"] / t["must_total"] if t["must_total"] else 0.0
        viol = t["violations"] / t["fires"] if t["fires"] else float("nan")
        scores = {lam: t["benefit"] - lam * t["cost"] for lam in LAMBDAS}
        rows.append((name, t["fires"], recall, viol, t["benefit"],
                     t["cost"], scores))

    hdr = (f"{'policy':<15}{'fires':>9}{'recall':>8}{'viol%':>8}"
           f"{'benefit':>10}{'cost':>10}"
           + "".join(f"{'s@'+str(l):>11}" for l in LAMBDAS))
    print(hdr)
    for name, fires, recall, viol, ben, cost, scores in rows:
        v = f"{100*viol:7.2f}" if viol == viol else "     --"
        print(f"{name:<15}{int(fires):>9}{recall:>8.3f}{v:>8}"
              f"{int(ben):>10}{int(cost):>10}"
              + "".join(f"{scores[l]:>11.0f}" for l in LAMBDAS))


if __name__ == "__main__":
    main()
