# Collatz Mapora Engine: Recursive Residue Network Analyzer

**Author:** Independent Researcher  
**Status:** Active Experiment  


## 🧪 Project Overview
The **Mapora Engine** (Recursive Residue Network Analyzer) is a Python-based computational tool designed to analyze the **Logical Density** of the Collatz Conjecture ($3n+1$). 

Unlike traditional brute-force counters that check individual numbers, this engine analyzes **Residue Classes** (sets of numbers $mk+r$) to quantify the structural stability of the Collatz graph.

## 🗝️ Key Findings
1.  **Stability Ratio:** The system exhibits a mean stability ratio of **~2.75**, indicating it acts as a lossy compressor.
2.  **The Fibonacci Weakness:** Identified a structural anomaly at Residue 987 ($F_{16}$), where the stability ratio drops to **2.57**.
3.  **The Horizon Event:** Longitudinal scans up to magnitude $2^{1000}$ show that stability **increases** with magnitude (Ratio 4.36), suggesting scale invariance.

## 🚀 How to Run the Code
This repository contains the `mapora_engine.py` script. You can run the different experiments by uncommenting the relevant sections at the bottom of the file.

### Prerequisites
* Python 3.x
* NetworkX (`pip install networkx`)
* Matplotlib (`pip install matplotlib`)

### Running the Horizon Scan
```bash
python mapora_engine.py
