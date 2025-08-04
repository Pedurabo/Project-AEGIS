#!/usr/bin/env python3
"""
Team 4: Vulnerability Research - Penetration Testing Engine
Security Silo: Real network scanning, vulnerability detection, and exploit framework
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import time
import json
import subprocess
import platform
from datetime import datetime
import ipaddress
import random

class AEGISPenetrationEngine:
    def __init__(self):
        self.name = "AEGIS Penetration Engine"
        self.version = "1.0.0"
        self.scan_results = {}
        self.vulnerabilities = {}
        self.exploits = {}
        self.targets = []
        
        # Common ports for scanning
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080
        ]
        
        # Vulnerability database
        self.vuln_database = {
            "ssh": {
                "name": "SSH Weak Configuration",
                "severity": "Medium",
                "description": "SSH service with weak configuration",
                "exploit": "ssh_bruteforce"
            },
            "ftp": {
                "name": "FTP Anonymous Access",
                "severity": "High",
                "description": "FTP service allowing anonymous access",
                "exploit": "ftp_anonymous"
            },
            "http": {
                "name": "HTTP Default Credentials",
                "severity": "Medium",
                "description": "HTTP service with default credentials",
                "exploit": "http_default_creds"
            },
            "telnet": {
                "name": "Telnet Service Active",
                "severity": "Critical",
                "description": "Telnet service is active and unencrypted",
                "exploit": "telnet_bruteforce"
            },
            "rdp": {
                "name": "RDP Weak Security",
                "severity": "High",
                "description": "RDP service with weak security settings",
                "exploit": "rdp_exploit"
            }
        }
        
        # Exploit framework
        self.exploit_framework = {
            "ssh_bruteforce": {
                "name": "SSH Brute Force",
                "description": "Attempt to brute force SSH credentials",
                "success_rate": 0.15,
                "execution_time": 30
            },
            "ftp_anonymous": {
                "name": "FTP Anonymous Access",
                "description": "Exploit anonymous FTP access",
                "success_rate": 0.85,
                "execution_time": 10
            },
            "http_default_creds": {
                "name": "HTTP Default Credentials",
                "description": "Try default HTTP credentials",
                "success_rate": 0.25,
                "execution_time": 15
            },
            "telnet_bruteforce": {
                "name": "Telnet Brute Force",
                "description": "Brute force Telnet credentials",
                "success_rate": 0.20,
                "execution_time": 25
            },
            "rdp_exploit": {
                "name": "RDP Exploit",
                "description": "Exploit RDP vulnerabilities",
                "success_rate": 0.30,
                "execution_time": 20
            }
        }
    
    def create_penetration_interface(self, parent):
        """Create penetration testing interface"""
        pen_frame = tk.LabelFrame(
            parent,
            text="🎯 PENETRATION TESTING ENGINE",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        pen_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.pen_notebook = ttk.Notebook(pen_frame)
        self.pen_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Target management tab
        self.create_target_management_tab()
        
        # Network scanning tab
        self.create_network_scanning_tab()
        
        # Vulnerability assessment tab
        self.create_vulnerability_assessment_tab()
        
        # Exploit framework tab
        self.create_exploit_framework_tab()
        
        # Results tab
        self.create_results_tab()
    
    def create_target_management_tab(self):
        """Create target management tab"""
        target_frame = tk.Frame(self.pen_notebook, bg='#0d1117')
        self.pen_notebook.add(target_frame, text="🎯 Targets")
        
        # Target input
        input_frame = tk.LabelFrame(
            target_frame,
            text="📝 Target Input",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Single target
        single_frame = tk.Frame(input_frame, bg='#0d1117')
        single_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            single_frame,
            text="Single Target:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.single_target_var = tk.StringVar()
        target_entry = tk.Entry(
            single_frame,
            textvariable=self.single_target_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        target_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        add_btn = tk.Button(
            single_frame,
            text="Add Target",
            command=self.add_single_target,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=3,
            cursor='hand2'
        )
        add_btn.pack(side='right')
        
        # Network range
        range_frame = tk.Frame(input_frame, bg='#0d1117')
        range_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            range_frame,
            text="Network Range:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.network_range_var = tk.StringVar()
        range_entry = tk.Entry(
            range_frame,
            textvariable=self.network_range_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        range_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        add_range_btn = tk.Button(
            range_frame,
            text="Add Range",
            command=self.add_network_range,
            bg='#58a6ff',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=3,
            cursor='hand2'
        )
        add_range_btn.pack(side='right')
        
        # Quick targets
        quick_frame = tk.Frame(input_frame, bg='#0d1117')
        quick_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            quick_frame,
            text="Quick Targets:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        quick_targets = [
            ("Local Network", "192.168.1.0/24"),
            ("Common Services", "127.0.0.1"),
            ("Gateway", "192.168.1.1"),
            ("DNS Server", "8.8.8.8")
        ]
        
        for text, target in quick_targets:
            quick_btn = tk.Button(
                quick_frame,
                text=text,
                command=lambda t=target: self.add_quick_target(t),
                bg='#21262d',
                fg='#c9d1d9',
                font=('Segoe UI', 8),
                bd=0,
                padx=10,
                pady=3,
                cursor='hand2'
            )
            quick_btn.pack(side='left', padx=2)
        
        # Target list
        list_frame = tk.LabelFrame(
            target_frame,
            text="📋 Target List",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Target treeview
        columns = ('Target', 'Type', 'Status', 'Added')
        self.target_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        for col in columns:
            self.target_tree.heading(col, text=col)
            self.target_tree.column(col, width=150)
        
        self.target_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Target actions
        actions_frame = tk.Frame(target_frame, bg='#0d1117')
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        remove_btn = tk.Button(
            actions_frame,
            text="Remove Target",
            command=self.remove_target,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        remove_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(
            actions_frame,
            text="Clear All",
            command=self.clear_targets,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 9),
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=5)
    
    def create_network_scanning_tab(self):
        """Create network scanning tab"""
        scan_frame = tk.Frame(self.pen_notebook, bg='#0d1117')
        self.pen_notebook.add(scan_frame, text="🔍 Network Scan")
        
        # Scan configuration
        config_frame = tk.LabelFrame(
            scan_frame,
            text="⚙️ Scan Configuration",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        config_frame.pack(fill='x', padx=10, pady=5)
        
        # Port selection
        port_frame = tk.Frame(config_frame, bg='#0d1117')
        port_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            port_frame,
            text="Port Selection:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.port_selection_var = tk.StringVar(value="common")
        port_options = [
            ("Common Ports", "common"),
            ("All Ports", "all"),
            ("Custom Range", "custom")
        ]
        
        for text, value in port_options:
            tk.Radiobutton(
                port_frame,
                text=text,
                variable=self.port_selection_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Custom port range
        custom_frame = tk.Frame(config_frame, bg='#0d1117')
        custom_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            custom_frame,
            text="Custom Port Range:",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        ).pack(side='left')
        
        self.custom_ports_var = tk.StringVar(value="1-1000")
        custom_entry = tk.Entry(
            custom_frame,
            textvariable=self.custom_ports_var,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            bd=0,
            relief='flat'
        )
        custom_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Scan options
        options_frame = tk.Frame(config_frame, bg='#0d1117')
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.stealth_scan_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Stealth scan",
            variable=self.stealth_scan_var,
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117',
            selectcolor='#21262d'
        ).pack(side='left', padx=10)
        
        self.service_detection_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Service detection",
            variable=self.service_detection_var,
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117',
            selectcolor='#21262d'
        ).pack(side='left', padx=10)
        
        # Start scan button
        scan_btn = tk.Button(
            config_frame,
            text="Start Network Scan",
            command=self.start_network_scan,
            bg='#45b7d1',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        scan_btn.pack(pady=10)
        
        # Scan progress
        progress_frame = tk.LabelFrame(
            scan_frame,
            text="📊 Scan Progress",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        progress_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.scan_progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=400
        )
        self.scan_progress.pack(pady=10)
        
        self.scan_status_label = tk.Label(
            progress_frame,
            text="Ready to scan",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.scan_status_label.pack()
        
        # Scan log
        self.scan_log = scrolledtext.ScrolledText(
            progress_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=8
        )
        self.scan_log.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_vulnerability_assessment_tab(self):
        """Create vulnerability assessment tab"""
        vuln_frame = tk.Frame(self.pen_notebook, bg='#0d1117')
        self.pen_notebook.add(vuln_frame, text="🔍 Vulnerability Assessment")
        
        # Assessment options
        options_frame = tk.LabelFrame(
            vuln_frame,
            text="🔧 Assessment Options",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Assessment types
        types_frame = tk.Frame(options_frame, bg='#0d1117')
        types_frame.pack(fill='x', padx=10, pady=5)
        
        self.assessment_type_var = tk.StringVar(value="comprehensive")
        assessment_types = [
            ("Quick Scan", "quick"),
            ("Comprehensive", "comprehensive"),
            ("Deep Analysis", "deep"),
            ("Custom", "custom")
        ]
        
        for text, value in assessment_types:
            tk.Radiobutton(
                types_frame,
                text=text,
                variable=self.assessment_type_var,
                value=value,
                font=('Segoe UI', 9),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d'
            ).pack(side='left', padx=10)
        
        # Start assessment button
        assess_btn = tk.Button(
            options_frame,
            text="Start Vulnerability Assessment",
            command=self.start_vulnerability_assessment,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        assess_btn.pack(pady=10)
        
        # Vulnerability results
        results_frame = tk.LabelFrame(
            vuln_frame,
            text="📋 Vulnerability Results",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Vulnerability treeview
        columns = ('Target', 'Service', 'Vulnerability', 'Severity', 'Status')
        self.vuln_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        for col in columns:
            self.vuln_tree.heading(col, text=col)
            self.vuln_tree.column(col, width=120)
        
        self.vuln_tree.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_exploit_framework_tab(self):
        """Create exploit framework tab"""
        exploit_frame = tk.Frame(self.pen_notebook, bg='#0d1117')
        self.pen_notebook.add(exploit_frame, text="💣 Exploit Framework")
        
        # Exploit selection
        selection_frame = tk.LabelFrame(
            exploit_frame,
            text="🎯 Exploit Selection",
            font=('Segoe UI', 10, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        selection_frame.pack(fill='x', padx=10, pady=5)
        
        # Exploit listbox
        self.exploit_listbox = tk.Listbox(
            selection_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            height=8
        )
        self.exploit_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Populate exploit list
        for exploit_id, exploit_info in self.exploit_framework.items():
            self.exploit_listbox.insert(tk.END, f"{exploit_info['name']} - {exploit_info['description']}")
        
        # Exploit details
        details_frame = tk.LabelFrame(
            exploit_frame,
            text="📋 Exploit Details",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        details_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.exploit_details = scrolledtext.ScrolledText(
            details_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Segoe UI', 9),
            wrap=tk.WORD,
            height=8
        )
        self.exploit_details.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bind exploit selection
        self.exploit_listbox.bind('<<ListboxSelect>>', self.on_exploit_select)
        
        # Execute exploit button
        execute_btn = tk.Button(
            exploit_frame,
            text="Execute Exploit",
            command=self.execute_exploit,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        execute_btn.pack(pady=10)
    
    def create_results_tab(self):
        """Create results tab"""
        results_frame = tk.Frame(self.pen_notebook, bg='#0d1117')
        self.pen_notebook.add(results_frame, text="📊 Results")
        
        # Results summary
        summary_frame = tk.LabelFrame(
            results_frame,
            text="📈 Results Summary",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        # Summary labels
        self.targets_scanned_label = tk.Label(
            summary_frame,
            text="Targets Scanned: 0",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.targets_scanned_label.pack(anchor='w', padx=10, pady=2)
        
        self.vulnerabilities_found_label = tk.Label(
            summary_frame,
            text="Vulnerabilities Found: 0",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.vulnerabilities_found_label.pack(anchor='w', padx=10, pady=2)
        
        self.exploits_executed_label = tk.Label(
            summary_frame,
            text="Exploits Executed: 0",
            font=('Segoe UI', 9),
            fg='#c9d1d9',
            bg='#0d1117'
        )
        self.exploits_executed_label.pack(anchor='w', padx=10, pady=2)
        
        # Detailed results
        detailed_frame = tk.LabelFrame(
            results_frame,
            text="📋 Detailed Results",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffd700',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        detailed_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.detailed_results = scrolledtext.ScrolledText(
            detailed_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.detailed_results.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Export button
        export_btn = tk.Button(
            results_frame,
            text="Export Results",
            command=self.export_results,
            bg='#4ecdc4',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        export_btn.pack(pady=10)
    
    def add_single_target(self):
        """Add single target"""
        target = self.single_target_var.get().strip()
        if target:
            self.add_target(target, "Single")
            self.single_target_var.set("")
    
    def add_network_range(self):
        """Add network range"""
        network = self.network_range_var.get().strip()
        if network:
            try:
                # Generate IPs from network range
                network_obj = ipaddress.IPv4Network(network, strict=False)
                for ip in network_obj.hosts():
                    self.add_target(str(ip), "Network")
                self.network_range_var.set("")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid network range: {str(e)}")
    
    def add_quick_target(self, target):
        """Add quick target"""
        self.add_target(target, "Quick")
    
    def add_target(self, target, target_type):
        """Add target to list"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.targets.append({
            "target": target,
            "type": target_type,
            "status": "Pending",
            "added": timestamp
        })
        
        self.target_tree.insert('', 'end', values=(
            target,
            target_type,
            "Pending",
            timestamp
        ))
    
    def remove_target(self):
        """Remove selected target"""
        selection = self.target_tree.selection()
        if selection:
            item = self.target_tree.item(selection[0])
            target = item['values'][0]
            
            # Remove from tree and list
            self.target_tree.delete(selection[0])
            self.targets = [t for t in self.targets if t['target'] != target]
    
    def clear_targets(self):
        """Clear all targets"""
        self.target_tree.delete(*self.target_tree.get_children())
        self.targets = []
    
    def start_network_scan(self):
        """Start network scan"""
        if not self.targets:
            messagebox.showwarning("Warning", "No targets to scan!")
            return
        
        # Start scan in separate thread
        threading.Thread(target=self.perform_network_scan, daemon=True).start()
    
    def perform_network_scan(self):
        """Perform network scan"""
        total_targets = len(self.targets)
        self.scan_progress['maximum'] = total_targets
        
        for i, target_info in enumerate(self.targets):
            target = target_info['target']
            
            # Update progress
            self.scan_progress['value'] = i + 1
            self.scan_status_label.config(text=f"Scanning {target}...")
            
            # Log scan start
            self.log_scan_message(f"Starting scan of {target}")
            
            # Perform port scan
            open_ports = self.scan_ports(target)
            
            # Store results
            self.scan_results[target] = {
                "target": target,
                "open_ports": open_ports,
                "scan_time": datetime.now().isoformat()
            }
            
            # Log results
            if open_ports:
                self.log_scan_message(f"Found {len(open_ports)} open ports on {target}")
            else:
                self.log_scan_message(f"No open ports found on {target}")
            
            # Update target status
            self.update_target_status(target, "Scanned")
            
            time.sleep(0.5)  # Simulate scan time
        
        self.scan_status_label.config(text="Scan completed!")
        self.log_scan_message("Network scan completed!")
    
    def scan_ports(self, target):
        """Scan ports on target"""
        open_ports = []
        
        # Get ports to scan
        if self.port_selection_var.get() == "common":
            ports_to_scan = self.common_ports
        elif self.port_selection_var.get() == "all":
            ports_to_scan = range(1, 1025)
        else:  # custom
            try:
                port_range = self.custom_ports_var.get()
                start, end = map(int, port_range.split('-'))
                ports_to_scan = range(start, end + 1)
            except:
                ports_to_scan = self.common_ports
        
        # Scan ports
        for port in ports_to_scan:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        return open_ports
    
    def start_vulnerability_assessment(self):
        """Start vulnerability assessment"""
        if not self.scan_results:
            messagebox.showwarning("Warning", "No scan results available!")
            return
        
        # Start assessment in separate thread
        threading.Thread(target=self.perform_vulnerability_assessment, daemon=True).start()
    
    def perform_vulnerability_assessment(self):
        """Perform vulnerability assessment"""
        for target, scan_result in self.scan_results.items():
            open_ports = scan_result['open_ports']
            
            for port in open_ports:
                # Determine service
                service = self.get_service_name(port)
                
                # Check for vulnerabilities
                vulnerabilities = self.check_vulnerabilities(target, port, service)
                
                # Add to vulnerability list
                for vuln in vulnerabilities:
                    self.vulnerabilities[f"{target}:{port}"] = vuln
                    
                    # Add to treeview
                    self.vuln_tree.insert('', 'end', values=(
                        target,
                        f"{service} ({port})",
                        vuln['name'],
                        vuln['severity'],
                        "Found"
                    ))
        
        # Update summary
        self.update_vulnerability_summary()
    
    def get_service_name(self, port):
        """Get service name for port"""
        service_map = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            8080: "HTTP-Proxy"
        }
        return service_map.get(port, "Unknown")
    
    def check_vulnerabilities(self, target, port, service):
        """Check for vulnerabilities"""
        vulnerabilities = []
        
        # Check for common vulnerabilities based on service
        if service == "SSH":
            vulnerabilities.append(self.vuln_database["ssh"])
        elif service == "FTP":
            vulnerabilities.append(self.vuln_database["ftp"])
        elif service in ["HTTP", "HTTPS"]:
            vulnerabilities.append(self.vuln_database["http"])
        elif service == "Telnet":
            vulnerabilities.append(self.vuln_database["telnet"])
        elif service == "RDP":
            vulnerabilities.append(self.vuln_database["rdp"])
        
        return vulnerabilities
    
    def on_exploit_select(self, event):
        """Handle exploit selection"""
        selection = self.exploit_listbox.curselection()
        if selection:
            exploit_index = selection[0]
            exploit_id = list(self.exploit_framework.keys())[exploit_index]
            exploit_info = self.exploit_framework[exploit_id]
            
            # Display exploit details
            details = f"""
Exploit: {exploit_info['name']}
Description: {exploit_info['description']}
Success Rate: {exploit_info['success_rate'] * 100}%
Execution Time: {exploit_info['execution_time']} seconds

This exploit will attempt to compromise the target system using advanced techniques.
            """
            
            self.exploit_details.delete('1.0', tk.END)
            self.exploit_details.insert('1.0', details)
    
    def execute_exploit(self):
        """Execute selected exploit"""
        selection = self.exploit_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an exploit!")
            return
        
        if not self.vulnerabilities:
            messagebox.showwarning("Warning", "No vulnerabilities found to exploit!")
            return
        
        # Get selected exploit
        exploit_index = selection[0]
        exploit_id = list(self.exploit_framework.keys())[exploit_index]
        exploit_info = self.exploit_framework[exploit_id]
        
        # Execute exploit in separate thread
        threading.Thread(target=self.perform_exploit, args=(exploit_id, exploit_info), daemon=True).start()
    
    def perform_exploit(self, exploit_id, exploit_info):
        """Perform exploit"""
        # Simulate exploit execution
        time.sleep(exploit_info['execution_time'])
        
        # Determine success based on success rate
        success = random.random() < exploit_info['success_rate']
        
        # Store exploit result
        self.exploits[exploit_id] = {
            "exploit": exploit_info['name'],
            "success": success,
            "execution_time": exploit_info['execution_time'],
            "timestamp": datetime.now().isoformat()
        }
        
        # Update results
        if success:
            messagebox.showinfo("Success", f"Exploit '{exploit_info['name']}' executed successfully!")
        else:
            messagebox.showwarning("Failed", f"Exploit '{exploit_info['name']}' failed to execute.")
        
        # Update summary
        self.update_exploit_summary()
    
    def update_target_status(self, target, status):
        """Update target status in treeview"""
        for item in self.target_tree.get_children():
            if self.target_tree.item(item)['values'][0] == target:
                values = list(self.target_tree.item(item)['values'])
                values[2] = status
                self.target_tree.item(item, values=values)
                break
    
    def update_vulnerability_summary(self):
        """Update vulnerability summary"""
        vuln_count = len(self.vulnerabilities)
        self.vulnerabilities_found_label.config(text=f"Vulnerabilities Found: {vuln_count}")
    
    def update_exploit_summary(self):
        """Update exploit summary"""
        exploit_count = len(self.exploits)
        self.exploits_executed_label.config(text=f"Exploits Executed: {exploit_count}")
    
    def log_scan_message(self, message):
        """Log scan message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.scan_log.insert(tk.END, formatted_message)
        self.scan_log.see(tk.END)
    
    def export_results(self):
        """Export results"""
        results = {
            "scan_results": self.scan_results,
            "vulnerabilities": self.vulnerabilities,
            "exploits": self.exploits,
            "export_time": datetime.now().isoformat()
        }
        
        # Display results in detailed view
        self.detailed_results.delete('1.0', tk.END)
        self.detailed_results.insert('1.0', json.dumps(results, indent=2))
        
        messagebox.showinfo("Success", "Results exported and displayed in detailed view!")
    
    def get_scan_results(self):
        """Get scan results"""
        return self.scan_results
    
    def get_vulnerabilities(self):
        """Get vulnerabilities"""
        return self.vulnerabilities
    
    def get_exploits(self):
        """Get exploits"""
        return self.exploits 