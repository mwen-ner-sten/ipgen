#!/usr/bin/env python3
"""
A simple test script to run the GUI.
"""
import tkinter as tk
from ipgen.gui import IPGenGUI

def main():
    """Start the GUI application."""
    print("Starting GUI application...")
    try:
        root = tk.Tk()
        print("Tkinter root window created")
        app = IPGenGUI(root)
        print("IPGenGUI instance created")
        print("Running mainloop...")
        root.mainloop()
        print("Mainloop exited")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 