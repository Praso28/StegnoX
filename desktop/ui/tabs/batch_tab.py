"""
Batch processing tab for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import threading
import json
import time

# Import components
from desktop.ui.components.file_browser import FileBrowser

class BatchTab(ttk.Frame):
    """Batch tab for processing multiple images at once"""
    
    def __init__(self, parent, app):
        """Initialize the batch tab"""
        super().__init__(parent)
        self.app = app
        
        # Initialize variables
        self.batch_in_progress = False
        self.batch_results = {}
        self.current_job_index = 0
        self.total_jobs = 0
        self.stop_requested = False
        
        # Configure the frame
        self.configure(style="BatchTab.TFrame", padding=10)
        
        # Create a style for the batch tab
        style = ttk.Style()
        style.configure("BatchTab.TFrame", background="#ffffff")
        
        # Create the batch tab content
        self._create_batch_tab_content()
    
    def _create_batch_tab_content(self):
        """Create the batch tab content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Title
        self.rowconfigure(1, weight=0)  # File selection
        self.rowconfigure(2, weight=0)  # Processing options
        self.rowconfigure(3, weight=0)  # Action buttons
        self.rowconfigure(4, weight=0)  # Progress section
        self.rowconfigure(5, weight=1)  # Results section
        
        # Add title
        self.title_label = ttk.Label(self, text="Batch Processing", 
                                    font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        # Add file selection section
        self.file_frame = ttk.LabelFrame(self, text="Image Selection")
        self.file_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure file frame
        self.file_frame.columnconfigure(0, weight=1)
        
        # Add file browser (with multiple file selection)
        self.file_browser = FileBrowser(self.file_frame, self.app, allow_multiple=True)
        self.file_browser.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Add processing options section
        self.options_frame = ttk.LabelFrame(self, text="Processing Options")
        self.options_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure options frame
        self.options_frame.columnconfigure(0, weight=0)
        self.options_frame.columnconfigure(1, weight=1)
        
        # Add processing type selection
        self.type_label = ttk.Label(self.options_frame, text="Process Type:")
        self.type_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.type_var = tk.StringVar(value="analyze")
        self.type_combo = ttk.Combobox(self.options_frame, textvariable=self.type_var, 
                                      state="readonly")
        self.type_combo["values"] = ("analyze", "encode", "decode")
        self.type_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.type_combo.bind("<<ComboboxSelected>>", self._on_type_changed)
        
        # Add method selection
        self.method_label = ttk.Label(self.options_frame, text="Method:")
        self.method_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.method_var = tk.StringVar(value="all")
        self.method_combo = ttk.Combobox(self.options_frame, textvariable=self.method_var, 
                                        state="readonly")
        self.method_combo["values"] = ("all", "lsb", "parity", "metadata", "dct", "bit_plane", "histogram")
        self.method_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Add message input (for encode type)
        self.message_label = ttk.Label(self.options_frame, text="Message:")
        self.message_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(self.options_frame, textvariable=self.message_var, width=40)
        self.message_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Hide message input initially (only shown for encode type)
        self.message_label.grid_remove()
        self.message_entry.grid_remove()
        
        # Add output directory selection
        self.output_label = ttk.Label(self.options_frame, text="Output Directory:")
        self.output_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        self.output_frame = ttk.Frame(self.options_frame)
        self.output_frame.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        # Configure output frame
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.columnconfigure(1, weight=0)
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_var)
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.output_button = ttk.Button(self.output_frame, text="Browse...", 
                                       command=self._browse_output_dir)
        self.output_button.grid(row=0, column=1, padx=5, pady=0)
        
        # Add threading options
        self.thread_label = ttk.Label(self.options_frame, text="Threads:")
        self.thread_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        
        self.thread_var = tk.IntVar(value=self.app.config.get("batch_processing", {}).get("max_threads", 4))
        self.thread_spinbox = ttk.Spinbox(self.options_frame, from_=1, to=16, 
                                         textvariable=self.thread_var, width=5)
        self.thread_spinbox.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Add action buttons section
        self.action_frame = ttk.Frame(self, style="BatchTab.TFrame")
        self.action_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure action frame
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=1)
        self.action_frame.columnconfigure(2, weight=1)
        
        # Add start button
        self.start_button = ttk.Button(self.action_frame, text="Start Processing", 
                                      command=self._start_batch)
        self.start_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        # Add stop button
        self.stop_button = ttk.Button(self.action_frame, text="Stop", 
                                     command=self._stop_batch)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.stop_button.configure(state="disabled")  # Initially disabled
        
        # Add export button
        self.export_button = ttk.Button(self.action_frame, text="Export Results", 
                                       command=self._export_results)
        self.export_button.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.export_button.configure(state="disabled")  # Initially disabled
        
        # Add progress section
        self.progress_frame = ttk.LabelFrame(self, text="Progress")
        self.progress_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure progress frame
        self.progress_frame.columnconfigure(0, weight=0)
        self.progress_frame.columnconfigure(1, weight=1)
        
        # Add progress bar
        self.progress_label = ttk.Label(self.progress_frame, text="Status:")
        self.progress_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           length=400, mode="determinate")
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Add progress status
        self.status_label = ttk.Label(self.progress_frame, text="Ready")
        self.status_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Add results section
        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.results_frame.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure results frame
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Add results treeview
        self.results_tree = ttk.Treeview(self.results_frame, columns=("file", "status", "details"), 
                                        show="headings")
        self.results_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure treeview columns
        self.results_tree.heading("file", text="File")
        self.results_tree.heading("status", text="Status")
        self.results_tree.heading("details", text="Details")
        
        self.results_tree.column("file", width=200)
        self.results_tree.column("status", width=100)
        self.results_tree.column("details", width=300)
        
        # Add treeview scrollbar
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", 
                                             command=self.results_tree.yview)
        self.results_scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
        self.results_tree.configure(yscrollcommand=self.results_scrollbar.set)
    
    def _on_type_changed(self, event):
        """Handle process type change"""
        process_type = self.type_var.get()
        
        if process_type == "encode":
            # Show message input
            self.message_label.grid()
            self.message_entry.grid()
            
            # Update method combo values
            self.method_combo["values"] = ("lsb", "parity", "metadata")
            self.method_var.set("lsb")
        elif process_type == "decode":
            # Hide message input
            self.message_label.grid_remove()
            self.message_entry.grid_remove()
            
            # Update method combo values
            self.method_combo["values"] = ("auto", "lsb", "parity", "metadata")
            self.method_var.set("auto")
        else:  # analyze
            # Hide message input
            self.message_label.grid_remove()
            self.message_entry.grid_remove()
            
            # Update method combo values
            self.method_combo["values"] = ("all", "lsb", "parity", "metadata", "dct", "bit_plane", "histogram")
            self.method_var.set("all")
    
    def _browse_output_dir(self):
        """Browse for output directory"""
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if output_dir:
            self.output_var.set(output_dir)
    
    def _start_batch(self):
        """Start batch processing"""
        # Validate inputs
        selected_files = self.file_browser.get_selected_files()
        if not selected_files:
            messagebox.showerror("Error", "Please select at least one image")
            return
        
        process_type = self.type_var.get()
        method = self.method_var.get()
        
        if process_type == "encode" and not self.message_var.get():
            messagebox.showerror("Error", "Please enter a message to encode")
            return
        
        output_dir = self.output_var.get()
        if not output_dir:
            # Use default output directory
            output_dir = os.path.join(os.path.expanduser("~"), "StegnoX_Output")
            self.output_var.set(output_dir)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create output directory: {str(e)}")
                return
        
        # Get thread count
        try:
            thread_count = int(self.thread_var.get())
            if thread_count < 1:
                thread_count = 1
            elif thread_count > 16:
                thread_count = 16
        except:
            thread_count = 4
        
        # Save thread count to config
        batch_config = self.app.config.get("batch_processing", {})
        batch_config["max_threads"] = thread_count
        self.app.config.set("batch_processing", batch_config)
        
        # Start batch processing
        self.batch_in_progress = True
        self.stop_requested = False
        self.batch_results = {}
        self.current_job_index = 0
        self.total_jobs = len(selected_files)
        
        # Update UI
        self._set_ui_state(False)
        self.stop_button.configure(state="normal")
        self.progress_var.set(0)
        self.status_label.configure(text="Starting batch processing...")
        
        # Clear results treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Start batch thread
        batch_thread = threading.Thread(
            target=self._run_batch,
            args=(selected_files, process_type, method, output_dir, thread_count)
        )
        batch_thread.daemon = True
        batch_thread.start()
    
    def _run_batch(self, files, process_type, method, output_dir, thread_count):
        """Run batch processing in a separate thread"""
        try:
            # Create a thread pool
            from concurrent.futures import ThreadPoolExecutor
            
            # Process files
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                # Submit all jobs
                future_to_file = {
                    executor.submit(
                        self._process_file, file_path, process_type, method, output_dir
                    ): file_path for file_path in files
                }
                
                # Process results as they complete
                for i, (future, file_path) in enumerate(future_to_file.items()):
                    if self.stop_requested:
                        executor.shutdown(wait=False)
                        break
                    
                    try:
                        result = future.result()
                        self.batch_results[file_path] = result
                        
                        # Update progress
                        self.current_job_index = i + 1
                        progress = (self.current_job_index / self.total_jobs) * 100
                        
                        # Update UI on the main thread
                        self.after(0, lambda p=progress, f=file_path, r=result: self._update_progress(p, f, r))
                    except Exception as e:
                        self.app.logger.error(f"Error processing {file_path}: {str(e)}")
                        self.batch_results[file_path] = {"status": "error", "error": str(e)}
                        
                        # Update UI on the main thread
                        self.after(0, lambda f=file_path, e=str(e): self._update_error(f, e))
            
            # Complete batch processing
            self.after(0, self._batch_complete)
        except Exception as e:
            # Handle errors
            self.app.logger.error(f"Batch processing error: {str(e)}")
            self.after(0, lambda: self._batch_error(str(e)))
    
    def _process_file(self, file_path, process_type, method, output_dir):
        """Process a single file"""
        try:
            file_name = os.path.basename(file_path)
            
            if process_type == "analyze":
                # Analyze the image
                if method == "all":
                    result = self.app.engine.extract_all_methods(file_path)
                else:
                    # Convert method name to engine method
                    engine_method = f"{method}_extraction" if method not in ["dct", "bit_plane", "histogram"] else f"{method}_analysis"
                    result = getattr(self.app.engine, engine_method)(file_path)
                
                # Save results to output directory
                output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_analysis.json")
                with open(output_file, "w") as f:
                    json.dump(result, f, indent=2)
                
                return {"status": "success", "output": output_file, "result": result}
            
            elif process_type == "encode":
                # Encode a message in the image
                message = self.message_var.get()
                output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_encoded.png")
                
                if method == "lsb":
                    result = self.app.engine.lsb_encoding(file_path, message, output_file)
                elif method == "parity":
                    result = self.app.engine.parity_bit_encoding(file_path, message, output_file)
                elif method == "metadata":
                    result = self.app.engine.metadata_encoding(file_path, message, output_file)
                
                return {"status": "success", "output": output_file, "result": result}
            
            elif process_type == "decode":
                # Decode a message from the image
                if method == "auto":
                    # Try all methods
                    results = {}
                    
                    # Try LSB first
                    lsb_result = self.app.engine.lsb_extraction(file_path)
                    if "message" in lsb_result and lsb_result["message"] != "No valid data found":
                        results["LSB"] = lsb_result["message"]
                    
                    # Try parity
                    parity_result = self.app.engine.parity_bit_extraction(file_path)
                    if "message" in parity_result and parity_result["message"] != "No readable text found with parity method":
                        results["Parity"] = parity_result["message"]
                    
                    # Try metadata
                    metadata_result = self.app.engine.metadata_extraction(file_path)
                    if "metadata" in metadata_result and metadata_result["metadata"]:
                        for key, value in metadata_result["metadata"].items():
                            if key.lower() == "comment" and value:
                                results["Metadata"] = value
                    
                    # Save results to output directory
                    output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_decoded.txt")
                    with open(output_file, "w") as f:
                        for method_name, message in results.items():
                            f.write(f"=== {method_name} Method ===\n")
                            f.write(f"{message}\n\n")
                    
                    return {"status": "success", "output": output_file, "result": results}
                else:
                    # Use specific method
                    if method == "lsb":
                        result = self.app.engine.lsb_extraction(file_path)
                    elif method == "parity":
                        result = self.app.engine.parity_bit_extraction(file_path)
                    elif method == "metadata":
                        result = self.app.engine.metadata_extraction(file_path)
                    
                    # Save results to output directory
                    output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_decoded.txt")
                    with open(output_file, "w") as f:
                        if method == "metadata" and "metadata" in result:
                            for key, value in result["metadata"].items():
                                f.write(f"{key}: {value}\n")
                        elif "message" in result:
                            f.write(result["message"])
                    
                    return {"status": "success", "output": output_file, "result": result}
        
        except Exception as e:
            raise Exception(f"Failed to process {file_path}: {str(e)}")
    
    def _update_progress(self, progress, file_path, result):
        """Update progress UI"""
        self.progress_var.set(progress)
        self.status_label.configure(text=f"Processing {self.current_job_index} of {self.total_jobs}: {os.path.basename(file_path)}")
        
        # Add to results treeview
        file_name = os.path.basename(file_path)
        status = "Success"
        
        if "output" in result:
            details = f"Output: {os.path.basename(result['output'])}"
        else:
            details = "Completed"
        
        self.results_tree.insert("", "end", values=(file_name, status, details))
    
    def _update_error(self, file_path, error):
        """Update UI with error"""
        file_name = os.path.basename(file_path)
        self.results_tree.insert("", "end", values=(file_name, "Error", error))
    
    def _batch_complete(self):
        """Handle batch completion"""
        self.batch_in_progress = False
        
        # Update UI
        self._set_ui_state(True)
        self.stop_button.configure(state="disabled")
        self.export_button.configure(state="normal")
        
        self.status_label.configure(text=f"Batch processing complete: {self.current_job_index} of {self.total_jobs} files processed")
        self.app.set_status("Batch processing complete")
        
        # Show completion message
        if self.stop_requested:
            messagebox.showinfo("Batch Stopped", f"Batch processing stopped. {self.current_job_index} of {self.total_jobs} files processed.")
        else:
            messagebox.showinfo("Batch Complete", f"Batch processing complete. {self.current_job_index} of {self.total_jobs} files processed.")
    
    def _batch_error(self, error_message):
        """Handle batch error"""
        self.batch_in_progress = False
        
        # Update UI
        self._set_ui_state(True)
        self.stop_button.configure(state="disabled")
        
        self.status_label.configure(text=f"Batch processing failed: {error_message}")
        self.app.set_status("Batch processing failed")
        
        # Show error message
        messagebox.showerror("Batch Error", f"Batch processing failed: {error_message}")
    
    def _stop_batch(self):
        """Stop batch processing"""
        if not self.batch_in_progress:
            return
        
        self.stop_requested = True
        self.status_label.configure(text="Stopping batch processing...")
        self.app.set_status("Stopping batch processing...")
    
    def _export_results(self):
        """Export batch results to a file"""
        if not self.batch_results:
            messagebox.showerror("Error", "No results to export")
            return
        
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            title="Export Batch Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Export results
            with open(file_path, "w") as f:
                json.dump(self.batch_results, f, indent=2)
            
            self.app.set_status(f"Batch results exported to {file_path}")
            messagebox.showinfo("Export Complete", f"Batch results have been exported to {file_path}")
        except Exception as e:
            self.app.logger.error(f"Export error: {str(e)}")
            messagebox.showerror("Export Error", f"Failed to export batch results: {str(e)}")
    
    def _set_ui_state(self, enabled):
        """Enable or disable UI elements during batch processing"""
        state = "normal" if enabled else "disabled"
        
        # Update UI elements
        self.file_browser.browse_button.configure(state=state)
        self.type_combo.configure(state="readonly" if enabled else "disabled")
        self.method_combo.configure(state="readonly" if enabled else "disabled")
        self.message_entry.configure(state=state)
        self.output_entry.configure(state=state)
        self.output_button.configure(state=state)
        self.thread_spinbox.configure(state=state)
        self.start_button.configure(state=state)
    
    def select_images(self):
        """Select images (called from main app)"""
        self.file_browser._browse_files()
