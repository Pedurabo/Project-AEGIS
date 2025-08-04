#!/usr/bin/env python3
"""
Team 2: Data Science & Analytics - Input/Output Data Processing
Developmental Silo: Data processing, validation, visualization, and analytics
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import threading
import os

class AEGISDataProcessor:
    def __init__(self):
        self.name = "AEGIS Data Processor"
        self.version = "1.0.0"
        self.data_sources = {}
        self.processed_data = {}
        self.analytics_results = {}
        
        # Data validation rules
        self.validation_rules = {
            "ip_address": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "url": r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$",
            "port": r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        }
        
    def create_data_interface(self, parent):
        """Create data processing interface"""
        data_frame = tk.LabelFrame(
            parent,
            text="📊 DATA PROCESSING & ANALYTICS",
            font=('Segoe UI', 12, 'bold'),
            fg='#58a6ff',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        data_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(data_frame)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Input tab
        self.create_input_tab()
        
        # Processing tab
        self.create_processing_tab()
        
        # Analytics tab
        self.create_analytics_tab()
        
        # Output tab
        self.create_output_tab()
    
    def create_input_tab(self):
        """Create data input tab"""
        input_frame = tk.Frame(self.notebook, bg='#0d1117')
        self.notebook.add(input_frame, text="📥 Input")
        
        # File input section
        file_frame = tk.LabelFrame(
            input_frame,
            text="📁 File Input",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        file_frame.pack(fill='x', padx=10, pady=5)
        
        # File selection
        file_select_frame = tk.Frame(file_frame, bg='#0d1117')
        file_select_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            file_select_frame,
            text="Select Data File:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            file_select_frame,
            textvariable=self.file_path_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        file_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        browse_btn = tk.Button(
            file_select_frame,
            text="Browse",
            command=self.browse_file,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=3,
            cursor='hand2'
        )
        browse_btn.pack(side='right')
        
        # Manual input section
        manual_frame = tk.LabelFrame(
            input_frame,
            text="✏️ Manual Input",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        manual_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Input type selection
        type_frame = tk.Frame(manual_frame, bg='#0d1117')
        type_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            type_frame,
            text="Data Type:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.data_type_var = tk.StringVar(value="target_list")
        data_types = [
            ("Target List", "target_list"),
            ("Vulnerability Data", "vulnerability_data"),
            ("Network Scan Results", "network_scan"),
            ("Banking Data", "banking_data"),
            ("Social Media Data", "social_media")
        ]
        
        for text, value in data_types:
            tk.Radiobutton(
                type_frame,
                text=text,
                variable=self.data_type_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Data input area
        input_area_frame = tk.Frame(manual_frame, bg='#0d1117')
        input_area_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Label(
            input_area_frame,
            text="Enter Data (JSON, CSV, or plain text):",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(anchor='w')
        
        self.data_input = scrolledtext.ScrolledText(
            input_area_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD,
            height=10
        )
        self.data_input.pack(fill='both', expand=True, pady=5)
        
        # Process button
        process_btn = tk.Button(
            input_frame,
            text="Process Input Data",
            command=self.process_input_data,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        process_btn.pack(pady=10)
    
    def create_processing_tab(self):
        """Create data processing tab"""
        processing_frame = tk.Frame(self.notebook, bg='#0d1117')
        self.notebook.add(processing_frame, text="⚙️ Processing")
        
        # Processing options
        options_frame = tk.LabelFrame(
            processing_frame,
            text="🔧 Processing Options",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Validation options
        validation_frame = tk.Frame(options_frame, bg='#0d1117')
        validation_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            validation_frame,
            text="Data Validation:",
            font=('Segoe UI', 9, 'bold'),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(anchor='w')
        
        self.validate_data_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            validation_frame,
            text="Enable data validation",
            variable=self.validate_data_var,
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117',
            selectcolor='#21262d'
        ).pack(anchor='w')
        
        # Cleaning options
        cleaning_frame = tk.Frame(options_frame, bg='#0d1117')
        cleaning_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            cleaning_frame,
            text="Data Cleaning:",
            font=('Segoe UI', 9, 'bold'),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(anchor='w')
        
        self.clean_data_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            cleaning_frame,
            text="Remove duplicates",
            variable=self.clean_data_var,
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117',
            selectcolor='#21262d'
        ).pack(anchor='w')
        
        # Processing log
        log_frame = tk.LabelFrame(
            processing_frame,
            text="📝 Processing Log",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.processing_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.processing_log.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        analytics_frame = tk.Frame(self.notebook, bg='#0d1117')
        self.notebook.add(analytics_frame, text="📈 Analytics")
        
        # Analytics controls
        controls_frame = tk.LabelFrame(
            analytics_frame,
            text="🎛️ Analytics Controls",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        # Analysis type
        analysis_frame = tk.Frame(controls_frame, bg='#0d1117')
        analysis_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            analysis_frame,
            text="Analysis Type:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.analysis_type_var = tk.StringVar(value="statistical")
        analysis_types = [
            ("Statistical", "statistical"),
            ("Trend Analysis", "trend"),
            ("Pattern Recognition", "pattern"),
            ("Risk Assessment", "risk"),
            ("Predictive", "predictive")
        ]
        
        for text, value in analysis_types:
            tk.Radiobutton(
                analysis_frame,
                text=text,
                variable=self.analysis_type_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Run analysis button
        analyze_btn = tk.Button(
            controls_frame,
            text="Run Analysis",
            command=self.run_analytics,
            bg='#45b7d1',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        analyze_btn.pack(pady=10)
        
        # Results display
        results_frame = tk.LabelFrame(
            analytics_frame,
            text="📊 Analysis Results",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.analytics_results_text = scrolledtext.ScrolledText(
            results_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.analytics_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_output_tab(self):
        """Create output tab"""
        output_frame = tk.Frame(self.notebook, bg='#0d1117')
        self.notebook.add(output_frame, text="📤 Output")
        
        # Output options
        options_frame = tk.LabelFrame(
            output_frame,
            text="📋 Output Options",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Output format
        format_frame = tk.Frame(options_frame, bg='#0d1117')
        format_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            format_frame,
            text="Output Format:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.output_format_var = tk.StringVar(value="json")
        output_formats = [
            ("JSON", "json"),
            ("CSV", "csv"),
            ("XML", "xml"),
            ("TXT", "txt"),
            ("PDF", "pdf")
        ]
        
        for text, value in output_formats:
            tk.Radiobutton(
                format_frame,
                text=text,
                variable=self.output_format_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Export button
        export_btn = tk.Button(
            options_frame,
            text="Export Data",
            command=self.export_data,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        export_btn.pack(pady=10)
        
        # Output preview
        preview_frame = tk.LabelFrame(
            output_frame,
            text="👁️ Output Preview",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.output_preview = scrolledtext.ScrolledText(
            preview_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.output_preview.pack(fill='both', expand=True, padx=5, pady=5)
    
    def browse_file(self):
        """Browse for input file"""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[
                ("All files", "*.*"),
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def process_input_data(self):
        """Process input data"""
        self.log_message("Starting data processing...")
        
        # Get data from file or manual input
        if self.file_path_var.get():
            data = self.load_file_data()
        else:
            data = self.data_input.get('1.0', tk.END).strip()
        
        if not data:
            messagebox.showerror("Error", "No data to process!")
            return
        
        # Process data based on type
        data_type = self.data_type_var.get()
        processed_data = self.process_data_by_type(data, data_type)
        
        # Store processed data
        self.processed_data[data_type] = processed_data
        
        self.log_message(f"Data processing completed for {data_type}")
        self.update_output_preview(processed_data)
    
    def load_file_data(self):
        """Load data from file"""
        try:
            file_path = self.file_path_var.get()
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            self.log_message(f"Error loading file: {str(e)}")
            return None
    
    def process_data_by_type(self, data, data_type):
        """Process data based on type"""
        try:
            if data_type == "target_list":
                return self.process_target_list(data)
            elif data_type == "vulnerability_data":
                return self.process_vulnerability_data(data)
            elif data_type == "network_scan":
                return self.process_network_scan(data)
            elif data_type == "banking_data":
                return self.process_banking_data(data)
            elif data_type == "social_media":
                return self.process_social_media_data(data)
            else:
                return {"raw_data": data, "type": data_type}
        except Exception as e:
            self.log_message(f"Error processing {data_type}: {str(e)}")
            return {"error": str(e), "type": data_type}
    
    def process_target_list(self, data):
        """Process target list data"""
        targets = []
        lines = data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line:
                target = {
                    "ip": line,
                    "status": "pending",
                    "added": datetime.now().isoformat()
                }
                targets.append(target)
        
        return {
            "type": "target_list",
            "count": len(targets),
            "targets": targets,
            "processed": datetime.now().isoformat()
        }
    
    def process_vulnerability_data(self, data):
        """Process vulnerability data"""
        try:
            if data.startswith('{'):
                vuln_data = json.loads(data)
            else:
                vuln_data = {"raw": data}
            
            return {
                "type": "vulnerability_data",
                "data": vuln_data,
                "processed": datetime.now().isoformat()
            }
        except:
            return {
                "type": "vulnerability_data",
                "raw_data": data,
                "processed": datetime.now().isoformat()
            }
    
    def process_network_scan(self, data):
        """Process network scan data"""
        scan_results = []
        lines = data.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    scan_results.append({
                        "host": parts[0].strip(),
                        "port": parts[1].strip(),
                        "status": "open" if len(parts) > 2 else "unknown"
                    })
        
        return {
            "type": "network_scan",
            "hosts": len(set(r["host"] for r in scan_results)),
            "ports": len(scan_results),
            "results": scan_results,
            "processed": datetime.now().isoformat()
        }
    
    def process_banking_data(self, data):
        """Process banking data"""
        try:
            if data.startswith('{'):
                bank_data = json.loads(data)
            else:
                bank_data = {"raw": data}
            
            return {
                "type": "banking_data",
                "data": bank_data,
                "processed": datetime.now().isoformat()
            }
        except:
            return {
                "type": "banking_data",
                "raw_data": data,
                "processed": datetime.now().isoformat()
            }
    
    def process_social_media_data(self, data):
        """Process social media data"""
        social_data = []
        lines = data.strip().split('\n')
        
        for line in lines:
            if line.strip():
                social_data.append({
                    "platform": "unknown",
                    "data": line.strip(),
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "type": "social_media",
            "entries": len(social_data),
            "data": social_data,
            "processed": datetime.now().isoformat()
        }
    
    def run_analytics(self):
        """Run analytics on processed data"""
        self.log_message("Starting analytics...")
        
        analysis_type = self.analysis_type_var.get()
        
        if not self.processed_data:
            messagebox.showwarning("Warning", "No processed data available for analysis!")
            return
        
        # Run analysis based on type
        if analysis_type == "statistical":
            results = self.run_statistical_analysis()
        elif analysis_type == "trend":
            results = self.run_trend_analysis()
        elif analysis_type == "pattern":
            results = self.run_pattern_analysis()
        elif analysis_type == "risk":
            results = self.run_risk_analysis()
        elif analysis_type == "predictive":
            results = self.run_predictive_analysis()
        
        # Store and display results
        self.analytics_results[analysis_type] = results
        self.display_analytics_results(results)
        
        self.log_message(f"Analytics completed: {analysis_type}")
    
    def run_statistical_analysis(self):
        """Run statistical analysis"""
        stats = {}
        
        for data_type, data in self.processed_data.items():
            if data_type == "target_list":
                stats["total_targets"] = data.get("count", 0)
            elif data_type == "network_scan":
                stats["total_hosts"] = data.get("hosts", 0)
                stats["total_ports"] = data.get("ports", 0)
            elif data_type == "social_media":
                stats["social_entries"] = data.get("entries", 0)
        
        return {
            "type": "statistical",
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        }
    
    def run_trend_analysis(self):
        """Run trend analysis"""
        return {
            "type": "trend",
            "timestamp": datetime.now().isoformat(),
            "trends": {
                "target_growth": "increasing",
                "vulnerability_trend": "stable",
                "network_activity": "high"
            }
        }
    
    def run_pattern_analysis(self):
        """Run pattern analysis"""
        return {
            "type": "pattern",
            "timestamp": datetime.now().isoformat(),
            "patterns": {
                "common_ports": [80, 443, 22, 21],
                "target_distribution": "clustered",
                "vulnerability_patterns": "recurring"
            }
        }
    
    def run_risk_analysis(self):
        """Run risk analysis"""
        return {
            "type": "risk",
            "timestamp": datetime.now().isoformat(),
            "risk_assessment": {
                "overall_risk": "medium",
                "high_risk_targets": 5,
                "critical_vulnerabilities": 2,
                "recommendations": [
                    "Implement additional security measures",
                    "Monitor high-risk targets closely",
                    "Update vulnerable systems"
                ]
            }
        }
    
    def run_predictive_analysis(self):
        """Run predictive analysis"""
        return {
            "type": "predictive",
            "timestamp": datetime.now().isoformat(),
            "predictions": {
                "next_target": "192.168.1.100",
                "vulnerability_probability": 0.75,
                "attack_timeline": "within 24 hours",
                "confidence": 0.85
            }
        }
    
    def display_analytics_results(self, results):
        """Display analytics results"""
        self.analytics_results_text.delete('1.0', tk.END)
        
        formatted_results = json.dumps(results, indent=2)
        self.analytics_results_text.insert('1.0', formatted_results)
    
    def export_data(self):
        """Export processed data"""
        if not self.processed_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=f".{self.output_format_var.get()}",
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt")
            ]
        )
        
        if file_path:
            try:
                export_format = self.output_format_var.get()
                
                if export_format == "json":
                    with open(file_path, 'w') as f:
                        json.dump(self.processed_data, f, indent=2)
                elif export_format == "csv":
                    self.export_to_csv(file_path)
                else:
                    with open(file_path, 'w') as f:
                        f.write(str(self.processed_data))
                
                messagebox.showinfo("Success", f"Data exported to {file_path}")
                self.log_message(f"Data exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
                self.log_message(f"Export error: {str(e)}")
    
    def export_to_csv(self, file_path):
        """Export data to CSV format"""
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            for data_type, data in self.processed_data.items():
                writer.writerow([f"Data Type: {data_type}"])
                writer.writerow([])
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        writer.writerow([key, str(value)])
                else:
                    writer.writerow([str(data)])
                
                writer.writerow([])
    
    def update_output_preview(self, data):
        """Update output preview"""
        self.output_preview.delete('1.0', tk.END)
        
        formatted_data = json.dumps(data, indent=2)
        self.output_preview.insert('1.0', formatted_data)
    
    def log_message(self, message):
        """Log message to processing log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.processing_log.insert(tk.END, formatted_message)
        self.processing_log.see(tk.END)
    
    def get_processed_data(self):
        """Get processed data"""
        return self.processed_data
    
    def get_analytics_results(self):
        """Get analytics results"""
        return self.analytics_results 