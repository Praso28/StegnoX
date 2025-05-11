"""
Home tab for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class HomeTab(ttk.Frame):
    """Home tab with welcome message and quick actions"""
    
    def __init__(self, parent, app):
        """Initialize the home tab"""
        super().__init__(parent)
        self.app = app
        
        # Configure the frame
        self.configure(style="HomeTab.TFrame", padding=20)
        
        # Create a style for the home tab
        style = ttk.Style()
        style.configure("HomeTab.TFrame", background="#ffffff")
        style.configure("Title.TLabel", font=("Arial", 24, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 14))
        style.configure("ActionButton.TButton", font=("Arial", 12), padding=10)
        
        # Create the home tab content
        self._create_home_tab_content()
    
    def _create_home_tab_content(self):
        """Create the home tab content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)
        
        # Create welcome section
        self.welcome_frame = ttk.Frame(self, style="HomeTab.TFrame")
        self.welcome_frame.grid(row=0, column=0, sticky="ew", pady=20)
        
        # Configure welcome frame
        self.welcome_frame.columnconfigure(0, weight=1)
        
        # Add title
        self.title_label = ttk.Label(self.welcome_frame, text="Welcome to StegnoX", 
                                    style="Title.TLabel")
        self.title_label.grid(row=0, column=0, pady=10)
        
        # Add subtitle
        self.subtitle_label = ttk.Label(self.welcome_frame, 
                                       text="Advanced Steganography Analysis Tool", 
                                       style="Subtitle.TLabel")
        self.subtitle_label.grid(row=1, column=0, pady=5)
        
        # Add description
        self.description_text = (
            "StegnoX is a powerful tool for analyzing and working with steganography in images. "
            "It provides advanced features for hiding and revealing messages, as well as "
            "analyzing images for hidden data using various steganography techniques."
        )
        self.description_label = ttk.Label(self.welcome_frame, text=self.description_text, 
                                         wraplength=600, justify="center")
        self.description_label.grid(row=2, column=0, pady=10)
        
        # Create quick actions section
        self.actions_frame = ttk.Frame(self, style="HomeTab.TFrame")
        self.actions_frame.grid(row=1, column=0, sticky="ew", pady=20)
        
        # Configure actions frame
        self.actions_frame.columnconfigure(0, weight=1)
        
        # Add section title
        self.actions_title = ttk.Label(self.actions_frame, text="Quick Actions", 
                                      font=("Arial", 18, "bold"))
        self.actions_title.grid(row=0, column=0, pady=10)
        
        # Create action buttons grid
        self.buttons_frame = ttk.Frame(self.actions_frame, style="HomeTab.TFrame")
        self.buttons_frame.grid(row=1, column=0, pady=10)
        
        # Configure buttons grid
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(1, weight=1)
        self.buttons_frame.columnconfigure(2, weight=1)
        
        # Create action buttons
        self.encode_button = self._create_action_button(
            "Encode Message", 
            "Hide a secret message in an image",
            lambda: self.app.notebook.select(self.app.encode_tab),
            0, 0
        )
        
        self.decode_button = self._create_action_button(
            "Decode Message", 
            "Extract a hidden message from an image",
            lambda: self.app.notebook.select(self.app.decode_tab),
            0, 1
        )
        
        self.analyze_button = self._create_action_button(
            "Analyze Image", 
            "Analyze an image for hidden data",
            lambda: self.app.notebook.select(self.app.analyze_tab),
            0, 2
        )
        
        self.batch_button = self._create_action_button(
            "Batch Processing", 
            "Process multiple images at once",
            lambda: self.app.notebook.select(self.app.batch_tab),
            1, 0
        )
        
        self.settings_button = self._create_action_button(
            "Settings", 
            "Configure application settings",
            lambda: self.app.notebook.select(self.app.settings_tab),
            1, 1
        )
        
        self.help_button = self._create_action_button(
            "Help", 
            "View documentation and help",
            self.app.show_help,
            1, 2
        )
        
        # Create recent activity section
        self.activity_frame = ttk.Frame(self, style="HomeTab.TFrame")
        self.activity_frame.grid(row=2, column=0, sticky="ew", pady=20)
        
        # Configure activity frame
        self.activity_frame.columnconfigure(0, weight=1)
        
        # Add section title
        self.activity_title = ttk.Label(self.activity_frame, text="Recent Activity", 
                                       font=("Arial", 18, "bold"))
        self.activity_title.grid(row=0, column=0, pady=10)
        
        # Get recent files from config
        recent_files = self.app.config.get("recent_files", [])
        
        if recent_files:
            # Create recent files list
            self.recent_files_frame = ttk.Frame(self.activity_frame, style="HomeTab.TFrame")
            self.recent_files_frame.grid(row=1, column=0, pady=10)
            
            # Add recent files (up to 5)
            for i, file_path in enumerate(recent_files[:5]):
                file_name = os.path.basename(file_path)
                file_button = tk.Button(self.recent_files_frame, text=file_name, 
                                       font=("Arial", 10), bg="#f0f0f0", fg="#333",
                                       padx=10, pady=5, bd=1,
                                       command=lambda path=file_path: self._open_recent_file(path))
                file_button.grid(row=i, column=0, sticky="ew", pady=2)
        else:
            # Show message if no recent files
            self.no_activity_label = ttk.Label(self.activity_frame, 
                                             text="No recent activity to display", 
                                             font=("Arial", 10, "italic"))
            self.no_activity_label.grid(row=1, column=0, pady=10)
    
    def _create_action_button(self, title, description, command, row, column):
        """Create an action button with title and description"""
        button_frame = ttk.Frame(self.buttons_frame, style="HomeTab.TFrame")
        button_frame.grid(row=row, column=column, padx=10, pady=10)
        
        # Configure button frame
        button_frame.columnconfigure(0, weight=1)
        
        # Create button
        button = tk.Button(button_frame, text=title, font=("Arial", 12, "bold"),
                          bg="#4CAF50", fg="white", padx=15, pady=10,
                          bd=0, highlightthickness=0, command=command)
        button.grid(row=0, column=0, sticky="ew", pady=5)
        
        # Create description
        desc_label = ttk.Label(button_frame, text=description, wraplength=150, 
                              justify="center")
        desc_label.grid(row=1, column=0, pady=5)
        
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
            # Default to analyze tab
            self.app.notebook.select(self.app.analyze_tab)
            self.app.analyze_tab.load_image(file_path)
        else:
            # Unknown file type
            tk.messagebox.showerror("Error", f"Unsupported file type: {file_path}")
    
    def refresh(self):
        """Refresh the home tab content"""
        # This method can be called to refresh the recent activity section
        # when files are opened or processed
        
        # Remove existing recent files frame if it exists
        for widget in self.activity_frame.grid_slaves():
            if widget.grid_info()["row"] == 1:
                widget.destroy()
        
        # Get recent files from config
        recent_files = self.app.config.get("recent_files", [])
        
        if recent_files:
            # Create recent files list
            self.recent_files_frame = ttk.Frame(self.activity_frame, style="HomeTab.TFrame")
            self.recent_files_frame.grid(row=1, column=0, pady=10)
            
            # Add recent files (up to 5)
            for i, file_path in enumerate(recent_files[:5]):
                file_name = os.path.basename(file_path)
                file_button = tk.Button(self.recent_files_frame, text=file_name, 
                                       font=("Arial", 10), bg="#f0f0f0", fg="#333",
                                       padx=10, pady=5, bd=1,
                                       command=lambda path=file_path: self._open_recent_file(path))
                file_button.grid(row=i, column=0, sticky="ew", pady=2)
        else:
            # Show message if no recent files
            self.no_activity_label = ttk.Label(self.activity_frame, 
                                             text="No recent activity to display", 
                                             font=("Arial", 10, "italic"))
            self.no_activity_label.grid(row=1, column=0, pady=10)
