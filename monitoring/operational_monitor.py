"""
OPERATIONAL SILO - Operational Monitoring System
Monitors UI/UX performance, user interactions, and system operations
"""

import time
import json
import threading
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import tkinter as tk
from tkinter import ttk
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class UIMetrics:
    """UI/UX Performance Metrics"""
    response_time: float
    render_time: float
    user_interactions: int
    errors_count: int
    active_users: int
    timestamp: datetime
    ui_component: str
    operation_type: str


@dataclass
class UserInteractionMetrics:
    """User Interaction Metrics"""
    user_id: str
    action_type: str
    target_component: str
    response_time: float
    success: bool
    error_message: str
    timestamp: datetime
    session_duration: float


@dataclass
class SystemOperationMetrics:
    """System Operation Metrics"""
    operation_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    success: bool
    error_count: int
    timestamp: datetime
    operation_type: str


@dataclass
class OperationalMetrics:
    """Overall Operational Metrics"""
    total_users: int
    active_sessions: int
    average_response_time: float
    error_rate: float
    system_uptime: float
    timestamp: datetime


class OperationalMonitor:
    """Operational Monitoring System for Operational Silo"""
    
    def __init__(self, metrics_history_size: int = 1000):
        self.metrics_history_size = metrics_history_size
        self.ui_metrics = deque(maxlen=metrics_history_size)
        self.user_interactions = deque(maxlen=metrics_history_size)
        self.system_operations = deque(maxlen=metrics_history_size)
        self.operational_metrics = deque(maxlen=metrics_history_size)
        
        # Performance tracking
        self.performance_history = defaultdict(list)
        self.user_sessions = defaultdict(dict)
        self.error_log = deque(maxlen=metrics_history_size)
        
        # Alert thresholds
        self.alert_thresholds = {
            'response_time_threshold': 2.0,  # seconds
            'error_rate_threshold': 0.05,    # 5%
            'memory_usage_threshold': 0.8,   # 80%
            'cpu_usage_threshold': 0.9,      # 90%
            'user_satisfaction_threshold': 0.7  # 70%
        }
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread = None
        self.monitoring_interval = 15  # seconds
        
        # UI performance tracking
        self.ui_start_times = {}
        self.ui_components = {}
        
        # Setup logging
        self.setup_logging()
        
        logger.info("Operational Monitor initialized")
    
    def setup_logging(self):
        """Setup monitoring-specific logging"""
        monitor_logger = logging.getLogger('operational_monitor')
        monitor_logger.setLevel(logging.INFO)
        
        # Create file handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = logging.FileHandler('logs/operational_monitor.log')
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        monitor_logger.addHandler(file_handler)
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if self.is_monitoring:
            logger.warning("Operational monitoring already running")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        logger.info("Operational monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("Operational monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect UI metrics
                self._collect_ui_metrics()
                
                # Collect system operation metrics
                self._collect_system_operation_metrics()
                
                # Collect user interaction metrics
                self._collect_user_interaction_metrics()
                
                # Check for alerts
                self._check_operational_alerts()
                
                # Generate operational reports
                self._generate_operational_report()
                
                # Clean up old sessions
                self._cleanup_old_sessions()
                
                # Wait for next interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in operational monitoring loop: {e}")
                time.sleep(5)
    
    def _collect_ui_metrics(self):
        """Collect UI/UX performance metrics"""
        try:
            # Simulate UI metrics collection
            ui_components = ['main_window', 'attack_panel', 'results_panel', 'settings_panel']
            
            for component in ui_components:
                ui_metric = UIMetrics(
                    response_time=np.random.uniform(0.1, 1.0),
                    render_time=np.random.uniform(0.05, 0.5),
                    user_interactions=np.random.randint(0, 10),
                    errors_count=np.random.randint(0, 3),
                    active_users=len(self.user_sessions),
                    timestamp=datetime.now(),
                    ui_component=component,
                    operation_type='render'
                )
                
                self.ui_metrics.append(ui_metric)
                
        except Exception as e:
            logger.error(f"Error collecting UI metrics: {e}")
    
    def _collect_system_operation_metrics(self):
        """Collect system operation metrics"""
        try:
            # Get system resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Simulate system operations
            operations = [
                'data_mining', 'pattern_analysis', 'model_training',
                'attack_execution', 'report_generation', 'user_authentication'
            ]
            
            for operation in operations:
                operation_metric = SystemOperationMetrics(
                    operation_name=operation,
                    execution_time=np.random.uniform(0.1, 5.0),
                    memory_usage=memory_percent / 100,
                    cpu_usage=cpu_percent / 100,
                    success=np.random.choice([True, False], p=[0.95, 0.05]),
                    error_count=np.random.randint(0, 2),
                    timestamp=datetime.now(),
                    operation_type='background'
                )
                
                self.system_operations.append(operation_metric)
                
        except Exception as e:
            logger.error(f"Error collecting system operation metrics: {e}")
    
    def _collect_user_interaction_metrics(self):
        """Collect user interaction metrics"""
        try:
            # Simulate user interactions
            interaction_types = [
                'button_click', 'form_submit', 'tab_switch', 'menu_selection',
                'data_input', 'file_upload', 'settings_change'
            ]
            
            for interaction_type in interaction_types:
                if np.random.random() < 0.3:  # 30% chance of interaction
                    user_interaction = UserInteractionMetrics(
                        user_id=f"user_{np.random.randint(1, 100)}",
                        action_type=interaction_type,
                        target_component=np.random.choice(['main', 'attack', 'results', 'settings']),
                        response_time=np.random.uniform(0.1, 2.0),
                        success=np.random.choice([True, False], p=[0.9, 0.1]),
                        error_message="" if np.random.random() > 0.1 else "Operation failed",
                        timestamp=datetime.now(),
                        session_duration=np.random.uniform(60, 3600)  # 1 min to 1 hour
                    )
                    
                    self.user_interactions.append(user_interaction)
                    
        except Exception as e:
            logger.error(f"Error collecting user interaction metrics: {e}")
    
    def _check_operational_alerts(self):
        """Check for operational alert conditions"""
        try:
            if not self.ui_metrics:
                return
            
            # Check response time
            recent_ui_metrics = list(self.ui_metrics)[-10:]
            avg_response_time = np.mean([m.response_time for m in recent_ui_metrics])
            
            if avg_response_time > self.alert_thresholds['response_time_threshold']:
                self._trigger_operational_alert(
                    'HIGH_RESPONSE_TIME',
                    f"Average response time: {avg_response_time:.2f}s"
                )
            
            # Check error rate
            total_errors = sum([m.errors_count for m in recent_ui_metrics])
            total_operations = len(recent_ui_metrics)
            error_rate = total_errors / total_operations if total_operations > 0 else 0
            
            if error_rate > self.alert_thresholds['error_rate_threshold']:
                self._trigger_operational_alert(
                    'HIGH_ERROR_RATE',
                    f"Error rate: {error_rate:.2%}"
                )
            
            # Check system operations
            if self.system_operations:
                recent_operations = list(self.system_operations)[-10:]
                failed_operations = [op for op in recent_operations if not op.success]
                
                if len(failed_operations) > 2:
                    self._trigger_operational_alert(
                        'SYSTEM_OPERATION_FAILURES',
                        f"{len(failed_operations)} failed operations detected"
                    )
            
        except Exception as e:
            logger.error(f"Error checking operational alerts: {e}")
    
    def _trigger_operational_alert(self, alert_type: str, message: str):
        """Trigger an operational alert"""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'severity': 'HIGH' if 'HIGH' in alert_type else 'MEDIUM',
            'silo': 'operational'
        }
        
        logger.warning(f"OPERATIONAL ALERT: {alert_type} - {message}")
        
        # Save alert to file
        self._save_operational_alert(alert)
        
        # Log error
        self.error_log.append({
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def _save_operational_alert(self, alert: Dict):
        """Save operational alert to file"""
        try:
            alert_file = 'logs/operational_alerts.json'
            
            # Load existing alerts
            alerts = []
            if os.path.exists(alert_file):
                with open(alert_file, 'r') as f:
                    alerts = json.load(f)
            
            # Add new alert
            alerts.append(alert)
            
            # Save back to file
            with open(alert_file, 'w') as f:
                json.dump(alerts, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving operational alert: {e}")
    
    def _generate_operational_report(self):
        """Generate operational performance report"""
        try:
            if not self.ui_metrics:
                return
            
            # Calculate operational metrics
            recent_ui_metrics = list(self.ui_metrics)[-10:]
            recent_user_interactions = list(self.user_interactions)[-10:]
            recent_system_operations = list(self.system_operations)[-10:]
            
            # UI Performance
            avg_response_time = np.mean([m.response_time for m in recent_ui_metrics])
            avg_render_time = np.mean([m.render_time for m in recent_ui_metrics])
            total_errors = sum([m.errors_count for m in recent_ui_metrics])
            
            # User Interactions
            successful_interactions = len([i for i in recent_user_interactions if i.success])
            total_interactions = len(recent_user_interactions)
            success_rate = successful_interactions / total_interactions if total_interactions > 0 else 0
            
            # System Operations
            successful_operations = len([op for op in recent_system_operations if op.success])
            total_operations = len(recent_system_operations)
            operation_success_rate = successful_operations / total_operations if total_operations > 0 else 0
            
            # Create operational metrics
            operational_metric = OperationalMetrics(
                total_users=len(set([i.user_id for i in recent_user_interactions])),
                active_sessions=len(self.user_sessions),
                average_response_time=avg_response_time,
                error_rate=total_errors / len(recent_ui_metrics) if recent_ui_metrics else 0,
                system_uptime=time.time() - self._get_start_time(),
                timestamp=datetime.now()
            )
            
            self.operational_metrics.append(operational_metric)
            
        except Exception as e:
            logger.error(f"Error generating operational report: {e}")
    
    def _cleanup_old_sessions(self):
        """Clean up old user sessions"""
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for user_id, session_data in self.user_sessions.items():
                if 'last_activity' in session_data:
                    last_activity = session_data['last_activity']
                    if isinstance(last_activity, str):
                        last_activity = datetime.fromisoformat(last_activity)
                    
                    # Remove sessions inactive for more than 1 hour
                    if (current_time - last_activity).total_seconds() > 3600:
                        expired_sessions.append(user_id)
            
            for user_id in expired_sessions:
                del self.user_sessions[user_id]
                
        except Exception as e:
            logger.error(f"Error cleaning up old sessions: {e}")
    
    def _get_start_time(self):
        """Get system start time"""
        if not hasattr(self, '_start_time'):
            self._start_time = time.time()
        return self._start_time
    
    def track_ui_component(self, component_name: str, operation: str = "render"):
        """Track UI component performance"""
        try:
            start_time = time.time()
            
            def track_completion():
                end_time = time.time()
                response_time = end_time - start_time
                
                ui_metric = UIMetrics(
                    response_time=response_time,
                    render_time=response_time * 0.8,  # Estimate render time
                    user_interactions=1,
                    errors_count=0,
                    active_users=len(self.user_sessions),
                    timestamp=datetime.now(),
                    ui_component=component_name,
                    operation_type=operation
                )
                
                self.ui_metrics.append(ui_metric)
            
            # Store completion callback
            self.ui_start_times[component_name] = {
                'start_time': start_time,
                'completion_callback': track_completion
            }
            
        except Exception as e:
            logger.error(f"Error tracking UI component: {e}")
    
    def complete_ui_component(self, component_name: str):
        """Complete UI component tracking"""
        try:
            if component_name in self.ui_start_times:
                callback = self.ui_start_times[component_name]['completion_callback']
                callback()
                del self.ui_start_times[component_name]
                
        except Exception as e:
            logger.error(f"Error completing UI component tracking: {e}")
    
    def track_user_interaction(self, user_id: str, action_type: str, target_component: str):
        """Track user interaction"""
        try:
            start_time = time.time()
            
            def complete_interaction(success: bool = True, error_message: str = ""):
                end_time = time.time()
                response_time = end_time - start_time
                
                user_interaction = UserInteractionMetrics(
                    user_id=user_id,
                    action_type=action_type,
                    target_component=target_component,
                    response_time=response_time,
                    success=success,
                    error_message=error_message,
                    timestamp=datetime.now(),
                    session_duration=time.time() - self._get_start_time()
                )
                
                self.user_interactions.append(user_interaction)
                
                # Update user session
                self.user_sessions[user_id] = {
                    'last_activity': datetime.now().isoformat(),
                    'total_interactions': self.user_sessions.get(user_id, {}).get('total_interactions', 0) + 1
                }
            
            # Store completion callback
            self.ui_start_times[f"interaction_{user_id}_{action_type}"] = {
                'start_time': start_time,
                'completion_callback': complete_interaction
            }
            
        except Exception as e:
            logger.error(f"Error tracking user interaction: {e}")
    
    def complete_user_interaction(self, user_id: str, action_type: str, success: bool = True, error_message: str = ""):
        """Complete user interaction tracking"""
        try:
            key = f"interaction_{user_id}_{action_type}"
            if key in self.ui_start_times:
                callback = self.ui_start_times[key]['completion_callback']
                callback(success, error_message)
                del self.ui_start_times[key]
                
        except Exception as e:
            logger.error(f"Error completing user interaction tracking: {e}")
    
    def get_ui_performance(self, component_name: str = None) -> Dict:
        """Get UI performance metrics"""
        try:
            if not self.ui_metrics:
                return {"message": "No UI metrics available"}
            
            if component_name:
                metrics = [m for m in self.ui_metrics if m.ui_component == component_name]
            else:
                metrics = list(self.ui_metrics)
            
            if not metrics:
                return {"message": f"No metrics for component: {component_name}"}
            
            # Calculate statistics
            response_times = [m.response_time for m in metrics]
            render_times = [m.render_time for m in metrics]
            error_counts = [m.errors_count for m in metrics]
            
            return {
                'component_name': component_name or 'all_components',
                'total_operations': len(metrics),
                'response_time': {
                    'mean': np.mean(response_times),
                    'std': np.std(response_times),
                    'min': np.min(response_times),
                    'max': np.max(response_times)
                },
                'render_time': {
                    'mean': np.mean(render_times),
                    'std': np.std(render_times),
                    'min': np.min(render_times),
                    'max': np.max(render_times)
                },
                'error_rate': sum(error_counts) / len(metrics),
                'performance_score': self._calculate_performance_score(response_times, error_counts)
            }
            
        except Exception as e:
            logger.error(f"Error getting UI performance: {e}")
            return {"error": str(e)}
    
    def _calculate_performance_score(self, response_times: List[float], error_counts: List[int]) -> float:
        """Calculate performance score (0-100)"""
        try:
            avg_response_time = np.mean(response_times)
            error_rate = sum(error_counts) / len(error_counts) if error_counts else 0
            
            # Score based on response time (faster = higher score)
            response_score = max(0, 100 - (avg_response_time * 20))
            
            # Score based on error rate (fewer errors = higher score)
            error_score = max(0, 100 - (error_rate * 100))
            
            # Combined score
            return (response_score + error_score) / 2
            
        except Exception as e:
            logger.error(f"Error calculating performance score: {e}")
            return 0.0
    
    def get_user_interaction_analytics(self) -> Dict:
        """Get user interaction analytics"""
        try:
            if not self.user_interactions:
                return {"message": "No user interaction data available"}
            
            interactions = list(self.user_interactions)
            
            # User activity
            unique_users = len(set([i.user_id for i in interactions]))
            total_interactions = len(interactions)
            successful_interactions = len([i for i in interactions if i.success])
            
            # Action type distribution
            action_counts = defaultdict(int)
            for interaction in interactions:
                action_counts[interaction.action_type] += 1
            
            # Component usage
            component_counts = defaultdict(int)
            for interaction in interactions:
                component_counts[interaction.target_component] += 1
            
            # Response time analysis
            response_times = [i.response_time for i in interactions]
            
            return {
                'user_activity': {
                    'unique_users': unique_users,
                    'total_interactions': total_interactions,
                    'successful_interactions': successful_interactions,
                    'success_rate': successful_interactions / total_interactions if total_interactions > 0 else 0
                },
                'action_distribution': dict(action_counts),
                'component_usage': dict(component_counts),
                'response_time_analysis': {
                    'mean': np.mean(response_times),
                    'median': np.median(response_times),
                    'std': np.std(response_times),
                    'percentile_95': np.percentile(response_times, 95)
                },
                'user_satisfaction_score': self._calculate_user_satisfaction(interactions)
            }
            
        except Exception as e:
            logger.error(f"Error getting user interaction analytics: {e}")
            return {"error": str(e)}
    
    def _calculate_user_satisfaction(self, interactions: List[UserInteractionMetrics]) -> float:
        """Calculate user satisfaction score"""
        try:
            if not interactions:
                return 0.0
            
            # Factors affecting satisfaction
            success_rate = len([i for i in interactions if i.success]) / len(interactions)
            avg_response_time = np.mean([i.response_time for i in interactions])
            
            # Response time satisfaction (faster = higher satisfaction)
            response_satisfaction = max(0, 1 - (avg_response_time / 2))  # 2s = 0 satisfaction
            
            # Combined satisfaction score
            satisfaction = (success_rate * 0.7) + (response_satisfaction * 0.3)
            
            return satisfaction * 100  # Convert to percentage
            
        except Exception as e:
            logger.error(f"Error calculating user satisfaction: {e}")
            return 0.0
    
    def get_system_operation_health(self) -> Dict:
        """Get system operation health metrics"""
        try:
            if not self.system_operations:
                return {"message": "No system operation data available"}
            
            operations = list(self.system_operations)
            
            # Operation success rates
            operation_success = defaultdict(lambda: {'success': 0, 'total': 0})
            for op in operations:
                operation_success[op.operation_name]['total'] += 1
                if op.success:
                    operation_success[op.operation_name]['success'] += 1
            
            # Calculate success rates
            success_rates = {}
            for op_name, counts in operation_success.items():
                success_rates[op_name] = counts['success'] / counts['total'] if counts['total'] > 0 else 0
            
            # Performance metrics
            execution_times = [op.execution_time for op in operations]
            memory_usage = [op.memory_usage for op in operations]
            cpu_usage = [op.cpu_usage for op in operations]
            
            return {
                'operation_success_rates': success_rates,
                'performance_metrics': {
                    'execution_time': {
                        'mean': np.mean(execution_times),
                        'max': np.max(execution_times),
                        'percentile_95': np.percentile(execution_times, 95)
                    },
                    'memory_usage': {
                        'mean': np.mean(memory_usage),
                        'max': np.max(memory_usage)
                    },
                    'cpu_usage': {
                        'mean': np.mean(cpu_usage),
                        'max': np.max(cpu_usage)
                    }
                },
                'overall_health': self._calculate_system_health(success_rates, execution_times)
            }
            
        except Exception as e:
            logger.error(f"Error getting system operation health: {e}")
            return {"error": str(e)}
    
    def _calculate_system_health(self, success_rates: Dict, execution_times: List[float]) -> str:
        """Calculate overall system health"""
        try:
            avg_success_rate = np.mean(list(success_rates.values()))
            avg_execution_time = np.mean(execution_times)
            
            if avg_success_rate > 0.95 and avg_execution_time < 1.0:
                return "excellent"
            elif avg_success_rate > 0.9 and avg_execution_time < 2.0:
                return "good"
            elif avg_success_rate > 0.8 and avg_execution_time < 5.0:
                return "fair"
            else:
                return "poor"
                
        except Exception as e:
            logger.error(f"Error calculating system health: {e}")
            return "unknown"
    
    def generate_operational_report(self) -> Dict:
        """Generate comprehensive operational report"""
        try:
            return {
                'timestamp': datetime.now().isoformat(),
                'monitoring_status': 'active' if self.is_monitoring else 'inactive',
                'ui_performance': self.get_ui_performance(),
                'user_interactions': self.get_user_interaction_analytics(),
                'system_operations': self.get_system_operation_health(),
                'alerts_count': len(self._load_operational_alerts()),
                'metrics_summary': {
                    'total_ui_metrics': len(self.ui_metrics),
                    'total_user_interactions': len(self.user_interactions),
                    'total_system_operations': len(self.system_operations),
                    'active_sessions': len(self.user_sessions),
                    'monitoring_duration': time.time() - self._get_start_time()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating operational report: {e}")
            return {"error": str(e)}
    
    def _load_operational_alerts(self) -> List[Dict]:
        """Load operational alerts from file"""
        try:
            alert_file = 'logs/operational_alerts.json'
            if os.path.exists(alert_file):
                with open(alert_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading operational alerts: {e}")
            return []
    
    def export_operational_metrics(self, filename: str = None):
        """Export operational metrics to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"operational_metrics_{timestamp}.json"
        
        try:
            export_data = {
                'ui_metrics': [asdict(m) for m in self.ui_metrics],
                'user_interactions': [asdict(m) for m in self.user_interactions],
                'system_operations': [asdict(m) for m in self.system_operations],
                'operational_metrics': [asdict(m) for m in self.operational_metrics],
                'user_sessions': dict(self.user_sessions),
                'error_log': list(self.error_log),
                'export_timestamp': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Operational metrics exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting operational metrics: {e}") 