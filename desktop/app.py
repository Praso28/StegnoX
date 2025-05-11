"""
StegnoX Desktop Application

This is the main entry point for the StegnoX desktop application.
It creates a modern, tabbed interface with advanced features.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
import logging
from PIL import Image, ImageTk

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import engine
from engine.stegnox_engine import StegnoxEngine

# Import UI components
from desktop.ui.components.header import Header
from desktop.ui.components.sidebar import Sidebar
from desktop.ui.components.status_bar import StatusBar

# Import tabs
from desktop.ui.tabs.home_tab import HomeTab
from desktop.ui.tabs.encode_tab import EncodeTab
from desktop.ui.tabs.decode_tab import DecodeTab
from desktop.ui.tabs.analyze_tab import AnalyzeTab
from desktop.ui.tabs.batch_tab import BatchTab
from desktop.ui.tabs.settings_tab import SettingsTab

# Import utilities
from desktop.utils.config import Config
from desktop.utils.image_utils import ImageUtils

class StegnoXApp:
    """Main StegnoX desktop application class"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("StegnoX - Advanced Steganography Tool")
        self.root.geometry('1024x768')
        self.root.minsize(800, 600)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(os.path.expanduser("~"), ".stegnox", "stegnox.log")),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("StegnoX")
        self.logger.info("Starting StegnoX Desktop Application")
        
        # Load configuration
        self.config = Config()
        
        # Initialize engine
        self.engine = StegnoxEngine()
        
        # Initialize utilities
        self.image_utils = ImageUtils()
        
        # Set up the UI
        self._setup_ui()
        
        # Set up event bindings
        self._setup_bindings()
        
        self.logger.info("StegnoX Desktop Application initialized")
    
    def _setup_ui(self):
        """Set up the user interface"""
        # Configure the grid
        self.root.columnconfigure(0, weight=0)  # Sidebar
        self.root.columnconfigure(1, weight=1)  # Main content
        self.root.rowconfigure(0, weight=0)     # Header
        self.root.rowconfigure(1, weight=1)     # Content
        self.root.rowconfigure(2, weight=0)     # Status bar
        
        # Create header
        self.header = Header(self.root, self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Create sidebar
        self.sidebar = Sidebar(self.root, self)
        self.sidebar.grid(row=1, column=0, sticky="ns")
        
        # Create main content area with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Create tabs
        self.home_tab = HomeTab(self.notebook, self)
        self.encode_tab = EncodeTab(self.notebook, self)
        self.decode_tab = DecodeTab(self.notebook, self)
        self.analyze_tab = AnalyzeTab(self.notebook, self)
        self.batch_tab = BatchTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.encode_tab, text="Encode")
        self.notebook.add(self.decode_tab, text="Decode")
        self.notebook.add(self.analyze_tab, text="Analyze")
        self.notebook.add(self.batch_tab, text="Batch Processing")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Create status bar
        self.status_bar = StatusBar(self.root, self)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        # Apply theme
        self._apply_theme()
    
    def _setup_bindings(self):
        """Set up event bindings"""
        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-q>", lambda e: self.quit_app())
        self.root.bind("<F1>", lambda e: self.show_help())
        
        # Window events
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
    
    def _apply_theme(self):
        """Apply the selected theme"""
        theme = self.config.get("theme")
        if theme == "dark":
            self.root.configure(bg='#2d2d2d')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure("TFrame", background='#2d2d2d')
            style.configure("TNotebook", background='#2d2d2d')
            style.configure("TNotebook.Tab", background='#1e1e1e', foreground='white')
            style.map("TNotebook.Tab", background=[("selected", "#3d3d3d")])
        else:
            self.root.configure(bg='#f0f0f0')
            style = ttk.Style()
            style.theme_use('clam')
    
    def open_file(self):
        """Open a file"""
        self.logger.info("Open file requested")
        # This will be implemented in the specific tabs
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Encode tab
            self.encode_tab.select_image()
        elif current_tab == 2:  # Decode tab
            self.decode_tab.select_image()
        elif current_tab == 3:  # Analyze tab
            self.analyze_tab.select_image()
        elif current_tab == 4:  # Batch tab
            self.batch_tab.select_images()
    
    def save_file(self):
        """Save a file"""
        self.logger.info("Save file requested")
        # This will be implemented in the specific tabs
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Encode tab
            self.encode_tab.save_image()
        elif current_tab == 3:  # Analyze tab
            self.analyze_tab.save_results()
    
    def quit_app(self):
        """Quit the application"""
        self.logger.info("Quit requested")
        # Save configuration
        self.config.save_config()
        self.root.destroy()
    
    def show_help(self):
        """Show help information"""
        self.logger.info("Help requested")
        # Show help dialog
        tk.messagebox.showinfo(
            "StegnoX Help",
            "StegnoX - Advanced Steganography Tool\n\n"
            "Keyboard Shortcuts:\n"
            "Ctrl+O: Open File\n"
            "Ctrl+S: Save File\n"
            "Ctrl+Q: Quit\n"
            "F1: Show Help\n\n"
            "For more information, visit the documentation."
        )
    
    def set_status(self, message):
        """Set the status bar message"""
        self.status_bar.set_status(message)

def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = StegnoXApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
