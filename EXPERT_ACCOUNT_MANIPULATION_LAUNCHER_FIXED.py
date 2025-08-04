#!/usr/bin/env python3
"""
EXPERT ACCOUNT MANIPULATION LAUNCHER - FIXED VERSION
Unified interface for expert account manipulation system
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import json
import os
from datetime import datetime

# Import expert system components with error handling
try:
    from silos.developmental.nlp_query_engine import NLPQueryEngine
    NLP_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ NLP Query Engine not available: {e}")
    NLP_AVAILABLE = False

try:
    from silos.developmental.advanced_algorithms import AdvancedAlgorithms
    ALGORITHMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Advanced Algorithms not available: {e}")
    ALGORITHMS_AVAILABLE = False

try:
    from silos.security.database_penetration_fixed import DatabasePenetration
    PENETRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Database Penetration not available: {e}")
    PENETRATION_AVAILABLE = False

class ExpertAccountManipulationLauncher:
    def __init__(self):
        self.name = "Expert Account Manipulation Launcher"
        self.version = "1.0.0"
        
        # Initialize components
        self.nlp_engine = None
        self.algorithms = None
        self.penetration = None
        
        self.init_components()
        self.init_launcher_interface()
    
    def init_components(self):
        """Initialize expert system components"""
        if NLP_AVAILABLE:
            try:
                self.nlp_engine = NLPQueryEngine()
                print("✅ NLP Query Engine initialized")
            except Exception as e:
                print(f"❌ NLP Query Engine initialization failed: {e}")
        
        if ALGORITHMS_AVAILABLE:
            try:
                self.algorithms = AdvancedAlgorithms()
                print("✅ Advanced Algorithms initialized")
            except Exception as e:
                print(f"❌ Advanced Algorithms initialization failed: {e}")
        
        if PENETRATION_AVAILABLE:
            try:
                self.penetration = DatabasePenetration()
                print("✅ Database Penetration initialized")
            except Exception as e:
                print(f"❌ Database Penetration initialization failed: {e}")
    
    def init_launcher_interface(self):
        """Initialize launcher interface"""
        self.root = tk.Tk()
        self.root.title(f"🔥 {self.name} v{self.version}")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0d1117')
        
        self.create_launcher_interface()
    
    def create_launcher_interface(self):
        """Create launcher interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#0d1117')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#0d1117')
        header_frame.pack(fill='x', pady=(0, 10))
        
        header_label = tk.Label(
            header_frame,
            text="🔥 EXPERT ACCOUNT MANIPULATION SYSTEM",
            font=('Segoe UI', 24, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117'
        )
        header_label.pack(side='left')
        
        # Component status
        status_frame = tk.Frame(header_frame, bg='#0d1117')
        status_frame.pack(side='right', pady=10)
        
        self.nlp_status = tk.Label(
            status_frame,
            text="🤖 NLP: Ready" if self.nlp_engine else "🤖 NLP: Error",
            font=('Segoe UI', 10),
            fg='#4ecdc4' if self.nlp_engine else '#ff6b6b',
            bg='#0d1117'
        )
        self.nlp_status.pack(side='left', padx=5)
        
        self.algo_status = tk.Label(
            status_frame,
            text="🧮 Algorithms: Ready" if self.algorithms else "🧮 Algorithms: Error",
            font=('Segoe UI', 10),
            fg='#4ecdc4' if self.algorithms else '#ff6b6b',
            bg='#0d1117'
        )
        self.algo_status.pack(side='left', padx=5)
        
        self.pen_status = tk.Label(
            status_frame,
            text="🛡️ Penetration: Ready" if self.penetration else "🛡️ Penetration: Error",
            font=('Segoe UI', 10),
            fg='#4ecdc4' if self.penetration else '#ff6b6b',
            bg='#0d1117'
        )
        self.pen_status.pack(side='left', padx=5)
        
        # Expert system control panel
        control_frame = tk.LabelFrame(
            main_frame,
            text="🎛️ EXPERT SYSTEM CONTROL PANEL",
            font=('Segoe UI', 14, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117',
            bd=2,
            relief='solid'
        )
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # NLP Query section
        nlp_frame = tk.LabelFrame(
            control_frame,
            text="🤖 NATURAL LANGUAGE QUERIES",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff9ff3',
            bg='#0d1117'
        )
        nlp_frame.pack(fill='x', padx=10, pady=5)
        
        # Query input
        query_frame = tk.Frame(nlp_frame, bg='#0d1117')
        query_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            query_frame,
            text="Enter your query in natural language:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(anchor='w')
        
        self.query_entry = tk.Entry(
            query_frame,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Segoe UI', 12),
            bd=0,
            relief='flat',
            insertbackground='#c9d1d9'
        )
        self.query_entry.pack(fill='x', pady=5)
        self.query_entry.insert(0, "Show me account information for 1000000001")
        
        # Query buttons
        query_btn_frame = tk.Frame(nlp_frame, bg='#0d1117')
        query_btn_frame.pack(fill='x', padx=10, pady=5)
        
        execute_query_btn = tk.Button(
            query_btn_frame,
            text="🚀 EXECUTE QUERY",
            command=self.execute_nlp_query,
            bg='#4ecdc4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        execute_query_btn.pack(side='left', padx=5)
        
        # Quick query buttons
        quick_queries = [
            ("Show account 1000000001", "Show me account information for 1000000001"),
            ("Customer John Smith", "Get customer data for John Smith"),
            ("Transaction history", "Display transaction history for account 1000000001"),
            ("Bank analysis", "Analyze banking data by bank")
        ]
        
        for text, query in quick_queries:
            quick_btn = tk.Button(
                query_btn_frame,
                text=text,
                command=lambda q=query: self.set_query(q),
                bg='#21262d',
                fg='#c9d1d9',
                font=('Segoe UI', 10),
                bd=0,
                padx=15,
                pady=5,
                cursor='hand2'
            )
            quick_btn.pack(side='left', padx=2)
        
        # Advanced algorithms section
        algo_frame = tk.LabelFrame(
            control_frame,
            text="🧮 ADVANCED ALGORITHMS",
            font=('Segoe UI', 12, 'bold'),
            fg='#96ceb4',
            bg='#0d1117'
        )
        algo_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm selection
        algo_select_frame = tk.Frame(algo_frame, bg='#0d1117')
        algo_select_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            algo_select_frame,
            text="Select Algorithm:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(side='left')
        
        self.algo_var = tk.StringVar(value="greedy")
        algo_combo = ttk.Combobox(
            algo_select_frame,
            textvariable=self.algo_var,
            values=["greedy", "dfs", "bfs", "dijkstra", "a_star", "kmeans", "genetic"],
            state="readonly",
            width=15
        )
        algo_combo.pack(side='left', padx=10)
        
        execute_algo_btn = tk.Button(
            algo_select_frame,
            text="🧮 EXECUTE ALGORITHM",
            command=self.execute_algorithm,
            bg='#96ceb4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        execute_algo_btn.pack(side='left', padx=10)
        
        # Database penetration section
        pen_frame = tk.LabelFrame(
            control_frame,
            text="🛡️ DATABASE PENETRATION",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff6b6b',
            bg='#0d1117'
        )
        pen_frame.pack(fill='x', padx=10, pady=5)
        
        # Database configuration
        db_frame = tk.Frame(pen_frame, bg='#0d1117')
        db_frame.pack(fill='x', padx=10, pady=5)
        
        # Database type selection
        db_type_frame = tk.Frame(db_frame, bg='#0d1117')
        db_type_frame.pack(fill='x', pady=5)
        
        tk.Label(
            db_type_frame,
            text="Database Type:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(side='left')
        
        self.db_type_var = tk.StringVar(value="sqlite")
        db_type_combo = ttk.Combobox(
            db_type_frame,
            textvariable=self.db_type_var,
            values=["sqlite", "mysql", "postgresql", "mongodb", "redis"],
            state="readonly",
            width=15
        )
        db_type_combo.pack(side='left', padx=10)
        
        # Penetration buttons
        pen_btn_frame = tk.Frame(pen_frame, bg='#0d1117')
        pen_btn_frame.pack(fill='x', padx=10, pady=5)
        
        scan_vuln_btn = tk.Button(
            pen_btn_frame,
            text="🔍 SCAN VULNERABILITIES",
            command=self.scan_vulnerabilities,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        scan_vuln_btn.pack(side='left', padx=5)
        
        penetrate_btn = tk.Button(
            pen_btn_frame,
            text="🔥 PENETRATE DATABASE",
            command=self.penetrate_database,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        penetrate_btn.pack(side='left', padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 EXPERT SYSTEM RESULTS",
            font=('Segoe UI', 14, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=2,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Results notebook
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create result tabs
        self.create_nlp_results_tab()
        self.create_algorithm_results_tab()
        self.create_penetration_results_tab()
        self.create_system_log_tab()
        
        # Log area
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 SYSTEM LOG",
            font=('Segoe UI', 12, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='x', padx=10, pady=5)
        
        self.system_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=6
        )
        self.system_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_system("🔥 Expert Account Manipulation System initialized")
        if self.nlp_engine:
            self.log_system("🤖 NLP Query Engine: Ready for natural language queries")
        else:
            self.log_system("❌ NLP Query Engine: Initialization failed")
        
        if self.algorithms:
            self.log_system("🧮 Advanced Algorithms: Ready for data analysis")
        else:
            self.log_system("❌ Advanced Algorithms: Initialization failed")
        
        if self.penetration:
            self.log_system("🛡️ Database Penetration: Ready for security testing")
        else:
            self.log_system("❌ Database Penetration: Initialization failed")
        
        self.log_system("🎯 System ready for expert-level account manipulation")
    
    def create_nlp_results_tab(self):
        """Create NLP results tab"""
        nlp_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(nlp_frame, text="🤖 NLP Results")
        
        self.nlp_results_text = scrolledtext.ScrolledText(
            nlp_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.nlp_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_algorithm_results_tab(self):
        """Create algorithm results tab"""
        algo_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(algo_frame, text="🧮 Algorithm Results")
        
        self.algo_results_text = scrolledtext.ScrolledText(
            algo_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.algo_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_penetration_results_tab(self):
        """Create penetration results tab"""
        pen_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(pen_frame, text="🛡️ Penetration Results")
        
        self.pen_results_text = scrolledtext.ScrolledText(
            pen_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.pen_results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_system_log_tab(self):
        """Create system log tab"""
        log_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(log_frame, text="📝 System Log")
        
        self.detailed_log_text = scrolledtext.ScrolledText(
            log_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.detailed_log_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def set_query(self, query):
        """Set query in entry field"""
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, query)
    
    def execute_nlp_query(self):
        """Execute NLP query"""
        if not self.nlp_engine:
            messagebox.showerror("Error", "NLP Query Engine not available")
            return
        
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a query")
            return
        
        self.log_system(f"🤖 Executing NLP query: {query}")
        
        # Execute in thread
        threading.Thread(target=self._execute_nlp_query_thread, args=(query,), daemon=True).start()
    
    def _execute_nlp_query_thread(self, query):
        """Execute NLP query in thread"""
        try:
            result = self.nlp_engine.process_natural_language_query(query)
            
            # Display result
            self.nlp_results_text.delete('1.0', tk.END)
            self.nlp_results_text.insert('1.0', result['formatted_response'])
            
            # Log result
            self.log_system(f"✅ NLP query completed successfully")
            self.log_detailed(f"NLP Query Result:\n{json.dumps(result, indent=2)}")
            
        except Exception as e:
            error_msg = f"❌ NLP query failed: {str(e)}"
            self.log_system(error_msg)
            self.nlp_results_text.delete('1.0', tk.END)
            self.nlp_results_text.insert('1.0', error_msg)
    
    def execute_algorithm(self):
        """Execute advanced algorithm"""
        if not self.algorithms:
            messagebox.showerror("Error", "Advanced Algorithms not available")
            return
        
        algorithm = self.algo_var.get()
        self.log_system(f"🧮 Executing {algorithm} algorithm...")
        
        # Execute in thread
        threading.Thread(target=self._execute_algorithm_thread, args=(algorithm,), daemon=True).start()
    
    def _execute_algorithm_thread(self, algorithm):
        """Execute algorithm in thread"""
        try:
            # Sample data for algorithm testing
            sample_data = {
                "accounts": [
                    {"account_number": "1000000001", "balance": 25000, "transactions": [1, 2, 3], "created_date": "2023-01-15"},
                    {"account_number": "1000000002", "balance": 15000, "transactions": [1], "created_date": "2023-02-20"},
                    {"account_number": "1000000003", "balance": 75000, "transactions": [1, 2, 3, 4, 5], "created_date": "2023-03-10"}
                ],
                "transactions": [
                    {"from_account": "1000000001", "to_account": "1000000002", "amount": 1000},
                    {"from_account": "1000000002", "to_account": "1000000003", "amount": 500},
                    {"from_account": "1000000003", "to_account": "1000000001", "amount": 2000}
                ]
            }
            
            result = self.algorithms.run_algorithm(algorithm, sample_data)
            
            # Display result
            self.algo_results_text.delete('1.0', tk.END)
            self.algo_results_text.insert('1.0', json.dumps(result, indent=2))
            
            # Log result
            self.log_system(f"✅ {algorithm} algorithm completed successfully")
            self.log_detailed(f"Algorithm Result:\n{json.dumps(result, indent=2)}")
            
        except Exception as e:
            error_msg = f"❌ Algorithm execution failed: {str(e)}"
            self.log_system(error_msg)
            self.algo_results_text.delete('1.0', tk.END)
            self.algo_results_text.insert('1.0', error_msg)
    
    def scan_vulnerabilities(self):
        """Scan database vulnerabilities"""
        if not self.penetration:
            messagebox.showerror("Error", "Database Penetration not available")
            return
        
        db_type = self.db_type_var.get()
        self.log_system(f"🔍 Scanning vulnerabilities for {db_type} database...")
        
        # Execute in thread
        threading.Thread(target=self._scan_vulnerabilities_thread, args=(db_type,), daemon=True).start()
    
    def _scan_vulnerabilities_thread(self, db_type):
        """Scan vulnerabilities in thread"""
        try:
            db_config = {"type": db_type}
            result = self.penetration.scan_database_vulnerabilities(db_config)
            
            # Display result
            self.pen_results_text.delete('1.0', tk.END)
            self.pen_results_text.insert('1.0', json.dumps(result, indent=2))
            
            # Log result
            self.log_system(f"✅ Vulnerability scan completed for {db_type}")
            self.log_detailed(f"Vulnerability Scan Result:\n{json.dumps(result, indent=2)}")
            
        except Exception as e:
            error_msg = f"❌ Vulnerability scan failed: {str(e)}"
            self.log_system(error_msg)
            self.pen_results_text.delete('1.0', tk.END)
            self.pen_results_text.insert('1.0', error_msg)
    
    def penetrate_database(self):
        """Penetrate database"""
        if not self.penetration:
            messagebox.showerror("Error", "Database Penetration not available")
            return
        
        db_type = self.db_type_var.get()
        self.log_system(f"🔥 Penetrating {db_type} database...")
        
        # Execute in thread
        threading.Thread(target=self._penetrate_database_thread, args=(db_type,), daemon=True).start()
    
    def _penetrate_database_thread(self, db_type):
        """Penetrate database in thread"""
        try:
            db_config = {"type": db_type}
            result = self.penetration.penetrate_database(db_config, "comprehensive")
            
            # Display result
            self.pen_results_text.delete('1.0', tk.END)
            self.pen_results_text.insert('1.0', json.dumps(result, indent=2))
            
            # Log result
            self.log_system(f"✅ Database penetration completed for {db_type}")
            self.log_detailed(f"Penetration Result:\n{json.dumps(result, indent=2)}")
            
        except Exception as e:
            error_msg = f"❌ Database penetration failed: {str(e)}"
            self.log_system(error_msg)
            self.pen_results_text.delete('1.0', tk.END)
            self.pen_results_text.insert('1.0', error_msg)
    
    def log_system(self, message):
        """Log system message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.system_log.insert(tk.END, formatted_message)
        self.system_log.see(tk.END)
    
    def log_detailed(self, message):
        """Log detailed message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.detailed_log_text.insert(tk.END, formatted_message)
        self.detailed_log_text.see(tk.END)
    
    def run(self):
        """Run launcher"""
        print(f"🔥 Starting {self.name}")
        self.root.mainloop()

def main():
    """Main entry point"""
    launcher = ExpertAccountManipulationLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 