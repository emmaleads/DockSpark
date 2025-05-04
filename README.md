# DockSpark - AutoDock Vina Docking Tool

## Description

DockSpark is a user-friendly graphical interface for performing molecular docking using AutoDock Vina. It allows users to easily select ligand and receptor files, set docking parameters, run the docking simulations, and view/export the results.

## Features

* Graphical user interface for AutoDock Vina.
* Ligand and receptor selection.
* Docking parameter configuration.
* Docking execution.
* Results table.
* Export results to CSV.

## Requirements
Operating System: Windows
Python: Python 3.6 or higher must be installed
No installation needed – Simply extract and run the app from terminal

## Directory Structure

The extracted folder should have the following structure:

```
DockSpark/
├── DockSpark.py
├── README.md
├── vina/
│   └── vina.exe
├── babel/
│   └── obabel.exe
└── MGLTools/
    ├── python.exe
    └── Lib/
    └── site-packages/
    └── AutoDockTools/
        └── Utilities24/
            ├── prepare_ligand4.py
            └── prepare_receptor4.py
        └── ... (other MGLTools files)
```


## How to Use

1.  **Download and Extract:** Download the `DockSpark.zip` file and extract its contents to a folder on your computer.
2.  **Run DockSpark:** Open a terminal or command prompt, navigate to the extracted folder, and run the application using the command:
    ```bash
    python DockSpark.py
    ```
3.  **Select Ligands:** Click the "Select Ligands" button and choose one or more ligand files in `.mol2` or `.sdf` format.
4.  **Select Receptor:** Click the "Select Receptor" button and choose a receptor file in `.pdb` format.
5.  **Set Docking Parameters:** Enter the center coordinates (X, Y, Z) and grid size (X, Y, Z) for the docking box.
6.  **Run Docking:** Click the "Run Docking" button to start the simulation.
7.  **View Results:** Once the docking is complete, the results (Ligand, Mode, Affinity, RMSD) will be displayed in the "DockingResults" table.
8.  **Export Results:** Click the "Export to CSV" button to save the docking results.

## Important Notes

* This package is configured to run on **Windows** systems as it includes the `.exe` executables for AutoDock Vina and Open Babel.
* Ensure that you maintain the directory structure within the extracted `DockSpark` folder for the application to find the necessary executables and scripts.
* Molecular docking can be computationally intensive.
* **macOS and Linux Users:** This bundled version is primarily for Windows. To run DockSpark on macOS or Linux, you will need to:
    * Obtain the appropriate executables for AutoDock Vina and Open Babel for your operating system and place them in the `vina` and `babel` subdirectories, respectively.
    * Ensure you have MGLTools installed and that the paths within the `DockSpark.py` script (`ADT_PYTHON`, `PREP_LIGAND`, `PREP_RECEPTOR`) correctly point to your MGLTools installation.  You may need to modify these paths in the code.
    * ## Support

For any issues or questions, please feel free to contact [Emmanuel/segungab98@gmail.com]
