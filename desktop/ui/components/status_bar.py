"""
Status bar component for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class StatusBar(ttk.Frame):
    """Status bar component with status message and progress indicator"""
    
    def __init__(self, parent, app):
        """Initialize the status bar component"""
        super().__init__(parent)
        self.app = app
        
        # Configure the frame
        self.configure(height=25, style="StatusBar.TFrame")
        
        # Create a style for the status bar
        style = ttk.Style()
        style.configure("StatusBar.TFrame", background="#e0e0e0")
        
        # Initialize variables
        self.status_text = tk.StringVar()
        self.status_text.set("Ready")
        
        self.progress_value = tk.DoubleVar()
        self.progress_value.set(0)
        
        self.progress_visible = False
        self.progress_thread = None
        
        # Create the status bar content
        self._create_status_bar_content()
    
    def _create_status_bar_content(self):
        """Create the status bar content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)  # Status message
        self.columnconfigure(1, weight=0)  # Progress bar
        
        # Create status message label
        self.status_label = tk.Label(self, textvariable=self.status_text, 
                                    font=("Arial", 9), bg="#e0e0e0", anchor="w")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        # Create progress bar (hidden by default)
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_value, 
                                           length=150, mode="determinate")
        # Progress bar is not initially visible
    
    def set_status(self, message):
        """Set the status message"""
        self.status_text.set(message)
        self.update_idletasks()
    
    def show_progress(self, determinate=True):
        """Show the progress bar"""
        if not self.progress_visible:
            self.progress_visible = True
            
            # Configure progress bar mode
            if determinate:
                self.progress_bar.configure(mode="determinate")
                self.progress_value.set(0)
            else:
                self.progress_bar.configure(mode="indeterminate")
                self.progress_bar.start(10)
            
            # Show progress bar
            self.progress_bar.grid(row=0, column=1, padx=10, pady=2)
            self.update_idletasks()
    
    def hide_progress(self):
        """Hide the progress bar"""
        if self.progress_visible:
            self.progress_visible = False
            
            # Stop indeterminate animation if active
            if self.progress_bar.cget("mode") == "indeterminate":
                self.progress_bar.stop()
            
            # Hide progress bar
            self.progress_bar.grid_forget()
            self.update_idletasks()
    
    def set_progress(self, value):
        """Set the progress value (0-100)"""
        if self.progress_visible and self.progress_bar.cget("mode") == "determinate":
            self.progress_value.set(value)
            self.update_idletasks()
    
    def start_task(self, message, determinate=True):
        """Start a task with progress indication"""
        self.set_status(message)
        self.show_progress(determinate)
    
    def complete_task(self, message="Ready"):
        """Complete a task and hide progress"""
        self.hide_progress()
        self.set_status(message)
    
    def start_timed_task(self, message, duration, completion_message="Ready"):
        """Start a task with a timed progress bar"""
        if self.progress_thread and self.progress_thread.is_alive():
            # Cancel existing thread
            self._cancel_progress_thread = True
            self.progress_thread.join()
        
        self._cancel_progress_thread = False
        self.progress_thread = threading.Thread(
            target=self._run_timed_progress,
            args=(message, duration, completion_message)
        )
        self.progress_thread.daemon = True
        self.progress_thread.start()
    
    def _run_timed_progress(self, message, duration, completion_message):
        """Run a timed progress bar"""
        # Start task
        self.app.root.after(0, lambda: self.start_task(message, True))
        
        # Update progress over time
        start_time = time.time()
        while time.time() - start_time < duration:
            if self._cancel_progress_thread:
                return
            
            # Calculate progress percentage
            elapsed = time.time() - start_time
            progress = min(100, (elapsed / duration) * 100)
            
            # Update progress bar
            self.app.root.after(0, lambda p=progress: self.set_progress(p))
            
            # Sleep briefly
            time.sleep(0.05)
        
        # Complete task
        self.app.root.after(0, lambda: self.complete_task(completion_message))
