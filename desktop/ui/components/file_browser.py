"""
File browser component for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
import sys

class FileBrowser(ttk.Frame):
    """File browser component with file selection and filtering"""
    
    def __init__(self, parent, app, allow_multiple=False, file_types=None):
        """Initialize the file browser component"""
        super().__init__(parent)
        self.app = app
        self.allow_multiple = allow_multiple
        
        # Set default file types if none provided
        if file_types is None:
            self.file_types = [
                ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("All files", "*.*")
            ]
        else:
            self.file_types = file_types
        
        # Initialize variables
        self.selected_files = []
        self.on_file_selected_callback = None
        
        # Configure the frame
        self.configure(style="FileBrowser.TFrame")
        
        # Create a style for the file browser
        style = ttk.Style()
        style.configure("FileBrowser.TFrame", background="#f5f5f5")
        
        # Create the file browser content
        self._create_file_browser_content()
    
    def _create_file_browser_content(self):
        """Create the file browser content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        
        # Create file path entry
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(self, textvariable=self.file_path_var)
        self.file_path_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Create browse button
        self.browse_button = ttk.Button(self, text="Browse...", command=self._browse_files)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Create file list (only shown when multiple files are allowed)
        if self.allow_multiple:
            self.file_list_frame = ttk.Frame(self, style="FileBrowser.TFrame")
            self.file_list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            
            # Configure the file list frame
            self.file_list_frame.columnconfigure(0, weight=1)
            self.file_list_frame.rowconfigure(0, weight=1)
            
            # Create a scrollable list
            self.file_list = tk.Listbox(self.file_list_frame, selectmode=tk.EXTENDED, 
                                       bg="white", bd=1, relief=tk.SOLID)
            self.file_list.grid(row=0, column=0, sticky="nsew")
            
            # Add scrollbar
            self.file_list_scrollbar = ttk.Scrollbar(self.file_list_frame, 
                                                   orient="vertical", 
                                                   command=self.file_list.yview)
            self.file_list_scrollbar.grid(row=0, column=1, sticky="ns")
            self.file_list.configure(yscrollcommand=self.file_list_scrollbar.set)
            
            # Add buttons for file list management
            self.file_list_buttons_frame = ttk.Frame(self.file_list_frame, style="FileBrowser.TFrame")
            self.file_list_buttons_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
            
            self.add_button = ttk.Button(self.file_list_buttons_frame, text="Add", 
                                       command=self._add_files)
            self.add_button.pack(side=tk.LEFT, padx=2)
            
            self.remove_button = ttk.Button(self.file_list_buttons_frame, text="Remove", 
                                          command=self._remove_selected_files)
            self.remove_button.pack(side=tk.LEFT, padx=2)
            
            self.clear_button = ttk.Button(self.file_list_buttons_frame, text="Clear", 
                                         command=self._clear_files)
            self.clear_button.pack(side=tk.LEFT, padx=2)
    
    def _browse_files(self):
        """Open file browser dialog"""
        if self.allow_multiple:
            file_paths = filedialog.askopenfilenames(
                title="Select files",
                filetypes=self.file_types
            )
            if file_paths:
                self._add_files_to_list(file_paths)
        else:
            file_path = filedialog.askopenfilename(
                title="Select file",
                filetypes=self.file_types
            )
            if file_path:
                self.file_path_var.set(file_path)
                self._notify_file_selected()
    
    def _add_files(self):
        """Add files to the list"""
        file_paths = filedialog.askopenfilenames(
            title="Select files",
            filetypes=self.file_types
        )
        if file_paths:
            self._add_files_to_list(file_paths)
    
    def _add_files_to_list(self, file_paths):
        """Add files to the list and update selected_files"""
        for file_path in file_paths:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                self.file_list.insert(tk.END, os.path.basename(file_path))
        
        # Update the file path entry with the count
        self.file_path_var.set(f"{len(self.selected_files)} files selected")
        
        # Notify callback
        self._notify_file_selected()
    
    def _remove_selected_files(self):
        """Remove selected files from the list"""
        selected_indices = self.file_list.curselection()
        
        # Remove in reverse order to avoid index shifting
        for i in sorted(selected_indices, reverse=True):
            del self.selected_files[i]
            self.file_list.delete(i)
        
        # Update the file path entry with the count
        if self.selected_files:
            self.file_path_var.set(f"{len(self.selected_files)} files selected")
        else:
            self.file_path_var.set("")
        
        # Notify callback
        self._notify_file_selected()
    
    def _clear_files(self):
        """Clear all files from the list"""
        self.selected_files = []
        self.file_list.delete(0, tk.END)
        self.file_path_var.set("")
        
        # Notify callback
        self._notify_file_selected()
    
    def get_selected_files(self):
        """Get the selected files"""
        if self.allow_multiple:
            return self.selected_files
        else:
            file_path = self.file_path_var.get()
            return [file_path] if file_path else []
    
    def set_on_file_selected_callback(self, callback):
        """Set callback for file selection events"""
        self.on_file_selected_callback = callback
    
    def _notify_file_selected(self):
        """Notify the callback of file selection"""
        if self.on_file_selected_callback:
            selected_files = self.get_selected_files()
            self.on_file_selected_callback(selected_files)
