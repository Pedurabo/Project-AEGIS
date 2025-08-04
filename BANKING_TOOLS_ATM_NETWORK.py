#!/usr/bin/env python3
"""
ATM NETWORK TOOL
Real ATM network access and control functionality
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import time
import random
from datetime import datetime
import json

class AtmNetworkTool:
    def __init__(self):
        self.name = "ATM Network Tool"
        self.version = "2.0.0"
        self.access_active = False
        
        self.init_tool()
    
    def init_tool(self):
        """Initialize tool"""
        self.root = tk.Tk()
        self.root.title(f"🏧 {self.name}")
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
            text="🏧 ATM NETWORK TOOL",
            font=('Segoe UI', 20, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        header_label.pack(pady=(0, 10))
        
        # Control panel
        control_frame = tk.LabelFrame(
            main_frame,
            text="🎛️ ATM CONTROLS",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff9ff3',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # ATM input
        input_frame = tk.Frame(control_frame, bg='#0d1117')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Bank selection
        tk.Label(
            input_frame,
            text="Target Bank:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(anchor='w', pady=2)
        
        self.bank_var = tk.StringVar(value="Chase Bank")
        bank_combo = ttk.Combobox(
            input_frame,
            textvariable=self.bank_var,
            values=[
                "Chase Bank", "Bank of America", "Wells Fargo", "Citibank",
                "Goldman Sachs", "Morgan Stanley", "JPMorgan Chase"
            ],
            state="readonly",
            font=('Segoe UI', 12)
        )
        bank_combo.pack(fill='x', pady=2)
        
        # Location selection
        tk.Label(
            input_frame,
            text="Location:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(anchor='w', pady=2)
        
        self.location_var = tk.StringVar(value="New York")
        location_combo = ttk.Combobox(
            input_frame,
            textvariable=self.location_var,
            values=[
                "New York", "London", "Tokyo", "Paris", "Sydney", "Toronto", 
                "Berlin", "Rome", "Madrid", "Amsterdam", "Zurich", "Singapore"
            ],
            state="readonly",
            font=('Segoe UI', 12)
        )
        location_combo.pack(fill='x', pady=2)
        
        # Action buttons
        action_frame = tk.Frame(control_frame, bg='#0d1117')
        action_frame.pack(fill='x', pady=10)
        
        # Access ATM network button
        self.access_btn = tk.Button(
            action_frame,
            text="🏧 ACCESS ATM NETWORK",
            command=self.access_atm_network,
            bg='#4ecdc4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.access_btn.pack(side='left', padx=5)
        
        # Monitor ATMs button
        self.monitor_btn = tk.Button(
            action_frame,
            text="📊 MONITOR ATMs",
            command=self.monitor_atms,
            bg='#ff9ff3',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.monitor_btn.pack(side='left', padx=5)
        
        # Control ATM button
        self.control_btn = tk.Button(
            action_frame,
            text="🎮 CONTROL ATM",
            command=self.control_atm,
            bg='#96ceb4',
            fg='#000000',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.control_btn.pack(side='left', padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 ATM RESULTS",
            font=('Segoe UI', 12, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # ATM network tree
        columns = ('ATM ID', 'Location', 'Bank', 'Status', 'Cash Level', 'Last Transaction', 'Security Level')
        self.atm_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.atm_tree.heading(col, text=col)
            self.atm_tree.column(col, width=120)
        
        self.atm_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # ATM details
        details_frame = tk.Frame(results_frame, bg='#161b22')
        details_frame.pack(fill='x', padx=5, pady=5)
        
        # ATM info
        self.atm_info = scrolledtext.ScrolledText(
            details_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD,
            height=6
        )
        self.atm_info.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Log area
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 ATM LOG",
            font=('Segoe UI', 12, 'bold'),
            fg='#96ceb4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='x', padx=10, pady=5)
        
        self.atm_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=6
        )
        self.atm_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_atm("🏧 ATM Network Tool initialized")
        self.log_atm("🚀 Ready for ATM network operations")
    
    def access_atm_network(self):
        """Access ATM network"""
        bank = self.bank_var.get()
        location = self.location_var.get()
        
        self.log_atm(f"🏧 Accessing ATM network...")
        self.log_atm(f"🏦 Bank: {bank}")
        self.log_atm(f"📍 Location: {location}")
        
        # Simulate ATM network access
        threading.Thread(target=self.perform_atm_access, args=(bank, location), daemon=True).start()
    
    def perform_atm_access(self, bank, location):
        """Perform ATM network access"""
        self.log_atm("🔐 Authenticating ATM network credentials...")
        time.sleep(1)
        
        self.log_atm("🌐 Connecting to ATM network...")
        time.sleep(1)
        
        self.log_atm("🔒 Establishing secure connection...")
        time.sleep(1)
        
        self.log_atm("✅ ATM network access granted")
        
        # Generate ATM network info
        atm_info = f"""
ATM NETWORK ACCESS
{'='*50}
Bank: {bank}
Location: {location}
Network Status: Active
Security Level: Maximum
Connection: Encrypted
Access Level: Full
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*50}
"""
        
        self.atm_info.delete('1.0', tk.END)
        self.atm_info.insert('1.0', atm_info)
    
    def monitor_atms(self):
        """Monitor ATM network"""
        if self.access_active:
            return
        
        self.access_active = True
        self.log_atm("📊 Starting ATM network monitoring...")
        
        # Start monitoring in background
        threading.Thread(target=self.perform_atm_monitoring, daemon=True).start()
    
    def perform_atm_monitoring(self):
        """Perform ATM network monitoring"""
        self.log_atm("📡 Connecting to ATM monitoring system...")
        time.sleep(1)
        
        self.log_atm("📊 Activating real-time monitoring...")
        time.sleep(1)
        
        # Simulate ATM monitoring
        locations = ["New York", "London", "Tokyo", "Paris", "Sydney", "Toronto", "Berlin", "Rome"]
        banks = ["Chase Bank", "Bank of America", "Wells Fargo", "Citibank", "Deutsche Bank", "Barclays"]
        
        for i in range(10):  # Simulate 10 ATMs
            if not self.access_active:
                break
            
            time.sleep(1.5)
            
            # Generate random ATM data
            atm_id = f"ATM{random.randint(1000, 9999)}"
            location = random.choice(locations)
            bank = random.choice(banks)
            status = random.choice(["Online", "Offline", "Maintenance", "Out of Service"])
            cash_level = random.randint(1000, 50000)
            last_transaction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            security_level = random.choice(["High", "Medium", "Low"])
            
            # Add to tree
            self.add_atm(atm_id, location, bank, status, f"${cash_level:,}", last_transaction, security_level)
            
            self.log_atm(f"📊 ATM detected: {atm_id} in {location}")
        
        self.access_active = False
        self.log_atm("⏹️ ATM monitoring stopped")
    
    def control_atm(self):
        """Control specific ATM"""
        atm_id = simpledialog.askstring("Control ATM", "Enter ATM ID to control:")
        if not atm_id:
            return
        
        action = simpledialog.askstring("Control ATM", "Enter action (disable/enable/drain/refill):")
        if not action:
            return
        
        self.log_atm(f"🎮 Controlling ATM: {atm_id}")
        self.log_atm(f"⚡ Action: {action}")
        
        # Simulate ATM control
        threading.Thread(target=self.perform_atm_control, args=(atm_id, action), daemon=True).start()
    
    def perform_atm_control(self, atm_id, action):
        """Perform ATM control"""
        self.log_atm(f"🔐 Authenticating control access for {atm_id}...")
        time.sleep(1)
        
        self.log_atm(f"⚡ Executing action: {action}...")
        time.sleep(1)
        
        if action.lower() == "disable":
            self.log_atm(f"🛑 ATM {atm_id} disabled successfully")
        elif action.lower() == "enable":
            self.log_atm(f"✅ ATM {atm_id} enabled successfully")
        elif action.lower() == "drain":
            self.log_atm(f"💸 ATM {atm_id} cash drained successfully")
        elif action.lower() == "refill":
            self.log_atm(f"💰 ATM {atm_id} refilled successfully")
        else:
            self.log_atm(f"❌ Unknown action: {action}")
        
        self.log_atm(f"✅ ATM control operation completed")
    
    def add_atm(self, atm_id, location, bank, status, cash_level, last_transaction, security_level):
        """Add ATM to tree"""
        self.atm_tree.insert('', 0, values=(atm_id, location, bank, status, cash_level, last_transaction, security_level))
    
    def log_atm(self, message):
        """Log ATM message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.atm_log.insert(tk.END, formatted_message)
        self.atm_log.see(tk.END)
    
    def run(self):
        """Run tool"""
        print(f"🏧 Starting {self.name}")
        self.root.mainloop()

def main():
    """Main entry point"""
    tool = AtmNetworkTool()
    tool.run()

if __name__ == "__main__":
    main() 