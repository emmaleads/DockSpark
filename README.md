# 🚀 DockSpark - Molecular Docking Application

**DockSpark** is a graphical user interface (GUI) application designed to streamline molecular docking workflows using **AutoDock Vina** and **Open Babel**. It offers a user-friendly interface for receptor-ligand docking, file format conversion, energy minimization, and result visualization.

---

## 🧬 Features

- **Receptor-Ligand Docking** using AutoDock Vina ** (PDBQT format only)
- **File Format Conversion**: PDB, PDBQT, SDF, MOL2
- **Energy Minimization**: MMFF94, UFF, GAFF
- **Results Visualization**: Affinity scores, RMSD, export options
- **Standalone EXE and Python Script Available**

---

## 📦 Installation

### Option 1: Standalone `.exe` (No Python Required)
1. Download **DockSpark.exe** from the [Releases](https://github.com/yourusername/DockSpark/releases) section.
2. Install dependencies:
   - [AutoDock Vina](http://vina.scripps.edu) *(Add to PATH)*
   - [Open Babel](https://openbabel.org) *(Add to PATH)*
   - [MGLTools (optional)](https://ccsb.scripps.edu/mgltools)
3. Double-click `DockSpark.exe` to run.

> If blocked by Windows Defender: Click **More Info → Run Anyway**

---

### Option 2: Python Version (`dockspark.py`)
1. Install [Python 3.7+](https://www.python.org/downloads) (64-bit recommended).
2. Install required packages:
```bash
pip install numpy openbabel tk
