"""
Encode tab for the StegnoX desktop application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import threading

# Import components
from desktop.ui.components.image_preview import ImagePreview
from desktop.ui.components.file_browser import FileBrowser

class EncodeTab(ttk.Frame):
    """Encode tab for hiding messages in images"""
    
    def __init__(self, parent, app):
        """Initialize the encode tab"""
        super().__init__(parent)
        self.app = app
        
        # Initialize variables
        self.image_path = None
        self.encoding_in_progress = False
        
        # Configure the frame
        self.configure(style="EncodeTab.TFrame", padding=10)
        
        # Create a style for the encode tab
        style = ttk.Style()
        style.configure("EncodeTab.TFrame", background="#ffffff")
        
        # Create the encode tab content
        self._create_encode_tab_content()
    
    def _create_encode_tab_content(self):
        """Create the encode tab content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)  # Left panel
        self.columnconfigure(1, weight=1)  # Right panel
        self.rowconfigure(0, weight=1)
        
        # Create left panel (image selection and preview)
        self.left_panel = ttk.Frame(self, style="EncodeTab.TFrame")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure left panel
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(0, weight=0)  # File browser
        self.left_panel.rowconfigure(1, weight=1)  # Image preview
        
        # Add file browser
        self.file_browser = FileBrowser(self.left_panel, self.app)
        self.file_browser.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.file_browser.set_on_file_selected_callback(self._on_file_selected)
        
        # Add image preview
        self.image_preview = ImagePreview(self.left_panel, self.app)
        self.image_preview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create right panel (encoding options)
        self.right_panel = ttk.Frame(self, style="EncodeTab.TFrame")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure right panel
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=0)  # Title
        self.right_panel.rowconfigure(1, weight=0)  # Message input
        self.right_panel.rowconfigure(2, weight=0)  # Encoding options
        self.right_panel.rowconfigure(3, weight=0)  # Output options
        self.right_panel.rowconfigure(4, weight=0)  # Action buttons
        self.right_panel.rowconfigure(5, weight=1)  # Spacer
        
        # Add title
        self.title_label = ttk.Label(self.right_panel, text="Hide Message in Image", 
                                    font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        # Add message input section
        self.message_frame = ttk.LabelFrame(self.right_panel, text="Message")
        self.message_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure message frame
        self.message_frame.columnconfigure(0, weight=1)
        
        # Add message text area
        self.message_text = tk.Text(self.message_frame, height=6, width=40, wrap=tk.WORD)
        self.message_text.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Add message scrollbar
        self.message_scrollbar = ttk.Scrollbar(self.message_frame, orient="vertical", 
                                             command=self.message_text.yview)
        self.message_scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
        self.message_text.configure(yscrollcommand=self.message_scrollbar.set)
        
        # Add encoding options section
        self.options_frame = ttk.LabelFrame(self.right_panel, text="Encoding Options")
        self.options_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure options frame
        self.options_frame.columnconfigure(0, weight=0)
        self.options_frame.columnconfigure(1, weight=1)
        
        # Add encoding method selection
        self.method_label = ttk.Label(self.options_frame, text="Method:")
        self.method_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.method_var = tk.StringVar(value="lsb")
        self.method_combo = ttk.Combobox(self.options_frame, textvariable=self.method_var, 
                                        state="readonly")
        self.method_combo["values"] = ("lsb", "parity", "metadata")
        self.method_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Add password option (for future encryption)
        self.password_label = ttk.Label(self.options_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.options_frame, textvariable=self.password_var, 
                                      show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Add password note
        self.password_note = ttk.Label(self.options_frame, 
                                      text="Note: Password is optional and used for encryption", 
                                      font=("Arial", 8, "italic"))
        self.password_note.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Add output options section
        self.output_frame = ttk.LabelFrame(self.right_panel, text="Output Options")
        self.output_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure output frame
        self.output_frame.columnconfigure(0, weight=0)
        self.output_frame.columnconfigure(1, weight=1)
        
        # Add output path selection
        self.output_label = ttk.Label(self.output_frame, text="Output:")
        self.output_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_var)
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Add browse button
        self.output_button = ttk.Button(self.output_frame, text="Browse...", 
                                       command=self._browse_output)
        self.output_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Add action buttons section
        self.action_frame = ttk.Frame(self.right_panel, style="EncodeTab.TFrame")
        self.action_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure action frame
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=1)
        
        # Add encode button
        self.encode_button = ttk.Button(self.action_frame, text="Encode Message", 
                                       command=self._encode_message)
        self.encode_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        # Add clear button
        self.clear_button = ttk.Button(self.action_frame, text="Clear All", 
                                      command=self._clear_all)
        self.clear_button.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    def _on_file_selected(self, file_paths):
        """Handle file selection"""
        if file_paths:
            self.image_path = file_paths[0]
            self.image_preview.load_image(self.image_path)
            
            # Set default output path
            if not self.output_var.get():
                dir_name = os.path.dirname(self.image_path)
                file_name = os.path.basename(self.image_path)
                name, ext = os.path.splitext(file_name)
                output_path = os.path.join(dir_name, f"{name}_encoded.png")
                self.output_var.set(output_path)
    
    def _browse_output(self):
        """Browse for output file location"""
        output_path = filedialog.asksaveasfilename(
            title="Save encoded image as",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if output_path:
            self.output_var.set(output_path)
    
    def _encode_message(self):
        """Encode the message into the image"""
        # Validate inputs
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide")
            return
        
        output_path = self.output_var.get()
        if not output_path:
            messagebox.showerror("Error", "Please specify an output path")
            return
        
        # Get encoding method
        method = self.method_var.get()
        
        # Get password (if any)
        password = self.password_var.get()
        
        # Start encoding in a separate thread
        self.encoding_in_progress = True
        self.app.set_status(f"Encoding message using {method} method...")
        self.app.status_bar.show_progress(False)
        
        # Disable UI elements during encoding
        self._set_ui_state(False)
        
        # Start encoding thread
        encoding_thread = threading.Thread(
            target=self._run_encoding,
            args=(method, message, password, output_path)
        )
        encoding_thread.daemon = True
        encoding_thread.start()
    
    def _run_encoding(self, method, message, password, output_path):
        """Run the encoding process in a separate thread"""
        try:
            # Encode the message
            if method == "lsb":
                result = self.app.engine.lsb_encoding(self.image_path, message, output_path)
            elif method == "parity":
                result = self.app.engine.parity_bit_encoding(self.image_path, message, output_path)
            elif method == "metadata":
                result = self.app.engine.metadata_encoding(self.image_path, message, output_path)
            else:
                # Should never happen due to combobox restrictions
                raise ValueError(f"Unknown encoding method: {method}")
            
            # Update UI on the main thread
            self.after(0, lambda: self._encoding_complete(result))
        except Exception as e:
            # Handle errors
            self.app.logger.error(f"Encoding error: {str(e)}")
            self.after(0, lambda: self._encoding_error(str(e)))
    
    def _encoding_complete(self, result):
        """Handle encoding completion"""
        self.encoding_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        if result.get("success", False):
            self.app.set_status("Encoding complete")
            messagebox.showinfo("Success", result.get("message", "Message successfully encoded"))
            
            # Add output file to recent files
            output_path = self.output_var.get()
            recent_files = self.app.config.get("recent_files", [])
            if output_path in recent_files:
                recent_files.remove(output_path)
            recent_files.insert(0, output_path)
            max_recent = self.app.config.get("max_recent_files", 10)
            recent_files = recent_files[:max_recent]
            self.app.config.set("recent_files", recent_files)
            
            # Update sidebar
            if hasattr(self.app, 'sidebar'):
                self.app.sidebar.update_recent_files()
            
            # Update home tab
            if hasattr(self.app, 'home_tab'):
                self.app.home_tab.refresh()
        else:
            self.app.set_status("Encoding failed")
            messagebox.showerror("Error", result.get("error", "Failed to encode message"))
    
    def _encoding_error(self, error_message):
        """Handle encoding error"""
        self.encoding_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        self.app.set_status("Encoding failed")
        messagebox.showerror("Encoding Error", f"Failed to encode message: {error_message}")
    
    def _set_ui_state(self, enabled):
        """Enable or disable UI elements during encoding"""
        state = "normal" if enabled else "disabled"
        
        # Update UI elements
        self.file_browser.browse_button.configure(state=state)
        self.message_text.configure(state=state)
        self.method_combo.configure(state="readonly" if enabled else "disabled")
        self.password_entry.configure(state=state)
        self.output_entry.configure(state=state)
        self.output_button.configure(state=state)
        self.encode_button.configure(state=state)
        self.clear_button.configure(state=state)
    
    def _clear_all(self):
        """Clear all inputs"""
        self.message_text.delete("1.0", tk.END)
        self.password_var.set("")
        self.output_var.set("")
        
        # Don't clear the image as it might be needed again
    
    def select_image(self):
        """Select an image (called from main app)"""
        self.file_browser._browse_files()
    
    def load_image(self, image_path):
        """Load an image (called from sidebar)"""
        self.image_path = image_path
        self.image_preview.load_image(image_path)
        
        # Update file browser
        self.file_browser.file_path_var.set(image_path)
        
        # Set default output path
        if not self.output_var.get():
            dir_name = os.path.dirname(image_path)
            file_name = os.path.basename(image_path)
            name, ext = os.path.splitext(file_name)
            output_path = os.path.join(dir_name, f"{name}_encoded.png")
            self.output_var.set(output_path)
    
    def save_image(self):
        """Save the encoded image (called from main app)"""
        if self.encoding_in_progress:
            messagebox.showinfo("Info", "Encoding is in progress. Please wait.")
            return
        
        self._encode_message()
