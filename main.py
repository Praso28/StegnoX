"""
StegnoX - Advanced Steganography Analysis Tool

This is the main entry point for the StegnoX application.
"""

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="StegnoX - Advanced Steganography Analysis Tool")
    parser.add_argument("--mode", choices=["web", "desktop"], default="web",
                        help="Run in web mode (with API) or desktop mode (GUI)")
    args = parser.parse_args()

    if args.mode == "web":
        # Import here to avoid loading unnecessary modules
        from backend.app import app
        app.run(debug=True)
    else:
        # Import here to avoid loading unnecessary modules
        import tkinter as tk
        from desktop.app import StegnoXApp
        root = tk.Tk()
        app = StegnoXApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()
