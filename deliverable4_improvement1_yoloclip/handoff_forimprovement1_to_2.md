# Deliverable 4 → Deliverable 5 Handoff

**Project:** Reducing False Positives in Real-Time Forest Fire and Smoke Detection via Semantic Verification
**Course:** CS437/CS5317/EE414/EE513 — Deep Learning, Spring 2026 (LUMS)
**Group 4:** Muhammad Baqir Hassan Babar (27100340) & Momin Fahed Khan (27100082)
**Handoff date:** April 2026

---

## How to use this document

This is a handoff file so a new Claude conversation can pick up Deliverable 5 (second improvement) without re-reading everything. Paste this entire file as context at the start of the new conversation along with the SOA PDF. The Deliverable 4 notebook and its JSON metrics are referenced throughout — attach them if the new session needs the exact code.

---

## 1. Project recap

### 1.1 The research problem

Forest fires are destructive. Early detection from PTZ camera feeds could enable faster response. Every deep learning method surveyed in our SOA treats fire/smoke detection as pure visual pattern-matching. The dominant failure mode across the literature is false positives — detectors confidently firing on fog, clouds, haze, sun glare, lamp lights, and reflective surfaces because those patterns visually resemble fire or smoke.

Our SOA (12 papers surveyed) identified the gap: no prior work combines a real-time detector with a vision-language model for semantic post-detection verification. Our proposed pipeline uses YOLOv8 for detection and CLIP for semantic verification of each detected region — asking "does this crop semantically look more like smoke, or more like fog?" rather than relying purely on learned visual patterns.

### 1.2 Our research question (verbatim from SOA)

> Can the integration of a vision-language model (CLIP) as a post-detection semantic verification stage, applied to candidate regions from a YOLOv8 detector, significantly reduce the false positive rate of forest fire and smoke detection from PTZ camera imagery while maintaining real-time inference latency (<100 ms) suitable for edge deployment?

### 1.3 Contingency path from SOA

If YOLO recall proves insufficient on distant/satellite views, the SOA identifies Deformable DETR as a fallback first-stage detector. This contingency has **not** been triggered by Deliverable 4 results (see Section 5).

---

## 2. Completed deliverables

| # | Deliverable | Status | Key artifact |
|---|---|---|---|
| 1 | SOA Survey | Done | SOA.pdf (12 papers, identifies gap) |
| 2 | Dataset exploration + annotation | Done | Group4_27100082_27100340.ipynb |
| 3 | Baseline model (YOLOv8n) | Done | trained.ipynb |
| 4 | **First Improvement (YOLO+CLIP)** | **Done — submitted** | Group4_27100082_27100340_Improvement1.ipynb + improvement1_metrics.json |
| 5 | **Second Improvement** | **Next** | — |

---

## 3. Dataset

**D-Fire** (primary benchmark, Kaggle: `sayedgamal99/smoke-fire-detection-yolo`)
- 21,527 RGB images, YOLO-format bounding boxes
- Class 0 = smoke, Class 1 = fire
- Empty label files = hard negatives (fog, sun glare, lamp lights, reflections)
- Path on Kaggle: `/kaggle/input/datasets/sayedgamal99/smoke-fire-detection-yolo/data`

Test split contains **2,005 hard-negative images** (the critical FPR evaluation subset).

FASDD (secondary) and WWF PTZ (pending footage) are not used yet. For Deliverable 5 we continue with D-Fire only unless WWF footage arrives.

---

## 4. Deliverable 3 baseline results (YOLOv8n)

**Training config:** YOLOv8n from COCO init, 50 epochs, batch 16, imgsz 640, seed 42, optimizer auto (SGD), lr0 0.01, mosaic 1.0, fliplr 0.5, patience 10, close_mosaic 10. Trained on Kaggle T4.

**Test set results (from `yolo.val()`):**
- mAP@0.5 = **0.7614**
- mAP@0.5:0.95 = 0.4339
- Mean Precision = **0.7696**
- Mean Recall = **0.6971**
- Per-class AP@0.5: smoke = 0.695, fire = 0.579

**Hard-negative FPR (image-level):** 49/2005 = **2.44%**

**Inference latency (T4, single image):** mean 14ms, well under 100ms target.

Baseline weights saved as: `/kaggle/working/yolov8n_dfire_best.pt`

---

## 5. Deliverable 4 results — YOLO+CLIP zero-shot verification

### 5.1 What we built

Pipeline: YOLOv8n (frozen, from D3) → for each detection, crop with context margin → CLIP ViT-B/32 image encoder → cosine similarity against a pre-encoded prompt bank → keep detection if top-match bucket agrees with YOLO class, else suppress.

Prompt bank: 5 fire prompts + 5 smoke prompts + 12 confounder prompts (fog, mist, clouds, haze, sun glare, lamp, reflective surface, normal forest, etc.).

Ablations run: CLIP model size (ViT-B/32 vs ViT-L/14), crop context margin (0, 20, 40, 60%), prompt bank (full vs minimal = fire+smoke only).

### 5.2 Headline result — hard-negative FPR (THE WIN)

| Config | FP images / 2005 | FPR | Relative reduction |
|---|---|---|---|
| YOLO-only | 49 | 2.44% | baseline |
| **YOLO+CLIP ViT-B/32, margin=0.20** | **9** | **0.45%** | **-81.6%** |
| YOLO+CLIP ViT-L/14, margin=0.20 | 13 | 0.65% | -73.4% |

**46 of 49 YOLO false-positive boxes were correctly suppressed by CLIP.** This is the headline finding and directly answers the SOA research question on FPR reduction.

### 5.3 Secondary result — prompt bank ablation (CLEAN FINDING)

| Prompt bank | FP images | FPR |
|---|---|---|
| Full (22 prompts incl. confounders) | 9 | 0.45% |
| Minimal (10 prompts, fire+smoke only) | 43 | 2.14% |

**4.8× improvement from naming confounders explicitly.** Clean publishable-quality ablation result. Proves that CLIP rejection is driven by similarity to explicit negative prompts, not by low similarity to fire/smoke prompts alone.

### 5.4 Latency (TARGET MET)

| Stage | Mean (ms) | P95 (ms) |
|---|---|---|
| YOLO only | 13.8 | — |
| CLIP only | 9.6 | — |
| **Total (YOLO+CLIP)** | **25.5** | **52.2** |
| Target | <100 | — |

ViT-L/14 only added ~0.6ms — surprisingly small — but produced worse FPR. ViT-B/32 is the correct edge-deployment choice.

### 5.5 THE PROBLEM — full test set recall collapse

This is the honest, serious issue we acknowledge in our Deliverable 4 submission. Full test set (4,306 images) custom mAP evaluator:

| Metric | YOLO-only | YOLO+CLIP | Δ |
|---|---|---|---|
| mAP@0.5 smoke | 0.695 | 0.351 | **-49%** |
| mAP@0.5 fire | 0.579 | 0.422 | **-27%** |
| **Recall smoke** | **0.791** | **0.359** | **-55%** |
| **Recall fire** | **0.663** | **0.469** | **-29%** |
| Precision smoke | 0.807 | 0.833 | +3% |
| Precision fire | 0.689 | 0.724 | +5% |
| Overall mAP@0.5 | 0.637 | 0.387 | -39% |
| Overall Recall | 0.727 | 0.414 | **-43%** |

**Diagnosis:** CLIP zero-shot is too aggressive. It correctly rejects fog-as-smoke false positives, but ALSO rejects legitimate distant/faint smoke that visually resembles fog. CLIP's internet-scale pre-training doesn't know what forest-domain smoke looks like specifically. Precision rose ~3-5 points; recall dropped ~40 points. The trade-off is unacceptable at default argmax rule.

### 5.6 Broken ablation (to fix in writeup — do not hide)

Crop margin ablation showed identical FPR (0.00449) at margins 0.00, 0.20, 0.40. Either the 9 filtered images are stable across margins (possible), or margin has no effect in this regime. Margin=0.60 gave 0.55% (slightly worse). Not a useful finding — frame as "margin proved insensitive within tested range on hard-negative subset; D-Fire negatives already carry enough context."

### 5.7 Files produced

- `Group4_27100082_27100340_Improvement1.ipynb` — the notebook (48 cells: setup, training, YOLO+CLIP pipeline, ablations, latency bench, save)
- `improvement1_metrics.json` — all quantitative results (already uploaded)
- `yolov8n_dfire_best.pt` — baseline weights for reuse
- PNGs: qualitative, FP-filtered, FP-missed, ablation_crop_margin, latency_comparison

---

## 6. What Deliverable 5 must do

### 6.1 Correct problem identification

Our Deliverable 4 results show the bottleneck is **the verifier, not the detector.** YOLO found the detections. CLIP zero-shot threw half of them away. DETR swap would change the detector while leaving the broken filter — fixes nothing.

The DETR contingency in SOA Section 3 is only triggered by **small-object recall failure on far-range/satellite imagery**. We have no such evidence on D-Fire. YOLO mAP@0.5 = 0.76 and recall = 0.70 are not small-object failure numbers. DETR is NOT the right second improvement.

### 6.2 Chosen direction: Fine-tuned CLIP Linear Probe + Confidence-Thresholded Decision Rule

This is explicitly committed in SOA Section 4 as the "fine-tuned CLIP linear probe" ablation. Deliverable 4 results make this the obvious next step, not a detour.

**Primary improvement — Linear Probe on CLIP features:**
- Freeze CLIP ViT-B/32 image encoder
- Add a linear classifier head (3-class: fire / smoke / negative)
- Train on D-Fire crops:
  - Positive crops extracted from ground-truth boxes (fire + smoke)
  - Negative crops: random crops from hard-negative images (fog, sun, lamps) + random background crops from positive images
- Goal: teach CLIP what forest-domain fire and smoke look like specifically, fixing the domain mismatch that drives the recall drop

**Secondary improvement — Confidence-thresholded decision rule:**
- Currently: argmax over buckets (reject if top bucket ≠ YOLO class)
- Proposed: `keep if P(yolo_class) > τ_keep OR (P(neg) - P(yolo_class)) < τ_margin`
- Tune `τ_keep, τ_margin` on val split — gives explicit precision-recall trade-off knob we currently lack
- Report PR curves at multiple operating points

### 6.3 Success criteria for Deliverable 5

Framed as correcting the Deliverable 4 recall drop while preserving the FPR win:

| Metric | D4 YOLO-only | D4 YOLO+CLIP zero-shot | **D5 target** |
|---|---|---|---|
| Hard-neg FPR | 2.44% | 0.45% | ≤ 1.0% |
| Smoke recall | 0.791 | 0.359 | **≥ 0.70** |
| Fire recall | 0.663 | 0.469 | **≥ 0.60** |
| Overall mAP@0.5 | 0.637 | 0.387 | ≥ 0.60 |
| Latency | 13.8ms | 25.5ms | <100ms |

If D5 hits these targets, the research arc is clean: zero-shot proved concept + identified limitation → fine-tuning closed the recall gap.

### 6.4 Ablations to run in Deliverable 5

1. **Linear probe vs zero-shot CLIP** (the core comparison)
2. **Frozen CLIP backbone vs fine-tuned last N transformer layers** (if time permits)
3. **Decision rule: argmax vs confidence-thresholded** on same features
4. **Training data composition: (a) GT crops only, (b) GT + hard-neg crops, (c) GT + hard-neg + augmented synthetic fog**
5. Keep crop margin at 0.20 (D4 showed margin insensitivity — don't waste compute)
6. Keep ViT-B/32 (D4 showed ViT-L/14 worse and adds latency)

### 6.5 What to NOT do

- Don't swap to DETR. Write it into the "Future Work" section of the final report as a WWF-PTZ contingency.
- Don't re-train YOLO. Baseline is frozen across all deliverables.
- Don't re-run the full test eval with every ablation — it takes 8-15 min on T4. Use the 2,005 hard-negative subset for FPR, and a stratified 500-image sample of positives for recall, then do ONE full eval at the end with the final config.
- Don't change seed from 42. Reproducibility across deliverables.
- Don't expand the prompt bank for linear probe — the probe replaces text embeddings entirely with a learned classifier, so the prompt bank becomes irrelevant for the probe branch (keep it for a zero-shot-vs-probe comparison cell).

### 6.6 Implementation steps for Deliverable 5 notebook

1. Load YOLOv8n baseline weights (same as D4)
2. Load CLIP ViT-B/32, freeze image encoder
3. Build crop extraction pipeline:
   - Positive crops: for each image with GT boxes, extract each box (with 20% margin) — labeled by class
   - Negative crops: for each hard-negative image, random crop at a plausible location with a YOLO-like aspect ratio — labeled "negative"
   - Train/val split: use D-Fire's train/val split for consistency
4. Pre-compute CLIP features for all crops (makes training fast — it's just logistic regression on 512-dim vectors)
5. Train linear probe (cross-entropy, Adam, ~10-20 epochs, early stopping on val F1)
6. Plug probe into the same pipeline as D4 — replace `clip_verify_crops` return value to use probe predictions instead of prompt similarities
7. Re-run the D4 evaluation suite: hard-neg FPR, full test mAP/P/R, latency, qualitative examples
8. Ablation: argmax vs confidence-thresholded decision rule — sweep thresholds, plot PR curve
9. Comparison table: YOLO-only vs D4 zero-shot vs D5 probe — all three side-by-side on same test set

### 6.7 Estimated time budget on Kaggle T4

| Step | Time |
|---|---|
| Load models + extract crops | ~10 min |
| Pre-compute CLIP features on ~30k crops | ~15 min |
| Train linear probe (lightweight) | ~5 min |
| Re-run D4 eval suite with probe | ~30 min |
| Ablations (decision rule sweeps, training data variants) | ~30 min |
| Final full test eval + save | ~15 min |
| **Total** | **~105 min** |

Fits in one Kaggle session comfortably.

---

## 7. Report framing for D4 + D5 as a unified story

The cleanest narrative for the final report:

1. **SOA identified gap:** No work combines YOLO with CLIP-style semantic verification for fire detection; FPR from confounders is the dominant unsolved failure mode.

2. **Deliverable 3 (baseline):** Reproduced YOLOv8n paper result. 0.76 mAP, 0.77 precision, 0.70 recall, **2.4% FPR on hard negatives.** Confirmed: YOLO is fast and mostly accurate, but still produces the FPs the literature documents.

3. **Deliverable 4 (first improvement, zero-shot CLIP):** Added CLIP semantic verification layer. **81.6% relative FPR reduction (2.4% → 0.45%).** Directly answers SOA research question on FPR. BUT: zero-shot CLIP over-rejects legitimate smoke due to domain mismatch (internet images vs forest cameras). Smoke recall dropped 55%, fire recall 29%. Trade-off unacceptable for deployment.

4. **Deliverable 5 (second improvement, fine-tuned CLIP linear probe):** Fine-tune on D-Fire crops to domain-adapt the verifier. Add confidence-thresholded decision rule for explicit precision-recall control. Target: **preserve FPR gain + recover recall to within 5-10% of YOLO-only baseline.**

5. **Future work:** WWF PTZ deployment. Transformer-based first stage (DETR) if PTZ imagery reveals small-object recall failure — this is where the SOA's contingency path activates.

This shape is iterative research: identified problem → solved it → found new problem → targeted fix. Grader-friendly.

---

## 8. Prompt for next conversation

When starting the Deliverable 5 conversation with a new Claude, use this prompt:

> I'm continuing my LUMS CS437 Deep Learning project on forest fire/smoke detection. I've completed Deliverables 1-4. Deliverable 4 (YOLO+CLIP zero-shot verification) achieved 81% relative FPR reduction on hard negatives but caused a 43-point recall drop due to CLIP's internet-domain pretraining not matching forest-camera imagery. I'm now building Deliverable 5 (second improvement): fine-tuned CLIP linear probe + confidence-thresholded decision rule. Attached: (1) SOA.pdf — the survey identifying the gap, (2) Group4_27100082_27100340_Improvement1.ipynb — the D4 notebook, (3) improvement1_metrics.json — D4 quantitative results, (4) handoff.md — this file with full context. Please read the handoff first, then build me the D5 notebook following the same simple-language, honest-framing style as D4, targeting the success criteria in handoff Section 6.3.

---

## 9. Critical gotchas to remember

- Weights were not saved persistently from D3. D4 notebook retrains YOLO inside the notebook. **For D5, check if D4's committed version has `yolov8n_dfire_best.pt` in its output — if yes, attach that committed notebook as input and skip training. If no, first cell of D5 should retrain (same hyperparameters).**
- All D-Fire images in the Kaggle copy have ~15 corrupt files flagged during `yolo.val()`. They're auto-skipped by ultralytics. Don't worry about them.
- `/kaggle/working/` persists only if "Persistence: Files only" is set in notebook options, AND you Commit/Save-Version.
- Kaggle T4 has 16GB VRAM. Full pipeline (YOLO + CLIP ViT-B/32) uses ~6GB. Plenty of room for linear probe training.
- Seed 42 everywhere. Any deviation breaks reproducibility claims.
- The D4 full test eval uses a custom IoU-matched AP calculator, not `yolo.val()`, because `yolo.val()` doesn't know about the CLIP filter. Reuse this exact function in D5 — do NOT re-implement mAP.

---

End of handoff.
