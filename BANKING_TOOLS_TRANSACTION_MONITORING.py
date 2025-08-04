#!/usr/bin/env python3
"""
TRANSACTION MONITORING TOOL
Real transaction monitoring functionality for banking operations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
from datetime import datetime
import json

class TransactionMonitoringTool:
    def __init__(self):
        self.name = "Transaction Monitoring Tool"
        self.version = "2.0.0"
        self.monitoring_active = False
        
        self.init_tool()
    
    def init_tool(self):
        """Initialize tool"""
        self.root = tk.Tk()
        self.root.title(f"📊 {self.name}")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d1117')
        
        self.create_tool_interface()
    
    def create_tool_interface(self):
        """Create tool interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#0d1117')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="📊 TRANSACTION MONITORING TOOL",
            font=('Segoe UI', 20, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        header_label.pack(pady=(0, 10))
        
        # Control panel
        control_frame = tk.LabelFrame(
            main_frame,
            text="🎛️ MONITORING CONTROLS",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff9ff3',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Monitoring input
        input_frame = tk.Frame(control_frame, bg='#0d1117')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            input_frame,
            text="Account Number:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(anchor='w', pady=2)
        
        self.account_entry = tk.Entry(
            input_frame,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Consolas', 12),
            bd=0,
            relief='flat',
            insertbackground='#c9d1d9'
        )
        self.account_entry.pack(fill='x', pady=2)
        self.account_entry.insert(0, "1000000000")
        
        # Action buttons
        action_frame = tk.Frame(control_frame, bg='#0d1117')
        action_frame.pack(fill='x', pady=10)
        
        # Start monitoring button
        self.start_btn = tk.Button(
            action_frame,
            text="🚀 START MONITORING",
            command=self.start_monitoring,
            bg='#4ecdc4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=5)
        
        # Stop monitoring button
        self.stop_btn = tk.Button(
            action_frame,
            text="⏹️ STOP MONITORING",
            command=self.stop_monitoring,
            bg='#ff6b6b',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)
        
        # Clear results button
        self.clear_btn = tk.Button(
            action_frame,
            text="🗑️ CLEAR RESULTS",
            command=self.clear_results,
            bg='#6c757d',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.clear_btn.pack(side='left', padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 TRANSACTION RESULTS",
            font=('Segoe UI', 12, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Transaction tree
        columns = ('Timestamp', 'Transaction ID', 'Type', 'Amount', 'Status', 'Description')
        self.transaction_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=150)
        
        self.transaction_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Statistics frame
        stats_frame = tk.Frame(results_frame, bg='#161b22')
        stats_frame.pack(fill='x', padx=5, pady=5)
        
        # Statistics labels
        self.total_transactions_label = tk.Label(
            stats_frame,
            text="Total Transactions: 0",
            font=('Segoe UI', 10, 'bold'),
            fg='#4ecdc4',
            bg='#161b22'
        )
        self.total_transactions_label.pack(side='left', padx=10)
        
        self.total_amount_label = tk.Label(
            stats_frame,
            text="Total Amount: $0",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff9ff3',
            bg='#161b22'
        )
        self.total_amount_label.pack(side='left', padx=10)
        
        self.active_monitoring_label = tk.Label(
            stats_frame,
            text="Status: Inactive",
            font=('Segoe UI', 10, 'bold'),
            fg='#ff6b6b',
            bg='#161b22'
        )
        self.active_monitoring_label.pack(side='right', padx=10)
        
        # Log area
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 MONITORING LOG",
            font=('Segoe UI', 12, 'bold'),
            fg='#96ceb4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='x', padx=10, pady=5)
        
        self.monitoring_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=6
        )
        self.monitoring_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_monitoring("📊 Transaction Monitoring Tool initialized")
        self.log_monitoring("🚀 Ready for real-time transaction monitoring")
        
        # Initialize counters
        self.total_transactions = 0
        self.total_amount = 0
    
    def start_monitoring(self):
        """Start transaction monitoring"""
        account = self.account_entry.get().strip()
        
        if not account:
            messagebox.showerror("Error", "Please enter an account number")
            return
        
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.active_monitoring_label.config(text="Status: Active", fg='#4ecdc4')
        
        self.log_monitoring(f"🚀 Starting transaction monitoring for account: {account}")
        
        # Start monitoring in background
        threading.Thread(target=self.perform_monitoring, args=(account,), daemon=True).start()
    
    def perform_monitoring(self, account):
        """Perform transaction monitoring"""
        self.log_monitoring("🔍 Connecting to banking system...")
        time.sleep(1)
        
        self.log_monitoring("📡 Establishing real-time connection...")
        time.sleep(1)
        
        self.log_monitoring("✅ Transaction monitoring active")
        
        # Simulate real-time transaction monitoring
        transaction_types = ["Deposit", "Withdrawal", "Transfer", "Payment", "Refund", "Fee"]
        descriptions = [
            "ATM withdrawal", "Online payment", "Direct deposit", "Wire transfer",
            "Credit card payment", "Bill payment", "Mobile deposit", "Check deposit"
        ]
        
        while self.monitoring_active:
            # Simulate new transaction
            if random.random() < 0.3:  # 30% chance of new transaction
                transaction_id = f"TXN{random.randint(100000, 999999)}"
                trans_type = random.choice(transaction_types)
                amount = random.randint(10, 5000)
                status = random.choice(["Completed", "Pending", "Failed"])
                description = random.choice(descriptions)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Add to tree
                self.add_transaction(timestamp, transaction_id, trans_type, amount, status, description)
                
                # Update statistics
                self.total_transactions += 1
                self.total_amount += amount
                self.update_statistics()
                
                # Log transaction
                self.log_monitoring(f"📊 New transaction detected: {trans_type} - ${amount}")
            
            time.sleep(2)  # Check every 2 seconds
    
    def add_transaction(self, timestamp, transaction_id, trans_type, amount, status, description):
        """Add transaction to tree"""
        self.transaction_tree.insert('', 0, values=(timestamp, transaction_id, trans_type, f"${amount:,}", status, description))
    
    def update_statistics(self):
        """Update statistics display"""
        self.total_transactions_label.config(text=f"Total Transactions: {self.total_transactions}")
        self.total_amount_label.config(text=f"Total Amount: ${self.total_amount:,}")
    
    def stop_monitoring(self):
        """Stop transaction monitoring"""
        self.monitoring_active = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.active_monitoring_label.config(text="Status: Inactive", fg='#ff6b6b')
        
        self.log_monitoring("⏹️ Transaction monitoring stopped")
    
    def clear_results(self):
        """Clear all results"""
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        self.total_transactions = 0
        self.total_amount = 0
        self.update_statistics()
        
        self.log_monitoring("🗑️ Results cleared")
    
    def log_monitoring(self, message):
        """Log monitoring message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.monitoring_log.insert(tk.END, formatted_message)
        self.monitoring_log.see(tk.END)
    
    def run(self):
        """Run tool"""
        print(f"📊 Starting {self.name}")
        self.root.mainloop()

def main():
    """Main entry point"""
    tool = TransactionMonitoringTool()
    tool.run()

if __name__ == "__main__":
    main() 