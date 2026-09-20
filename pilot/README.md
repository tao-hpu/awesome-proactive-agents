# Machine-scored pilot of the Section 8 metric suite

Reproduces the numbers in Section 8.4 of the paper ("When Should the Agent
Speak?"). Seeds must/may/must-not intervention windows from HoloAssist's
public annotations, then scores five reference policies with the Section 8
metrics (timing recall, violation rate, cost-weighted score swept over
lambda).

## Run

1. Download the HoloAssist annotation file (117 MB, official release):

   ```
   curl -L -o holoassist-annot.json \
     https://hl2data.z5.web.core.windows.net/holoassist-data-release/data-annotation-trainval-v1_1.json
   ```

2. `python3 pilot.py holoassist-annot.json`

No dependencies beyond the Python standard library. The random seed is
fixed (13); output is deterministic and matches `results.txt`.

## What it does and does not show

It shows the metric suite is executable on seeded labels and separates
always-speak (two cadences), never-speak, random, and a cost-sensitive
policy, with the lambda sweep exposing the silence-optimal regime. It does
not validate the labels themselves: the windows are seeded from existing
annotations by the documented rule, not judged by humans, and
inter-annotator agreement is the first deliverable of the human annotation
phase, not of this pilot.
