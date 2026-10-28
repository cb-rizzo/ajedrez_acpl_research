# Comparative Research on Chess Skill Evolution & ELO Deflation (2019 vs 2026)

An empirical data science investigation analyzing tactical precision, Centipawn Loss (CPL) distributions, and game-phase mechanics on Lichess open data using Stockfish evaluation pipelines.

---

## 📌 Executive Summary

This project investigates the widespread community hypothesis of **ELO deflation** on online chess platforms (Lichess). By evaluating historical games from 2019 against 2026 data through Stockfish UCI engine analysis, we mapped the calibration curve of player ratings against tactical accuracy metrics.

### Key Finding: The Asymmetric Modern Player Profile
* **Quantifiable ELO Deflation (~150–200 points):** The median baseline precision (Median CPL ≈ 30) of a **1200 ELO player in 2019** currently aligns with a **~1000 ELO player in 2026**.
* **Tactical Volatility & Blunder Asymmetry:** Despite possessing equivalent foundational precision and opening knowledge, calibrated sub-samples reveal that the modern **1000 ELO player exhibits a slightly higher Blunder Rate (CPL >= 300)** than the historical 1200 ELO player (~13% vs ~10%).

---

## 🔬 Methodology & Architecture

The analytical pipeline is built in Python, leveraging a memory-efficient streaming design to process compressed Lichess open data blocks (`.pgn.zst`).
[ Lichess Open Data Stream (.pgn.zst) ]
│
▼
[ fetch_open_data.py / build_datasets.py ] ──► Cohort Filtering & Range Sampling
│
▼
[ dataset_processor.py ]               ──► Stockfish 16 Engine Evaluation (UCI)
│
▼
[ chess_acpl_cohorts.csv ]          ──► Consolidated Metrics Pipeline
│
▼
[ eda.ipynb ]                    ──► ELO Calibration & Statistical Analytics

### Metrics Tracked:
1. **Average Centipawn Loss (ACPL):** Global average move accuracy (capped at 300 CP).
2. **Median CPL & Standard Deviation (`std_cpl`):** Measures baseline accuracy and tactical inconsistency/volatility.
3. **Blunder Rate (%):** Percentage of total moves yielding a loss of >= 300 centipawns (decisive piece/advantage blunders).
4. **Phase-Segmented ACPL:** Partitioned evaluations across Opening (Moves 1–10), Middlegame, and Endgame.

---

## 📊 Analytical Insights & Results

### 1. ELO Calibration Curve (Deflation Mapping)
By expanding the 2026 sample across an extended spectrum (800–1300 ELO), the regression curve demonstrates that current ratings require higher tactical precision to sustain equivalent ELO milestones compared to 2019.

### 2. Paired Sub-sample Comparison (1200 ELO '19 vs 1000 ELO '26)
* **Opening & Theory:** Modern players display higher theory retention in opening phases due to accessible online resources and engines.
* **Middlegame Complexity:** The increased theoretical accuracy leads to sharper middlegame structures, driving higher tactical friction and resulting in elevated blunder spikes under time pressure.

---

## 💻 Repository Structure
.
├── fetch_open_data.py    # Streaming utility for Lichess compressed zstd datasets
├── dataset_processor.py  # Stockfish parsing engine, CPL evaluation & blunder calculator
├── build_datasets.py     # Cohort extraction and multi-year dataset builder
├── eda.ipynb             # Jupyter Notebook containing exploratory data analytics & charts
├── chess_acpl_cohorts.csv # Evaluated dataset output
└── README.md             # Project documentation

---

## 🛠️ Setup & Execution

1. **Environment Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install chess zstandard requests pandas matplotlib seaborn jupyter

   Download Stockfish:
   Place the executable binary (stockfish.exe or stockfish) in the project root directory.

   Build Dataset:
   Bash
   python build_datasets.py

   Run Analysis Notebook:
   Bash
   jupyter notebook
