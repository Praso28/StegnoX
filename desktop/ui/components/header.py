"""
Header component for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class Header(ttk.Frame):
    """Header component with logo and main menu"""
    
    def __init__(self, parent, app):
        """Initialize the header component"""
        super().__init__(parent)
        self.app = app
        
        # Configure the frame
        self.configure(height=60, style="Header.TFrame")
        
        # Create a style for the header
        style = ttk.Style()
        style.configure("Header.TFrame", background="#3f51b5")
        
        # Create the header content
        self._create_header_content()
    
    def _create_header_content(self):
        """Create the header content"""
        # Configure the grid
        self.columnconfigure(0, weight=0)  # Logo
        self.columnconfigure(1, weight=1)  # Title
        self.columnconfigure(2, weight=0)  # Menu
        
        # Create logo (placeholder for now)
        self.logo_frame = ttk.Frame(self, width=60, height=60, style="Header.TFrame")
        self.logo_frame.grid(row=0, column=0, padx=10)
        self.logo_frame.pack_propagate(False)
        
        # Try to load logo image
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                     "assets", "logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((50, 50), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                self.logo_label = tk.Label(self.logo_frame, image=self.logo_photo, bg="#3f51b5")
                self.logo_label.pack(fill=tk.BOTH, expand=True)
            else:
                # Fallback to text
                self.logo_label = tk.Label(self.logo_frame, text="SX", font=("Arial", 24, "bold"), 
                                          fg="white", bg="#3f51b5")
                self.logo_label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            self.app.logger.error(f"Failed to load logo: {str(e)}")
            # Fallback to text
            self.logo_label = tk.Label(self.logo_frame, text="SX", font=("Arial", 24, "bold"), 
                                      fg="white", bg="#3f51b5")
            self.logo_label.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        self.title_label = tk.Label(self, text="StegnoX", font=("Arial", 18, "bold"), 
                                   fg="white", bg="#3f51b5")
        self.title_label.grid(row=0, column=1, sticky="w", padx=10)
        
        # Create menu frame
        self.menu_frame = ttk.Frame(self, style="Header.TFrame")
        self.menu_frame.grid(row=0, column=2, padx=10)
        
        # Create menu buttons
        self.file_menu_button = self._create_menu_button("File")
        self.help_menu_button = self._create_menu_button("Help")
        
        # Create file menu
        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open...", command=self.app.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save...", command=self.app.save_file, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Settings", 
                                  command=lambda: self.app.notebook.select(self.app.settings_tab))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.app.quit_app, accelerator="Ctrl+Q")
        
        # Create help menu
        self.help_menu = tk.Menu(self, tearoff=0)
        self.help_menu.add_command(label="Documentation", command=self._open_documentation)
        self.help_menu.add_command(label="About", command=self._show_about)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Help", command=self.app.show_help, accelerator="F1")
    
    def _create_menu_button(self, text):
        """Create a menu button"""
        button = tk.Button(self.menu_frame, text=text, font=("Arial", 10),
                          bg="#3f51b5", fg="white", bd=0, padx=10,
                          activebackground="#303f9f", activeforeground="white")
        button.pack(side=tk.LEFT)
        
        # Bind events
        if text == "File":
            button.bind("<Button-1>", self._show_file_menu)
        elif text == "Help":
            button.bind("<Button-1>", self._show_help_menu)
        
        return button
    
    def _show_file_menu(self, event):
        """Show the file menu"""
        self.file_menu.post(event.widget.winfo_rootx(), 
                           event.widget.winfo_rooty() + event.widget.winfo_height())
    
    def _show_help_menu(self, event):
        """Show the help menu"""
        self.help_menu.post(event.widget.winfo_rootx(), 
                           event.widget.winfo_rooty() + event.widget.winfo_height())
    
    def _open_documentation(self):
        """Open the documentation"""
        # This would typically open a web browser with documentation
        self.app.logger.info("Documentation requested")
        import webbrowser
        webbrowser.open("https://github.com/yourusername/stegnox")
    
    def _show_about(self):
        """Show the about dialog"""
        self.app.logger.info("About dialog requested")
        tk.messagebox.showinfo(
            "About StegnoX",
            "StegnoX - Advanced Steganography Tool\n\n"
            "Version: 1.0.0\n\n"
            "A powerful tool for analyzing and working with steganography in images.\n\n"
            "© 2023 StegnoX Team"
        )
