"""
Analyze tab for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import threading
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io

# Import components
from desktop.ui.components.image_preview import ImagePreview
from desktop.ui.components.file_browser import FileBrowser

class AnalyzeTab(ttk.Frame):
    """Analyze tab for detecting steganography in images"""
    
    def __init__(self, parent, app):
        """Initialize the analyze tab"""
        super().__init__(parent)
        self.app = app
        
        # Initialize variables
        self.image_path = None
        self.analysis_results = {}
        self.analysis_in_progress = False
        self.current_method = None
        
        # Configure the frame
        self.configure(style="AnalyzeTab.TFrame", padding=10)
        
        # Create a style for the analyze tab
        style = ttk.Style()
        style.configure("AnalyzeTab.TFrame", background="#ffffff")
        
        # Create the analyze tab content
        self._create_analyze_tab_content()
    
    def _create_analyze_tab_content(self):
        """Create the analyze tab content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)  # Left panel
        self.columnconfigure(1, weight=1)  # Right panel
        self.rowconfigure(0, weight=1)
        
        # Create left panel (image selection and preview)
        self.left_panel = ttk.Frame(self, style="AnalyzeTab.TFrame")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure left panel
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(0, weight=0)  # File browser
        self.left_panel.rowconfigure(1, weight=1)  # Image preview
        
        # Add file browser
        self.file_browser = FileBrowser(self.left_panel, self.app)
        self.file_browser.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.file_browser.set_on_file_selected_callback(self._on_file_selected)
        
        # Add image preview
        self.image_preview = ImagePreview(self.left_panel, self.app)
        self.image_preview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create right panel (analysis options and results)
        self.right_panel = ttk.Frame(self, style="AnalyzeTab.TFrame")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure right panel
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=0)  # Title
        self.right_panel.rowconfigure(1, weight=0)  # Analysis options
        self.right_panel.rowconfigure(2, weight=0)  # Action buttons
        self.right_panel.rowconfigure(3, weight=1)  # Results
        
        # Add title
        self.title_label = ttk.Label(self.right_panel, text="Analyze Image for Steganography", 
                                    font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        # Add analysis options section
        self.options_frame = ttk.LabelFrame(self.right_panel, text="Analysis Options")
        self.options_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure options frame
        self.options_frame.columnconfigure(0, weight=0)
        self.options_frame.columnconfigure(1, weight=1)
        
        # Add analysis methods checkboxes
        self.methods_label = ttk.Label(self.options_frame, text="Methods:")
        self.methods_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Create methods frame
        self.methods_frame = ttk.Frame(self.options_frame)
        self.methods_frame.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Add method checkboxes
        self.lsb_var = tk.BooleanVar(value=True)
        self.lsb_check = ttk.Checkbutton(self.methods_frame, text="LSB Analysis", 
                                        variable=self.lsb_var)
        self.lsb_check.grid(row=0, column=0, sticky="w", padx=5)
        
        self.parity_var = tk.BooleanVar(value=True)
        self.parity_check = ttk.Checkbutton(self.methods_frame, text="Parity Analysis", 
                                           variable=self.parity_var)
        self.parity_check.grid(row=0, column=1, sticky="w", padx=5)
        
        self.metadata_var = tk.BooleanVar(value=True)
        self.metadata_check = ttk.Checkbutton(self.methods_frame, text="Metadata Analysis", 
                                             variable=self.metadata_var)
        self.metadata_check.grid(row=1, column=0, sticky="w", padx=5)
        
        self.dct_var = tk.BooleanVar(value=True)
        self.dct_check = ttk.Checkbutton(self.methods_frame, text="DCT Analysis", 
                                        variable=self.dct_var)
        self.dct_check.grid(row=1, column=1, sticky="w", padx=5)
        
        self.bit_plane_var = tk.BooleanVar(value=True)
        self.bit_plane_check = ttk.Checkbutton(self.methods_frame, text="Bit Plane Analysis", 
                                              variable=self.bit_plane_var)
        self.bit_plane_check.grid(row=2, column=0, sticky="w", padx=5)
        
        self.histogram_var = tk.BooleanVar(value=True)
        self.histogram_check = ttk.Checkbutton(self.methods_frame, text="Histogram Analysis", 
                                              variable=self.histogram_var)
        self.histogram_check.grid(row=2, column=1, sticky="w", padx=5)
        
        # Add action buttons section
        self.action_frame = ttk.Frame(self.right_panel, style="AnalyzeTab.TFrame")
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure action frame
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=1)
        
        # Add analyze button
        self.analyze_button = ttk.Button(self.action_frame, text="Analyze Image", 
                                        command=self._analyze_image)
        self.analyze_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        # Add export button
        self.export_button = ttk.Button(self.action_frame, text="Export Results", 
                                       command=self._export_results)
        self.export_button.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.export_button.configure(state="disabled")  # Initially disabled
        
        # Add results section
        self.results_frame = ttk.LabelFrame(self.right_panel, text="Analysis Results")
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure results frame
        self.results_frame.columnconfigure(0, weight=0)  # Methods list
        self.results_frame.columnconfigure(1, weight=1)  # Results display
        self.results_frame.rowconfigure(0, weight=1)
        
        # Add methods list
        self.methods_list = tk.Listbox(self.results_frame, width=20, height=15, 
                                      exportselection=0)
        self.methods_list.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        self.methods_list.bind("<<ListboxSelect>>", self._on_method_selected)
        
        # Add results notebook (for different result types)
        self.results_notebook = ttk.Notebook(self.results_frame)
        self.results_notebook.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Create result tabs
        self.text_tab = ttk.Frame(self.results_notebook)
        self.visual_tab = ttk.Frame(self.results_notebook)
        
        self.results_notebook.add(self.text_tab, text="Text")
        self.results_notebook.add(self.visual_tab, text="Visualization")
        
        # Configure text tab
        self.text_tab.columnconfigure(0, weight=1)
        self.text_tab.rowconfigure(0, weight=1)
        
        # Add text results
        self.text_results = tk.Text(self.text_tab, wrap=tk.WORD, state="disabled")
        self.text_results.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add text scrollbar
        self.text_scrollbar = ttk.Scrollbar(self.text_tab, orient="vertical", 
                                          command=self.text_results.yview)
        self.text_scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
        self.text_results.configure(yscrollcommand=self.text_scrollbar.set)
        
        # Configure visual tab
        self.visual_tab.columnconfigure(0, weight=1)
        self.visual_tab.rowconfigure(0, weight=1)
        
        # Visual tab will be populated dynamically based on the selected method
    
    def _on_file_selected(self, file_paths):
        """Handle file selection"""
        if file_paths:
            self.image_path = file_paths[0]
            self.image_preview.load_image(self.image_path)
            
            # Clear previous results
            self._clear_results()
    
    def _analyze_image(self):
        """Analyze the image for steganography"""
        # Validate inputs
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first")
            return
        
        # Get selected methods
        methods = []
        if self.lsb_var.get():
            methods.append("lsb_extraction")
        if self.parity_var.get():
            methods.append("parity_bit_extraction")
        if self.metadata_var.get():
            methods.append("metadata_extraction")
        if self.dct_var.get():
            methods.append("dct_analysis")
        if self.bit_plane_var.get():
            methods.append("bit_plane_analysis")
        if self.histogram_var.get():
            methods.append("histogram_analysis")
        
        if not methods:
            messagebox.showerror("Error", "Please select at least one analysis method")
            return
        
        # Start analysis in a separate thread
        self.analysis_in_progress = True
        self.app.set_status("Analyzing image...")
        self.app.status_bar.show_progress(False)
        
        # Disable UI elements during analysis
        self._set_ui_state(False)
        
        # Clear previous results
        self._clear_results()
        
        # Start analysis thread
        analysis_thread = threading.Thread(
            target=self._run_analysis,
            args=(methods,)
        )
        analysis_thread.daemon = True
        analysis_thread.start()
    
    def _run_analysis(self, methods):
        """Run the analysis process in a separate thread"""
        try:
            # Initialize results
            self.analysis_results = {}
            
            # Run each selected method
            for method in methods:
                try:
                    # Call the appropriate method in the engine
                    result = getattr(self.app.engine, method)(self.image_path)
                    self.analysis_results[method] = result
                except Exception as e:
                    self.app.logger.error(f"Error in {method}: {str(e)}")
                    self.analysis_results[method] = {"error": str(e)}
            
            # Update UI on the main thread
            self.after(0, self._analysis_complete)
        except Exception as e:
            # Handle errors
            self.app.logger.error(f"Analysis error: {str(e)}")
            self.after(0, lambda: self._analysis_error(str(e)))
    
    def _analysis_complete(self):
        """Handle analysis completion"""
        self.analysis_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        if self.analysis_results:
            self.app.set_status("Analysis complete")
            
            # Populate methods list
            for method in self.analysis_results:
                # Format method name for display
                display_name = method.replace("_", " ").title()
                self.methods_list.insert(tk.END, display_name)
            
            # Select the first method
            if self.methods_list.size() > 0:
                self.methods_list.selection_set(0)
                self._on_method_selected(None)
            
            # Enable export button
            self.export_button.configure(state="normal")
        else:
            self.app.set_status("Analysis failed")
            messagebox.showerror("Error", "Analysis failed. No results were generated.")
    
    def _analysis_error(self, error_message):
        """Handle analysis error"""
        self.analysis_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        self.app.set_status("Analysis failed")
        messagebox.showerror("Analysis Error", f"Failed to analyze image: {error_message}")
    
    def _on_method_selected(self, event):
        """Handle method selection from the list"""
        if not self.methods_list.curselection():
            return
        
        # Get selected method
        index = self.methods_list.curselection()[0]
        display_name = self.methods_list.get(index)
        
        # Convert display name back to method name
        method = display_name.lower().replace(" ", "_")
        
        # Save current method
        self.current_method = method
        
        # Display results for the selected method
        self._display_results(method)
    
    def _display_results(self, method):
        """Display results for the selected method"""
        if method not in self.analysis_results:
            return
        
        result = self.analysis_results[method]
        
        # Display text results
        self.text_results.configure(state="normal")
        self.text_results.delete("1.0", tk.END)
        
        if "error" in result:
            self.text_results.insert(tk.END, f"Error: {result['error']}")
        else:
            # Format results based on method
            if method == "lsb_extraction":
                if "message" in result:
                    self.text_results.insert(tk.END, f"Extracted message:\n{result['message']}")
                else:
                    self.text_results.insert(tk.END, "No message found")
            elif method == "parity_bit_extraction":
                if "message" in result:
                    self.text_results.insert(tk.END, f"Extracted message:\n{result['message']}")
                else:
                    self.text_results.insert(tk.END, "No message found")
            elif method == "metadata_extraction":
                if "metadata" in result and result["metadata"]:
                    self.text_results.insert(tk.END, "Metadata:\n")
                    for key, value in result["metadata"].items():
                        self.text_results.insert(tk.END, f"{key}: {value}\n")
                else:
                    self.text_results.insert(tk.END, "No metadata found")
            else:
                # Generic display for other methods
                self.text_results.insert(tk.END, json.dumps(result, indent=2))
        
        self.text_results.configure(state="disabled")
        
        # Display visualization if available
        self._display_visualization(method, result)
    
    def _display_visualization(self, method, result):
        """Display visualization for the selected method"""
        # Clear previous visualization
        for widget in self.visual_tab.winfo_children():
            widget.destroy()
        
        # Create visualization based on method
        if method == "bit_plane_analysis" and "bit_planes" in result:
            self._create_bit_plane_visualization(result)
        elif method == "histogram_analysis" and "histograms" in result:
            self._create_histogram_visualization(result)
        elif method == "dct_analysis" and "dct_coefficients" in result:
            self._create_dct_visualization(result)
        else:
            # No visualization available
            no_visual_label = ttk.Label(self.visual_tab, text="No visualization available for this method", 
                                       font=("Arial", 12, "italic"))
            no_visual_label.pack(expand=True)
    
    def _create_bit_plane_visualization(self, result):
        """Create visualization for bit plane analysis"""
        # This is a placeholder - in a real implementation, you would create
        # a visualization of the bit planes using matplotlib or similar
        
        # Create a figure with subplots
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.visual_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add a label explaining the visualization
        label = ttk.Label(self.visual_tab, text="Bit Plane Visualization", font=("Arial", 12, "bold"))
        label.pack(side=tk.BOTTOM)
    
    def _create_histogram_visualization(self, result):
        """Create visualization for histogram analysis"""
        # This is a placeholder - in a real implementation, you would create
        # a visualization of the histograms using matplotlib or similar
        
        # Create a figure with subplots
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.visual_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add a label explaining the visualization
        label = ttk.Label(self.visual_tab, text="Histogram Visualization", font=("Arial", 12, "bold"))
        label.pack(side=tk.BOTTOM)
    
    def _create_dct_visualization(self, result):
        """Create visualization for DCT analysis"""
        # This is a placeholder - in a real implementation, you would create
        # a visualization of the DCT coefficients using matplotlib or similar
        
        # Create a figure with subplots
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.visual_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add a label explaining the visualization
        label = ttk.Label(self.visual_tab, text="DCT Coefficient Visualization", font=("Arial", 12, "bold"))
        label.pack(side=tk.BOTTOM)
    
    def _export_results(self):
        """Export analysis results to a file"""
        if not self.analysis_results:
            messagebox.showerror("Error", "No results to export")
            return
        
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Export results
            with open(file_path, "w") as f:
                json.dump(self.analysis_results, f, indent=2)
            
            self.app.set_status(f"Results exported to {file_path}")
            messagebox.showinfo("Export Complete", f"Results have been exported to {file_path}")
        except Exception as e:
            self.app.logger.error(f"Export error: {str(e)}")
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")
    
    def _set_ui_state(self, enabled):
        """Enable or disable UI elements during analysis"""
        state = "normal" if enabled else "disabled"
        
        # Update UI elements
        self.file_browser.browse_button.configure(state=state)
        self.lsb_check.configure(state=state)
        self.parity_check.configure(state=state)
        self.metadata_check.configure(state=state)
        self.dct_check.configure(state=state)
        self.bit_plane_check.configure(state=state)
        self.histogram_check.configure(state=state)
        self.analyze_button.configure(state=state)
        
        # Export button is only enabled when results are available
        if enabled and self.analysis_results:
            self.export_button.configure(state="normal")
        else:
            self.export_button.configure(state="disabled")
    
    def _clear_results(self):
        """Clear all results"""
        self.analysis_results = {}
        self.methods_list.delete(0, tk.END)
        
        self.text_results.configure(state="normal")
        self.text_results.delete("1.0", tk.END)
        self.text_results.configure(state="disabled")
        
        # Clear visualization
        for widget in self.visual_tab.winfo_children():
            widget.destroy()
        
        # Disable export button
        self.export_button.configure(state="disabled")
    
    def select_image(self):
        """Select an image (called from main app)"""
        self.file_browser._browse_files()
    
    def load_image(self, image_path):
        """Load an image (called from sidebar)"""
        self.image_path = image_path
        self.image_preview.load_image(image_path)
        
        # Update file browser
        self.file_browser.file_path_var.set(image_path)
        
        # Clear previous results
        self._clear_results()
    
    def save_results(self):
        """Save the analysis results (called from main app)"""
        self._export_results()
