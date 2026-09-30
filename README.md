# 🚀 DockSpark 2.1 – Molecular Docking & Interaction Analysis Platform

**🗓️ Release Date:** September 30, 2026
**👤 Author:** @emmaleads
**💻 Platform:** Windows (Portable)

DockSpark is a user-friendly graphical interface for molecular docking with **AutoDock Vina**. It takes you from a raw PDB file to publication-ready results in one portable app: prepare a receptor, define a trustworthy docking box, dock one or many ligands (or screen many receptors), visualize poses in 3D, and analyze protein–ligand interactions. No installation is needed. Extract the folder and run.

---

## 📑 Table of Contents

1. [What's New in v2.1](#-whats-new-in-v21)
2. [Feature Overview](#-feature-overview)
3. [System Requirements](#-system-requirements)
4. [Installation & Quick Start](#-installation--quick-start)
5. [Detailed Workflows](#-detailed-workflows)
6. [Application Structure](#-application-structure)
7. [Advanced Usage Scenarios](#-advanced-usage-scenarios)
8. [Running on macOS / Linux](#-running-on-macos--linux)
9. [Known Issues & Limitations](#-known-issues--limitations)
10. [Troubleshooting](#-troubleshooting)
11. [Version History](#-version-history)
12. [Support & Community](#-support--community)

---

## 🎯 What's New in v2.1

DockSpark 2.1 focuses on the **front end** of a docking workflow: cleaning and preparing a receptor, defining a trustworthy docking box, and scaling a run across multiple targets, on top of everything 2.0 already offered.

### 🧹 New: Protein Prep tab
A standalone preparation step, separate from the Docking tab, so it is just as useful to people who prepare proteins with other software and only want DockSpark for docking and analysis.
- Scans a raw receptor PDB and lists **chains**, **water molecules** (aggregated per chain), and every **non-water hetero group** (the cocrystallized ligand, ions, cofactors) individually, each with a one-click **Keep/Remove** toggle.
- Optional cleanup: keep only the primary alternate conformation per residue, and/or strip existing hydrogens (AutoDockTools adds its own polar hydrogens during preparation anyway).
- **Clean & Save Receptor** writes a new PDB (the original is never modified) and reports exactly how many atoms were kept vs. removed.
- **Preview Cleaned Structure** opens the result in the same 3D viewer used elsewhere in the app, so you can visually confirm the cleanup before trusting it.
- **Use in Docking Tab** is an optional one-click bridge that loads the cleaned file straight into the Docking tab.

### 📦 New: Docking box from the cocrystallized ligand
Select one or more hetero components in the Protein Prep tab (typically the cocrystallized ligand) and compute a docking box centered on their actual coordinates, the standard "redocking box" approach, even though those same atoms are stripped from the prepared receptor. The box carries straight over into the Docking tab.

### 🎯 New: Blind Docking helper
One click computes a docking box that spans a receptor's entire coordinate extent (padded outward), for when the binding site is not known in advance. Available on the main Docking tab and per receptor during virtual screening. DockSpark warns you and suggests raising Exhaustiveness when the search volume is large.

### 👁 New: Box preview in the 3D Viewer
Before running anything, open the receptor in the browser-based 3D viewer with the current Center/Size box drawn as a wireframe cube directly over the structure, a real visual sanity check instead of trusting raw numbers.

### 🧪 New: Virtual Screening (multiple receptors × multiple ligands)
Select more than one receptor to screen your whole ligand list against every one of them in a single queue.
- Each receptor gets its own confirmation step for its docking box (auto-filled from a saved preset when one exists, or built with Blind Dock / the ligand-box tool), since different targets almost never share one binding site.
- Results, on-disk output folders, and CSV export are all organized per receptor, with a **Receptor** column added throughout.
- A failed receptor (bad file, preparation error) is skipped with a log entry rather than aborting the whole screen.

### 🛠️ Fixed: Open Babel version / data-directory mismatch
Open Babel's executable and its `data/` folder (element tables, force field definitions) now come from the same matched install, bundled inside `MGLTools/OpenBabel-2.3.2/`. Previously a standalone `babel/obabel.exe` was paired with a data folder from a different version, which caused version-mismatch warnings and "Could not setup force field" failures during minimization and conversion.

---

## 🌟 Feature Overview

### 🧹 Protein Prep Module *(new in 2.1)*
- Water / ion / cofactor / cocrystallized-ligand removal, per component
- Alternate-conformation and hydrogen stripping
- Docking box computed directly from a selected ligand's coordinates
- Cleaned-structure preview before use

### 🔄 Docking Module
- AutoDock Vina integration with full GUI controls
- Ligand and receptor selection through file dialogs
- Batch ligand docking
- Virtual screening across multiple receptors *(new in 2.1)*
- Blind docking box and box preview *(new in 2.1)*
- Adjustable parameters: box center and size, exhaustiveness, CPU count, number of modes
- Named parameter presets per target, saved to disk
- Real-time progress monitoring
- Results table with ligand, mode, affinity and RMSD values, now including receptor *(new in 2.1)*
- CSV export for downstream analysis

### ⚡ Energy Minimization
- Force fields: MMFF94, MMFF94s, UFF, Ghemical, GAFF
- Customizable optimization steps
- Batch-capable 3D structure generation

### 🔁 Format Conversion
- Open Babel integration (version-matched executable + data directory as of 2.1)
- 50+ supported molecular formats
- Hydrogen addition and partial charge assignment
- Direct GUI access to Open Babel tools
- Supports `.mol2`, `.sdf`, `.pdb`, `.pdbqt`

### 👁️ 3D Visualization
- Interactive **3Dmol.js** viewer running in your browser
- Load and switch between multiple ligands; combine them for comparison
- Automatic multi-pose detection and separation from docking results
- Cartoon, stick, sphere and surface styles, with custom colors and lighting
- Distance measurement and interactive selection
- Protein sequence viewer with clickable, draggable residue selection
- Docking-box wireframe preview *(new in 2.1)*

### 🔬 Interaction Analysis
- Detects H-bonds, hydrophobic contacts, halogen bonds, salt bridges, π–π stacking, π–cation interactions and van der Waals contacts
- Residue-specific analysis: focus only on interacting residues
- Filter by interaction type
- Export interaction data to CSV for reports and publications

### 💾 Export
- High-resolution PNG and SVG images
- Batch pose export (all docking poses at once)
- Interactive HTML output
- Viewer session saving and restoring
- Docking results, interaction tables and viewer states

---

## 🧰 System Requirements

| Requirement | Details |
|---|---|
| OS | Windows 10/11 (portable, no installer) |
| Python | 3.7 or higher, installed on your system, to launch `DockSpark.py` |
| Bundled tools | AutoDock Vina, MGLTools (with its own Python interpreter) and Open Babel 2.3.2 are all included |
| Storage | 500 MB free |
| Memory | 4 GB (8 GB recommended) |
| Browser | Any modern browser with JavaScript enabled (for the 3D viewer) |

---

## 🚀 Installation & Quick Start

**1️⃣ Download & Extract**
Download the DockSpark zip file and extract it to a folder on your computer. Keep the folder structure intact (see [Application Structure](#-application-structure)), because DockSpark locates its bundled tools relative to itself.

**2️⃣ Run the Application**
Open a terminal or command prompt, navigate to the extracted folder, and run:
```bash
python DockSpark.py
```
Alternatively, double-click `DockSpark.py` if `.py` / `.pyw` files are associated with Python on your machine.

**3️⃣ Prepare Your Receptor** *(optional, new in 2.1)*
- Go to the **Protein Prep** tab and load a raw receptor PDB
- Review and toggle chains, water, ligands and ions to keep or remove
- Optionally compute a docking box from the cocrystallized ligand
- **Clean & Save**, then **Preview** or send straight to the Docking tab

**4️⃣ Dock**
- Go to the **Docking** tab
- Select receptor(s) (`.pdb`) and ligand(s) (`.mol2`, `.sdf`, `.pdbqt`). Select multiple receptors to run a virtual screen
- Set the docking box (center and size), or use **Blind Dock** / **Preview Box**
- Configure exhaustiveness, CPUs and number of modes
- Click **Start Docking** (for multiple receptors, confirm each receptor's box first)
- Review results in the results table and export to CSV

**5️⃣ Visualize & Analyze**
- Open the **3D Viewer** tab
- Load protein and ligand PDB files (use Multiple Ligands for comparisons)
- Launch the viewer in your browser
- Detect interactions, then export images, poses or interaction tables

---

## 🧭 Detailed Workflows

### Docking box parameters
| Parameter | Meaning |
|---|---|
| Center X / Y / Z | Center of the search box, in Å, in the receptor's coordinate frame |
| Size X / Y / Z | Box dimensions in Å |
| Exhaustiveness | How thorough the search is. Higher is more reliable but slower |
| CPUs | Number of threads Vina may use |
| Modes | Maximum number of binding poses to report |

Three ways to define the box:
1. **Manual**: type in center and size values.
2. **From the cocrystallized ligand** (Protein Prep tab): the standard redocking approach when a known ligand is present.
3. **Blind docking**: covers the whole receptor when the site is unknown. Increase Exhaustiveness for large boxes.

Always use **Preview Box** to check the box visually before starting a long run.

### Reading the results
The results table reports, per ligand and pose: **Receptor**, **Ligand**, **Mode**, **Affinity** (kcal/mol, more negative is stronger predicted binding) and **RMSD** values. Use **Export to CSV** to save the table.

---

## 📁 Application Structure

```
DockSpark-2.1/
├── DockSpark.py                 # Main application
├── README.md
├── vina/                        # AutoDock Vina binaries
│   └── vina.exe
├── MGLTools/                    # AutoDock preparation tools
│   ├── python.exe
│   ├── OpenBabel-2.3.2/         # Open Babel (matched exe + data, used app-wide as of 2.1)
│   │   ├── obabel.exe
│   │   ├── obgui.exe
│   │   └── data/
│   └── Lib/site-packages/AutoDockTools/Utilities24/
│       ├── prepare_receptor4.py
│       └── prepare_ligand4.py
├── dockspark_presets.json       # Saved per-target docking parameter presets
├── docking_output/              # Docking results (per-receptor and virtual-screening subfolders)
└── minimized_ligands/           # Energy-minimized structures
```

> **Upgrading from 2.0 or 1.x?** The standalone `babel/` folder is no longer used. Open Babel now lives inside `MGLTools/OpenBabel-2.3.2/`.

---

## 🔧 Advanced Usage Scenarios

### 🧪 Multi-Ligand Virtual Screening *(expanded in 2.1)*
- Load one or more receptors and multiple ligand files
- Confirm or adjust each receptor's docking box (blind, ligand-derived, preset or manual)
- Run batch docking across every receptor × ligand pair
- Compare results and visualize top hits, filtered by receptor

### 🧹 Receptor Cleanup Before Docking *(new in 2.1)*
- Load a raw, as-downloaded PDB straight from the PDB
- Strip crystallographic water, buffer/cryoprotectant molecules and the cocrystallized ligand
- Optionally keep a catalytic ion or cofactor
- Use the cocrystallized ligand's own coordinates to define a targeted docking box before it is removed

### 🔍 Interaction Mechanism Studies
- Load a protein–ligand complex
- Detect and filter interactions by type
- Export interaction tables for reports or publications

---

## 🍎 Running on macOS / Linux

This bundle targets **Windows** because it ships `.exe` binaries for AutoDock Vina and Open Babel. To run DockSpark on macOS or Linux you will need to:

1. Obtain the appropriate AutoDock Vina and Open Babel executables for your operating system and place them where DockSpark expects them (`vina/` for Vina; for Open Babel, point DockSpark at a matching executable **and** its data directory, since mismatched versions cause the errors described in the 2.1 fix above).
2. Install MGLTools and make sure the paths in `DockSpark.py` (`ADT_PYTHON`, `PREP_LIGAND`, `PREP_RECEPTOR`) point to your MGLTools installation. You may need to edit these paths in the code.

Native cross-platform support is not yet available.

---

## 🐛 Known Issues & Limitations

- **Platform:** Windows-only (temporary).
- **Large structures:** Performance is reduced with more than 100k atoms.
- **File formats:** Some rare formats may require conversion first.
- **Protein Prep identifies components, not their meaning.** It works on PDB text directly (no chemistry engine), so it lists every hetero group it finds but cannot tell which one is the biologically relevant cocrystallized ligand and which is a buffer additive. Review the list before removing or keeping components.
- **Blind docking cost:** Boxes covering large structures need higher Exhaustiveness for reliable sampling, which increases runtime accordingly.
- Molecular docking can be computationally intensive, especially for batch and virtual-screening runs.

---

## 🆘 Troubleshooting

**General**
- Keep the directory structure intact
- Run as Administrator if file permission issues occur
- Check the console output for detailed error logs
- Verify your input file formats

**3D Viewer not opening?**
- Check your default browser settings
- Ensure JavaScript is enabled
- Try another browser

**"Could not setup force field" or version-mismatch warnings during conversion/minimization?**
- Fixed in 2.1 by matching Open Babel's executable and data directory. Update to this version if you still see it.

**DockSpark can't find Vina, Open Babel or the preparation scripts?**
- Make sure you extracted the whole folder and did not move individual files out of it.

---

## 📜 Version History

| Version | Highlights |
|---|---|
| **2.1** (2026-09-30) | Protein Prep tab, ligand-derived docking box, Blind Docking helper, box preview in 3D viewer, multi-receptor virtual screening, Open Babel version-match fix |
| **2.0** | 3Dmol.js viewer, multi-pose detection, interaction analysis, energy minimization, format conversion, parameter presets, professional export |
| **1.x** | Original AutoDock Vina GUI: ligand/receptor selection, docking parameters, results table, CSV export |

---

## 📞 Support & Community

- **Issues / feature requests:** Submit a bug report or feature request
- **Questions:** Emmanuel, segungab98@gmail.com
