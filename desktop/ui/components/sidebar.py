"""
Sidebar component for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class Sidebar(ttk.Frame):
    """Sidebar component with navigation buttons"""
    
    def __init__(self, parent, app):
        """Initialize the sidebar component"""
        super().__init__(parent)
        self.app = app
        
        # Configure the frame
        self.configure(width=200, style="Sidebar.TFrame")
        
        # Create a style for the sidebar
        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="#f5f5f5")
        style.configure("NavButton.TButton", font=("Arial", 11), padding=10)
        
        # Create the sidebar content
        self._create_sidebar_content()
    
    def _create_sidebar_content(self):
        """Create the sidebar content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)
        
        # Create navigation buttons
        self.home_button = self._create_nav_button("Home", 0, 
                                                 lambda: self.app.notebook.select(self.app.home_tab))
        self.encode_button = self._create_nav_button("Encode Message", 1, 
                                                   lambda: self.app.notebook.select(self.app.encode_tab))
        self.decode_button = self._create_nav_button("Decode Message", 2, 
                                                   lambda: self.app.notebook.select(self.app.decode_tab))
        self.analyze_button = self._create_nav_button("Analyze Image", 3, 
                                                    lambda: self.app.notebook.select(self.app.analyze_tab))
        self.batch_button = self._create_nav_button("Batch Processing", 4, 
                                                  lambda: self.app.notebook.select(self.app.batch_tab))
        self.settings_button = self._create_nav_button("Settings", 5, 
                                                     lambda: self.app.notebook.select(self.app.settings_tab))
        
        # Add a separator
        ttk.Separator(self, orient="horizontal").grid(row=6, column=0, sticky="ew", pady=10)
        
        # Add quick actions
        self.quick_actions_label = tk.Label(self, text="Quick Actions", font=("Arial", 12, "bold"), 
                                          bg="#f5f5f5")
        self.quick_actions_label.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 5))
        
        self.open_button = self._create_action_button("Open Image", 8, self.app.open_file)
        self.save_button = self._create_action_button("Save Result", 9, self.app.save_file)
        
        # Add a spacer
        self.spacer = ttk.Frame(self, style="Sidebar.TFrame", height=50)
        self.spacer.grid(row=10, column=0)
        
        # Add recent files section
        self.recent_files_label = tk.Label(self, text="Recent Files", font=("Arial", 12, "bold"), 
                                         bg="#f5f5f5")
        self.recent_files_label.grid(row=11, column=0, sticky="w", padx=10, pady=(10, 5))
        
        # Get recent files from config
        recent_files = self.app.config.get("recent_files", [])
        
        # Display recent files (up to 5)
        for i, file_path in enumerate(recent_files[:5]):
            file_name = os.path.basename(file_path)
            file_button = tk.Button(self, text=file_name, font=("Arial", 9),
                                   bg="#f5f5f5", fg="#333", bd=0, anchor="w",
                                   padx=10, pady=2, highlightthickness=0,
                                   command=lambda path=file_path: self._open_recent_file(path))
            file_button.grid(row=12+i, column=0, sticky="ew")
        
        # Add a spacer at the bottom
        self.bottom_spacer = ttk.Frame(self, style="Sidebar.TFrame")
        self.bottom_spacer.grid(row=100, column=0, sticky="ew")
        self.rowconfigure(100, weight=1)
    
    def _create_nav_button(self, text, row, command):
        """Create a navigation button"""
        button = ttk.Button(self, text=text, style="NavButton.TButton", command=command)
        button.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        return button
    
    def _create_action_button(self, text, row, command):
        """Create an action button"""
        button = tk.Button(self, text=text, font=("Arial", 10),
                          bg="#e0e0e0", fg="#333", bd=0,
                          padx=10, pady=5, highlightthickness=0,
                          command=command)
        button.grid(row=row, column=0, sticky="ew", padx=10, pady=2)
        return button
    
    def _open_recent_file(self, file_path):
        """Open a recent file"""
        self.app.logger.info(f"Opening recent file: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            tk.messagebox.showerror("Error", f"File not found: {file_path}")
            
            # Remove from recent files
            recent_files = self.app.config.get("recent_files", [])
            if file_path in recent_files:
                recent_files.remove(file_path)
                self.app.config.set("recent_files", recent_files)
            
            return
        
        # Determine file type and open in appropriate tab
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # It's an image, determine which tab to use based on current tab
            current_tab = self.app.notebook.index(self.app.notebook.select())
            
            if current_tab == 1:  # Encode tab
                self.app.encode_tab.load_image(file_path)
            elif current_tab == 2:  # Decode tab
                self.app.decode_tab.load_image(file_path)
            elif current_tab == 3:  # Analyze tab
                self.app.analyze_tab.load_image(file_path)
            else:
                # Default to analyze tab
                self.app.notebook.select(self.app.analyze_tab)
                self.app.analyze_tab.load_image(file_path)
        else:
            # Unknown file type
            tk.messagebox.showerror("Error", f"Unsupported file type: {file_path}")
    
    def update_recent_files(self):
        """Update the recent files list"""
        # Clear existing recent file buttons
        for widget in self.grid_slaves():
            if isinstance(widget, tk.Button) and widget.grid_info()["row"] >= 12 and widget.grid_info()["row"] < 17:
                widget.destroy()
        
        # Get recent files from config
        recent_files = self.app.config.get("recent_files", [])
        
        # Display recent files (up to 5)
        for i, file_path in enumerate(recent_files[:5]):
            file_name = os.path.basename(file_path)
            file_button = tk.Button(self, text=file_name, font=("Arial", 9),
                                   bg="#f5f5f5", fg="#333", bd=0, anchor="w",
                                   padx=10, pady=2, highlightthickness=0,
                                   command=lambda path=file_path: self._open_recent_file(path))
            file_button.grid(row=12+i, column=0, sticky="ew")
