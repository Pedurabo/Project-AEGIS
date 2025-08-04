"""
SILO 1: DEVELOPMENTAL - AI/ML Engine
Advanced machine learning capabilities with automated training pipelines
"""

import numpy as np
import pandas as pd
import joblib
import pickle
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading
import queue
from pathlib import Path

# Try to import advanced ML libraries
try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False

# Always available
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """AI/ML Model Types"""
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    NEURAL_NETWORK = "neural_network"
    DEEP_LEARNING = "deep_learning"
    AUTOENCODER = "autoencoder"
    CLUSTERING = "clustering"
    ANOMALY_DETECTION = "anomaly_detection"


@dataclass
class TrainingJob:
    """Training job configuration"""
    job_id: str
    model_type: ModelType
    dataset_path: str
    hyperparameters: Dict[str, Any]
    priority: int = 1
    created_at: datetime = None
    status: str = "pending"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ModelPerformance:
    """Model performance metrics"""
    model_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time: float
    inference_time: float
    timestamp: datetime
    dataset_size: int


class AIMLEngine:
    """Advanced AI/ML Engine for Developmental Silo"""
    
    def __init__(self, models_dir: str = "silos/developmental/models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Model registry
        self.models = {}
        self.scalers = {}
        self.performance_history = []
        
        # Training queue
        self.training_queue = queue.PriorityQueue()
        self.training_threads = []
        self.max_training_threads = 3
        
        # Auto-training configuration
        self.auto_training_enabled = True
        self.performance_threshold = 0.8
        self.retrain_interval_hours = 24
        
        # Initialize
        self._initialize_models()
        self._start_training_workers()
        
        logger.info("AI/ML Engine initialized")
    
    def _initialize_models(self):
        """Initialize all model types"""
        for model_type in ModelType:
            model_key = f"{model_type.value}_model"
            
            if model_type == ModelType.RANDOM_FOREST:
                self.models[model_key] = RandomForestClassifier(n_estimators=100, random_state=42)
            elif model_type == ModelType.GRADIENT_BOOSTING:
                self.models[model_key] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            elif model_type == ModelType.NEURAL_NETWORK:
                self.models[model_key] = MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42)
            elif model_type == ModelType.DEEP_LEARNING and TENSORFLOW_AVAILABLE:
                self.models[model_key] = self._create_deep_learning_model()
            elif model_type == ModelType.CLUSTERING:
                self.models[model_key] = KMeans(n_clusters=5, random_state=42)
            elif model_type == ModelType.ANOMALY_DETECTION:
                from sklearn.ensemble import IsolationForest
                self.models[model_key] = IsolationForest(contamination=0.1, random_state=42)
            
            # Initialize scaler for each model
            self.scalers[model_key] = StandardScaler()
    
    def _create_deep_learning_model(self):
        """Create TensorFlow deep learning model"""
        if not TENSORFLOW_AVAILABLE:
            return None
        
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(50,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def _start_training_workers(self):
        """Start automated training workers"""
        for i in range(self.max_training_threads):
            worker = threading.Thread(target=self._training_worker, args=(i,), daemon=True)
            worker.start()
            self.training_threads.append(worker)
        
        logger.info(f"Started {self.max_training_threads} training workers")
    
    def _training_worker(self, worker_id: int):
        """Training worker thread"""
        while True:
            try:
                # Get training job from queue
                priority, job = self.training_queue.get(timeout=1)
                
                logger.info(f"Worker {worker_id} processing job: {job.job_id}")
                job.status = "training"
                
                # Execute training
                success = self._execute_training_job(job)
                
                if success:
                    job.status = "completed"
                    logger.info(f"Job {job.job_id} completed successfully")
                else:
                    job.status = "failed"
                    logger.error(f"Job {job.job_id} failed")
                
                self.training_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Training worker {worker_id} error: {e}")
    
    def _execute_training_job(self, job: TrainingJob) -> bool:
        """Execute a training job"""
        try:
            # Load dataset
            dataset = self._load_dataset(job.dataset_path)
            if dataset is None:
                return False
            
            X, y = dataset
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Get model
            model_key = f"{job.model_type.value}_model"
            model = self.models.get(model_key)
            scaler = self.scalers.get(model_key)
            
            if model is None:
                logger.error(f"Model not found: {model_key}")
                return False
            
            # Scale features
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            start_time = time.time()
            
            if TENSORFLOW_AVAILABLE and hasattr(model, 'fit'):
                # TensorFlow model
                history = model.fit(
                    X_train_scaled, y_train,
                    validation_data=(X_test_scaled, y_test),
                    epochs=job.hyperparameters.get('epochs', 50),
                    batch_size=job.hyperparameters.get('batch_size', 32),
                    verbose=0
                )
                training_time = time.time() - start_time
                
                # Evaluate
                y_pred = model.predict(X_test_scaled, verbose=0)
                y_pred_binary = (y_pred > 0.5).astype(int)
                
            else:
                # Scikit-learn model
                model.fit(X_train_scaled, y_train)
                training_time = time.time() - start_time
                
                # Evaluate
                y_pred = model.predict(X_test_scaled)
                y_pred_binary = y_pred
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred_binary)
            precision = precision_score(y_test, y_pred_binary, average='weighted')
            recall = recall_score(y_test, y_pred_binary, average='weighted')
            f1 = f1_score(y_test, y_pred_binary, average='weighted')
            
            # Measure inference time
            inference_start = time.time()
            model.predict(X_test_scaled[:10])
            inference_time = time.time() - inference_start
            
            # Store performance
            performance = ModelPerformance(
                model_id=job.job_id,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1,
                training_time=training_time,
                inference_time=inference_time,
                timestamp=datetime.now(),
                dataset_size=len(X)
            )
            
            self.performance_history.append(performance)
            
            # Save model
            self._save_model(model, scaler, job.job_id)
            
            # Check if auto-retraining is needed
            if self.auto_training_enabled and accuracy < self.performance_threshold:
                self._schedule_retraining(job)
            
            return True
            
        except Exception as e:
            logger.error(f"Training job execution failed: {e}")
            return False
    
    def _load_dataset(self, dataset_path: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """Load dataset from various formats"""
        try:
            if dataset_path.endswith('.csv'):
                df = pd.read_csv(dataset_path)
            elif dataset_path.endswith('.json'):
                df = pd.read_json(dataset_path)
            elif dataset_path.endswith('.pkl'):
                df = pd.read_pickle(dataset_path)
            else:
                logger.error(f"Unsupported dataset format: {dataset_path}")
                return None
            
            # Assume last column is target
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None
    
    def _save_model(self, model: Any, scaler: Any, model_id: str):
        """Save model and scaler"""
        try:
            model_data = {
                'model': model,
                'scaler': scaler,
                'saved_at': datetime.now(),
                'model_id': model_id
            }
            
            model_path = self.models_dir / f"{model_id}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            logger.info(f"Model saved: {model_path}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def _schedule_retraining(self, original_job: TrainingJob):
        """Schedule model retraining"""
        retrain_job = TrainingJob(
            job_id=f"{original_job.job_id}_retrain_{datetime.now().strftime('%Y%m%d_%H%M')}",
            model_type=original_job.model_type,
            dataset_path=original_job.dataset_path,
            hyperparameters=original_job.hyperparameters,
            priority=original_job.priority + 1
        )
        
        self.training_queue.put((retrain_job.priority, retrain_job))
        logger.info(f"Scheduled retraining: {retrain_job.job_id}")
    
    def add_training_job(self, model_type: ModelType, dataset_path: str, 
                        hyperparameters: Dict[str, Any] = None, priority: int = 1) -> str:
        """Add training job to queue"""
        job_id = f"{model_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        job = TrainingJob(
            job_id=job_id,
            model_type=model_type,
            dataset_path=dataset_path,
            hyperparameters=hyperparameters or {},
            priority=priority
        )
        
        self.training_queue.put((priority, job))
        logger.info(f"Added training job: {job_id}")
        
        return job_id
    
    def predict(self, model_type: ModelType, features: np.ndarray) -> np.ndarray:
        """Make predictions using trained model"""
        try:
            model_key = f"{model_type.value}_model"
            model = self.models.get(model_key)
            scaler = self.scalers.get(model_key)
            
            if model is None or scaler is None:
                logger.error(f"Model not found: {model_key}")
                return np.array([])
            
            # Scale features
            features_scaled = scaler.transform(features)
            
            # Make prediction
            if TENSORFLOW_AVAILABLE and hasattr(model, 'predict'):
                predictions = model.predict(features_scaled, verbose=0)
                return predictions.flatten()
            else:
                predictions = model.predict(features_scaled)
                return predictions
                
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return np.array([])
    
    def get_model_performance(self, model_type: ModelType) -> Dict[str, Any]:
        """Get performance metrics for model type"""
        try:
            model_key = f"{model_type.value}_model"
            performances = [p for p in self.performance_history if model_key in p.model_id]
            
            if not performances:
                return {"message": f"No performance data for {model_type.value}"}
            
            latest = performances[-1]
            
            return {
                'model_type': model_type.value,
                'latest_performance': {
                    'accuracy': latest.accuracy,
                    'precision': latest.precision,
                    'recall': latest.recall,
                    'f1_score': latest.f1_score,
                    'training_time': latest.training_time,
                    'inference_time': latest.inference_time,
                    'timestamp': latest.timestamp.isoformat()
                },
                'performance_trend': self._calculate_performance_trend(performances),
                'total_training_runs': len(performances)
            }
            
        except Exception as e:
            logger.error(f"Error getting model performance: {e}")
            return {"error": str(e)}
    
    def _calculate_performance_trend(self, performances: List[ModelPerformance]) -> str:
        """Calculate performance trend"""
        if len(performances) < 2:
            return "insufficient_data"
        
        recent_accuracies = [p.accuracy for p in performances[-5:]]
        
        if len(recent_accuracies) >= 2:
            if recent_accuracies[-1] > recent_accuracies[0]:
                return "improving"
            elif recent_accuracies[-1] < recent_accuracies[0]:
                return "declining"
            else:
                return "stable"
        
        return "unknown"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get AI/ML engine system status"""
        return {
            'total_models': len(self.models),
            'training_queue_size': self.training_queue.qsize(),
            'active_training_jobs': len([t for t in self.training_threads if t.is_alive()]),
            'performance_history_count': len(self.performance_history),
            'auto_training_enabled': self.auto_training_enabled,
            'tensorflow_available': TENSORFLOW_AVAILABLE,
            'pytorch_available': PYTORCH_AVAILABLE,
            'system_healthy': True
        }
    
    def enable_auto_training(self, enabled: bool = True):
        """Enable/disable auto-training"""
        self.auto_training_enabled = enabled
        logger.info(f"Auto-training {'enabled' if enabled else 'disabled'}")
    
    def set_performance_threshold(self, threshold: float):
        """Set performance threshold for auto-retraining"""
        self.performance_threshold = threshold
        logger.info(f"Performance threshold set to: {threshold}")
    
    def export_performance_report(self, file_path: str = None) -> str:
        """Export performance report"""
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"silos/developmental/reports/performance_report_{timestamp}.json"
        
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'system_status': self.get_system_status(),
                'model_performances': {
                    model_type.value: self.get_model_performance(model_type)
                    for model_type in ModelType
                },
                'performance_history': [
                    {
                        'model_id': p.model_id,
                        'accuracy': p.accuracy,
                        'precision': p.precision,
                        'recall': p.recall,
                        'f1_score': p.f1_score,
                        'training_time': p.training_time,
                        'timestamp': p.timestamp.isoformat()
                    }
                    for p in self.performance_history
                ]
            }
            
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Performance report exported: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error exporting performance report: {e}")
            return "" 