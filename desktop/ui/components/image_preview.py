"""
Image preview component for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class ImagePreview(ttk.Frame):
    """Image preview component with zoom and pan capabilities"""
    
    def __init__(self, parent, app, max_size=(500, 500)):
        """Initialize the image preview component"""
        super().__init__(parent)
        self.app = app
        self.max_size = max_size
        
        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.displayed_image = None
        self.photo_image = None
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Configure the frame
        self.configure(style="ImagePreview.TFrame")
        
        # Create a style for the image preview
        style = ttk.Style()
        style.configure("ImagePreview.TFrame", background="#ffffff")
        
        # Create the image preview content
        self._create_image_preview_content()
    
    def _create_image_preview_content(self):
        """Create the image preview content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        
        # Create canvas for image display
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Create scrollbars
        self.h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Configure canvas scrolling
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Create control panel
        self.control_panel = ttk.Frame(self, style="ImagePreview.TFrame", height=30)
        self.control_panel.grid(row=1, column=0, sticky="ew")
        
        # Create zoom controls
        self.zoom_out_button = ttk.Button(self.control_panel, text="-", width=3, 
                                         command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.zoom_level_label = ttk.Label(self.control_panel, text="100%")
        self.zoom_level_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.zoom_in_button = ttk.Button(self.control_panel, text="+", width=3, 
                                        command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.reset_button = ttk.Button(self.control_panel, text="Reset", 
                                      command=self.reset_view)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Create image info label
        self.info_label = ttk.Label(self.control_panel, text="No image loaded")
        self.info_label.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self._start_pan)
        self.canvas.bind("<B1-Motion>", self._pan_image)
        self.canvas.bind("<MouseWheel>", self._mouse_wheel)  # Windows
        self.canvas.bind("<Button-4>", self._mouse_wheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self._mouse_wheel)    # Linux scroll down
    
    def load_image(self, image_path):
        """Load an image for preview"""
        try:
            # Save the image path
            self.image_path = image_path
            
            # Open the image
            self.original_image = Image.open(image_path)
            
            # Reset view parameters
            self.zoom_level = 1.0
            self.pan_x = 0
            self.pan_y = 0
            
            # Update the display
            self._update_display()
            
            # Update image info
            self._update_image_info()
            
            # Add to recent files
            self._add_to_recent_files()
            
            return True
        except Exception as e:
            self.app.logger.error(f"Failed to load image: {str(e)}")
            self.info_label.configure(text="Failed to load image")
            return False
    
    def _update_display(self):
        """Update the image display"""
        if self.original_image:
            # Calculate the display size based on zoom level
            width, height = self.original_image.size
            display_width = int(width * self.zoom_level)
            display_height = int(height * self.zoom_level)
            
            # Resize the image
            self.displayed_image = self.original_image.resize((display_width, display_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            self.photo_image = ImageTk.PhotoImage(self.displayed_image)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(self.pan_x, self.pan_y, anchor="nw", image=self.photo_image, tags="image")
            
            # Configure scrollregion
            self.canvas.configure(scrollregion=(0, 0, display_width, display_height))
            
            # Update zoom level label
            self.zoom_level_label.configure(text=f"{int(self.zoom_level * 100)}%")
    
    def _update_image_info(self):
        """Update the image information"""
        if self.original_image:
            width, height = self.original_image.size
            format_name = self.original_image.format
            mode = self.original_image.mode
            file_size = os.path.getsize(self.image_path) / 1024  # KB
            
            info_text = f"{width}x{height} | {format_name} | {mode} | {file_size:.1f} KB"
            self.info_label.configure(text=info_text)
    
    def _add_to_recent_files(self):
        """Add the current image to recent files"""
        if self.image_path:
            # Get recent files from config
            recent_files = self.app.config.get("recent_files", [])
            
            # Remove if already exists
            if self.image_path in recent_files:
                recent_files.remove(self.image_path)
            
            # Add to the beginning
            recent_files.insert(0, self.image_path)
            
            # Limit to max_recent_files
            max_recent = self.app.config.get("max_recent_files", 10)
            recent_files = recent_files[:max_recent]
            
            # Update config
            self.app.config.set("recent_files", recent_files)
            
            # Update sidebar
            if hasattr(self.app, 'sidebar'):
                self.app.sidebar.update_recent_files()
    
    def zoom_in(self):
        """Zoom in on the image"""
        if self.original_image:
            self.zoom_level = min(5.0, self.zoom_level * 1.25)
            self._update_display()
    
    def zoom_out(self):
        """Zoom out from the image"""
        if self.original_image:
            self.zoom_level = max(0.1, self.zoom_level / 1.25)
            self._update_display()
    
    def reset_view(self):
        """Reset the view to default"""
        if self.original_image:
            self.zoom_level = 1.0
            self.pan_x = 0
            self.pan_y = 0
            self._update_display()
    
    def _start_pan(self, event):
        """Start panning the image"""
        self.canvas.scan_mark(event.x, event.y)
    
    def _pan_image(self, event):
        """Pan the image"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    
    def _mouse_wheel(self, event):
        """Handle mouse wheel events for zooming"""
        if self.original_image:
            # Determine zoom direction
            if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
                # Zoom in
                self.zoom_level = min(5.0, self.zoom_level * 1.1)
            elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
                # Zoom out
                self.zoom_level = max(0.1, self.zoom_level / 1.1)
            
            # Update display
            self._update_display()
