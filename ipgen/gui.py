"""
GUI application for testing the IP generator.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import json
import yaml
from typing import Optional
import os

from .core import IPGenerator
from .parsers import (
    parse_csv,
    parse_excel,
    parse_json,
    parse_yaml,
    parse_cidr,
    parse_range,
    parse_wildcard,
    parse_gateway_subnet
)

class IPGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IPGen - IP Address Generator")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        self.generator = IPGenerator()
        self.file_path = tk.StringVar()
        self.ip_count = 0
        self.setup_gui()
        self.show_single_ip_fields()  # Show default fields
    
    def setup_gui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - 0 IPs loaded")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="5")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Input type selection frame
        input_type_frame = ttk.Frame(input_frame)
        input_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_type_frame, text="Input Type:").pack(side=tk.LEFT, padx=5)
        self.input_type = ttk.Combobox(input_type_frame, width=15, values=[
            "Single IP",
            "IP Range",
            "CIDR",
            "Wildcard",
            "Gateway/Subnet",
            "CSV File",
            "Excel File",
            "JSON File",
            "YAML File"
        ])
        self.input_type.pack(side=tk.LEFT, padx=5)
        self.input_type.set("Single IP")
        self.input_type.bind('<<ComboboxSelected>>', self.on_input_type_change)
        
        # File selection button
        self.file_button = ttk.Button(input_type_frame, text="Select File", command=self.select_file)
        self.file_button.pack(side=tk.LEFT, padx=5)
        self.file_button.pack_forget()  # Hidden by default
        
        # File path display
        self.file_label = ttk.Label(input_type_frame, textvariable=self.file_path, width=30)
        self.file_label.pack(side=tk.LEFT, padx=5)
        self.file_label.pack_forget()  # Hidden by default
        
        # Input fields container
        self.input_fields_frame = ttk.Frame(input_frame, padding="5")
        self.input_fields_frame.pack(fill=tk.X, pady=5)
        
        # Add button frame
        add_button_frame = ttk.Frame(input_frame)
        add_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(add_button_frame, text="Add to Generator", command=self.add_to_generator).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_button_frame, text="Clear Generator", command=self.clear_generator).pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Output controls frame
        output_controls_frame = ttk.Frame(output_frame)
        output_controls_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_controls_frame, text="Output Type:").pack(side=tk.LEFT, padx=5)
        self.output_type = ttk.Combobox(output_controls_frame, width=15, values=[
            "Preview",
            "CSV File",
            "Excel File",
            "JSON File",
            "YAML File"
        ])
        self.output_type.pack(side=tk.LEFT, padx=5)
        self.output_type.set("Preview")
        
        ttk.Button(output_controls_frame, text="Generate Output", command=self.generate_output).pack(side=tk.LEFT, padx=5)
        
        # Preview text with scrollbar
        preview_frame = ttk.Frame(output_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
    
    def on_input_type_change(self, event=None):
        # Clear previous input fields
        for widget in self.input_fields_frame.winfo_children():
            widget.destroy()
        
        input_type = self.input_type.get()
        
        if input_type in ["CSV File", "Excel File", "JSON File", "YAML File"]:
            self.file_button.pack(side=tk.LEFT, padx=5)
            self.file_label.pack(side=tk.LEFT, padx=5)
        else:
            self.file_button.pack_forget()
            self.file_label.pack_forget()
            
            if input_type == "Single IP":
                self.show_single_ip_fields()
            elif input_type == "IP Range":
                self.show_ip_range_fields()
            elif input_type == "CIDR":
                self.show_cidr_fields()
            elif input_type == "Wildcard":
                self.show_wildcard_fields()
            elif input_type == "Gateway/Subnet":
                self.show_gateway_subnet_fields()
    
    def show_single_ip_fields(self):
        """Display fields for single IP input."""
        frame = ttk.Frame(self.input_fields_frame)
        frame.pack(fill=tk.X)
        
        ttk.Label(frame, text="IP Address:").pack(side=tk.LEFT, padx=5)
        self.ip_entry = ttk.Entry(frame, width=20)
        self.ip_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Focus the entry field
        self.ip_entry.focus_set()
    
    def show_ip_range_fields(self):
        """Display fields for IP range input."""
        # Start IP
        start_frame = ttk.Frame(self.input_fields_frame)
        start_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(start_frame, text="Start IP:").pack(side=tk.LEFT, padx=5)
        self.start_ip = ttk.Entry(start_frame, width=20)
        self.start_ip.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # End IP
        end_frame = ttk.Frame(self.input_fields_frame)
        end_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(end_frame, text="End IP:").pack(side=tk.LEFT, padx=5)
        self.end_ip = ttk.Entry(end_frame, width=20)
        self.end_ip.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Focus the first entry field
        self.start_ip.focus_set()
    
    def show_cidr_fields(self):
        """Display fields for CIDR input."""
        frame = ttk.Frame(self.input_fields_frame)
        frame.pack(fill=tk.X)
        
        ttk.Label(frame, text="CIDR Notation:").pack(side=tk.LEFT, padx=5)
        self.cidr_entry = ttk.Entry(frame, width=20)
        self.cidr_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Example label
        example_frame = ttk.Frame(self.input_fields_frame)
        example_frame.pack(fill=tk.X, pady=2)
        ttk.Label(example_frame, text="Example: 192.168.1.0/24").pack(side=tk.LEFT, padx=5)
        
        # Focus the entry field
        self.cidr_entry.focus_set()
    
    def show_wildcard_fields(self):
        """Display fields for wildcard pattern input."""
        # IP
        ip_frame = ttk.Frame(self.input_fields_frame)
        ip_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(ip_frame, text="IP Address:").pack(side=tk.LEFT, padx=5)
        self.wildcard_ip = ttk.Entry(ip_frame, width=20)
        self.wildcard_ip.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Wildcard
        wildcard_frame = ttk.Frame(self.input_fields_frame)
        wildcard_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(wildcard_frame, text="Wildcard Mask:").pack(side=tk.LEFT, padx=5)
        self.wildcard_mask = ttk.Entry(wildcard_frame, width=20)
        self.wildcard_mask.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Example
        example_frame = ttk.Frame(self.input_fields_frame)
        example_frame.pack(fill=tk.X, pady=2)
        ttk.Label(example_frame, text="Example: IP=192.168.1.0, Mask=0.0.0.255").pack(side=tk.LEFT, padx=5)
        
        # Focus the first entry field
        self.wildcard_ip.focus_set()
    
    def show_gateway_subnet_fields(self):
        """Display fields for gateway/subnet input."""
        # Gateway
        gateway_frame = ttk.Frame(self.input_fields_frame)
        gateway_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(gateway_frame, text="Gateway:").pack(side=tk.LEFT, padx=5)
        self.gateway_entry = ttk.Entry(gateway_frame, width=20)
        self.gateway_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Subnet
        subnet_frame = ttk.Frame(self.input_fields_frame)
        subnet_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(subnet_frame, text="Subnet Mask:").pack(side=tk.LEFT, padx=5)
        self.subnet_entry = ttk.Entry(subnet_frame, width=20)
        self.subnet_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Example
        example_frame = ttk.Frame(self.input_fields_frame)
        example_frame.pack(fill=tk.X, pady=2)
        ttk.Label(example_frame, text="Example: Gateway=192.168.1.1, Subnet=255.255.255.0").pack(side=tk.LEFT, padx=5)
        
        # Focus the first entry field
        self.gateway_entry.focus_set()
    
    def select_file(self):
        """Handle file selection for file-based inputs."""
        filetypes = {
            "CSV File": [("CSV files", "*.csv")],
            "Excel File": [("Excel files", "*.xlsx")],
            "JSON File": [("JSON files", "*.json")],
            "YAML File": [("YAML files", "*.yaml;*.yml")]
        }
        
        input_type = self.input_type.get()
        filetype = filetypes.get(input_type, [("All files", "*.*")])
        
        filename = filedialog.askopenfilename(filetypes=filetype)
        if filename:
            self.file_path.set(os.path.basename(filename))
            self.file_full_path = filename
    
    def add_to_generator(self):
        """Add IP addresses to the generator based on current input type."""
        try:
            input_type = self.input_type.get()
            
            if input_type == "Single IP":
                ip = self.ip_entry.get().strip()
                if ip:
                    self.generator.add_ip(ip)
                    messagebox.showinfo("Success", f"Added IP: {ip}")
                else:
                    messagebox.showerror("Error", "Please enter an IP address")
                    return
            
            elif input_type == "IP Range":
                start = self.start_ip.get().strip()
                end = self.end_ip.get().strip()
                if start and end:
                    self.generator.add_range(start, end)
                    messagebox.showinfo("Success", f"Added range: {start} - {end}")
                else:
                    messagebox.showerror("Error", "Please enter both start and end IP addresses")
                    return
            
            elif input_type == "CIDR":
                cidr = self.cidr_entry.get().strip()
                if cidr:
                    self.generator.add_cidr(cidr)
                    messagebox.showinfo("Success", f"Added CIDR: {cidr}")
                else:
                    messagebox.showerror("Error", "Please enter a CIDR notation")
                    return
            
            elif input_type == "Wildcard":
                ip = self.wildcard_ip.get().strip()
                wildcard = self.wildcard_mask.get().strip()
                if ip and wildcard:
                    self.generator.add_wildcard(ip, wildcard)
                    messagebox.showinfo("Success", f"Added wildcard pattern: {ip}/{wildcard}")
                else:
                    messagebox.showerror("Error", "Please enter both IP address and wildcard mask")
                    return
            
            elif input_type == "Gateway/Subnet":
                gateway = self.gateway_entry.get().strip()
                subnet = self.subnet_entry.get().strip()
                if gateway and subnet:
                    self.generator.add_gateway_subnet(gateway, subnet)
                    messagebox.showinfo("Success", f"Added gateway/subnet: {gateway}/{subnet}")
                else:
                    messagebox.showerror("Error", "Please enter both gateway and subnet mask")
                    return
            
            elif input_type in ["CSV File", "Excel File", "JSON File", "YAML File"]:
                if hasattr(self, 'file_full_path') and self.file_full_path:
                    if input_type == "CSV File":
                        new_generator = parse_csv(self.file_full_path)
                    elif input_type == "Excel File":
                        new_generator = parse_excel(self.file_full_path)
                    elif input_type == "JSON File":
                        new_generator = parse_json(self.file_full_path)
                    elif input_type == "YAML File":
                        new_generator = parse_yaml(self.file_full_path)
                    
                    # Merge the generators
                    self.generator = new_generator
                    messagebox.showinfo("Success", f"Loaded file: {self.file_path.get()}")
                else:
                    messagebox.showerror("Error", "Please select a file first")
                    return
            
            # Update IP count and status
            self.count_ips()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def count_ips(self):
        """Count IPs in the generator and update status."""
        # This could be slow for large generators, consider using a background thread
        ip_count = sum(1 for _ in self.generator.generate())
        self.ip_count = ip_count
        self.status_var.set(f"Ready - {ip_count} IPs loaded")
        
        # Show preview
        self.preview_ips()
    
    def clear_generator(self):
        """Clear all IP addresses from the generator."""
        self.generator = IPGenerator()
        self.ip_count = 0
        self.status_var.set("Ready - 0 IPs loaded")
        self.preview_text.delete(1.0, tk.END)
        messagebox.showinfo("Success", "Generator cleared")
    
    def preview_ips(self):
        """Show preview of generated IPs."""
        self.preview_text.delete(1.0, tk.END)
        count = 0
        
        for ip in self.generator.generate():
            if count >= 100:
                self.preview_text.insert(tk.END, "...\n")
                self.preview_text.insert(tk.END, f"(Showing 100 of {self.ip_count} IPs)")
                break
            self.preview_text.insert(tk.END, f"{ip}\n")
            count += 1
    
    def generate_output(self):
        """Generate output based on selected output type."""
        try:
            output_type = self.output_type.get()
            
            if output_type == "Preview":
                self.preview_ips()
                return
            
            filetypes = {
                "CSV File": [("CSV files", "*.csv")],
                "Excel File": [("Excel files", "*.xlsx")],
                "JSON File": [("JSON files", "*.json")],
                "YAML File": [("YAML files", "*.yaml")]
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=filetypes[output_type][0][1].split('*')[1],
                filetypes=filetypes[output_type]
            )
            
            if filename:
                if output_type == "CSV File":
                    self.generator.to_csv(filename)
                elif output_type == "Excel File":
                    self.generator.to_excel(filename)
                elif output_type == "JSON File":
                    self.generator.to_json(filename)
                elif output_type == "YAML File":
                    self.generator.to_yaml(filename)
                messagebox.showinfo("Success", f"Saved output to: {os.path.basename(filename)}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    """Start the GUI application."""
    root = tk.Tk()
    app = IPGenGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 