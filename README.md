# Reducing False Positives in Real-Time Forest Fire and Smoke Detection via Cascaded Vision-Language Verification

**Course:** CS437/CS5317/EE414/EE513 — Deep Learning, Spring 2026, LUMS
**Group 4:**
- Muhammad Baqir Hassan Babar (27100340)
- Momin Fahed Khan (27100082)

This repository contains all code, notebooks, results, and the final report for our course project on reducing false positives in real-time forest fire and smoke detection. The work was carried out across the six course deliverables (SOA → dataset → baseline → improvement 1 → improvement 2 → final report).

---

## 1. Project at a glance

**Problem.** Off-the-shelf YOLO detectors are fast and accurate enough for real-time fire/smoke detection from PTZ camera feeds — but they produce a steady stream of false alarms on visually similar phenomena (fog, clouds, haze, sun glare, lamp lights). Across 12 papers surveyed in our SOA, this is the dominant unsolved failure mode.

**Hypothesis.** A vision-language model (CLIP) attached to YOLO as a post-detection semantic verifier can reject these confounder false positives without retraining the detector or sacrificing real-time inference latency.

**What we built.** A cascaded YOLO → CLIP verification pipeline, in two improvement stages:

| Stage | What it does | Headline result |
|---|---|---|
| Baseline (D3) | YOLOv8n fine-tuned on D-Fire, 50 epochs | mAP@0.5 = 0.7614, **HN-FPR = 2.44%** |
| Improvement 1 (D4) | YOLO + zero-shot CLIP w/ confounder prompts | **HN-FPR 0.55%** (−77%), but recall −23 pp |
| **Improvement 2 (D5)** | YOLO + LR linear probe over frozen CLIP feats, with hard-neg mining + text-anchored synthetic negs + cascaded gating | **HN-FPR 0.70% (−71%), recall only −4 pp**, 21 ms latency |

The right role for CLIP in fire detection is not zero-shot classification but as a frozen feature extractor for a domain-adapted probe. The full report is in `final_report/`.

---

## 2. Repository structure

```
.
├── README.md                                  ← you are here
├── deliverable1_soa_survey/                   ← state-of-the-art survey
│   ├── Group4_27100340_27100082_SOA.pdf       ← submitted PDF
│   ├── SOA.pdf                                ← duplicate (compiled from soa_survey.tex)
│   └── soa_survey.tex                         ← LaTeX source
│
├── deliverable2_dataset_exploration/
│   └── Group4_27100082_27100340.ipynb         ← D-Fire EDA + annotation analysis
│
├── deliverable3_baseline/
│   ├── baseline.ipynb                         ← YOLOv8n training notebook
│   └── yolov8n_dfire_best.pt                  ← trained weights (6 MB) -- reused by D4 & D5
│
├── deliverable4_improvement1_yoloclip/
│   ├── improvement1_final.ipynb               ← YOLO + zero-shot CLIP, full pipeline + ablations
│   ├── improvement1_metrics.json              ← all D4 quantitative results
│   └── handoff_forimprovement1_to_2.md        ← design notes that motivated D5
│
├── deliverable5_improvement2_probe/
│   └── improvement2_final.ipynb               ← YOLO + linear probe over CLIP features (HEADLINE)
│
├── final_report/                              ← Deliverable 6
│   ├── main.tex                               ← LaTeX source (ICML 2021 template)
│   ├── main.bib                               ← bibliography
│   ├── icml2021.sty + algorithm{,ic}.sty + fancyhdr.sty + icml2021.bst
│   ├── make_figs.py                           ← matplotlib script that generates all paper figures
│   └── figures/                               ← .pdf + .png versions of each figure
│       ├── fpr_recall_frontier.{pdf,png}
│       ├── per_class.{pdf,png}
│       └── tau_sweep.{pdf,png}
│
└── docs/
    ├── forest_fire_project_context.md         ← long-form project background
    └── fire_detection_summary.md              ← detailed notes on the survey paper
```

---

## 3. Reproducing the results

All notebooks in this repo were developed and run on **Kaggle** with a single Tesla T4 GPU. The recommended way to reproduce is to upload the notebooks into Kaggle, attach the inputs below, and re-run.

### 3.1 Kaggle inputs

Each notebook expects the following Kaggle inputs (attach them via "Add Input" in the sidebar):

| Notebook | Required inputs |
|---|---|
| `deliverable3_baseline/baseline.ipynb` | `sayedgamal99/smoke-fire-detection-yolo` (D-Fire dataset) |
| `deliverable4_improvement1_yoloclip/improvement1_final.ipynb` | D-Fire + a private dataset containing `yolov8n_dfire_best.pt` (the weights from D3) |
| `deliverable5_improvement2_probe/improvement2_final.ipynb` | Same as D4 |

Both improvement notebooks pip-install CLIP from OpenAI's GitHub at start.

### 3.2 Reproducibility commitments

- Seed 42 is set in every notebook (`random`, `numpy`, `torch`).
- YOLO baseline hyperparameters are frozen across all deliverables (50 epochs, imgsz 640, batch 16, lr0 0.01, mosaic 1.0, fliplr 0.5, optimiser auto).
- CLIP is frozen (no fine-tuning of the encoder); only the linear probe head is trained.
- All Improvement 2 ablations re-use the same baseline weights `yolov8n_dfire_best.pt` to isolate the effect of the verifier.

### 3.3 Time budget

On a single Tesla T4:
- Baseline training: ~30 minutes
- Improvement 1 full notebook (with ablations + full test eval): ~25 minutes
- Improvement 2 full notebook (probe training + 4 ablations + 3 full test evals + ensemble): ~70–90 minutes

---

## 4. The final report

The final research paper is in `final_report/main.tex`. To compile to PDF:

**Option A — Overleaf (easiest):**
1. Create a new project on https://overleaf.com.
2. Upload everything from `final_report/` (the `.tex`, `.bib`, `.sty`, `.bst` files, and the `figures/` folder).
3. Set the main document to `main.tex` and compile (it uses `pdflatex`).
4. Output: `Group4_27100340_27100082_Report.pdf` (rename after compiling).

**Option B — local LaTeX install:**
```bash
cd final_report
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
mv main.pdf Group4_27100340_27100082_Report.pdf
```

The figures (`figures/*.pdf`) are pre-generated by `make_figs.py` and committed; you do not need to re-run that script unless you want to regenerate them.

---

## 5. Headline results (one-table summary)

All numbers from `deliverable5_improvement2_probe/improvement2_final.ipynb`. Cascade rows use a single shared 11-point AP / IoU=0.5 evaluator; the YOLO-only canonical reference uses Ultralytics' `yolo.val()`.

| System                          | mAP@0.5 | Mean P | Mean R | HN-FPR  | Latency (ms)   |
|---------------------------------|--------:|-------:|-------:|--------:|---------------:|
| Native YOLO (yolo.val)          | 0.7614  | 0.7696 | 0.6971 | 2.44%   | 16.5           |
| YOLO-only (custom harness)      | 0.6370  | 0.7481 | 0.7272 | 2.44%   | 13.2           |
| I1 — zero-shot CLIP             | 0.5559  | 0.8091 | 0.5625 | 0.55%   | 20.8           |
| I2 — LR probe v1                | 0.6365  | 0.7649 | 0.7029 | 1.25%   | 21.2           |
| **I2 — LR probe v2 (headline)** | 0.6355  | 0.7714 | 0.6830 | **0.70%** | 21.1         |
| I2 — ensemble (v2 + text)       | 0.5576  | 0.7968 | 0.6063 | 0.30%   | 21.0           |

The latency budget for edge deployment is 100 ms per frame. All systems clear it by a >2× margin.

---

## 6. Dataset

The benchmark used throughout this project is **D-Fire** (de Venâncio et al., 2022): 21,527 RGB images with YOLO-format bounding-box annotations for two classes (`0=smoke`, `1=fire`). The standard split is 14,122 / 3,099 / 4,306 images for train / val / test. The 2,005 test images with empty label files (the "hard-negative" subset — fog, sun glare, lamp lights, reflections) are the critical FPR-evaluation subset.

Public mirror: https://github.com/gaia-solutions-on-demand/DFireDataset
Kaggle: https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo

We do not redistribute the raw dataset in this repository to respect dataset licensing; please attach it via Kaggle as described in §3.1.

---

## 7. Citation

If you build on this work, you can cite the report as:

```bibtex
@misc{group4_dlproject_2026,
  author       = {Babar, Muhammad Baqir Hassan and Khan, Momin Fahed},
  title        = {Reducing False Positives in Real-Time Forest Fire and Smoke Detection
                  via Cascaded Vision-Language Verification},
  year         = {2026},
  howpublished = {LUMS CS437/CS5317/EE414/EE513 Spring 2026 Project Report},
  url          = {https://github.com/<USERNAME>/dl-forest-fire-detection}
}
```

(Replace `<USERNAME>` with the GitHub account you push this repo under.)

---

## 8. Acknowledgments

We thank the course staff of CS437/CS5317/EE414/EE513 (Spring 2026) for guidance throughout the project, and WWF for motivating the deployment scenario that shaped our problem framing.
