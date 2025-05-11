"""
Settings tab for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

class SettingsTab(ttk.Frame):
    """Settings tab for configuring application preferences"""
    
    def __init__(self, parent, app):
        """Initialize the settings tab"""
        super().__init__(parent)
        self.app = app
        
        # Configure the frame
        self.configure(style="SettingsTab.TFrame", padding=20)
        
        # Create a style for the settings tab
        style = ttk.Style()
        style.configure("SettingsTab.TFrame", background="#ffffff")
        style.configure("SettingsTitle.TLabel", font=("Arial", 16, "bold"))
        style.configure("SettingsSection.TLabel", font=("Arial", 12, "bold"))
        
        # Create the settings tab content
        self._create_settings_tab_content()
    
    def _create_settings_tab_content(self):
        """Create the settings tab content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)
        
        # Add title
        self.title_label = ttk.Label(self, text="Settings", style="SettingsTitle.TLabel")
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        # Add appearance section
        self.appearance_frame = ttk.LabelFrame(self, text="Appearance")
        self.appearance_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure appearance frame
        self.appearance_frame.columnconfigure(0, weight=0)
        self.appearance_frame.columnconfigure(1, weight=1)
        
        # Add theme selection
        self.theme_label = ttk.Label(self.appearance_frame, text="Theme:")
        self.theme_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.theme_var = tk.StringVar(value=self.app.config.get("theme", "light"))
        self.theme_combo = ttk.Combobox(self.appearance_frame, textvariable=self.theme_var, 
                                       state="readonly")
        self.theme_combo["values"] = ("light", "dark")
        self.theme_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self._on_theme_changed)
        
        # Add image size limit
        self.image_size_label = ttk.Label(self.appearance_frame, text="Max Image Size:")
        self.image_size_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # Get current max image size
        max_size = self.app.config.get("max_image_size", (800, 800))
        
        self.image_size_frame = ttk.Frame(self.appearance_frame)
        self.image_size_frame.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.image_width_var = tk.IntVar(value=max_size[0])
        self.image_width_spinbox = ttk.Spinbox(self.image_size_frame, from_=100, to=2000, 
                                              textvariable=self.image_width_var, width=5)
        self.image_width_spinbox.pack(side=tk.LEFT)
        
        ttk.Label(self.image_size_frame, text="×").pack(side=tk.LEFT, padx=5)
        
        self.image_height_var = tk.IntVar(value=max_size[1])
        self.image_height_spinbox = ttk.Spinbox(self.image_size_frame, from_=100, to=2000, 
                                               textvariable=self.image_height_var, width=5)
        self.image_height_spinbox.pack(side=tk.LEFT)
        
        ttk.Label(self.image_size_frame, text="pixels").pack(side=tk.LEFT, padx=5)
        
        # Add file management section
        self.file_frame = ttk.LabelFrame(self, text="File Management")
        self.file_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure file frame
        self.file_frame.columnconfigure(0, weight=0)
        self.file_frame.columnconfigure(1, weight=1)
        
        # Add default output directory
        self.output_dir_label = ttk.Label(self.file_frame, text="Default Output Directory:")
        self.output_dir_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.output_dir_frame = ttk.Frame(self.file_frame)
        self.output_dir_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Configure output dir frame
        self.output_dir_frame.columnconfigure(0, weight=1)
        self.output_dir_frame.columnconfigure(1, weight=0)
        
        self.output_dir_var = tk.StringVar(value=self.app.config.get("default_output_dir", ""))
        self.output_dir_entry = ttk.Entry(self.output_dir_frame, textvariable=self.output_dir_var)
        self.output_dir_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.output_dir_button = ttk.Button(self.output_dir_frame, text="Browse...", 
                                          command=self._browse_output_dir)
        self.output_dir_button.grid(row=0, column=1, padx=5, pady=0)
        
        # Add results directory
        self.results_dir_label = ttk.Label(self.file_frame, text="Results Directory:")
        self.results_dir_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.results_dir_frame = ttk.Frame(self.file_frame)
        self.results_dir_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Configure results dir frame
        self.results_dir_frame.columnconfigure(0, weight=1)
        self.results_dir_frame.columnconfigure(1, weight=0)
        
        self.results_dir_var = tk.StringVar(value=self.app.config.get("results_dir", ""))
        self.results_dir_entry = ttk.Entry(self.results_dir_frame, textvariable=self.results_dir_var)
        self.results_dir_entry.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.results_dir_button = ttk.Button(self.results_dir_frame, text="Browse...", 
                                           command=self._browse_results_dir)
        self.results_dir_button.grid(row=0, column=1, padx=5, pady=0)
        
        # Add recent files limit
        self.recent_files_label = ttk.Label(self.file_frame, text="Max Recent Files:")
        self.recent_files_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.recent_files_var = tk.IntVar(value=self.app.config.get("max_recent_files", 10))
        self.recent_files_spinbox = ttk.Spinbox(self.file_frame, from_=0, to=50, 
                                               textvariable=self.recent_files_var, width=5)
        self.recent_files_spinbox.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Add auto-save option
        self.auto_save_var = tk.BooleanVar(value=self.app.config.get("auto_save_results", True))
        self.auto_save_check = ttk.Checkbutton(self.file_frame, text="Auto-save results", 
                                              variable=self.auto_save_var)
        self.auto_save_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Add encoding section
        self.encoding_frame = ttk.LabelFrame(self, text="Encoding Defaults")
        self.encoding_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure encoding frame
        self.encoding_frame.columnconfigure(0, weight=0)
        self.encoding_frame.columnconfigure(1, weight=1)
        
        # Add default encoding method
        self.encoding_method_label = ttk.Label(self.encoding_frame, text="Default Method:")
        self.encoding_method_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.encoding_method_var = tk.StringVar(value=self.app.config.get("default_encoding_method", "lsb"))
        self.encoding_method_combo = ttk.Combobox(self.encoding_frame, 
                                                 textvariable=self.encoding_method_var, 
                                                 state="readonly")
        self.encoding_method_combo["values"] = ("lsb", "parity", "metadata")
        self.encoding_method_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Add advanced options
        self.advanced_options_var = tk.BooleanVar(value=self.app.config.get("show_advanced_options", False))
        self.advanced_options_check = ttk.Checkbutton(self.encoding_frame, 
                                                     text="Show advanced options", 
                                                     variable=self.advanced_options_var)
        self.advanced_options_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Add batch processing section
        self.batch_frame = ttk.LabelFrame(self, text="Batch Processing")
        self.batch_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure batch frame
        self.batch_frame.columnconfigure(0, weight=0)
        self.batch_frame.columnconfigure(1, weight=1)
        
        # Add max threads
        self.max_threads_label = ttk.Label(self.batch_frame, text="Max Threads:")
        self.max_threads_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        batch_config = self.app.config.get("batch_processing", {})
        
        self.max_threads_var = tk.IntVar(value=batch_config.get("max_threads", 4))
        self.max_threads_spinbox = ttk.Spinbox(self.batch_frame, from_=1, to=16, 
                                              textvariable=self.max_threads_var, width=5)
        self.max_threads_spinbox.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Add batch auto-save option
        self.batch_auto_save_var = tk.BooleanVar(value=batch_config.get("auto_save", True))
        self.batch_auto_save_check = ttk.Checkbutton(self.batch_frame, 
                                                    text="Auto-save batch results", 
                                                    variable=self.batch_auto_save_var)
        self.batch_auto_save_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Add action buttons
        self.button_frame = ttk.Frame(self, style="SettingsTab.TFrame")
        self.button_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=20)
        
        # Configure button frame
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=0)
        self.button_frame.columnconfigure(2, weight=0)
        
        # Add save button
        self.save_button = ttk.Button(self.button_frame, text="Save Settings", 
                                     command=self._save_settings)
        self.save_button.grid(row=0, column=1, padx=5, pady=0)
        
        # Add reset button
        self.reset_button = ttk.Button(self.button_frame, text="Reset to Defaults", 
                                      command=self._reset_settings)
        self.reset_button.grid(row=0, column=2, padx=5, pady=0)
    
    def _browse_output_dir(self):
        """Browse for default output directory"""
        output_dir = filedialog.askdirectory(title="Select Default Output Directory")
        if output_dir:
            self.output_dir_var.set(output_dir)
    
    def _browse_results_dir(self):
        """Browse for results directory"""
        results_dir = filedialog.askdirectory(title="Select Results Directory")
        if results_dir:
            self.results_dir_var.set(results_dir)
    
    def _on_theme_changed(self, event):
        """Handle theme change"""
        theme = self.theme_var.get()
        self.app.config.set("theme", theme)
        self.app._apply_theme()
    
    def _save_settings(self):
        """Save settings to config"""
        try:
            # Update appearance settings
            self.app.config.set("theme", self.theme_var.get())
            
            # Update max image size
            max_width = int(self.image_width_var.get())
            max_height = int(self.image_height_var.get())
            self.app.config.set("max_image_size", (max_width, max_height))
            
            # Update file management settings
            self.app.config.set("default_output_dir", self.output_dir_var.get())
            self.app.config.set("results_dir", self.results_dir_var.get())
            self.app.config.set("max_recent_files", int(self.recent_files_var.get()))
            self.app.config.set("auto_save_results", self.auto_save_var.get())
            
            # Update encoding settings
            self.app.config.set("default_encoding_method", self.encoding_method_var.get())
            self.app.config.set("show_advanced_options", self.advanced_options_var.get())
            
            # Update batch processing settings
            batch_config = {
                "max_threads": int(self.max_threads_var.get()),
                "auto_save": self.batch_auto_save_var.get()
            }
            self.app.config.set("batch_processing", batch_config)
            
            # Save config to file
            self.app.config.save_config()
            
            # Show success message
            self.app.set_status("Settings saved")
            messagebox.showinfo("Settings", "Settings have been saved successfully")
        except Exception as e:
            self.app.logger.error(f"Failed to save settings: {str(e)}")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def _reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            # Reset config to defaults
            self.app.config.reset_to_defaults()
            
            # Update UI with default values
            self.theme_var.set(self.app.config.get("theme", "light"))
            
            max_size = self.app.config.get("max_image_size", (800, 800))
            self.image_width_var.set(max_size[0])
            self.image_height_var.set(max_size[1])
            
            self.output_dir_var.set(self.app.config.get("default_output_dir", ""))
            self.results_dir_var.set(self.app.config.get("results_dir", ""))
            self.recent_files_var.set(self.app.config.get("max_recent_files", 10))
            self.auto_save_var.set(self.app.config.get("auto_save_results", True))
            
            self.encoding_method_var.set(self.app.config.get("default_encoding_method", "lsb"))
            self.advanced_options_var.set(self.app.config.get("show_advanced_options", False))
            
            batch_config = self.app.config.get("batch_processing", {})
            self.max_threads_var.set(batch_config.get("max_threads", 4))
            self.batch_auto_save_var.set(batch_config.get("auto_save", True))
            
            # Apply theme
            self.app._apply_theme()
            
            # Show success message
            self.app.set_status("Settings reset to defaults")
            messagebox.showinfo("Settings", "Settings have been reset to defaults")
