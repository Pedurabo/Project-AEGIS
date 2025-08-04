"""
DEVELOPMENTAL SILO - Deep Learning Core
Advanced neural network capabilities for AI-powered penetration testing
"""

import numpy as np
import pandas as pd
import joblib
import pickle
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import warnings

# Try to import TensorFlow, fallback to scikit-learn if not available
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers, callbacks
    TENSORFLOW_AVAILABLE = True
    logging.info("TensorFlow successfully imported")
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow not available, using scikit-learn alternatives")

# Always available ML libraries
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Types of deep learning models"""
    NEURAL_NETWORK = "neural_network"
    CONVOLUTIONAL_NN = "convolutional_nn"
    RECURRENT_NN = "recurrent_nn"
    AUTOENCODER = "autoencoder"
    GAN = "generative_adversarial_network"


@dataclass
class ModelConfig:
    """Configuration for deep learning models"""
    model_type: ModelType
    input_shape: Tuple[int, ...]
    hidden_layers: List[int]
    activation: str = 'relu'
    dropout_rate: float = 0.2
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2


@dataclass
class TrainingResult:
    """Results from model training"""
    model_name: str
    accuracy: float
    loss: float
    training_time: float
    epochs_completed: int
    validation_accuracy: float
    timestamp: datetime
    model_path: str


class DeepLearningCore:
    """Advanced Deep Learning Core for AI Penetration Testing"""
    
    def __init__(self, models_dir: str = "models/deep_learning"):
        self.models_dir = models_dir
        self.models = {}
        self.scalers = {}
        self.training_history = []
        self.model_configs = {}
        
        # Create models directory
        import os
        os.makedirs(models_dir, exist_ok=True)
        
        # Initialize TensorFlow if available
        if TENSORFLOW_AVAILABLE:
            self._setup_tensorflow()
        
        logger.info("Deep Learning Core initialized")
    
    def _setup_tensorflow(self):
        """Setup TensorFlow configuration"""
        try:
            # Configure TensorFlow for better performance
            tf.config.optimizer.set_jit(True)
            
            # Set memory growth to avoid GPU memory issues
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logger.info(f"GPU devices configured: {len(gpus)}")
            
            # Set random seeds for reproducibility
            tf.random.set_seed(42)
            np.random.seed(42)
            
        except Exception as e:
            logger.warning(f"TensorFlow setup warning: {e}")
    
    def create_neural_network(self, config: ModelConfig) -> Any:
        """Create a neural network model"""
        try:
            if TENSORFLOW_AVAILABLE:
                return self._create_tensorflow_nn(config)
            else:
                return self._create_sklearn_nn(config)
        except Exception as e:
            logger.error(f"Error creating neural network: {e}")
            return None
    
    def _create_tensorflow_nn(self, config: ModelConfig) -> keras.Model:
        """Create TensorFlow neural network"""
        model = models.Sequential()
        
        # Input layer
        model.add(layers.Dense(config.hidden_layers[0], 
                              input_shape=config.input_shape,
                              activation=config.activation))
        model.add(layers.Dropout(config.dropout_rate))
        
        # Hidden layers
        for units in config.hidden_layers[1:]:
            model.add(layers.Dense(units, activation=config.activation))
            model.add(layers.Dropout(config.dropout_rate))
        
        # Output layer
        model.add(layers.Dense(1, activation='sigmoid'))
        
        # Compile model
        model.compile(
            optimizer=optimizers.Adam(learning_rate=config.learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def _create_sklearn_nn(self, config: ModelConfig) -> MLPClassifier:
        """Create scikit-learn neural network"""
        return MLPClassifier(
            hidden_layer_sizes=tuple(config.hidden_layers),
            activation=config.activation,
            solver='adam',
            alpha=0.001,
            batch_size=config.batch_size,
            learning_rate='adaptive',
            max_iter=config.epochs,
            random_state=42,
            early_stopping=True,
            validation_fraction=config.validation_split
        )
    
    def create_autoencoder(self, input_dim: int, encoding_dim: int = 32) -> Any:
        """Create an autoencoder for anomaly detection"""
        try:
            if TENSORFLOW_AVAILABLE:
                return self._create_tensorflow_autoencoder(input_dim, encoding_dim)
            else:
                return self._create_sklearn_autoencoder(input_dim, encoding_dim)
        except Exception as e:
            logger.error(f"Error creating autoencoder: {e}")
            return None
    
    def _create_tensorflow_autoencoder(self, input_dim: int, encoding_dim: int) -> keras.Model:
        """Create TensorFlow autoencoder"""
        # Encoder
        input_layer = layers.Input(shape=(input_dim,))
        encoded = layers.Dense(encoding_dim * 2, activation='relu')(input_layer)
        encoded = layers.Dense(encoding_dim, activation='relu')(encoded)
        
        # Decoder
        decoded = layers.Dense(encoding_dim * 2, activation='relu')(encoded)
        decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)
        
        # Create autoencoder model
        autoencoder = keras.Model(input_layer, decoded)
        autoencoder.compile(optimizer='adam', loss='mse')
        
        return autoencoder
    
    def _create_sklearn_autoencoder(self, input_dim: int, encoding_dim: int) -> MLPRegressor:
        """Create scikit-learn autoencoder (simplified)"""
        return MLPRegressor(
            hidden_layer_sizes=(encoding_dim * 2, encoding_dim, encoding_dim * 2),
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42
        )
    
    def train_model(self, model: Any, X_train: np.ndarray, y_train: np.ndarray, 
                   config: ModelConfig, model_name: str) -> TrainingResult:
        """Train a deep learning model"""
        try:
            start_time = time.time()
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            
            # Train model
            if TENSORFLOW_AVAILABLE and hasattr(model, 'fit'):
                # TensorFlow model
                history = model.fit(
                    X_train_scaled, y_train,
                    batch_size=config.batch_size,
                    epochs=config.epochs,
                    validation_split=config.validation_split,
                    verbose=0,
                    callbacks=[
                        callbacks.EarlyStopping(patience=10, restore_best_weights=True)
                    ]
                )
                
                # Evaluate
                val_loss, val_accuracy = model.evaluate(X_train_scaled, y_train, verbose=0)
                epochs_completed = len(history.history['loss'])
                
            else:
                # Scikit-learn model
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_train_scaled)
                val_accuracy = accuracy_score(y_train, y_pred)
                val_loss = 0.0  # Not directly available in sklearn
                epochs_completed = config.epochs
            
            training_time = time.time() - start_time
            
            # Save model and scaler
            model_path = f"{self.models_dir}/{model_name}.pkl"
            self._save_model(model, scaler, model_path)
            
            # Create training result
            result = TrainingResult(
                model_name=model_name,
                accuracy=val_accuracy,
                loss=val_loss,
                training_time=training_time,
                epochs_completed=epochs_completed,
                validation_accuracy=val_accuracy,
                timestamp=datetime.now(),
                model_path=model_path
            )
            
            # Store model and scaler
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            self.training_history.append(result)
            
            logger.info(f"Model {model_name} trained successfully: "
                       f"Accuracy={val_accuracy:.3f}, Time={training_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Error training model {model_name}: {e}")
            raise
    
    def predict(self, model_name: str, X: np.ndarray) -> np.ndarray:
        """Make predictions using a trained model"""
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            model = self.models[model_name]
            scaler = self.scalers[model_name]
            
            # Scale features
            X_scaled = scaler.transform(X)
            
            # Make predictions
            if TENSORFLOW_AVAILABLE and hasattr(model, 'predict'):
                predictions = model.predict(X_scaled, verbose=0)
                return predictions.flatten()
            else:
                predictions = model.predict(X_scaled)
                return predictions
                
        except Exception as e:
            logger.error(f"Error making predictions with {model_name}: {e}")
            return np.array([])
    
    def predict_proba(self, model_name: str, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities"""
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            model = self.models[model_name]
            scaler = self.scalers[model_name]
            
            # Scale features
            X_scaled = scaler.transform(X)
            
            # Get probabilities
            if TENSORFLOW_AVAILABLE and hasattr(model, 'predict'):
                probabilities = model.predict(X_scaled, verbose=0)
                return probabilities
            elif hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(X_scaled)
                return probabilities[:, 1] if probabilities.shape[1] > 1 else probabilities.flatten()
            else:
                # Fallback to binary predictions
                predictions = model.predict(X_scaled)
                return predictions
                
        except Exception as e:
            logger.error(f"Error getting probabilities for {model_name}: {e}")
            return np.array([])
    
    def detect_anomalies(self, model_name: str, X: np.ndarray, threshold: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
        """Detect anomalies using autoencoder"""
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            model = self.models[model_name]
            scaler = self.scalers[model_name]
            
            # Scale features
            X_scaled = scaler.transform(X)
            
            # Get reconstruction error
            if TENSORFLOW_AVAILABLE and hasattr(model, 'predict'):
                X_reconstructed = model.predict(X_scaled, verbose=0)
                reconstruction_error = np.mean(np.square(X_scaled - X_reconstructed), axis=1)
            else:
                # For sklearn models, use prediction as reconstruction
                X_reconstructed = model.predict(X_scaled)
                reconstruction_error = np.mean(np.square(X_scaled - X_reconstructed.reshape(-1, 1)), axis=1)
            
            # Detect anomalies
            anomalies = reconstruction_error > threshold
            
            return anomalies, reconstruction_error
            
        except Exception as e:
            logger.error(f"Error detecting anomalies with {model_name}: {e}")
            return np.array([]), np.array([])
    
    def _save_model(self, model: Any, scaler: Any, path: str):
        """Save model and scaler"""
        try:
            save_data = {
                'model': model,
                'scaler': scaler,
                'tensorflow_available': TENSORFLOW_AVAILABLE,
                'save_timestamp': datetime.now().isoformat()
            }
            
            with open(path, 'wb') as f:
                pickle.dump(save_data, f)
                
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def load_model(self, model_name: str) -> bool:
        """Load a saved model"""
        try:
            model_path = f"{self.models_dir}/{model_name}.pkl"
            
            with open(model_path, 'rb') as f:
                save_data = pickle.load(f)
            
            self.models[model_name] = save_data['model']
            self.scalers[model_name] = save_data['scaler']
            
            logger.info(f"Model {model_name} loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return False
    
    def get_model_performance(self, model_name: str) -> Dict[str, Any]:
        """Get performance metrics for a model"""
        try:
            if model_name not in self.models:
                return {"error": f"Model {model_name} not found"}
            
            # Find training result
            training_result = None
            for result in self.training_history:
                if result.model_name == model_name:
                    training_result = result
                    break
            
            if not training_result:
                return {"error": f"No training history for {model_name}"}
            
            return {
                'model_name': model_name,
                'accuracy': training_result.accuracy,
                'loss': training_result.loss,
                'training_time': training_result.training_time,
                'epochs_completed': training_result.epochs_completed,
                'validation_accuracy': training_result.validation_accuracy,
                'timestamp': training_result.timestamp.isoformat(),
                'model_path': training_result.model_path,
                'tensorflow_used': TENSORFLOW_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"Error getting model performance: {e}")
            return {"error": str(e)}
    
    def get_all_models(self) -> List[str]:
        """Get list of all available models"""
        return list(self.models.keys())
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model"""
        try:
            if model_name in self.models:
                del self.models[model_name]
            if model_name in self.scalers:
                del self.scalers[model_name]
            
            # Remove from training history
            self.training_history = [r for r in self.training_history if r.model_name != model_name]
            
            # Remove file
            import os
            model_path = f"{self.models_dir}/{model_name}.pkl"
            if os.path.exists(model_path):
                os.remove(model_path)
            
            logger.info(f"Model {model_name} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting model {model_name}: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get deep learning system status"""
        return {
            'tensorflow_available': TENSORFLOW_AVAILABLE,
            'total_models': len(self.models),
            'training_history_count': len(self.training_history),
            'models_directory': self.models_dir,
            'available_models': list(self.models.keys()),
            'system_ready': True
        } 