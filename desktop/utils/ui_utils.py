"""
UI utilities for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class UIUtils:
    """Utility class for UI-related functions"""
    
    @staticmethod
    def create_tooltip(widget, text):
        """
        Create a tooltip for a widget
        
        Args:
            widget: The widget to add a tooltip to
            text: The tooltip text
        """
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create a toplevel window
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            # Create tooltip content
            label = ttk.Label(tooltip, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("Arial", 9, "normal"))
            label.pack(padx=2, pady=2)
            
            # Store tooltip reference
            widget.tooltip = tooltip
        
        def leave(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()
                del widget.tooltip
        
        # Bind events
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    @staticmethod
    def create_scrollable_frame(parent):
        """
        Create a scrollable frame
        
        Args:
            parent: The parent widget
            
        Returns:
            tuple: (container_frame, scrollable_frame)
        """
        # Create a container frame
        container = ttk.Frame(parent)
        
        # Create a canvas
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Create the scrollable frame
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Add the scrollable frame to the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the widgets
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure the canvas to expand with the container
        container.bind("<Configure>", lambda e: canvas.configure(width=e.width-20))
        
        return container, scrollable_frame
    
    @staticmethod
    def create_section_header(parent, text):
        """
        Create a section header
        
        Args:
            parent: The parent widget
            text: The header text
            
        Returns:
            ttk.Label: The header label
        """
        # Create a style for the header
        style = ttk.Style()
        style.configure("SectionHeader.TLabel", font=("Arial", 12, "bold"))
        
        # Create the header label
        header = ttk.Label(parent, text=text, style="SectionHeader.TLabel")
        
        return header
    
    @staticmethod
    def create_info_panel(parent, title, content):
        """
        Create an information panel with title and content
        
        Args:
            parent: The parent widget
            title: The panel title
            content: The panel content (text or widget)
            
        Returns:
            ttk.LabelFrame: The panel frame
        """
        # Create the panel frame
        panel = ttk.LabelFrame(parent, text=title)
        
        # Add content
        if isinstance(content, str):
            # Create a label for text content
            label = ttk.Label(panel, text=content, wraplength=300)
            label.pack(padx=10, pady=10, fill="both", expand=True)
        else:
            # Assume content is a widget
            content.pack(padx=10, pady=10, fill="both", expand=True)
        
        return panel
    
    @staticmethod
    def create_status_indicator(parent, status, text):
        """
        Create a status indicator
        
        Args:
            parent: The parent widget
            status: The status value ("success", "warning", "error", "info")
            text: The status text
            
        Returns:
            ttk.Frame: The indicator frame
        """
        # Create the indicator frame
        frame = ttk.Frame(parent)
        
        # Determine indicator color
        if status == "success":
            color = "#4CAF50"  # Green
        elif status == "warning":
            color = "#FF9800"  # Orange
        elif status == "error":
            color = "#F44336"  # Red
        else:  # info
            color = "#2196F3"  # Blue
        
        # Create indicator
        indicator = tk.Canvas(frame, width=16, height=16, bg=parent.cget("background"),
                             highlightthickness=0)
        indicator.create_oval(2, 2, 14, 14, fill=color, outline="")
        indicator.pack(side="left", padx=(0, 5))
        
        # Create text label
        label = ttk.Label(frame, text=text)
        label.pack(side="left")
        
        return frame
    
    @staticmethod
    def create_button_group(parent, buttons):
        """
        Create a group of buttons
        
        Args:
            parent: The parent widget
            buttons: List of button configurations [(text, command), ...]
            
        Returns:
            ttk.Frame: The button group frame
        """
        # Create the button group frame
        frame = ttk.Frame(parent)
        
        # Create buttons
        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(frame, text=text, command=command)
            button.grid(row=0, column=i, padx=5, pady=5)
        
        return frame
    
    @staticmethod
    def create_form_field(parent, label_text, widget_type, **kwargs):
        """
        Create a form field with label and input widget
        
        Args:
            parent: The parent widget
            label_text: The label text
            widget_type: The widget class (ttk.Entry, ttk.Combobox, etc.)
            **kwargs: Additional arguments for the widget
            
        Returns:
            tuple: (frame, widget)
        """
        # Create the field frame
        frame = ttk.Frame(parent)
        
        # Create label
        label = ttk.Label(frame, text=label_text)
        label.pack(side="left", padx=(0, 5))
        
        # Create widget
        widget = widget_type(frame, **kwargs)
        widget.pack(side="left", fill="x", expand=True)
        
        return frame, widget
    
    @staticmethod
    def center_window(window, width, height):
        """
        Center a window on the screen
        
        Args:
            window: The window to center
            width: The window width
            height: The window height
        """
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set geometry
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def create_dialog(parent, title, width=400, height=300):
        """
        Create a dialog window
        
        Args:
            parent: The parent window
            title: The dialog title
            width: The dialog width
            height: The dialog height
            
        Returns:
            tk.Toplevel: The dialog window
        """
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        UIUtils.center_window(dialog, width, height)
        
        # Make dialog modal
        dialog.focus_set()
        
        return dialog
