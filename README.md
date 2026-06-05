# Hotel Booking Demand Clustering Study

Unsupervised Learning — 2025/2026  
Alexandre Santos (72970) · David Natal (72997) · Miguel Mestre (73018)

## Overview

A reproducible clustering study of 117,430 hotel booking records. The project identifies three booking segments — Non-Refundable Advance Booker, Standard Flexible City Guest, and Premium Resort Long-Stay — using K-Means, iK-Means, and Agglomerative Hierarchical (Ward) clustering, with extensions for PCA representation study (E4) and cluster-aware anomaly analysis (E1).

## Repository Structure

```
UnsupervisedLearningProj/
├── project.ipynb          # Main notebook (all code, figures, and results)
├── run_all.py             # Single entry point — reproduces all results
├── experiments.csv        # Experiment log (method, parameters, metrics)
├── requirements.txt       # Pip dependencies with pinned versions
├── environment.yml        # Full conda environment export
├── assignment.tex         # Report source
├── assignment.pdf         # Compiled report
└── data/                  # Place dataset here (not committed)
```

## Setup

### 1. Create the conda environment

```bash
conda env create -f environment.yml
conda activate UnsupervisedLearning
```

Or with pip only:

```bash
pip install -r requirements.txt
```

### 2. Register the Jupyter kernel

```bash
python -m ipykernel install --user --name UnsupervisedLearning --display-name "UnsupervisedLearning"
```

### 3. Place the dataset

Download the course release CSV and place it at:

```
data/hotel_bookings_course_release_v1.csv
```

Expected SHA-256: `7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06`

## Reproducing All Results

```bash
conda activate UnsupervisedLearning
python run_all.py
```

This will:
1. Check that `nbconvert` is installed (installs it if missing)
2. Verify the dataset is present
3. Set `FAST_MODE = False` (full 10-seed run)
4. Execute `project.ipynb` end-to-end and overwrite it with fresh outputs

All figures and tables are embedded in the executed notebook. Use `python run_all.py --fast` for a quick pipeline integrity check (single seed, faster).

## Experiment Log

`experiments.csv` records every model run: representation, method, parameters, seed, silhouette, Calinski–Harabász, Davies–Bouldin, and notes. It is appended automatically on each execution.
