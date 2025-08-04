#!/usr/bin/env python3
"""
Team 5: Penetration Testing Core - Banking Operations Engine
Security Silo: Banking system access, transaction monitoring, and account manipulation
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import json
import random
from datetime import datetime, timedelta
import socket
import hashlib

class AEGISBankingOperations:
    def __init__(self):
        self.name = "AEGIS Banking Operations"
        self.version = "1.0.0"
        self.banking_targets = {}
        self.account_data = {}
        self.transactions = {}
        self.swift_operations = {}
        self.social_media_data = {}
        
        # Banking systems database
        self.banking_systems = {
            "swift": {
                "name": "SWIFT Network",
                "description": "Society for Worldwide Interbank Financial Telecommunication",
                "access_level": "Critical",
                "vulnerabilities": ["Message manipulation", "Network infiltration", "Transaction interception"]
            },
            "federal_reserve": {
                "name": "Federal Reserve System",
                "description": "Central banking system of the United States",
                "access_level": "Ultra-Critical",
                "vulnerabilities": ["System compromise", "Data exfiltration", "Control manipulation"]
            },
            "core_banking": {
                "name": "Core Banking Systems",
                "description": "Primary banking infrastructure",
                "access_level": "High",
                "vulnerabilities": ["Account takeover", "Transaction fraud", "Data breach"]
            },
            "atm_networks": {
                "name": "ATM Networks",
                "description": "Automated Teller Machine networks",
                "access_level": "Medium",
                "vulnerabilities": ["Card skimming", "Network attacks", "Cash extraction"]
            }
        }
        
        # Account manipulation techniques
        self.account_techniques = {
            "balance_manipulation": {
                "name": "Balance Manipulation",
                "description": "Modify account balances",
                "success_rate": 0.75,
                "detection_risk": "High"
            },
            "transaction_injection": {
                "name": "Transaction Injection",
                "description": "Inject fake transactions",
                "success_rate": 0.60,
                "detection_risk": "Medium"
            },
            "account_creation": {
                "name": "Account Creation",
                "description": "Create fake accounts",
                "success_rate": 0.85,
                "detection_risk": "Low"
            },
            "privilege_escalation": {
                "name": "Privilege Escalation",
                "description": "Elevate account privileges",
                "success_rate": 0.45,
                "detection_risk": "High"
            }
        }
        
        # Social media platforms
        self.social_platforms = [
            "Facebook", "Twitter", "Instagram", "LinkedIn", 
            "TikTok", "YouTube", "Reddit", "Telegram"
        ]
        
        # Phishing techniques
        self.phishing_techniques = {
            "spear_phishing": {
                "name": "Spear Phishing",
                "description": "Targeted phishing attacks",
                "success_rate": 0.90,
                "sophistication": "High"
            },
            "whaling": {
                "name": "Whaling",
                "description": "CEO/executive targeting",
                "success_rate": 0.85,
                "sophistication": "Very High"
            },
            "vishing": {
                "name": "Vishing",
                "description": "Voice phishing attacks",
                "success_rate": 0.80,
                "sophistication": "Medium"
            },
            "smishing": {
                "name": "Smishing",
                "description": "SMS phishing attacks",
                "success_rate": 0.75,
                "sophistication": "Medium"
            }
        }
    
    def create_banking_interface(self, parent):
        """Create banking operations interface"""
        banking_frame = tk.LabelFrame(
            parent,
            text="🏦 BANKING OPERATIONS ENGINE",
            font=('Segoe UI', 12, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        banking_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.banking_notebook = ttk.Notebook(banking_frame)
        self.banking_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Banking systems tab
        self.create_banking_systems_tab()
        
        # Account manipulation tab
        self.create_account_manipulation_tab()
        
        # Transaction monitoring tab
        self.create_transaction_monitoring_tab()
        
        # SWIFT operations tab
        self.create_swift_operations_tab()
        
        # Social media intelligence tab
        self.create_social_media_tab()
        
        # Phishing operations tab
        self.create_phishing_operations_tab()
    
    def create_banking_systems_tab(self):
        """Create banking systems tab"""
        systems_frame = tk.Frame(self.banking_notebook, bg='#0d1117')
        self.banking_notebook.add(systems_frame, text="🏦 Banking Systems")
        
        # Systems overview
        overview_frame = tk.LabelFrame(
            systems_frame,
            text="📊 Banking Systems Overview",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        overview_frame.pack(fill='x', padx=10, pady=5)
        
        # Systems treeview
        columns = ('System', 'Access Level', 'Status', 'Vulnerabilities')
        self.systems_tree = ttk.Treeview(
            overview_frame,
            columns=columns,
            show='headings',
            height=8
        )
        
        for col in columns:
            self.systems_tree.heading(col, text=col)
            self.systems_tree.column(col, width=150)
        
        self.systems_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate systems
        for system_id, system_info in self.banking_systems.items():
            vuln_count = len(system_info['vulnerabilities'])
            self.systems_tree.insert('', 'end', values=(
                system_info['name'],
                system_info['access_level'],
                "Targeted",
                f"{vuln_count} vulnerabilities"
            ))
        
        # System actions
        actions_frame = tk.Frame(systems_frame, bg='#0d1117')
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        access_btn = tk.Button(
            actions_frame,
            text="Access System",
            command=self.access_banking_system,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        access_btn.pack(side='left', padx=5)
        
        scan_btn = tk.Button(
            actions_frame,
            text="Scan Vulnerabilities",
            command=self.scan_banking_vulnerabilities,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        scan_btn.pack(side='left', padx=5)
        
        # System details
        details_frame = tk.LabelFrame(
            systems_frame,
            text="📋 System Details",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        details_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.system_details = scrolledtext.ScrolledText(
            details_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.system_details.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bind system selection
        self.systems_tree.bind('<<TreeviewSelect>>', self.on_system_select)
    
    def create_account_manipulation_tab(self):
        """Create account manipulation tab"""
        account_frame = tk.Frame(self.banking_notebook, bg='#0d1117')
        self.banking_notebook.add(account_frame, text="💳 Account Manipulation")
        
        # Account input
        input_frame = tk.LabelFrame(
            account_frame,
            text="📝 Account Information",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Account number
        acc_frame = tk.Frame(input_frame, bg='#0d1117')
        acc_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            acc_frame,
            text="Account Number:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.account_number_var = tk.StringVar()
        acc_entry = tk.Entry(
            acc_frame,
            textvariable=self.account_number_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        acc_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        # Bank selection
        bank_frame = tk.Frame(input_frame, bg='#0d1117')
        bank_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            bank_frame,
            text="Bank:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.bank_var = tk.StringVar(value="swift")
        banks = [
            ("SWIFT Network", "swift"),
            ("Federal Reserve", "federal_reserve"),
            ("Core Banking", "core_banking"),
            ("ATM Network", "atm_networks")
        ]
        
        for text, value in banks:
            tk.Radiobutton(
                bank_frame,
                text=text,
                variable=self.bank_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Manipulation techniques
        techniques_frame = tk.LabelFrame(
            account_frame,
            text="🔧 Manipulation Techniques",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        techniques_frame.pack(fill='x', padx=10, pady=5)
        
        # Techniques listbox
        self.techniques_listbox = tk.Listbox(
            techniques_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            height=6
        )
        self.techniques_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate techniques
        for technique_id, technique_info in self.account_techniques.items():
            self.techniques_listbox.insert(tk.END, f"{technique_info['name']} - {technique_info['description']}")
        
        # Execute button
        execute_btn = tk.Button(
            techniques_frame,
            text="Execute Manipulation",
            command=self.execute_account_manipulation,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        execute_btn.pack(pady=10)
        
        # Results
        results_frame = tk.LabelFrame(
            account_frame,
            text="📊 Manipulation Results",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.manipulation_results = scrolledtext.ScrolledText(
            results_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.manipulation_results.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_transaction_monitoring_tab(self):
        """Create transaction monitoring tab"""
        monitoring_frame = tk.Frame(self.banking_notebook, bg='#0d1117')
        self.banking_notebook.add(monitoring_frame, text="📊 Transaction Monitoring")
        
        # Monitoring controls
        controls_frame = tk.LabelFrame(
            monitoring_frame,
            text="🎛️ Monitoring Controls",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        # Start monitoring button
        start_btn = tk.Button(
            controls_frame,
            text="Start Transaction Monitoring",
            command=self.start_transaction_monitoring,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        start_btn.pack(pady=10)
        
        # Monitoring status
        status_frame = tk.LabelFrame(
            monitoring_frame,
            text="📈 Monitoring Status",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.monitoring_status_label = tk.Label(
            status_frame,
            text="Status: Not Monitoring",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.monitoring_status_label.pack(pady=5)
        
        # Transaction log
        log_frame = tk.LabelFrame(
            monitoring_frame,
            text="📋 Transaction Log",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Transaction treeview
        columns = ('Time', 'Account', 'Type', 'Amount', 'Status')
        self.transaction_tree = ttk.Treeview(
            log_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=120)
        
        self.transaction_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Monitoring log
        self.monitoring_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=6
        )
        self.monitoring_log.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_swift_operations_tab(self):
        """Create SWIFT operations tab"""
        swift_frame = tk.Frame(self.banking_notebook, bg='#0d1117')
        self.banking_notebook.add(swift_frame, text="🌐 SWIFT Operations")
        
        # SWIFT message creation
        message_frame = tk.LabelFrame(
            swift_frame,
            text="📨 SWIFT Message Creation",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        message_frame.pack(fill='x', padx=10, pady=5)
        
        # Message type
        type_frame = tk.Frame(message_frame, bg='#0d1117')
        type_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            type_frame,
            text="Message Type:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.swift_type_var = tk.StringVar(value="MT103")
        swift_types = [
            ("MT103 - Single Customer Credit Transfer", "MT103"),
            ("MT202 - General Financial Institution Transfer", "MT202"),
            ("MT300 - Foreign Exchange Confirmation", "MT300"),
            ("MT400 - Advice of Payment", "MT400")
        ]
        
        for text, value in swift_types:
            tk.Radiobutton(
                type_frame,
                text=text,
                variable=self.swift_type_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(anchor='w', padx=10, pady=2)
        
        # Message details
        details_frame = tk.Frame(message_frame, bg='#0d1117')
        details_frame.pack(fill='x', padx=10, pady=5)
        
        # Sender
        sender_frame = tk.Frame(details_frame, bg='#0d1117')
        sender_frame.pack(fill='x', pady=2)
        
        tk.Label(
            sender_frame,
            text="Sender BIC:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.sender_bic_var = tk.StringVar()
        sender_entry = tk.Entry(
            sender_frame,
            textvariable=self.sender_bic_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        sender_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Receiver
        receiver_frame = tk.Frame(details_frame, bg='#0d1117')
        receiver_frame.pack(fill='x', pady=2)
        
        tk.Label(
            receiver_frame,
            text="Receiver BIC:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.receiver_bic_var = tk.StringVar()
        receiver_entry = tk.Entry(
            receiver_frame,
            textvariable=self.receiver_bic_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        receiver_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Amount
        amount_frame = tk.Frame(details_frame, bg='#0d1117')
        amount_frame.pack(fill='x', pady=2)
        
        tk.Label(
            amount_frame,
            text="Amount:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.swift_amount_var = tk.StringVar()
        amount_entry = tk.Entry(
            amount_frame,
            textvariable=self.swift_amount_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        amount_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Send button
        send_btn = tk.Button(
            message_frame,
            text="Send SWIFT Message",
            command=self.send_swift_message,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        send_btn.pack(pady=10)
        
        # SWIFT operations log
        log_frame = tk.LabelFrame(
            swift_frame,
            text="📋 SWIFT Operations Log",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.swift_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.swift_log.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_social_media_tab(self):
        """Create social media intelligence tab"""
        social_frame = tk.Frame(self.banking_notebook, bg='#0d1117')
        self.banking_notebook.add(social_frame, text="📱 Social Media Intelligence")
        
        # Platform selection
        platform_frame = tk.LabelFrame(
            social_frame,
            text="📱 Social Media Platforms",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        platform_frame.pack(fill='x', padx=10, pady=5)
        
        # Platform buttons
        platform_buttons_frame = tk.Frame(platform_frame, bg='#0d1117')
        platform_buttons_frame.pack(fill='x', padx=10, pady=5)
        
        for platform in self.social_platforms:
            platform_btn = tk.Button(
                platform_buttons_frame,
                text=f"📱 {platform}",
                command=lambda p=platform: self.scan_social_media(p),
                bg='#21262d',
                fg='#c9d1d9',
                font=('Segoe UI', 9),
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2'
            )
            platform_btn.pack(side='left', padx=2)
        
        # Intelligence gathering
        intel_frame = tk.LabelFrame(
            social_frame,
            text="🔍 Intelligence Gathering",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        intel_frame.pack(fill='x', padx=10, pady=5)
        
        # Target input
        target_frame = tk.Frame(intel_frame, bg='#0d1117')
        target_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            target_frame,
            text="Target:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.social_target_var = tk.StringVar()
        target_entry = tk.Entry(
            target_frame,
            textvariable=self.social_target_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        target_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        gather_btn = tk.Button(
            target_frame,
            text="Gather Intelligence",
            command=self.gather_social_intelligence,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=3,
            cursor='hand2'
        )
        gather_btn.pack(side='right')
        
        # Intelligence results
        results_frame = tk.LabelFrame(
            social_frame,
            text="📊 Intelligence Results",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.social_results = scrolledtext.ScrolledText(
            results_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.social_results.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_phishing_operations_tab(self):
        """Create phishing operations tab"""
        phishing_frame = tk.Frame(self.banking_notebook, bg='#0d1117')
        self.banking_notebook.add(phishing_frame, text="🎣 Phishing Operations")
        
        # Phishing techniques
        techniques_frame = tk.LabelFrame(
            phishing_frame,
            text="🎣 Phishing Techniques",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        techniques_frame.pack(fill='x', padx=10, pady=5)
        
        # Techniques listbox
        self.phishing_listbox = tk.Listbox(
            techniques_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            height=6
        )
        self.phishing_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate techniques
        for technique_id, technique_info in self.phishing_techniques.items():
            self.phishing_listbox.insert(tk.END, f"{technique_info['name']} - {technique_info['description']}")
        
        # Target input
        target_frame = tk.Frame(phishing_frame, bg='#0d1117')
        target_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            target_frame,
            text="Target Email/Phone:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.phishing_target_var = tk.StringVar()
        target_entry = tk.Entry(
            target_frame,
            textvariable=self.phishing_target_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        target_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        # Execute button
        execute_btn = tk.Button(
            target_frame,
            text="Execute Phishing Attack",
            command=self.execute_phishing_attack,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        execute_btn.pack(side='right')
        
        # Phishing results
        results_frame = tk.LabelFrame(
            phishing_frame,
            text="📊 Phishing Results",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.phishing_results = scrolledtext.ScrolledText(
            results_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.phishing_results.pack(fill='both', expand=True, padx=5, pady=5)
    
    def on_system_select(self, event):
        """Handle system selection"""
        selection = self.systems_tree.selection()
        if selection:
            item = self.systems_tree.item(selection[0])
            system_name = item['values'][0]
            
            # Find system info
            for system_id, system_info in self.banking_systems.items():
                if system_info['name'] == system_name:
                    details = f"""
System: {system_info['name']}
Description: {system_info['description']}
Access Level: {system_info['access_level']}
Vulnerabilities:
"""
                    for vuln in system_info['vulnerabilities']:
                        details += f"  • {vuln}\n"
                    
                    self.system_details.delete('1.0', tk.END)
                    self.system_details.insert('1.0', details)
                    break
    
    def access_banking_system(self):
        """Access banking system"""
        selection = self.systems_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a banking system!")
            return
        
        item = self.systems_tree.item(selection[0])
        system_name = item['values'][0]
        
        # Simulate system access
        threading.Thread(target=self.perform_system_access, args=(system_name,), daemon=True).start()
    
    def perform_system_access(self, system_name):
        """Perform system access"""
        self.log_message(f"Attempting to access {system_name}...")
        time.sleep(2)
        
        # Simulate access success
        success = random.random() > 0.3  # 70% success rate
        
        if success:
            self.log_message(f"✅ Successfully accessed {system_name}")
            messagebox.showinfo("Success", f"Successfully accessed {system_name}")
        else:
            self.log_message(f"❌ Failed to access {system_name}")
            messagebox.showerror("Error", f"Failed to access {system_name}")
    
    def scan_banking_vulnerabilities(self):
        """Scan banking vulnerabilities"""
        selection = self.systems_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a banking system!")
            return
        
        item = self.systems_tree.item(selection[0])
        system_name = item['values'][0]
        
        # Simulate vulnerability scan
        threading.Thread(target=self.perform_vulnerability_scan, args=(system_name,), daemon=True).start()
    
    def perform_vulnerability_scan(self, system_name):
        """Perform vulnerability scan"""
        self.log_message(f"Scanning {system_name} for vulnerabilities...")
        
        # Find system info
        for system_id, system_info in self.banking_systems.items():
            if system_info['name'] == system_name:
                vulnerabilities = system_info['vulnerabilities']
                break
        
        for i, vuln in enumerate(vulnerabilities, 1):
            time.sleep(1)
            self.log_message(f"  {i}. Found vulnerability: {vuln}")
        
        self.log_message(f"✅ Vulnerability scan completed for {system_name}")
        messagebox.showinfo("Scan Complete", f"Found {len(vulnerabilities)} vulnerabilities in {system_name}")
    
    def execute_account_manipulation(self):
        """Execute account manipulation"""
        account = self.account_number_var.get().strip()
        if not account:
            messagebox.showwarning("Warning", "Please enter an account number!")
            return
        
        selection = self.techniques_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a manipulation technique!")
            return
        
        technique_index = selection[0]
        technique_id = list(self.account_techniques.keys())[technique_index]
        technique_info = self.account_techniques[technique_id]
        
        # Execute manipulation
        threading.Thread(target=self.perform_manipulation, args=(account, technique_id, technique_info), daemon=True).start()
    
    def perform_manipulation(self, account, technique_id, technique_info):
        """Perform account manipulation"""
        self.log_manipulation(f"Executing {technique_info['name']} on account {account}...")
        
        # Simulate manipulation
        time.sleep(technique_info['execution_time'])
        
        # Determine success
        success = random.random() < technique_info['success_rate']
        
        if success:
            result = f"✅ {technique_info['name']} executed successfully on account {account}"
            self.log_manipulation(result)
            messagebox.showinfo("Success", f"{technique_info['name']} executed successfully!")
        else:
            result = f"❌ {technique_info['name']} failed on account {account}"
            self.log_manipulation(result)
            messagebox.showerror("Failed", f"{technique_info['name']} failed to execute.")
    
    def start_transaction_monitoring(self):
        """Start transaction monitoring"""
        self.monitoring_status_label.config(text="Status: Monitoring Active")
        self.log_monitoring("Starting transaction monitoring...")
        
        # Start monitoring in separate thread
        threading.Thread(target=self.monitor_transactions, daemon=True).start()
    
    def monitor_transactions(self):
        """Monitor transactions"""
        while True:
            # Simulate transaction detection
            if random.random() < 0.3:  # 30% chance of transaction
                transaction = self.generate_fake_transaction()
                self.add_transaction_to_log(transaction)
                self.log_monitoring(f"Detected transaction: {transaction['type']} - ${transaction['amount']}")
            
            time.sleep(5)  # Check every 5 seconds
    
    def generate_fake_transaction(self):
        """Generate fake transaction"""
        transaction_types = ["Transfer", "Withdrawal", "Deposit", "Payment"]
        amounts = [100, 500, 1000, 2500, 5000, 10000]
        
        return {
            "time": datetime.now().strftime("%H:%M:%S"),
            "account": f"ACC{random.randint(1000, 9999)}",
            "type": random.choice(transaction_types),
            "amount": random.choice(amounts),
            "status": "Completed"
        }
    
    def add_transaction_to_log(self, transaction):
        """Add transaction to log"""
        self.transaction_tree.insert('', 'end', values=(
            transaction["time"],
            transaction["account"],
            transaction["type"],
            f"${transaction['amount']}",
            transaction["status"]
        ))
    
    def send_swift_message(self):
        """Send SWIFT message"""
        message_type = self.swift_type_var.get()
        sender_bic = self.sender_bic_var.get().strip()
        receiver_bic = self.receiver_bic_var.get().strip()
        amount = self.swift_amount_var.get().strip()
        
        if not all([sender_bic, receiver_bic, amount]):
            messagebox.showwarning("Warning", "Please fill in all SWIFT message fields!")
            return
        
        # Send SWIFT message
        threading.Thread(target=self.perform_swift_send, args=(message_type, sender_bic, receiver_bic, amount), daemon=True).start()
    
    def perform_swift_send(self, message_type, sender_bic, receiver_bic, amount):
        """Perform SWIFT send"""
        self.log_swift(f"Sending {message_type} message...")
        self.log_swift(f"From: {sender_bic}")
        self.log_swift(f"To: {receiver_bic}")
        self.log_swift(f"Amount: ${amount}")
        
        time.sleep(3)  # Simulate SWIFT processing
        
        # Simulate success
        success = random.random() > 0.2  # 80% success rate
        
        if success:
            self.log_swift("✅ SWIFT message sent successfully!")
            messagebox.showinfo("Success", "SWIFT message sent successfully!")
        else:
            self.log_swift("❌ SWIFT message failed to send!")
            messagebox.showerror("Error", "SWIFT message failed to send!")
    
    def scan_social_media(self, platform):
        """Scan social media platform"""
        self.log_social(f"Scanning {platform} for intelligence...")
        
        # Simulate social media scan
        time.sleep(2)
        
        # Generate fake data
        data_points = random.randint(5, 15)
        self.log_social(f"Found {data_points} data points on {platform}")
        
        for i in range(data_points):
            time.sleep(0.5)
            data_type = random.choice(["Profile", "Post", "Connection", "Activity"])
            self.log_social(f"  {i+1}. {data_type} data collected")
        
        self.log_social(f"✅ {platform} scan completed")
    
    def gather_social_intelligence(self):
        """Gather social media intelligence"""
        target = self.social_target_var.get().strip()
        if not target:
            messagebox.showwarning("Warning", "Please enter a target!")
            return
        
        self.log_social(f"Gathering intelligence on target: {target}")
        
        # Simulate intelligence gathering
        threading.Thread(target=self.perform_intelligence_gathering, args=(target,), daemon=True).start()
    
    def perform_intelligence_gathering(self, target):
        """Perform intelligence gathering"""
        self.log_social(f"Starting comprehensive intelligence gathering on {target}...")
        
        intelligence_types = [
            "Profile analysis",
            "Connection mapping",
            "Activity patterns",
            "Financial indicators",
            "Behavioral analysis"
        ]
        
        for intel_type in intelligence_types:
            time.sleep(1)
            self.log_social(f"  📊 {intel_type} completed")
        
        self.log_social(f"✅ Intelligence gathering completed for {target}")
        messagebox.showinfo("Complete", f"Intelligence gathering completed for {target}")
    
    def execute_phishing_attack(self):
        """Execute phishing attack"""
        target = self.phishing_target_var.get().strip()
        if not target:
            messagebox.showwarning("Warning", "Please enter a target!")
            return
        
        selection = self.phishing_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a phishing technique!")
            return
        
        technique_index = selection[0]
        technique_id = list(self.phishing_techniques.keys())[technique_index]
        technique_info = self.phishing_techniques[technique_id]
        
        # Execute phishing attack
        threading.Thread(target=self.perform_phishing_attack, args=(target, technique_id, technique_info), daemon=True).start()
    
    def perform_phishing_attack(self, target, technique_id, technique_info):
        """Perform phishing attack"""
        self.log_phishing(f"Executing {technique_info['name']} on {target}...")
        
        # Simulate phishing attack
        time.sleep(3)
        
        # Determine success based on technique
        success = random.random() < technique_info['success_rate']
        
        if success:
            result = f"✅ {technique_info['name']} successful on {target}"
            self.log_phishing(result)
            messagebox.showinfo("Success", f"{technique_info['name']} attack successful!")
        else:
            result = f"❌ {technique_info['name']} failed on {target}"
            self.log_phishing(result)
            messagebox.showerror("Failed", f"{technique_info['name']} attack failed.")
    
    def log_message(self, message):
        """Log message to system details"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.system_details.insert(tk.END, formatted_message)
        self.system_details.see(tk.END)
    
    def log_manipulation(self, message):
        """Log manipulation message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.manipulation_results.insert(tk.END, formatted_message)
        self.manipulation_results.see(tk.END)
    
    def log_monitoring(self, message):
        """Log monitoring message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.monitoring_log.insert(tk.END, formatted_message)
        self.monitoring_log.see(tk.END)
    
    def log_swift(self, message):
        """Log SWIFT message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.swift_log.insert(tk.END, formatted_message)
        self.swift_log.see(tk.END)
    
    def log_social(self, message):
        """Log social media message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.social_results.insert(tk.END, formatted_message)
        self.social_results.see(tk.END)
    
    def log_phishing(self, message):
        """Log phishing message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.phishing_results.insert(tk.END, formatted_message)
        self.phishing_results.see(tk.END)
    
    def get_banking_targets(self):
        """Get banking targets"""
        return self.banking_targets
    
    def get_account_data(self):
        """Get account data"""
        return self.account_data
    
    def get_transactions(self):
        """Get transactions"""
        return self.transactions 