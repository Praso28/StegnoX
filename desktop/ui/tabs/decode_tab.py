"""
Decode tab for the StegnoX desktop application.
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

class DecodeTab(ttk.Frame):
    """Decode tab for extracting hidden messages from images"""
    
    def __init__(self, parent, app):
        """Initialize the decode tab"""
        super().__init__(parent)
        self.app = app
        
        # Initialize variables
        self.image_path = None
        self.decoding_in_progress = False
        
        # Configure the frame
        self.configure(style="DecodeTab.TFrame", padding=10)
        
        # Create a style for the decode tab
        style = ttk.Style()
        style.configure("DecodeTab.TFrame", background="#ffffff")
        
        # Create the decode tab content
        self._create_decode_tab_content()
    
    def _create_decode_tab_content(self):
        """Create the decode tab content"""
        # Configure the grid
        self.columnconfigure(0, weight=1)  # Left panel
        self.columnconfigure(1, weight=1)  # Right panel
        self.rowconfigure(0, weight=1)
        
        # Create left panel (image selection and preview)
        self.left_panel = ttk.Frame(self, style="DecodeTab.TFrame")
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
        
        # Create right panel (decoding options and results)
        self.right_panel = ttk.Frame(self, style="DecodeTab.TFrame")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure right panel
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=0)  # Title
        self.right_panel.rowconfigure(1, weight=0)  # Decoding options
        self.right_panel.rowconfigure(2, weight=0)  # Action buttons
        self.right_panel.rowconfigure(3, weight=1)  # Results
        
        # Add title
        self.title_label = ttk.Label(self.right_panel, text="Extract Hidden Message", 
                                    font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        # Add decoding options section
        self.options_frame = ttk.LabelFrame(self.right_panel, text="Decoding Options")
        self.options_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure options frame
        self.options_frame.columnconfigure(0, weight=0)
        self.options_frame.columnconfigure(1, weight=1)
        
        # Add decoding method selection
        self.method_label = ttk.Label(self.options_frame, text="Method:")
        self.method_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.method_var = tk.StringVar(value="auto")
        self.method_combo = ttk.Combobox(self.options_frame, textvariable=self.method_var, 
                                        state="readonly")
        self.method_combo["values"] = ("auto", "lsb", "parity", "metadata")
        self.method_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Add password option (for future decryption)
        self.password_label = ttk.Label(self.options_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.options_frame, textvariable=self.password_var, 
                                      show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Add password note
        self.password_note = ttk.Label(self.options_frame, 
                                      text="Note: Only needed if the message was encrypted", 
                                      font=("Arial", 8, "italic"))
        self.password_note.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        # Add action buttons section
        self.action_frame = ttk.Frame(self.right_panel, style="DecodeTab.TFrame")
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        
        # Configure action frame
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(1, weight=1)
        
        # Add decode button
        self.decode_button = ttk.Button(self.action_frame, text="Decode Message", 
                                       command=self._decode_message)
        self.decode_button.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        # Add clear button
        self.clear_button = ttk.Button(self.action_frame, text="Clear Results", 
                                      command=self._clear_results)
        self.clear_button.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Add results section
        self.results_frame = ttk.LabelFrame(self.right_panel, text="Extracted Message")
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure results frame
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Add results text area
        self.results_text = tk.Text(self.results_frame, height=15, width=40, wrap=tk.WORD, 
                                   state="disabled")
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add results scrollbar
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", 
                                             command=self.results_text.yview)
        self.results_scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
        self.results_text.configure(yscrollcommand=self.results_scrollbar.set)
        
        # Add copy button
        self.copy_button = ttk.Button(self.results_frame, text="Copy to Clipboard", 
                                     command=self._copy_to_clipboard)
        self.copy_button.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    
    def _on_file_selected(self, file_paths):
        """Handle file selection"""
        if file_paths:
            self.image_path = file_paths[0]
            self.image_preview.load_image(self.image_path)
    
    def _decode_message(self):
        """Decode the message from the image"""
        # Validate inputs
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first")
            return
        
        # Get decoding method
        method = self.method_var.get()
        
        # Get password (if any)
        password = self.password_var.get()
        
        # Start decoding in a separate thread
        self.decoding_in_progress = True
        self.app.set_status(f"Decoding message using {method} method...")
        self.app.status_bar.show_progress(False)
        
        # Disable UI elements during decoding
        self._set_ui_state(False)
        
        # Start decoding thread
        decoding_thread = threading.Thread(
            target=self._run_decoding,
            args=(method, password)
        )
        decoding_thread.daemon = True
        decoding_thread.start()
    
    def _run_decoding(self, method, password):
        """Run the decoding process in a separate thread"""
        try:
            # Decode the message
            if method == "auto":
                # Try all methods
                results = {}
                
                # Try LSB first
                lsb_result = self.app.engine.lsb_extraction(self.image_path)
                if "message" in lsb_result and lsb_result["message"] != "No valid data found":
                    results["LSB"] = lsb_result["message"]
                
                # Try parity
                parity_result = self.app.engine.parity_bit_extraction(self.image_path)
                if "message" in parity_result and parity_result["message"] != "No readable text found with parity method":
                    results["Parity"] = parity_result["message"]
                
                # Try metadata
                metadata_result = self.app.engine.metadata_extraction(self.image_path)
                if "metadata" in metadata_result and metadata_result["metadata"]:
                    for key, value in metadata_result["metadata"].items():
                        if key.lower() == "comment" and value:
                            results["Metadata"] = value
                
                # Update UI on the main thread
                self.after(0, lambda: self._decoding_complete_auto(results))
            else:
                # Use specific method
                if method == "lsb":
                    result = self.app.engine.lsb_extraction(self.image_path)
                elif method == "parity":
                    result = self.app.engine.parity_bit_extraction(self.image_path)
                elif method == "metadata":
                    result = self.app.engine.metadata_extraction(self.image_path)
                else:
                    # Should never happen due to combobox restrictions
                    raise ValueError(f"Unknown decoding method: {method}")
                
                # Update UI on the main thread
                self.after(0, lambda: self._decoding_complete(result, method))
        except Exception as e:
            # Handle errors
            self.app.logger.error(f"Decoding error: {str(e)}")
            self.after(0, lambda: self._decoding_error(str(e)))
    
    def _decoding_complete_auto(self, results):
        """Handle auto decoding completion"""
        self.decoding_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        if results:
            self.app.set_status("Decoding complete")
            
            # Clear previous results
            self.results_text.configure(state="normal")
            self.results_text.delete("1.0", tk.END)
            
            # Display all results
            for method, message in results.items():
                self.results_text.insert(tk.END, f"=== {method} Method ===\n")
                self.results_text.insert(tk.END, f"{message}\n\n")
            
            self.results_text.configure(state="disabled")
        else:
            self.app.set_status("No hidden message found")
            
            # Clear previous results
            self.results_text.configure(state="normal")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, "No hidden message found in this image.")
            self.results_text.configure(state="disabled")
            
            messagebox.showinfo("No Message", "No hidden message was found in this image.")
    
    def _decoding_complete(self, result, method):
        """Handle decoding completion"""
        self.decoding_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        # Clear previous results
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)
        
        if method == "lsb":
            if "message" in result and result["message"] != "No valid data found":
                self.app.set_status("Message extracted successfully")
                self.results_text.insert(tk.END, result["message"])
            else:
                self.app.set_status("No hidden message found")
                self.results_text.insert(tk.END, "No hidden message found using LSB method.")
                messagebox.showinfo("No Message", "No hidden message was found using LSB method.")
        elif method == "parity":
            if "message" in result and result["message"] != "No readable text found with parity method":
                self.app.set_status("Message extracted successfully")
                self.results_text.insert(tk.END, result["message"])
            else:
                self.app.set_status("No hidden message found")
                self.results_text.insert(tk.END, "No hidden message found using parity bit method.")
                messagebox.showinfo("No Message", "No hidden message was found using parity bit method.")
        elif method == "metadata":
            if "metadata" in result and result["metadata"]:
                self.app.set_status("Metadata extracted successfully")
                
                # Look for comment field first
                if "comment" in result["metadata"] and result["metadata"]["comment"]:
                    self.results_text.insert(tk.END, f"Comment: {result['metadata']['comment']}\n\n")
                
                # Display all metadata
                self.results_text.insert(tk.END, "All Metadata:\n")
                for key, value in result["metadata"].items():
                    self.results_text.insert(tk.END, f"{key}: {value}\n")
            else:
                self.app.set_status("No metadata found")
                self.results_text.insert(tk.END, "No metadata found in this image.")
                messagebox.showinfo("No Metadata", "No metadata was found in this image.")
        
        self.results_text.configure(state="disabled")
    
    def _decoding_error(self, error_message):
        """Handle decoding error"""
        self.decoding_in_progress = False
        self.app.status_bar.hide_progress()
        
        # Re-enable UI elements
        self._set_ui_state(True)
        
        self.app.set_status("Decoding failed")
        
        # Clear previous results
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, f"Error: {error_message}")
        self.results_text.configure(state="disabled")
        
        messagebox.showerror("Decoding Error", f"Failed to decode message: {error_message}")
    
    def _set_ui_state(self, enabled):
        """Enable or disable UI elements during decoding"""
        state = "normal" if enabled else "disabled"
        
        # Update UI elements
        self.file_browser.browse_button.configure(state=state)
        self.method_combo.configure(state="readonly" if enabled else "disabled")
        self.password_entry.configure(state=state)
        self.decode_button.configure(state=state)
        self.clear_button.configure(state=state)
        self.copy_button.configure(state=state)
    
    def _clear_results(self):
        """Clear the results"""
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.configure(state="disabled")
        self.password_var.set("")
    
    def _copy_to_clipboard(self):
        """Copy results to clipboard"""
        text = self.results_text.get("1.0", tk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.app.set_status("Copied to clipboard")
    
    def select_image(self):
        """Select an image (called from main app)"""
        self.file_browser._browse_files()
    
    def load_image(self, image_path):
        """Load an image (called from sidebar)"""
        self.image_path = image_path
        self.image_preview.load_image(image_path)
        
        # Update file browser
        self.file_browser.file_path_var.set(image_path)
