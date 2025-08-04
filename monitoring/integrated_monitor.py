"""
INTEGRATED MONITORING SYSTEM
Combines Developmental (AI/ML) and Operational (UI/UX) Monitoring
"""

import time
import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import os

# Import monitoring components
from monitoring.ai_ml_monitor import AIMLMonitor
from monitoring.operational_monitor import OperationalMonitor

logger = logging.getLogger(__name__)


class IntegratedMonitor:
    """Integrated Monitoring System for Both Silos"""
    
    def __init__(self):
        # Initialize both monitoring systems
        self.ai_ml_monitor = AIMLMonitor()
        self.operational_monitor = OperationalMonitor()
        
        # Integrated metrics
        self.integrated_metrics = []
        self.alert_history = []
        
        # Dashboard state
        self.dashboard_running = False
        self.dashboard_thread = None
        
        # Setup logging
        self.setup_logging()
        
        logger.info("Integrated Monitor initialized")
    
    def setup_logging(self):
        """Setup integrated monitoring logging"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/integrated_monitor.log'),
                logging.StreamHandler()
            ]
        )
    
    def start_monitoring(self):
        """Start monitoring both silos"""
        try:
            # Start AI/ML monitoring
            self.ai_ml_monitor.start_monitoring()
            logger.info("AI/ML monitoring started")
            
            # Start operational monitoring
            self.operational_monitor.start_monitoring()
            logger.info("Operational monitoring started")
            
            # Start integrated dashboard
            self.start_dashboard()
            
        except Exception as e:
            logger.error(f"Error starting integrated monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop monitoring both silos"""
        try:
            # Stop AI/ML monitoring
            self.ai_ml_monitor.stop_monitoring()
            
            # Stop operational monitoring
            self.operational_monitor.stop_monitoring()
            
            # Stop dashboard
            self.stop_dashboard()
            
            logger.info("Integrated monitoring stopped")
            
        except Exception as e:
            logger.error(f"Error stopping integrated monitoring: {e}")
    
    def start_dashboard(self):
        """Start the integrated monitoring dashboard"""
        if self.dashboard_running:
            logger.warning("Dashboard already running")
            return
        
        self.dashboard_running = True
        self.dashboard_thread = threading.Thread(target=self._run_dashboard)
        self.dashboard_thread.daemon = True
        self.dashboard_thread.start()
        
        logger.info("Integrated dashboard started")
    
    def stop_dashboard(self):
        """Stop the integrated monitoring dashboard"""
        self.dashboard_running = False
        if self.dashboard_thread:
            self.dashboard_thread.join(timeout=5)
    
    def _run_dashboard(self):
        """Run the monitoring dashboard"""
        try:
            # Create dashboard window
            self.root = tk.Tk()
            self.root.title("🔐 AI Penetration Testing - Integrated Monitor")
            self.root.geometry("1400x900")
            self.root.configure(bg='#1e1e1e')
            
            # Setup dashboard UI
            self.setup_dashboard_ui()
            
            # Start update loop
            self.update_dashboard()
            
            # Run dashboard
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error running dashboard: {e}")
    
    def setup_dashboard_ui(self):
        """Setup dashboard user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🔐 AI Penetration Testing - Integrated Monitor",
                               font=('Consolas', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_ai_ml_tab()
        self.create_operational_tab()
        self.create_alerts_tab()
        self.create_analytics_tab()
    
    def create_overview_tab(self):
        """Create overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Overview")
        
        # System status
        status_frame = ttk.LabelFrame(overview_frame, text="System Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, 
                                                    bg='#2b2b2b', fg='#00ff00',
                                                    font=('Consolas', 10))
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Performance metrics
        metrics_frame = ttk.LabelFrame(overview_frame, text="Performance Metrics", padding=10)
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create metrics display
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, height=15,
                                                     bg='#2b2b2b', fg='#ffffff',
                                                     font=('Consolas', 10))
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
    
    def create_ai_ml_tab(self):
        """Create AI/ML monitoring tab"""
        ai_ml_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_ml_frame, text="🧠 AI/ML Monitor")
        
        # AI/ML metrics
        ai_metrics_frame = ttk.LabelFrame(ai_ml_frame, text="AI/ML Metrics", padding=10)
        ai_metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.ai_ml_text = scrolledtext.ScrolledText(ai_metrics_frame, height=20,
                                                   bg='#2b2b2b', fg='#00ff00',
                                                   font=('Consolas', 10))
        self.ai_ml_text.pack(fill=tk.BOTH, expand=True)
    
    def create_operational_tab(self):
        """Create operational monitoring tab"""
        operational_frame = ttk.Frame(self.notebook)
        self.notebook.add(operational_frame, text="⚙️ Operational Monitor")
        
        # Operational metrics
        op_metrics_frame = ttk.LabelFrame(operational_frame, text="Operational Metrics", padding=10)
        op_metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.operational_text = scrolledtext.ScrolledText(op_metrics_frame, height=20,
                                                         bg='#2b2b2b', fg='#00ff00',
                                                         font=('Consolas', 10))
        self.operational_text.pack(fill=tk.BOTH, expand=True)
    
    def create_alerts_tab(self):
        """Create alerts tab"""
        alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(alerts_frame, text="🚨 Alerts")
        
        # Alerts display
        alerts_display_frame = ttk.LabelFrame(alerts_frame, text="Active Alerts", padding=10)
        alerts_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.alerts_text = scrolledtext.ScrolledText(alerts_display_frame, height=20,
                                                    bg='#2b2b2b', fg='#ff0000',
                                                    font=('Consolas', 10))
        self.alerts_text.pack(fill=tk.BOTH, expand=True)
    
    def create_analytics_tab(self):
        """Create analytics tab with charts"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="📈 Analytics")
        
        # Create matplotlib figure
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor('#2b2b2b')
        
        # Create canvas
        canvas = FigureCanvasTkAgg(self.fig, analytics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = canvas
    
    def update_dashboard(self):
        """Update dashboard with latest metrics"""
        if not self.dashboard_running:
            return
        
        try:
            # Update overview
            self.update_overview()
            
            # Update AI/ML tab
            self.update_ai_ml_tab()
            
            # Update operational tab
            self.update_operational_tab()
            
            # Update alerts
            self.update_alerts_tab()
            
            # Update analytics
            self.update_analytics()
            
            # Schedule next update
            self.root.after(5000, self.update_dashboard)  # Update every 5 seconds
            
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")
    
    def update_overview(self):
        """Update overview tab"""
        try:
            # Get system status
            ai_ml_status = "🟢 Active" if self.ai_ml_monitor.is_monitoring else "🔴 Inactive"
            operational_status = "🟢 Active" if self.operational_monitor.is_monitoring else "🔴 Inactive"
            
            status_info = f"""
System Overview - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

🧠 AI/ML Monitor: {ai_ml_status}
⚙️  Operational Monitor: {operational_status}
📊 Dashboard: {'🟢 Active' if self.dashboard_running else '🔴 Inactive'}

System Health:
- AI Models: {len(self.ai_ml_monitor.model_metrics)} active
- User Sessions: {len(self.operational_monitor.user_sessions)} active
- Total Alerts: {len(self.get_all_alerts())} active

Performance Summary:
- AI Accuracy: {self.get_ai_accuracy():.2%}
- UI Response Time: {self.get_ui_response_time():.2f}s
- System Uptime: {self.get_system_uptime():.1f}s
"""
            
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, status_info)
            
            # Update metrics
            metrics_info = self.get_integrated_metrics()
            self.metrics_text.delete(1.0, tk.END)
            self.metrics_text.insert(tk.END, metrics_info)
            
        except Exception as e:
            logger.error(f"Error updating overview: {e}")
    
    def update_ai_ml_tab(self):
        """Update AI/ML monitoring tab"""
        try:
            # Get AI/ML metrics
            ai_ml_report = self.ai_ml_monitor.generate_monitoring_report()
            
            # Format for display
            ai_ml_info = f"""
AI/ML Monitoring Report
{'='*30}

Model Performance:
{json.dumps(ai_ml_report.get('model_performance', {}), indent=2)}

Learning Progress:
{json.dumps(ai_ml_report.get('learning_progress', {}), indent=2)}

System Health:
{json.dumps(ai_ml_report.get('system_health', {}), indent=2)}

Metrics Summary:
{json.dumps(ai_ml_report.get('metrics_summary', {}), indent=2)}
"""
            
            self.ai_ml_text.delete(1.0, tk.END)
            self.ai_ml_text.insert(tk.END, ai_ml_info)
            
        except Exception as e:
            logger.error(f"Error updating AI/ML tab: {e}")
    
    def update_operational_tab(self):
        """Update operational monitoring tab"""
        try:
            # Get operational metrics
            operational_report = self.operational_monitor.generate_operational_report()
            
            # Format for display
            operational_info = f"""
Operational Monitoring Report
{'='*35}

UI Performance:
{json.dumps(operational_report.get('ui_performance', {}), indent=2)}

User Interactions:
{json.dumps(operational_report.get('user_interactions', {}), indent=2)}

System Operations:
{json.dumps(operational_report.get('system_operations', {}), indent=2)}

Metrics Summary:
{json.dumps(operational_report.get('metrics_summary', {}), indent=2)}
"""
            
            self.operational_text.delete(1.0, tk.END)
            self.operational_text.insert(tk.END, operational_info)
            
        except Exception as e:
            logger.error(f"Error updating operational tab: {e}")
    
    def update_alerts_tab(self):
        """Update alerts tab"""
        try:
            # Get all alerts
            alerts = self.get_all_alerts()
            
            if not alerts:
                alerts_info = "No active alerts at this time."
            else:
                alerts_info = "Active Alerts:\n" + "="*20 + "\n\n"
                for alert in alerts[-10:]:  # Show last 10 alerts
                    alerts_info += f"🚨 {alert.get('type', 'Unknown')}\n"
                    alerts_info += f"   Message: {alert.get('message', 'No message')}\n"
                    alerts_info += f"   Time: {alert.get('timestamp', 'Unknown')}\n"
                    alerts_info += f"   Severity: {alert.get('severity', 'Unknown')}\n"
                    alerts_info += "-" * 30 + "\n"
            
            self.alerts_text.delete(1.0, tk.END)
            self.alerts_text.insert(tk.END, alerts_info)
            
        except Exception as e:
            logger.error(f"Error updating alerts tab: {e}")
    
    def update_analytics(self):
        """Update analytics charts"""
        try:
            # Clear previous plots
            for ax in self.axes.flat:
                ax.clear()
            
            # Get data for charts
            ai_metrics = self.ai_ml_monitor.ai_metrics
            operational_metrics = self.operational_monitor.operational_metrics
            
            if ai_metrics:
                # AI Accuracy over time
                timestamps = [m.timestamp for m in ai_metrics[-20:]]
                accuracies = [m.average_accuracy for m in ai_metrics[-20:]]
                
                self.axes[0, 0].plot(timestamps, accuracies, 'g-', linewidth=2)
                self.axes[0, 0].set_title('AI Model Accuracy Over Time', color='white')
                self.axes[0, 0].set_ylabel('Accuracy', color='white')
                self.axes[0, 0].tick_params(colors='white')
                self.axes[0, 0].grid(True, alpha=0.3)
            
            if operational_metrics:
                # UI Response Time over time
                timestamps = [m.timestamp for m in operational_metrics[-20:]]
                response_times = [m.average_response_time for m in operational_metrics[-20:]]
                
                self.axes[0, 1].plot(timestamps, response_times, 'b-', linewidth=2)
                self.axes[0, 1].set_title('UI Response Time Over Time', color='white')
                self.axes[0, 1].set_ylabel('Response Time (s)', color='white')
                self.axes[0, 1].tick_params(colors='white')
                self.axes[0, 1].grid(True, alpha=0.3)
            
            # System Health pie chart
            health_data = self.get_system_health_distribution()
            if health_data:
                labels = list(health_data.keys())
                sizes = list(health_data.values())
                colors = ['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6']
                
                self.axes[1, 0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
                self.axes[1, 0].set_title('System Health Distribution', color='white')
            
            # Alert distribution
            alert_data = self.get_alert_distribution()
            if alert_data:
                alert_types = list(alert_data.keys())
                alert_counts = list(alert_data.values())
                
                self.axes[1, 1].bar(alert_types, alert_counts, color=['#e74c3c', '#f39c12', '#3498db'])
                self.axes[1, 1].set_title('Alert Distribution', color='white')
                self.axes[1, 1].set_ylabel('Count', color='white')
                self.axes[1, 1].tick_params(colors='white')
                self.axes[1, 1].tick_params(axis='x', rotation=45)
            
            # Update canvas
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            logger.error(f"Error updating analytics: {e}")
    
    def get_all_alerts(self) -> List[Dict]:
        """Get all alerts from both monitoring systems"""
        alerts = []
        
        try:
            # Get AI/ML alerts
            ai_alerts = self.ai_ml_monitor._load_alerts()
            alerts.extend(ai_alerts)
            
            # Get operational alerts
            op_alerts = self.operational_monitor._load_operational_alerts()
            alerts.extend(op_alerts)
            
            # Sort by timestamp
            alerts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
        except Exception as e:
            logger.error(f"Error getting all alerts: {e}")
        
        return alerts
    
    def get_ai_accuracy(self) -> float:
        """Get current AI accuracy"""
        try:
            if self.ai_ml_monitor.ai_metrics:
                return self.ai_ml_monitor.ai_metrics[-1].average_accuracy
            return 0.0
        except:
            return 0.0
    
    def get_ui_response_time(self) -> float:
        """Get current UI response time"""
        try:
            if self.operational_monitor.operational_metrics:
                return self.operational_monitor.operational_metrics[-1].average_response_time
            return 0.0
        except:
            return 0.0
    
    def get_system_uptime(self) -> float:
        """Get system uptime"""
        try:
            return time.time() - self.ai_ml_monitor._get_start_time()
        except:
            return 0.0
    
    def get_integrated_metrics(self) -> str:
        """Get integrated metrics summary"""
        try:
            return f"""
Integrated Metrics Summary
{'='*30}

AI/ML Metrics:
- Total Models: {len(self.ai_ml_monitor.model_metrics)}
- Learning Rate: {self.get_ai_accuracy():.2%}
- Pattern Discovery: {len(self.ai_ml_monitor.unsupervised_learning.success_patterns) if hasattr(self.ai_ml_monitor, 'unsupervised_learning') else 0}

Operational Metrics:
- Active Users: {len(self.operational_monitor.user_sessions)}
- UI Performance: {self.get_ui_response_time():.2f}s
- System Operations: {len(self.operational_monitor.system_operations)}

Overall Health:
- System Status: {'🟢 Healthy' if self.get_system_health_score() > 0.8 else '🟡 Warning' if self.get_system_health_score() > 0.6 else '🔴 Critical'}
- Health Score: {self.get_system_health_score():.1%}
"""
        except Exception as e:
            return f"Error getting integrated metrics: {e}"
    
    def get_system_health_score(self) -> float:
        """Calculate overall system health score"""
        try:
            # AI/ML health
            ai_accuracy = self.get_ai_accuracy()
            
            # Operational health
            ui_response = self.get_ui_response_time()
            ui_health = max(0, 1 - (ui_response / 2))  # 2s = 0 health
            
            # Combined score
            return (ai_accuracy * 0.6) + (ui_health * 0.4)
            
        except:
            return 0.0
    
    def get_system_health_distribution(self) -> Dict:
        """Get system health distribution"""
        try:
            return {
                'Excellent': 0.4,
                'Good': 0.3,
                'Fair': 0.2,
                'Poor': 0.1
            }
        except:
            return {}
    
    def get_alert_distribution(self) -> Dict:
        """Get alert distribution"""
        try:
            alerts = self.get_all_alerts()
            distribution = {}
            
            for alert in alerts:
                alert_type = alert.get('type', 'Unknown')
                distribution[alert_type] = distribution.get(alert_type, 0) + 1
            
            return distribution
        except:
            return {}
    
    def export_integrated_report(self, filename: str = None):
        """Export integrated monitoring report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"integrated_monitoring_report_{timestamp}.json"
        
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'ai_ml_report': self.ai_ml_monitor.generate_monitoring_report(),
                'operational_report': self.operational_monitor.generate_operational_report(),
                'integrated_metrics': {
                    'system_health_score': self.get_system_health_score(),
                    'ai_accuracy': self.get_ai_accuracy(),
                    'ui_response_time': self.get_ui_response_time(),
                    'system_uptime': self.get_system_uptime(),
                    'total_alerts': len(self.get_all_alerts())
                },
                'alerts': self.get_all_alerts()
            }
            
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"Integrated report exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting integrated report: {e}")


def main():
    """Main function to run integrated monitoring"""
    try:
        # Create and start integrated monitor
        monitor = IntegratedMonitor()
        monitor.start_monitoring()
        
        print("🔐 Integrated Monitoring System Started")
        print("📊 Dashboard will open automatically")
        print("🛑 Press Ctrl+C to stop monitoring")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping integrated monitoring...")
            monitor.stop_monitoring()
            print("✅ Monitoring stopped")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 