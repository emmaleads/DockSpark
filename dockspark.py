import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import csv
import sys

class SystemOpenBabelDockingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DockSpark")
        self.root.geometry("1200x900")
        
        # Variables
        self.receptor_file = ""
        self.ligand_files = []
        self.output_dir = os.getcwd()
        self.docking_results = []
        
        # Docking parameters
        self.exhaustiveness = tk.IntVar(value=8)
        self.num_modes = tk.IntVar(value=9)
        self.energy_range = tk.DoubleVar(value=3.0)
        
        # Open Babel settings (for system calls)
        self.obabel_ff = tk.StringVar(value="mmff94")
        self.obabel_steps = tk.IntVar(value=500)
        
        # AutoDock Tools path
        self.adt_path = r'"C:\Program Files (x86)\MGLTools-1.5.7\adt.bat"'
        
        # Verify system Open Babel
        self.obabel_available = self.check_system_obabel()
        
        # UI Setup
        self.create_widgets()

    def check_system_obabel(self):
        """Check if Open Babel is available in system PATH"""
        try:
            result = subprocess.run(["obabel", "--version"], 
                                  capture_output=True, 
                                  text=True,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            if "Open Babel" in result.stdout:
                return True
        except FileNotFoundError:
            pass
        messagebox.showwarning(
            "Open Babel Not Found",
            "System Open Babel not found in PATH.\n"
            "Please install Open Babel for Windows and add it to your system PATH."
        )
        return False

    def create_widgets(self):
        # Main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.docking_tab = ttk.Frame(self.notebook)
        self.tools_tab = ttk.Frame(self.notebook) if self.obabel_available else ttk.Frame()
        self.adt_tab = ttk.Frame(self.notebook)  # AutoDock Tools tab
        self.results_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.docking_tab, text="Docking Setup")
        if self.obabel_available:
            self.notebook.add(self.tools_tab, text="Open Babel Tools")
        self.notebook.add(self.adt_tab, text="AutoDock Tools")
        self.notebook.add(self.results_tab, text="Results")
        
        # Build interfaces
        self.build_docking_tab()
        if self.obabel_available:
            self.build_tools_tab()
        self.build_adt_tab()  # Build ADT tab
        self.build_results_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.update_status("Ready")

    def build_adt_tab(self):
        """Simplified AutoDock Tools interface that just launches ADT"""
        main_frame = ttk.Frame(self.adt_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        ttk.Label(main_frame, 
                 text="AutoDock Tools Launcher",
                 font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Description
        ttk.Label(main_frame, 
                 text="This will launch AutoDock Tools (ADT) for independent use.\n"
                      "The application will not control ADT - use it normally.",
                 wraplength=500).pack(pady=10)
        
        # Launch Button
        launch_btn = ttk.Button(main_frame, 
                              text="Launch AutoDock Tools", 
                              command=self.launch_adt)
        launch_btn.pack(pady=20)
        
        # Status
        self.adt_status_var = tk.StringVar(value="Ready to launch AutoDock Tools")
        ttk.Label(main_frame, 
                 textvariable=self.adt_status_var,
                 wraplength=500).pack(pady=10)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.adt_log = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.adt_log.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.adt_log)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.adt_log.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.adt_log.yview)

    def launch_adt(self):
        """Simply launch AutoDock Tools without any control"""
        self.adt_log_message("Attempting to launch AutoDock Tools...")
        self.adt_status_var.set("Launching AutoDock Tools...")
        self.root.update()
        
        try:
            # Just launch ADT without any parameters or control
            subprocess.Popen(self.adt_path, shell=True)
            self.adt_log_message("AutoDock Tools launched successfully")
            self.adt_log_message("Note: The application has no control over ADT - use it independently")
            self.adt_status_var.set("AutoDock Tools is running independently")
        except Exception as e:
            self.adt_log_message(f"Failed to launch AutoDock Tools: {str(e)}")
            self.adt_status_var.set("Error launching AutoDock Tools")
            messagebox.showerror("Error", f"Could not launch AutoDock Tools:\n{str(e)}")

    def adt_log_message(self, message):
        """Add message to ADT log"""
        self.adt_log.config(state=tk.NORMAL)
        self.adt_log.insert(tk.END, message + "\n")
        self.adt_log.see(tk.END)
        self.adt_log.config(state=tk.DISABLED)
        self.root.update()

    # [Rest of your existing methods remain unchanged...]
    # build_docking_tab, build_tools_tab, build_results_tab, etc.
    def build_docking_tab(self):
        # File selection frame
        file_frame = ttk.LabelFrame(self.docking_tab, text="Molecular Files")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Receptor
        ttk.Label(file_frame, text="Receptor:").grid(row=0, column=0, sticky=tk.W)
        self.receptor_entry = ttk.Entry(file_frame, width=60)
        self.receptor_entry.grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.select_receptor).grid(row=0, column=2)
        ttk.Button(file_frame, text="Remove", command=self.remove_receptor).grid(row=0, column=3)
        
         # Ligands
        ttk.Label(file_frame, text="Ligands:").grid(row=1, column=0, sticky=tk.W)
        self.ligands_listbox = tk.Listbox(file_frame, height=5, selectmode=tk.MULTIPLE)
        self.ligands_listbox.grid(row=1, column=1, padx=5, sticky=tk.EW)
        
        btn_frame = ttk.Frame(file_frame)
        btn_frame.grid(row=1, column=2, columnspan=2, sticky=tk.W)
        ttk.Button(btn_frame, text="Add...", command=self.add_ligands).grid(row=0, column=0, padx=2)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected_ligands).grid(row=0, column=1, padx=2)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all_ligands).grid(row=0, column=2, padx=2)
        
         # Output directory
        ttk.Label(file_frame, text="Output:").grid(row=2, column=0, sticky=tk.W)
        self.output_entry = ttk.Entry(file_frame, width=60)
        self.output_entry.grid(row=2, column=1, padx=5)
        self.output_entry.insert(0, self.output_dir)
        ttk.Button(file_frame, text="Browse...", command=self.select_output_dir).grid(row=2, column=2)
        
         # Docking parameters
        params_frame = ttk.LabelFrame(self.docking_tab, text="Docking Parameters")
        params_frame.pack(fill=tk.X, padx=5, pady=5)
        
         # Grid center
        ttk.Label(params_frame, text="Center (Å):").grid(row=0, column=0, sticky=tk.W)
        self.x_entry = ttk.Entry(params_frame, width=8)
        self.x_entry.grid(row=0, column=1)
        self.y_entry = ttk.Entry(params_frame, width=8)
        self.y_entry.grid(row=0, column=2)
        self.z_entry = ttk.Entry(params_frame, width=8)
        self.z_entry.grid(row=0, column=3)
        
        ttk.Label(params_frame, text="Size (Å):").grid(row=0, column=4, sticky=tk.W)
        self.size_entry = ttk.Entry(params_frame, width=8)
        self.size_entry.insert(0, "20")
        self.size_entry.grid(row=0, column=5)
        
         # Advanced parameters
        ttk.Label(params_frame, text="Exhaustiveness:").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(params_frame, from_=1, to=32, textvariable=self.exhaustiveness, width=5).grid(row=1, column=1)
        
        ttk.Label(params_frame, text="Modes:").grid(row=1, column=2, sticky=tk.W)
        ttk.Spinbox(params_frame, from_=1, to=20, textvariable=self.num_modes, width=5).grid(row=1, column=3)
        
        ttk.Label(params_frame, text="Energy Range:").grid(row=1, column=4, sticky=tk.W)
        ttk.Spinbox(params_frame, from_=0.1, to=10.0, increment=0.1,
                     textvariable=self.energy_range, width=5).grid(row=1, column=5)
        
         # Run button
        self.run_btn = ttk.Button(self.docking_tab, text="Run Docking", command=self.start_docking)
        self.run_btn.pack(pady=10)
        
         # Progress bar
        self.progress = ttk.Progressbar(self.docking_tab, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
         # Log area
        log_frame = ttk.LabelFrame(self.docking_tab, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

    def build_tools_tab(self):
        """Open Babel tools interface using system commands"""
        main_frame = ttk.Frame(self.tools_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Conversion frame
        conv_frame = ttk.LabelFrame(main_frame, text="File Conversion")
        conv_frame.pack(fill=tk.X, pady=5)
        
        formats = [
            ("PDB → PDBQT", "pdb", "pdbqt"),
            ("PDBQT → PDB", "pdbqt", "pdb"),
            ("SDF → PDBQT", "sdf", "pdbqt"),
            ("MOL2 → PDBQT", "mol2", "pdbqt")
        ]
        
        for i, (label, in_fmt, out_fmt) in enumerate(formats):
            ttk.Button(conv_frame, text=label,
                      command=lambda f=in_fmt, t=out_fmt: self.system_convert(f, t)
                     ).grid(row=i//2, column=i%2, padx=5, pady=5, sticky=tk.W)
        
        # Minimization frame
        min_frame = ttk.LabelFrame(main_frame, text="Energy Minimization")
        min_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(min_frame, text="Force Field:").grid(row=0, column=0)
        ttk.Combobox(min_frame, textvariable=self.obabel_ff,
                    values=["mmff94", "uff", "gaff"], width=10).grid(row=0, column=1)
        
        ttk.Label(min_frame, text="Steps:").grid(row=0, column=2)
        ttk.Spinbox(min_frame, from_=100, to=5000, increment=100,
                   textvariable=self.obabel_steps, width=5).grid(row=0, column=3)
        
        ttk.Button(min_frame, text="Minimize Selected",
                  command=self.system_minimize).grid(row=0, column=4, padx=5)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Open Babel Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.obabel_log = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.obabel_log.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.obabel_log)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.obabel_log.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.obabel_log.yview)

    def build_results_tab(self):
        """Results display interface"""
        main_frame = ttk.Frame(self.results_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for results
        tree_frame = ttk.LabelFrame(main_frame, text="Docking Results")
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.results_tree = ttk.Treeview(tree_frame, columns=('Ligand','Mode', 'Affinity', 'RMSD lb', 'RMSD ub', 'Output'),
                                       show='headings')
        
        # Configure columns
        self.results_tree.heading('Ligand', text='Ligand')
        self.results_tree.heading('Mode', text='Mode')
        self.results_tree.heading('Affinity', text='Affinity (kcal/mol)')
        self.results_tree.heading('RMSD lb', text='RMSD lb')
        self.results_tree.heading('RMSD ub', text='RMSD ub')
        self.results_tree.heading('Output', text='Output File')
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Export to CSV", command=self.export_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Open in Viewer", command=self.open_result).pack(side=tk.LEFT, padx=5)

    # Core functions
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update()

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def obabel_log_message(self, message):
        self.obabel_log.config(state=tk.NORMAL)
        self.obabel_log.insert(tk.END, message + "\n")
        self.obabel_log.see(tk.END)
        self.obabel_log.config(state=tk.DISABLED)
        self.root.update()

    # File operations
    def select_receptor(self):
        file_path = filedialog.askopenfilename(
            title="Select Receptor File",
            filetypes=[("PDBQT Files", "*.pdbqt"), ("PDB Files", "*.pdb")]
        )
        if file_path:
            self.receptor_file = file_path
            self.receptor_entry.delete(0, tk.END)
            self.receptor_entry.insert(0, file_path)
            self.update_status(f"Receptor: {os.path.basename(file_path)}")

    def add_ligands(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Ligand Files",
            filetypes=[("PDBQT Files", "*.pdbqt"), ("PDB Files", "*.pdb"), 
                      ("SDF Files", "*.sdf"), ("MOL2 Files", "*.mol2")]
        )
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.ligand_files:
                    self.ligand_files.append(file_path)
                    self.ligands_listbox.insert(tk.END, os.path.basename(file_path))
            self.update_status(f"Added {len(file_paths)} ligand(s)")

    def remove_receptor(self):
        self.receptor_file = ""
        self.receptor_entry.delete(0, tk.END)
        self.update_status("Receptor removed")

    def remove_selected_ligands(self):
        selected = self.ligands_listbox.curselection()
        if selected:
            for i in reversed(selected):
                self.ligands_listbox.delete(i)
                del self.ligand_files[i]
            self.update_status(f"Removed {len(selected)} ligand(s)")

    def clear_all_ligands(self):
        self.ligands_listbox.delete(0, tk.END)
        self.ligand_files = []
        self.update_status("All ligands cleared")

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)
            self.update_status(f"Output directory: {dir_path}")

    # System Open Babel functions
    def system_convert(self, in_format, out_format):
        """Convert files using system Open Babel"""
        file_paths = filedialog.askopenfilenames(
            title=f"Select {in_format.upper()} files to convert",
            filetypes=[(f"{in_format.upper()} Files", f"*.{in_format}")]
        )
        
        if not file_paths:
            return
            
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
            
        success = 0
        for file_path in file_paths:
            try:
                out_file = os.path.join(
                    output_dir,
                    f"{os.path.splitext(os.path.basename(file_path))[0]}.{out_format}"
                )
                
                cmd = [
                    "obabel",
                    f"-i{in_format}",
                    file_path,
                    f"-o{out_format}",
                    f"-O{out_file}"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if os.path.exists(out_file):
                    self.obabel_log_message(f"Converted: {file_path} → {out_file}")
                    success += 1
                else:
                    self.obabel_log_message(f"Failed: {file_path}\n{result.stderr}")
            except Exception as e:
                self.obabel_log_message(f"Error converting {file_path}: {str(e)}")
        
        self.update_status(f"Converted {success}/{len(file_paths)} files")
        messagebox.showinfo("Conversion Complete", f"Processed {success} of {len(file_paths)} files")

    def system_minimize(self):
        """Energy minimization using system Open Babel"""
        file_paths = filedialog.askopenfilenames(
            title="Select files to minimize",
            filetypes=[("All Supported", "*.pdb *.pdbqt *.mol2 *.sdf")]
        )
        
        if not file_paths:
            return
            
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
            
        success = 0
        for file_path in file_paths:
            try:
                fmt = os.path.splitext(file_path)[1][1:]
                out_file = os.path.join(
                    output_dir,
                    f"min_{os.path.basename(file_path)}"
                )
                
                cmd = [
                    "obminimize",
                    f"-ff{self.obabel_ff.get()}",
                    f"-n{self.obabel_steps.get()}",
                    file_path,
                    f"-o{fmt}",
                    f"-O{out_file}"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if os.path.exists(out_file):
                    self.obabel_log_message(f"Minimized: {file_path} → {out_file}")
                    success += 1
                else:
                    self.obabel_log_message(f"Failed: {file_path}\n{result.stderr}")
            except Exception as e:
                self.obabel_log_message(f"Error minimizing {file_path}: {str(e)}")
        
        self.update_status(f"Minimized {success}/{len(file_paths)} files")
        messagebox.showinfo("Minimization Complete", f"Processed {success} of {len(file_paths)} files")

    # Docking functions
    def validate_parameters(self):
        try:
            # Validate grid parameters
            float(self.x_entry.get())
            float(self.y_entry.get())
            float(self.z_entry.get())
            float(self.size_entry.get())
            
            # Validate receptor
            if not self.receptor_file:
                raise ValueError("No receptor file selected!")
                
            if not self.receptor_file.endswith('.pdbqt'):
                # Auto-convert receptor
                out_file = os.path.join(
                    self.output_dir,
                    f"{os.path.splitext(os.path.basename(self.receptor_file))[0]}_converted.pdbqt"
                )
                
                cmd = [
                    "obabel",
                    f"-ipdb",
                    self.receptor_file,
                    "-opdbqt",
                    f"-O{out_file}"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if os.path.exists(out_file):
                    self.receptor_file = out_file
                    self.receptor_entry.delete(0, tk.END)
                    self.receptor_entry.insert(0, out_file)
                    self.log_message(f"Auto-converted receptor to PDBQT: {out_file}")
                else:
                    raise ValueError(f"Failed to convert receptor:\n{result.stderr}")
            
            # Validate ligands
            if not self.ligand_files:
                raise ValueError("No ligand files selected!")
                
            for i, ligand in enumerate(self.ligand_files[:]):
                if not ligand.endswith('.pdbqt'):
                    out_file = os.path.join(
                        self.output_dir,
                        f"{os.path.splitext(os.path.basename(ligand))[0]}_converted.pdbqt"
                    )
                    
                    # Detect input format
                    fmt = os.path.splitext(ligand)[1][1:]
                    
                    cmd = [
                        "obabel",
                        f"-i{fmt}",
                        ligand,
                        "-opdbqt",
                        f"-O{out_file}"
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    if os.path.exists(out_file):
                        self.ligand_files[i] = out_file
                        self.ligands_listbox.delete(i)
                        self.ligands_listbox.insert(i, os.path.basename(out_file))
                        self.log_message(f"Auto-converted ligand to PDBQT: {out_file}")
                    else:
                        raise ValueError(f"Failed to convert {ligand}:\n{result.stderr}")
            
            # Validate output directory
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            
            return True
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return False

    def start_docking(self):
        if not self.validate_parameters():
            return
            
        selected = self.ligands_listbox.curselection()
        ligands_to_dock = [self.ligand_files[i] for i in selected] if selected else self.ligand_files
        
        if not ligands_to_dock:
            messagebox.showwarning("No Ligands", "No ligands selected for docking!")
            return
            
        self.run_btn.config(state=tk.DISABLED)
        self.progress["value"] = 0
        self.progress["maximum"] = len(ligands_to_dock)
        
        threading.Thread(
            target=self.run_docking,
            args=(ligands_to_dock,),
            daemon=True
        ).start()

    def run_docking(self, ligands):
        try:
            center_x = float(self.x_entry.get())
            center_y = float(self.y_entry.get())
            center_z = float(self.z_entry.get())
            size = float(self.size_entry.get())
            
            for i, ligand_file in enumerate(ligands):
                ligand_name = os.path.splitext(os.path.basename(ligand_file))[0]
                output_file = os.path.join(self.output_dir, f"{ligand_name}_out.pdbqt")
                log_file = os.path.join(self.output_dir, f"{ligand_name}_log.txt")
                
                self.log_message(f"\nDocking {ligand_name}...")
                
                cmd = [
                    "vina",
                    "--receptor", self.receptor_file,
                    "--ligand", ligand_file,
                    "--center_x", str(center_x),
                    "--center_y", str(center_y),
                    "--center_z", str(center_z),
                    "--size_x", str(size),
                    "--size_y", str(size),
                    "--size_z", str(size),
                    "--out", output_file,
                    "--log", log_file,
                    "--exhaustiveness", str(self.exhaustiveness.get()),
                    "--num_modes", str(self.num_modes.get()),
                    "--energy_range", str(self.energy_range.get())
                ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    self.log_message(result.stdout)
                    
                    if os.path.exists(output_file):
                        self.log_message(f"Success! Results in {output_file}")
                        self.update_results(ligand_name, output_file, log_file)
                    else:
                        self.log_message(f"Failed! Error: {result.stderr}")
                except Exception as e:
                    self.log_message(f"Error docking {ligand_name}: {str(e)}")
                
                self.progress["value"] = i + 1
                self.root.update()
            
            messagebox.showinfo("Complete", f"Docked {len(ligands)} ligands")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.run_btn.config(state=tk.NORMAL)
            self.progress["value"] = 0

    def update_results(self, ligand_name, output_file, log_file):
        """Parse, sort, and display all docking poses from the log file, highlighting the best one."""
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()

            parsing = False
            all_poses = []

            for line in lines:
                if line.startswith('-----+'):
                    parsing = True
                    continue

                if parsing:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            mode = int(parts[0])
                            affinity = float(parts[1])
                            rmsd_lb = float(parts[2])
                            rmsd_ub = float(parts[3])

                            pose = {
                                'ligand': ligand_name,
                                'mode': mode,
                                'affinity': affinity,
                                'rmsd_lb': rmsd_lb,
                                'rmsd_ub': rmsd_ub,
                                'output_file': output_file
                            }

                            all_poses.append(pose)
                        except (ValueError, IndexError):
                            continue

            if all_poses:
                # Sort poses by affinity (lowest = best)
                all_poses.sort(key=lambda x: x['affinity'])

                self.docking_results.extend(all_poses)

                for index, pose in enumerate(all_poses):
                    tag = 'best' if index == 0 else ''
                    self.results_tree.insert('', tk.END, values=(
                        pose['ligand'],
                        pose['mode'],
                        f"{pose['affinity']:.2f}",
                        f"{pose['rmsd_lb']:.2f}",
                        f"{pose['rmsd_ub']:.2f}",
                        pose['output_file']
                    ), tags=(tag,))

                # Configure tag to highlight best pose (first one after sorting)
                self.results_tree.tag_configure('best', background='lightgreen')

                self.notebook.tab(2, state='normal')
                self.notebook.select(2)

        except Exception as e:
            self.log_message(f"Error parsing results: {str(e)}")

    def export_results(self):
        if not self.docking_results:
            messagebox.showwarning("No Results", "Nothing to export!")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Results as CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Ligand', 'Affinity (kcal/mol)', 'RMSD lb', 'RMSD ub', 'Output File'])
                for result in self.docking_results:
                    writer.writerow([
                        result['ligand'],
                        f"{result['affinity']:.2f}",
                        f"{result['rmsd_lb']:.2f}",
                        f"{result['rmsd_ub']:.2f}",
                        result['output_file']
                    ])
            messagebox.showinfo("Success", f"Results saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def clear_results(self):
        self.docking_results = []
        self.results_tree.delete(*self.results_tree.get_children())
        self.log_message("Cleared all results")

    def open_result(self):
        selected = self.results_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a result first")
            return
            
        item = self.results_tree.item(selected)
        output_file = item['values'][4]
        
        try:
            os.startfile(output_file)
        except:
            try:
                subprocess.run(['xdg-open', output_file])
            except:
                try:
                    subprocess.run(['open', output_file])
                except:
                    messagebox.showerror("Error", "Could not open file")


if __name__ == "__main__":
    # Verify Vina is installed
    try:
        subprocess.run(["vina", "--help"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except FileNotFoundError:
        messagebox.showerror("Error", "AutoDock Vina not found in PATH!")
        sys.exit(1)
    
    root = tk.Tk()
    app = SystemOpenBabelDockingApp(root)
    root.mainloop()
