#!/usr/bin/env python3
"""
BANKING TOOLS EXPORT SYSTEM
Comprehensive export functionality for all banking tools results
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import csv
import os
from datetime import datetime
import threading
import time

class BankingToolsExportSystem:
    def __init__(self):
        self.name = "Banking Tools Export System"
        self.version = "2.0.0"
        self.export_active = False
        
        # Sample data from banking tools
        self.sample_data = {
            "account_manipulation": {
                "tool_name": "Account Manipulation Tool",
                "operations": [
                    {
                        "account_number": "1000000001",
                        "bank": "Chase Bank",
                        "balance": "$45,678",
                        "status": "Active",
                        "access_level": "Full Access",
                        "operation": "Account Access",
                        "timestamp": "2024-01-15 14:30:25"
                    },
                    {
                        "account_number": "1000000002",
                        "bank": "Bank of America",
                        "balance": "$123,456",
                        "status": "Active",
                        "access_level": "Full Access",
                        "operation": "Balance Modification",
                        "timestamp": "2024-01-15 14:32:10"
                    }
                ]
            },
            "transaction_monitoring": {
                "tool_name": "Transaction Monitoring Tool",
                "operations": [
                    {
                        "account": "1000000001",
                        "transaction_id": "TXN123456",
                        "amount": "$1,250",
                        "type": "Deposit",
                        "status": "Completed",
                        "timestamp": "2024-01-15 14:35:42"
                    },
                    {
                        "account": "1000000002",
                        "transaction_id": "TXN123457",
                        "amount": "$500",
                        "type": "Withdrawal",
                        "status": "Completed",
                        "timestamp": "2024-01-15 14:36:15"
                    }
                ]
            },
            "swift_access": {
                "tool_name": "SWIFT Access Tool",
                "operations": [
                    {
                        "message_id": "SWIFT123456",
                        "source_bank": "Chase Bank",
                        "target_bank": "Deutsche Bank",
                        "amount": "50,000 EUR",
                        "currency": "EUR",
                        "status": "Sent",
                        "direction": "Outbound",
                        "timestamp": "2024-01-15 14:40:30"
                    },
                    {
                        "message_id": "SWIFT123457",
                        "source_bank": "Barclays",
                        "target_bank": "Bank of America",
                        "amount": "25,000 GBP",
                        "currency": "GBP",
                        "status": "Received",
                        "direction": "Inbound",
                        "timestamp": "2024-01-15 14:42:15"
                    }
                ]
            },
            "atm_network": {
                "tool_name": "ATM Network Tool",
                "operations": [
                    {
                        "atm_id": "ATM1234",
                        "location": "New York",
                        "bank": "Chase Bank",
                        "status": "Online",
                        "cash_level": "$45,000",
                        "last_transaction": "2024-01-15 14:45:20",
                        "security_level": "High"
                    },
                    {
                        "atm_id": "ATM5678",
                        "location": "London",
                        "bank": "Barclays",
                        "status": "Online",
                        "cash_level": "£30,000",
                        "last_transaction": "2024-01-15 14:46:30",
                        "security_level": "High"
                    }
                ]
            },
            "credit_card": {
                "tool_name": "Credit Card Operations Tool",
                "operations": [
                    {
                        "card_number": "**** **** **** 1234",
                        "bank": "Chase Bank",
                        "type": "Visa",
                        "limit": "$25,000",
                        "balance": "$8,500",
                        "status": "Active",
                        "expiry": "12/26"
                    },
                    {
                        "card_number": "**** **** **** 5678",
                        "bank": "Bank of America",
                        "type": "Mastercard",
                        "limit": "$30,000",
                        "balance": "$12,300",
                        "status": "Active",
                        "expiry": "09/25"
                    }
                ]
            },
            "cryptocurrency": {
                "tool_name": "Cryptocurrency Operations Tool",
                "operations": [
                    {
                        "wallet": "BTC123456",
                        "currency": "Bitcoin",
                        "balance": "2.4567",
                        "transactions": "45",
                        "status": "Active",
                        "last_activity": "2024-01-15 14:50:10",
                        "value_usd": "$98,268.00"
                    },
                    {
                        "wallet": "ETH789012",
                        "currency": "Ethereum",
                        "balance": "15.7890",
                        "transactions": "32",
                        "status": "Active",
                        "last_activity": "2024-01-15 14:51:25",
                        "value_usd": "$47,367.00"
                    }
                ]
            }
        }
        
        self.init_export_system()
    
    def init_export_system(self):
        """Initialize export system"""
        self.root = tk.Tk()
        self.root.title(f"📊 {self.name}")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0d1117')
        
        self.create_export_interface()
    
    def create_export_interface(self):
        """Create export interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#0d1117')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="📊 BANKING TOOLS EXPORT SYSTEM",
            font=('Segoe UI', 24, 'bold'),
            fg='#4ecdc4',
            bg='#0d1117'
        )
        header_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Comprehensive Export Functionality for All Banking Tools",
            font=('Segoe UI', 14),
            fg='#ffffff',
            bg='#0d1117'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = tk.LabelFrame(
            main_frame,
            text="🎛️ EXPORT CONTROLS",
            font=('Segoe UI', 12, 'bold'),
            fg='#ff9ff3',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Tool selection
        tools_frame = tk.Frame(control_frame, bg='#0d1117')
        tools_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            tools_frame,
            text="Select Banking Tools to Export:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(anchor='w', pady=2)
        
        # Tool checkboxes
        self.tool_vars = {}
        tool_configs = [
            ("account_manipulation", "💳 Account Manipulation", "Account access and manipulation data"),
            ("transaction_monitoring", "📊 Transaction Monitoring", "Real-time transaction data"),
            ("swift_access", "🌍 SWIFT Access", "International banking network data"),
            ("atm_network", "🏧 ATM Network", "ATM system access and control data"),
            ("credit_card", "💳 Credit Card Operations", "Credit card data and operations"),
            ("cryptocurrency", "₿ Cryptocurrency Operations", "Digital currency operations data")
        ]
        
        for tool_id, name, desc in tool_configs:
            var = tk.BooleanVar(value=True)
            self.tool_vars[tool_id] = var
            
            tool_frame = tk.Frame(tools_frame, bg='#0d1117')
            tool_frame.pack(fill='x', pady=2)
            
            cb = tk.Checkbutton(
                tool_frame,
                text=name,
                variable=var,
                font=('Segoe UI', 10, 'bold'),
                fg='#c9d1d9',
                bg='#0d1117',
                selectcolor='#21262d',
                activebackground='#0d1117',
                activeforeground='#c9d1d9'
            )
            cb.pack(side='left')
            
            tk.Label(
                tool_frame,
                text=f"- {desc}",
                font=('Segoe UI', 9),
                fg='#7d8590',
                bg='#0d1117'
            ).pack(side='left', padx=(10, 0))
        
        # Format selection
        format_frame = tk.Frame(control_frame, bg='#0d1117')
        format_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            format_frame,
            text="Export Format:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#0d1117'
        ).pack(anchor='w', pady=2)
        
        self.format_var = tk.StringVar(value="JSON")
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=["JSON", "CSV", "TXT", "All Formats"],
            state="readonly",
            font=('Segoe UI', 12)
        )
        format_combo.pack(fill='x', pady=2)
        
        # Action buttons
        action_frame = tk.Frame(control_frame, bg='#0d1117')
        action_frame.pack(fill='x', pady=10)
        
        # Export all button
        self.export_all_btn = tk.Button(
            action_frame,
            text="📊 EXPORT ALL RESULTS",
            command=self.export_all_results,
            bg='#4ecdc4',
            fg='#000000',
            font=('Segoe UI', 14, 'bold'),
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.export_all_btn.pack(side='left', padx=5)
        
        # Export selected button
        self.export_selected_btn = tk.Button(
            action_frame,
            text="📋 EXPORT SELECTED",
            command=self.export_selected_results,
            bg='#ff9ff3',
            fg='#000000',
            font=('Segoe UI', 14, 'bold'),
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.export_selected_btn.pack(side='left', padx=5)
        
        # Preview data button
        self.preview_btn = tk.Button(
            action_frame,
            text="👁️ PREVIEW DATA",
            command=self.preview_data,
            bg='#96ceb4',
            fg='#000000',
            font=('Segoe UI', 14, 'bold'),
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.preview_btn.pack(side='left', padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 EXPORT RESULTS",
            font=('Segoe UI', 12, 'bold'),
            fg='#45b7d1',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Results notebook
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create result tabs
        self.create_export_preview_tab()
        self.create_export_log_tab()
        
        # Log area
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 EXPORT LOG",
            font=('Segoe UI', 12, 'bold'),
            fg='#96ceb4',
            bg='#0d1117',
            bd=1,
            relief='solid'
        )
        log_frame.pack(fill='x', padx=10, pady=5)
        
        self.export_log = scrolledtext.ScrolledText(
            log_frame,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=6
        )
        self.export_log.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_export("📊 Banking Tools Export System initialized")
        self.log_export("🚀 Ready for comprehensive data export")
    
    def create_export_preview_tab(self):
        """Create export preview tab"""
        preview_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(preview_frame, text="👁️ Export Preview")
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.preview_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_export_log_tab(self):
        """Create export log tab"""
        log_frame = tk.Frame(self.results_notebook, bg='#161b22')
        self.results_notebook.add(log_frame, text="📝 Export Log")
        
        self.export_log_text = scrolledtext.ScrolledText(
            log_frame,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.export_log_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def export_all_results(self):
        """Export all results"""
        self.log_export("📊 Starting export of all banking tools results...")
        
        # Start export in background
        threading.Thread(target=self.perform_export_all, daemon=True).start()
    
    def perform_export_all(self):
        """Perform export of all results"""
        try:
            # Get export format
            export_format = self.format_var.get()
            
            # Create export directory
            export_dir = f"banking_tools_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(export_dir, exist_ok=True)
            
            self.log_export(f"📁 Created export directory: {export_dir}")
            
            # Export each tool's data
            for tool_id, data in self.sample_data.items():
                if self.export_active:
                    break
                
                self.log_export(f"📊 Exporting {data['tool_name']} data...")
                
                if export_format == "JSON" or export_format == "All Formats":
                    self.export_to_json(data, tool_id, export_dir)
                
                if export_format == "CSV" or export_format == "All Formats":
                    self.export_to_csv(data, tool_id, export_dir)
                
                if export_format == "TXT" or export_format == "All Formats":
                    self.export_to_txt(data, tool_id, export_dir)
                
                time.sleep(0.5)
            
            # Create summary report
            self.create_summary_report(export_dir)
            
            self.log_export("✅ All exports completed successfully!")
            self.log_export(f"📁 Export directory: {os.path.abspath(export_dir)}")
            
            messagebox.showinfo(
                "Export Complete",
                f"✅ All banking tools results exported successfully!\n\n"
                f"📁 Export directory: {os.path.abspath(export_dir)}\n"
                f"📊 Format: {export_format}\n"
                f"📋 Tools exported: {len(self.sample_data)}"
            )
            
        except Exception as e:
            self.log_export(f"❌ Export error: {str(e)}")
            messagebox.showerror("Export Error", f"Export failed: {str(e)}")
    
    def export_selected_results(self):
        """Export selected results"""
        selected_tools = [tool_id for tool_id, var in self.tool_vars.items() if var.get()]
        
        if not selected_tools:
            messagebox.showwarning("No Selection", "Please select at least one tool to export")
            return
        
        self.log_export(f"📊 Starting export of selected tools: {', '.join(selected_tools)}")
        
        # Start export in background
        threading.Thread(target=self.perform_export_selected, args=(selected_tools,), daemon=True).start()
    
    def perform_export_selected(self, selected_tools):
        """Perform export of selected results"""
        try:
            # Get export format
            export_format = self.format_var.get()
            
            # Create export directory
            export_dir = f"banking_tools_selected_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(export_dir, exist_ok=True)
            
            self.log_export(f"📁 Created export directory: {export_dir}")
            
            # Export selected tools' data
            for tool_id in selected_tools:
                if tool_id in self.sample_data:
                    data = self.sample_data[tool_id]
                    self.log_export(f"📊 Exporting {data['tool_name']} data...")
                    
                    if export_format == "JSON" or export_format == "All Formats":
                        self.export_to_json(data, tool_id, export_dir)
                    
                    if export_format == "CSV" or export_format == "All Formats":
                        self.export_to_csv(data, tool_id, export_dir)
                    
                    if export_format == "TXT" or export_format == "All Formats":
                        self.export_to_txt(data, tool_id, export_dir)
                    
                    time.sleep(0.5)
            
            # Create summary report
            self.create_summary_report(export_dir, selected_tools)
            
            self.log_export("✅ Selected exports completed successfully!")
            self.log_export(f"📁 Export directory: {os.path.abspath(export_dir)}")
            
            messagebox.showinfo(
                "Export Complete",
                f"✅ Selected banking tools results exported successfully!\n\n"
                f"📁 Export directory: {os.path.abspath(export_dir)}\n"
                f"📊 Format: {export_format}\n"
                f"📋 Tools exported: {len(selected_tools)}"
            )
            
        except Exception as e:
            self.log_export(f"❌ Export error: {str(e)}")
            messagebox.showerror("Export Error", f"Export failed: {str(e)}")
    
    def export_to_json(self, data, tool_id, export_dir):
        """Export data to JSON format"""
        filename = os.path.join(export_dir, f"{tool_id}_results.json")
        
        export_data = {
            "export_info": {
                "tool_name": data["tool_name"],
                "export_timestamp": datetime.now().isoformat(),
                "format": "JSON",
                "version": self.version
            },
            "operations": data["operations"]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.log_export(f"📄 JSON export: {filename}")
    
    def export_to_csv(self, data, tool_id, export_dir):
        """Export data to CSV format"""
        filename = os.path.join(export_dir, f"{tool_id}_results.csv")
        
        if data["operations"]:
            fieldnames = data["operations"][0].keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data["operations"])
        
        self.log_export(f"📄 CSV export: {filename}")
    
    def export_to_txt(self, data, tool_id, export_dir):
        """Export data to TXT format"""
        filename = os.path.join(export_dir, f"{tool_id}_results.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"BANKING TOOLS EXPORT REPORT\n")
            f.write(f"{'='*50}\n")
            f.write(f"Tool: {data['tool_name']}\n")
            f.write(f"Export Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Format: TXT\n")
            f.write(f"Version: {self.version}\n")
            f.write(f"{'='*50}\n\n")
            
            for i, operation in enumerate(data["operations"], 1):
                f.write(f"Operation {i}:\n")
                f.write(f"{'-'*30}\n")
                for key, value in operation.items():
                    f.write(f"{key}: {value}\n")
                f.write(f"\n")
        
        self.log_export(f"📄 TXT export: {filename}")
    
    def create_summary_report(self, export_dir, selected_tools=None):
        """Create summary report"""
        filename = os.path.join(export_dir, "export_summary.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"BANKING TOOLS EXPORT SUMMARY\n")
            f.write(f"{'='*50}\n")
            f.write(f"Export Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Export Directory: {os.path.abspath(export_dir)}\n")
            f.write(f"Export Format: {self.format_var.get()}\n")
            f.write(f"System Version: {self.version}\n")
            f.write(f"{'='*50}\n\n")
            
            if selected_tools:
                f.write(f"Tools Exported: {len(selected_tools)}\n")
                for tool_id in selected_tools:
                    if tool_id in self.sample_data:
                        f.write(f"  - {self.sample_data[tool_id]['tool_name']}\n")
            else:
                f.write(f"Tools Exported: {len(self.sample_data)}\n")
                for tool_id, data in self.sample_data.items():
                    f.write(f"  - {data['tool_name']}\n")
            
            f.write(f"\nFiles Generated:\n")
            for file in os.listdir(export_dir):
                f.write(f"  - {file}\n")
        
        self.log_export(f"📄 Summary report: {filename}")
    
    def preview_data(self):
        """Preview export data"""
        self.log_export("👁️ Generating data preview...")
        
        preview_content = "BANKING TOOLS EXPORT PREVIEW\n"
        preview_content += "="*50 + "\n\n"
        
        for tool_id, data in self.sample_data.items():
            preview_content += f"Tool: {data['tool_name']}\n"
            preview_content += f"Operations: {len(data['operations'])}\n"
            preview_content += "-"*30 + "\n"
            
            for i, operation in enumerate(data['operations'][:2], 1):  # Show first 2 operations
                preview_content += f"Operation {i}:\n"
                for key, value in operation.items():
                    preview_content += f"  {key}: {value}\n"
                preview_content += "\n"
            
            preview_content += "\n"
        
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview_content)
        
        self.log_export("✅ Data preview generated")
    
    def log_export(self, message):
        """Log export message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.export_log.insert(tk.END, formatted_message)
        self.export_log.see(tk.END)
        
        # Also log to export log tab
        self.export_log_text.insert(tk.END, formatted_message)
        self.export_log_text.see(tk.END)
    
    def run(self):
        """Run export system"""
        print(f"📊 Starting {self.name}")
        self.root.mainloop()

def main():
    """Main entry point"""
    export_system = BankingToolsExportSystem()
    export_system.run()

if __name__ == "__main__":
    main() 