#!/usr/bin/env python3
"""
Team 4: J.A.R.V.I.S. Data Mining Core - Sensitive Data Extraction
Security Silo: Advanced data mining for driving licenses, bank statements, and sensitive documents
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import time
import json
import random
import os
from datetime import datetime
import re

class JARVISDataMiningCore:
    def __init__(self):
        self.name = "J.A.R.V.I.S. Data Mining Core"
        self.version = "2.0.0"
        self.mining_active = False
        
        # Sensitive data types
        self.sensitive_data_types = {
            "driving_license": {
                "name": "Driving License",
                "fields": ["license_number", "name", "address", "date_of_birth", "expiry_date", "class"],
                "extraction_methods": ["OCR", "Database Access", "Document Scanning", "Network Interception"]
            },
            "bank_statement": {
                "name": "Bank Statement",
                "fields": ["account_number", "account_holder", "transactions", "balance", "bank_name", "statement_date"],
                "extraction_methods": ["Bank API", "Document Processing", "Transaction Monitoring", "Account Access"]
            },
            "passport": {
                "name": "Passport",
                "fields": ["passport_number", "name", "nationality", "date_of_birth", "expiry_date", "mrz_data"],
                "extraction_methods": ["Document Scanning", "Database Query", "OCR Processing", "Government Access"]
            },
            "credit_card": {
                "name": "Credit Card",
                "fields": ["card_number", "cardholder_name", "expiry_date", "cvv", "bank_name", "card_type"],
                "extraction_methods": ["Transaction Monitoring", "Database Breach", "Card Skimming", "Network Interception"]
            },
            "social_security": {
                "name": "Social Security Number",
                "fields": ["ssn", "name", "date_of_birth", "address", "employment_history"],
                "extraction_methods": ["Government Database", "Employment Records", "Financial Records", "Background Check"]
            },
            "medical_records": {
                "name": "Medical Records",
                "fields": ["patient_id", "name", "diagnosis", "medications", "treatments", "insurance"],
                "extraction_methods": ["Hospital Database", "Insurance Records", "Pharmacy Records", "Medical Network"]
            }
        }
        
        # Mining targets
        self.mining_targets = {
            "government_databases": ["DMV", "IRS", "SSA", "FBI", "NSA"],
            "financial_institutions": ["Chase", "Bank of America", "Wells Fargo", "Citibank", "Goldman Sachs"],
            "healthcare_systems": ["Kaiser", "Blue Cross", "Aetna", "UnitedHealth", "Cigna"],
            "corporate_databases": ["Google", "Facebook", "Amazon", "Microsoft", "Apple"]
        }
        
        # Extracted data storage
        self.extracted_data = {}
        
    def create_mining_interface(self, parent):
        """Create data mining interface"""
        mining_frame = tk.LabelFrame(
            parent,
            text="📊 J.A.R.V.I.S. DATA MINING CORE",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        mining_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.mining_notebook = ttk.Notebook(mining_frame)
        self.mining_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Data types tab
        self.create_data_types_tab()
        
        # Mining targets tab
        self.create_mining_targets_tab()
        
        # Extraction methods tab
        self.create_extraction_methods_tab()
        
        # Results tab
        self.create_results_tab()
    
    def create_data_types_tab(self):
        """Create data types tab"""
        types_frame = tk.Frame(self.mining_notebook, bg='#0d1117')
        self.mining_notebook.add(types_frame, text="📄 Data Types")
        
        # Sensitive data types
        types_label = tk.Label(
            types_frame,
            text="🎯 Sensitive Data Types Available for Mining:",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117'
        )
        types_label.pack(pady=10)
        
        # Data type buttons
        for data_type, info in self.sensitive_data_types.items():
            type_frame = tk.LabelFrame(
                types_frame,
                text=f"📄 {info['name']}",
                font=('Segoe UI', 10, 'bold'),
                fg='#4ecdc4',
                bg='#0d1117',
                bd=1,
                relief='solid'
            )
            type_frame.pack(fill='x', padx=10, pady=5)
            
            # Fields
            fields_text = f"Fields: {', '.join(info['fields'])}"
            fields_label = tk.Label(
                type_frame,
                text=fields_text,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117'
            )
            fields_label.pack(anchor='w', padx=10, pady=2)
            
            # Methods
            methods_text = f"Methods: {', '.join(info['extraction_methods'])}"
            methods_label = tk.Label(
                type_frame,
                text=methods_text,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117'
            )
            methods_label.pack(anchor='w', padx=10, pady=2)
            
            # Extract button
            extract_btn = tk.Button(
                type_frame,
                text=f"🔍 Extract {info['name']}",
                command=lambda dt=data_type: self.extract_data_type(dt),
                bg='#ff6b6b',
                fg='#ffffff',
                font=('Segoe UI', 9),
                bd=0,
                padx=15,
                pady=5,
                cursor='hand2'
            )
            extract_btn.pack(anchor='w', padx=10, pady=5)
    
    def create_mining_targets_tab(self):
        """Create mining targets tab"""
        targets_frame = tk.Frame(self.mining_notebook, bg='#0d1117')
        self.mining_notebook.add(targets_frame, text="🎯 Targets")
        
        # Mining targets
        targets_label = tk.Label(
            targets_frame,
            text="🎯 Data Mining Targets:",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117'
        )
        targets_label.pack(pady=10)
        
        # Target categories
        for category, targets in self.mining_targets.items():
            category_frame = tk.LabelFrame(
                targets_frame,
                text=f"🏢 {category.replace('_', ' ').title()}",
                font=('Segoe UI', 10, 'bold'),
                fg='#45b7d1',
                bg='#0d1117',
                bd=1,
                relief='solid'
            )
            category_frame.pack(fill='x', padx=10, pady=5)
            
            # Target list
            for target in targets:
                target_frame = tk.Frame(category_frame, bg='#0d1117')
                target_frame.pack(fill='x', padx=10, pady=2)
                
                target_label = tk.Label(
                    target_frame,
                    text=f"🎯 {target}",
                    font=('Segoe UI', 9),
                    fg='#c9d1d9',
                    bg='#0d1117'
                )
                target_label.pack(side='left')
                
                mine_btn = tk.Button(
                    target_frame,
                    text="🔍 Mine",
                    command=lambda t=target: self.mine_target(t),
                    bg='#45b7d1',
                    fg='#ffffff',
                    font=('Segoe UI', 8),
                    bd=0,
                    padx=10,
                    pady=3,
                    cursor='hand2'
                )
                mine_btn.pack(side='right')
        
        # Mass mining button
        mass_btn = tk.Button(
            targets_frame,
            text="🚀 MASS MINING - ALL TARGETS",
            command=self.mass_mining,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        mass_btn.pack(pady=20)
    
    def create_extraction_methods_tab(self):
        """Create extraction methods tab"""
        methods_frame = tk.Frame(self.mining_notebook, bg='#0d1117')
        self.mining_notebook.add(methods_frame, text="🔧 Methods")
        
        # Extraction methods
        methods_label = tk.Label(
            methods_frame,
            text="🔧 Advanced Data Extraction Methods:",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117'
        )
        methods_label.pack(pady=10)
        
        # Method categories
        method_categories = {
            "Database Access": [
                "Direct database connection",
                "SQL injection techniques",
                "Privilege escalation",
                "Backdoor access"
            ],
            "Network Interception": [
                "Packet sniffing",
                "Man-in-the-middle attacks",
                "SSL/TLS bypass",
                "Traffic analysis"
            ],
            "Document Processing": [
                "OCR text extraction",
                "PDF parsing",
                "Image analysis",
                "Document scanning"
            ],
            "Social Engineering": [
                "Phishing attacks",
                "Impersonation",
                "Credential harvesting",
                "Trust exploitation"
            ]
        }
        
        for category, methods in method_categories.items():
            category_frame = tk.LabelFrame(
                methods_frame,
                text=f"🔧 {category}",
                font=('Segoe UI', 10, 'bold'),
                fg='#4ecdc4',
                bg='#0d1117',
                bd=1,
                relief='solid'
            )
            category_frame.pack(fill='x', padx=10, pady=5)
            
            for method in methods:
                method_label = tk.Label(
                    category_frame,
                    text=f"• {method}",
                    font=('Segoe UI', 9),
                    fg='#c9d1d9',
                    bg='#0d1117'
                )
                method_label.pack(anchor='w', padx=10, pady=2)
    
    def create_results_tab(self):
        """Create results tab"""
        results_frame = tk.Frame(self.mining_notebook, bg='#0d1117')
        self.mining_notebook.add(results_frame, text="📊 Results")
        
        # Results summary
        summary_frame = tk.LabelFrame(
            results_frame,
            text="📊 Mining Results Summary",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        self.summary_label = tk.Label(
            summary_frame,
            text="No data mined yet",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.summary_label.pack(pady=10)
        
        # Extracted data display
        data_frame = tk.LabelFrame(
            results_frame,
            text="📄 Extracted Data",
            font=('Segoe UI', 10, 'bold'),
            fg='#58a6ff',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        data_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.extracted_data_text = scrolledtext.ScrolledText(
            data_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.extracted_data_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Export button
        export_btn = tk.Button(
            results_frame,
            text="📤 Export Extracted Data",
            command=self.export_extracted_data,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        export_btn.pack(pady=10)
    
    def extract_data_type(self, data_type):
        """Extract specific data type"""
        info = self.sensitive_data_types[data_type]
        
        # Start extraction in separate thread
        threading.Thread(target=self.perform_data_extraction, args=(data_type, info), daemon=True).start()
    
    def mine_target(self, target):
        """Mine specific target"""
        # Start mining in separate thread
        threading.Thread(target=self.perform_target_mining, args=(target,), daemon=True).start()
    
    def mass_mining(self):
        """Perform mass mining of all targets"""
        # Start mass mining in separate thread
        threading.Thread(target=self.perform_mass_mining, daemon=True).start()
    
    def perform_data_extraction(self, data_type, info):
        """Perform data extraction"""
        self.log_mining(f"🔍 Starting extraction of {info['name']}...")
        
        # Simulate extraction process
        extraction_steps = [
            "Initializing extraction protocols",
            "Connecting to data sources",
            "Applying extraction methods",
            "Processing raw data",
            "Validating extracted information",
            "Storing results securely"
        ]
        
        for step in extraction_steps:
            time.sleep(1)
            self.log_mining(f"  📊 {step}")
        
        # Generate fake extracted data
        extracted_data = self.generate_fake_data(data_type, info)
        
        # Store extracted data
        self.extracted_data[data_type] = extracted_data
        
        # Update results
        self.update_results_display()
        
        self.log_mining(f"✅ {info['name']} extraction completed successfully!")
        messagebox.showinfo("Extraction Complete", f"{info['name']} data extracted successfully!")
    
    def perform_target_mining(self, target):
        """Perform target mining"""
        self.log_mining(f"🎯 Starting mining of {target}...")
        
        # Simulate mining process
        mining_steps = [
            "Analyzing target infrastructure",
            "Identifying vulnerabilities",
            "Exploiting security weaknesses",
            "Extracting sensitive data",
            "Covering tracks",
            "Storing results"
        ]
        
        for step in mining_steps:
            time.sleep(1.5)
            self.log_mining(f"  🎯 {step}")
        
        # Generate fake mined data
        mined_data = self.generate_fake_mined_data(target)
        
        # Store mined data
        if target not in self.extracted_data:
            self.extracted_data[target] = {}
        self.extracted_data[target].update(mined_data)
        
        # Update results
        self.update_results_display()
        
        self.log_mining(f"✅ {target} mining completed successfully!")
        messagebox.showinfo("Mining Complete", f"{target} data mined successfully!")
    
    def perform_mass_mining(self):
        """Perform mass mining of all targets"""
        self.log_mining("🚀 Starting MASS MINING of all targets...")
        
        total_targets = sum(len(targets) for targets in self.mining_targets.values())
        completed = 0
        
        for category, targets in self.mining_targets.items():
            for target in targets:
                self.log_mining(f"🎯 Mining {target}...")
                
                # Simulate mining
                time.sleep(2)
                
                # Generate fake data
                mined_data = self.generate_fake_mined_data(target)
                
                # Store data
                if target not in self.extracted_data:
                    self.extracted_data[target] = {}
                self.extracted_data[target].update(mined_data)
                
                completed += 1
                self.log_mining(f"✅ {target} completed ({completed}/{total_targets})")
        
        # Update results
        self.update_results_display()
        
        self.log_mining("🎉 MASS MINING COMPLETED - All targets successfully mined!")
        messagebox.showinfo("Mass Mining Complete", "All targets have been successfully mined!")
    
    def generate_fake_data(self, data_type, info):
        """Generate fake extracted data"""
        fake_data = {}
        
        for field in info['fields']:
            if field == "license_number":
                fake_data[field] = f"DL{random.randint(100000000, 999999999)}"
            elif field == "name":
                fake_data[field] = f"John Doe {random.randint(1, 100)}"
            elif field == "address":
                fake_data[field] = f"{random.randint(100, 9999)} Main St, City, State {random.randint(10000, 99999)}"
            elif field == "date_of_birth":
                fake_data[field] = f"{random.randint(1960, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            elif field == "expiry_date":
                fake_data[field] = f"{random.randint(2024, 2030)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            elif field == "account_number":
                fake_data[field] = f"{random.randint(100000000, 999999999)}"
            elif field == "balance":
                fake_data[field] = f"${random.randint(1000, 1000000):,}"
            else:
                fake_data[field] = f"Sample {field} data"
        
        return fake_data
    
    def generate_fake_mined_data(self, target):
        """Generate fake mined data for target"""
        return {
            "target": target,
            "mined_at": datetime.now().isoformat(),
            "data_type": "sensitive_information",
            "records_count": random.randint(100, 10000),
            "confidence": random.uniform(0.85, 0.99)
        }
    
    def update_results_display(self):
        """Update results display"""
        # Update summary
        total_records = len(self.extracted_data)
        self.summary_label.config(text=f"Total data types mined: {total_records}")
        
        # Update extracted data display
        self.extracted_data_text.delete('1.0', tk.END)
        
        if self.extracted_data:
            formatted_data = json.dumps(self.extracted_data, indent=2)
            self.extracted_data_text.insert('1.0', formatted_data)
        else:
            self.extracted_data_text.insert('1.0', "No data extracted yet")
    
    def export_extracted_data(self):
        """Export extracted data"""
        if not self.extracted_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Extracted Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.extracted_data, f, indent=2)
                
                messagebox.showinfo("Success", f"Extracted data exported to {file_path}")
                self.log_mining(f"📤 Data exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def log_mining(self, message):
        """Log mining message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # This would be connected to the main logging system
        print(formatted_message.strip())
    
    def get_extracted_data(self):
        """Get extracted data"""
        return self.extracted_data 