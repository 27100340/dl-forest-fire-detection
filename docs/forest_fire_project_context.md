# 🔥 Project Context File (LLM Transfer Ready)

---

# 📌 Project Title

**Early Warning System for Forest Fire Detection (WWF Collaboration)**

---

# 🎯 Project Objective

Develop a **real-time deep learning system** to detect **early-stage fire and smoke** from **PTZ camera images/videos**, enabling early intervention before large-scale damage occurs.

---

# 🧩 Problem Description

* Forest fires cause massive environmental and economic damage
* Early smoke detection is **extremely challenging** due to:

  * Low contrast
  * Visual similarity to fog/clouds
* System must:

  * Detect **fire + smoke**
  * Work in **real-time**
  * Be deployable on **edge devices**

---

# ⚙️ System Requirements

## Functional

* Detect fire and smoke
* Work on image/video data
* Output:

  * Classification OR
  * Bounding boxes OR
  * Segmentation masks

## Non-Functional

* Real-time inference
* Edge deployment (Jetson / Raspberry Pi)
* High precision (low false positives)
* Robust to:

  * Lighting variation
  * Weather (fog, haze)
  * Camera movement (PTZ)

---

# 🧠 Core Technical Areas

* Object Detection → YOLO family
* Vision Transformers → DETR, ViT
* Multimodal Models → CLIP
* Temporal Models → LSTM / Video models
* Edge AI Optimization

---

# 🧪 Dataset Requirements

* Source: PTZ camera feeds
* Must be **annotated manually**
* Classes:

  * Fire
  * Smoke

## Possible Annotation Types

* Classification labels
* Bounding boxes
* Segmentation masks

---

# 👩‍🏫 TA Deliverable Requirements (SOA Survey)

## Must Do

* Read papers involving:

  * YOLO
  * Transformers
  * CLIP / multimodal models
* Understand:

  * YOLO + Transformer integration
* Identify:

  * 3–4 datasets
* Write **State-of-the-Art Survey (LaTeX)**

## Provided Papers

1. *An Improved Forest Fire Detection Method Based on Detectron2*
2. *Attention Enhanced BiLSTM for Smoke Recognition*
3. *Image Fire Detection using CNNs*

---

# 📚 Survey Methodology (From Guide)

## Key Rules

* Start with a **survey paper**
* Build a **reading list (5–10 papers)**:

  * 1–2 foundational
  * 2–3 baseline
  * 2–3 recent SOTA

## Critical Insight Rule

> "Prior work does X but struggles with Y → we propose Z"

## How to Find Research Gap

* Compare papers
* Read limitations sections
* Analyze result tables

## Dataset Rule

* Must validate dataset BEFORE defining solution

---

# 🧠 System Understanding

## Why This Project is Hard

### 1. Vision Challenge

* Smoke is subtle, diffused, low-contrast

### 2. Real-Time Constraint

* Must run fast (→ YOLO)

### 3. Edge Deployment

* Limited compute → model efficiency required

### 4. Semantic Understanding

* Need to distinguish:

  * Smoke vs fog
  * Fire vs sunlight

---

# 🧩 Model Design Insight

## Component Roles

### YOLO

* Fast object detection
* Outputs bounding boxes
* Weakness: limited contextual understanding

### Transformers (ViT / DETR)

* Capture global relationships
* Improve smoke detection

### CLIP

* Image-text alignment
* Adds semantic reasoning

---

## 💡 Proposed Hybrid Pipeline (Concept)

Image → YOLO → Region proposals
→ Transformer → Feature refinement
→ CLIP → Semantic validation
→ Final prediction

---

# 📄 Literature Survey Progress

## ✅ Selected REAL Survey Papers

1. **Visual Fire Detection Using Deep Learning: A Survey** (2024, Neurocomputing)
2. **Fire Detection with Deep Learning: A Comprehensive Review** (2024)
3. **Early Fire and Smoke Detection Using Deep Learning: A Review** (2025, MDPI)

---

## 📖 Curated Reading List (REAL PAPERS)

### 🟢 Foundational

* *You Only Look Once (YOLO)* — Redmon et al.
* CNN-based fire detection (TA paper)

---

### 🔵 Baselines

* YOLOv5 fire detection (2023)
* YOLOv8 fire detection (2023)
* FSDNet (YOLOv3 + DenseNet)

---

### 🟣 Transformer / Advanced

* DETR (Carion et al.)
* CNN + Vision Transformer for smoke detection (2023)

---

### 🔴 Recent / Frontier

* FireMatch (semi-supervised fire detection, 2023)
* Spectral-based smoke detection (2023)

---

### 🟡 TA Papers (Mandatory)

* Detectron2-based fire detection
* BiLSTM smoke detection
* CNN fire detection

---

# 🔍 Key Insights from Literature

## Method Categories

* CNN-based
* YOLO-based (real-time)
* Transformer-based
* Hybrid models

## Major Challenges

* Early smoke detection
* False positives (clouds, fog)
* Real-time vs accuracy tradeoff
* Dataset limitations

## Trends

* CNN → YOLO → Transformers
* Increasing hybrid models
* Emerging multimodal (CLIP-like systems)

---

# 🚨 Identified Research Gap (Draft)

Current methods:

* Detect fire visually
* Lack semantic understanding

Common problems:

* Smoke vs fog confusion
* Poor early detection
* High false positives
* Weak contextual reasoning

---

## 💡 Potential Contribution

"Combine YOLO (speed) + Transformer (context) + CLIP (semantic reasoning)
to improve early smoke detection in real-time edge environments."

---

# 🧭 Execution Plan (Deliverable 1: SOA Survey)

## Step 1 — Survey Paper

* Read 1–2 survey papers fully

## Step 2 — Paper Review

For each paper:

* Method
* Dataset
* Strengths
* Weaknesses

## Step 3 — Dataset Identification

Find 3–4 datasets:

* FireNet
* FLAME
* DeepFire
* Others from survey

## Step 4 — Comparison Table

Columns:

* Method
* Model
* Dataset
* Accuracy
* Limitations

## Step 5 — Identify Gap

* Repeated limitations across papers

## Step 6 — Write Survey (LaTeX)

Sections:

1. Introduction
2. Related Work
3. Comparison
4. Research Gap
5. Proposed Direction

## Step 7 — Align with Template

* Use provided LaTeX file strictly

---

# 📂 Files Provided

* `soa_survey_template.tex`
* `Getting Started with Your Survey.docx`

---

# 📌 Current Status

✅ Project understood
✅ Survey papers identified
✅ Reading list created
⬜ Papers not yet deeply analyzed
⬜ Dataset not finalized
⬜ LaTeX survey not written

---

# 🚀 Next Actions

1. Read 1 survey paper completely
2. Summarize 5–10 papers
3. Identify datasets
4. Start LaTeX writing

---

# 🔁 Update Policy

This file must be:

* Updated after every step
* Used to transfer context across LLM chats
* Treated as single source of truth

---
