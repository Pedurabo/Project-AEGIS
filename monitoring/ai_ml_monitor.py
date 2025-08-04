"""
DEVELOPMENTAL SILO - AI/ML Monitoring System
Monitors AI models, learning progress, and ML performance metrics
"""

import time
import json
import threading
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import psutil
import os
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


@dataclass
class ModelMetrics:
    """AI Model Performance Metrics"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time: float
    inference_time: float
    timestamp: datetime
    dataset_size: int
    features_count: int


@dataclass
class LearningMetrics:
    """Learning Progress Metrics"""
    attack_type: str
    success_rate: float
    patterns_learned: int
    adaptation_speed: float
    confidence_improvement: float
    timestamp: datetime
    total_attempts: int
    successful_attempts: int


@dataclass
class AIMetrics:
    """Overall AI System Metrics"""
    total_models: int
    active_models: int
    average_accuracy: float
    learning_rate: float
    pattern_discovery_rate: float
    anomaly_detection_rate: float
    timestamp: datetime


class AIMLMonitor:
    """AI/ML Monitoring System for Developmental Silo"""
    
    def __init__(self, metrics_history_size: int = 1000):
        self.metrics_history_size = metrics_history_size
        self.model_metrics = deque(maxlen=metrics_history_size)
        self.learning_metrics = deque(maxlen=metrics_history_size)
        self.ai_metrics = deque(maxlen=metrics_history_size)
        
        # Performance tracking
        self.performance_history = defaultdict(list)
        self.alert_thresholds = {
            'accuracy_threshold': 0.7,
            'learning_rate_threshold': 0.1,
            'memory_usage_threshold': 0.8,
            'cpu_usage_threshold': 0.9
        }
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread = None
        self.monitoring_interval = 30  # seconds
        
        # Setup logging
        self.setup_logging()
        
        logger.info("AI/ML Monitor initialized")
    
    def setup_logging(self):
        """Setup monitoring-specific logging"""
        monitor_logger = logging.getLogger('ai_ml_monitor')
        monitor_logger.setLevel(logging.INFO)
        
        # Create file handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = logging.FileHandler('logs/ai_ml_monitor.log')
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
            logger.warning("Monitoring already running")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        logger.info("AI/ML monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("AI/ML monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Collect AI metrics
                self._collect_ai_metrics()
                
                # Check for alerts
                self._check_alerts()
                
                # Generate reports
                self._generate_performance_report()
                
                # Wait for next interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Process-specific metrics
            process = psutil.Process()
            process_cpu = process.cpu_percent()
            process_memory = process.memory_percent()
            
            system_metrics = {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'process_cpu': process_cpu,
                'process_memory': process_memory
            }
            
            self.performance_history['system'].append(system_metrics)
            
            # Check thresholds
            if cpu_percent > self.alert_thresholds['cpu_usage_threshold'] * 100:
                self._trigger_alert('HIGH_CPU_USAGE', f"CPU usage: {cpu_percent}%")
            
            if memory_percent > self.alert_thresholds['memory_usage_threshold'] * 100:
                self._trigger_alert('HIGH_MEMORY_USAGE', f"Memory usage: {memory_percent}%")
                
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def _collect_ai_metrics(self):
        """Collect AI/ML specific metrics"""
        try:
            # This would integrate with the AI core to get real metrics
            # For now, we'll simulate metrics
            
            # Simulate model performance
            model_metrics = ModelMetrics(
                model_name="RandomForest_Classifier",
                accuracy=np.random.uniform(0.7, 0.95),
                precision=np.random.uniform(0.6, 0.9),
                recall=np.random.uniform(0.6, 0.9),
                f1_score=np.random.uniform(0.6, 0.9),
                training_time=np.random.uniform(10, 60),
                inference_time=np.random.uniform(0.001, 0.1),
                timestamp=datetime.now(),
                dataset_size=np.random.randint(1000, 10000),
                features_count=np.random.randint(10, 100)
            )
            
            self.model_metrics.append(model_metrics)
            
            # Simulate learning metrics
            learning_metrics = LearningMetrics(
                attack_type="sql_injection",
                success_rate=np.random.uniform(0.3, 0.8),
                patterns_learned=np.random.randint(5, 50),
                adaptation_speed=np.random.uniform(0.1, 0.5),
                confidence_improvement=np.random.uniform(0.05, 0.2),
                timestamp=datetime.now(),
                total_attempts=np.random.randint(100, 1000),
                successful_attempts=np.random.randint(30, 400)
            )
            
            self.learning_metrics.append(learning_metrics)
            
        except Exception as e:
            logger.error(f"Error collecting AI metrics: {e}")
    
    def _check_alerts(self):
        """Check for alert conditions"""
        try:
            if not self.model_metrics:
                return
            
            latest_model = self.model_metrics[-1]
            
            # Check accuracy threshold
            if latest_model.accuracy < self.alert_thresholds['accuracy_threshold']:
                self._trigger_alert(
                    'LOW_MODEL_ACCURACY',
                    f"Model accuracy below threshold: {latest_model.accuracy:.3f}"
                )
            
            # Check learning rate
            if self.learning_metrics:
                latest_learning = self.learning_metrics[-1]
                if latest_learning.adaptation_speed < self.alert_thresholds['learning_rate_threshold']:
                    self._trigger_alert(
                        'SLOW_LEARNING_RATE',
                        f"Learning rate below threshold: {latest_learning.adaptation_speed:.3f}"
                    )
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    def _trigger_alert(self, alert_type: str, message: str):
        """Trigger an alert"""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'severity': 'HIGH' if 'HIGH' in alert_type else 'MEDIUM'
        }
        
        logger.warning(f"ALERT: {alert_type} - {message}")
        
        # Save alert to file
        self._save_alert(alert)
        
        # Could also send notifications here (email, Slack, etc.)
    
    def _save_alert(self, alert: Dict):
        """Save alert to file"""
        try:
            alert_file = 'logs/ai_ml_alerts.json'
            
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
            logger.error(f"Error saving alert: {e}")
    
    def _generate_performance_report(self):
        """Generate performance report"""
        try:
            if not self.model_metrics:
                return
            
            # Calculate average metrics
            recent_models = list(self.model_metrics)[-10:]  # Last 10 models
            
            avg_accuracy = np.mean([m.accuracy for m in recent_models])
            avg_precision = np.mean([m.precision for m in recent_models])
            avg_recall = np.mean([m.recall for m in recent_models])
            avg_f1 = np.mean([m.f1_score for m in recent_models])
            
            # Calculate learning progress
            if self.learning_metrics:
                recent_learning = list(self.learning_metrics)[-10:]
                avg_success_rate = np.mean([l.success_rate for l in recent_learning])
                avg_patterns_learned = np.mean([l.patterns_learned for l in recent_learning])
            else:
                avg_success_rate = 0
                avg_patterns_learned = 0
            
            # Create AI metrics
            ai_metrics = AIMetrics(
                total_models=len(set([m.model_name for m in self.model_metrics])),
                active_models=len(recent_models),
                average_accuracy=avg_accuracy,
                learning_rate=avg_success_rate,
                pattern_discovery_rate=avg_patterns_learned / 10,  # Per interval
                anomaly_detection_rate=np.random.uniform(0.8, 0.95),  # Simulated
                timestamp=datetime.now()
            )
            
            self.ai_metrics.append(ai_metrics)
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
    
    def get_model_performance(self, model_name: str = None) -> Dict:
        """Get model performance metrics"""
        try:
            if not self.model_metrics:
                return {"message": "No model metrics available"}
            
            if model_name:
                models = [m for m in self.model_metrics if m.model_name == model_name]
            else:
                models = list(self.model_metrics)
            
            if not models:
                return {"message": f"No metrics for model: {model_name}"}
            
            # Calculate statistics
            accuracies = [m.accuracy for m in models]
            precisions = [m.precision for m in models]
            recalls = [m.recall for m in models]
            f1_scores = [m.f1_score for m in models]
            
            return {
                'model_name': model_name or 'all_models',
                'total_models': len(models),
                'accuracy': {
                    'mean': np.mean(accuracies),
                    'std': np.std(accuracies),
                    'min': np.min(accuracies),
                    'max': np.max(accuracies)
                },
                'precision': {
                    'mean': np.mean(precisions),
                    'std': np.std(precisions),
                    'min': np.min(precisions),
                    'max': np.max(precisions)
                },
                'recall': {
                    'mean': np.mean(recalls),
                    'std': np.std(recalls),
                    'min': np.min(recalls),
                    'max': np.max(recalls)
                },
                'f1_score': {
                    'mean': np.mean(f1_scores),
                    'std': np.std(f1_scores),
                    'min': np.min(f1_scores),
                    'max': np.max(f1_scores)
                },
                'latest_metrics': asdict(models[-1])
            }
            
        except Exception as e:
            logger.error(f"Error getting model performance: {e}")
            return {"error": str(e)}
    
    def get_learning_progress(self, attack_type: str = None) -> Dict:
        """Get learning progress metrics"""
        try:
            if not self.learning_metrics:
                return {"message": "No learning metrics available"}
            
            if attack_type:
                metrics = [m for m in self.learning_metrics if m.attack_type == attack_type]
            else:
                metrics = list(self.learning_metrics)
            
            if not metrics:
                return {"message": f"No metrics for attack type: {attack_type}"}
            
            # Calculate learning statistics
            success_rates = [m.success_rate for m in metrics]
            patterns_learned = [m.patterns_learned for m in metrics]
            adaptation_speeds = [m.adaptation_speed for m in metrics]
            
            return {
                'attack_type': attack_type or 'all_attacks',
                'total_records': len(metrics),
                'success_rate': {
                    'mean': np.mean(success_rates),
                    'trend': 'improving' if success_rates[-1] > success_rates[0] else 'declining',
                    'latest': success_rates[-1]
                },
                'patterns_learned': {
                    'total': sum(patterns_learned),
                    'average_per_interval': np.mean(patterns_learned),
                    'latest': patterns_learned[-1]
                },
                'adaptation_speed': {
                    'mean': np.mean(adaptation_speeds),
                    'latest': adaptation_speeds[-1]
                },
                'learning_efficiency': np.mean(success_rates) * np.mean(adaptation_speeds)
            }
            
        except Exception as e:
            logger.error(f"Error getting learning progress: {e}")
            return {"error": str(e)}
    
    def get_system_health(self) -> Dict:
        """Get system health metrics"""
        try:
            if not self.performance_history.get('system'):
                return {"message": "No system metrics available"}
            
            recent_metrics = self.performance_history['system'][-10:]
            
            cpu_usage = [m['cpu_percent'] for m in recent_metrics]
            memory_usage = [m['memory_percent'] for m in recent_metrics]
            disk_usage = [m['disk_percent'] for m in recent_metrics]
            
            return {
                'cpu_health': {
                    'current': cpu_usage[-1],
                    'average': np.mean(cpu_usage),
                    'status': 'healthy' if cpu_usage[-1] < 80 else 'warning' if cpu_usage[-1] < 90 else 'critical'
                },
                'memory_health': {
                    'current': memory_usage[-1],
                    'average': np.mean(memory_usage),
                    'status': 'healthy' if memory_usage[-1] < 80 else 'warning' if memory_usage[-1] < 90 else 'critical'
                },
                'disk_health': {
                    'current': disk_usage[-1],
                    'average': np.mean(disk_usage),
                    'status': 'healthy' if disk_usage[-1] < 80 else 'warning' if disk_usage[-1] < 90 else 'critical'
                },
                'overall_status': 'healthy' if all([
                    cpu_usage[-1] < 80,
                    memory_usage[-1] < 80,
                    disk_usage[-1] < 80
                ]) else 'warning'
            }
            
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {"error": str(e)}
    
    def generate_monitoring_report(self) -> Dict:
        """Generate comprehensive monitoring report"""
        try:
            return {
                'timestamp': datetime.now().isoformat(),
                'monitoring_status': 'active' if self.is_monitoring else 'inactive',
                'system_health': self.get_system_health(),
                'model_performance': self.get_model_performance(),
                'learning_progress': self.get_learning_progress(),
                'alerts_count': len(self._load_alerts()),
                'metrics_summary': {
                    'total_model_metrics': len(self.model_metrics),
                    'total_learning_metrics': len(self.learning_metrics),
                    'total_ai_metrics': len(self.ai_metrics),
                    'monitoring_duration': self._get_monitoring_duration()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating monitoring report: {e}")
            return {"error": str(e)}
    
    def _load_alerts(self) -> List[Dict]:
        """Load alerts from file"""
        try:
            alert_file = 'logs/ai_ml_alerts.json'
            if os.path.exists(alert_file):
                with open(alert_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading alerts: {e}")
            return []
    
    def _get_monitoring_duration(self) -> str:
        """Get monitoring duration"""
        if not self.ai_metrics:
            return "0 minutes"
        
        start_time = self.ai_metrics[0].timestamp
        end_time = self.ai_metrics[-1].timestamp
        duration = end_time - start_time
        
        return str(duration)
    
    def export_metrics(self, filename: str = None):
        """Export metrics to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_ml_metrics_{timestamp}.json"
        
        try:
            export_data = {
                'model_metrics': [asdict(m) for m in self.model_metrics],
                'learning_metrics': [asdict(m) for m in self.learning_metrics],
                'ai_metrics': [asdict(m) for m in self.ai_metrics],
                'system_metrics': self.performance_history.get('system', []),
                'export_timestamp': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Metrics exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}") 