"""
DEVELOPMENTAL SILO - Model Manager
Robust model persistence, validation, and management with proven development techniques
"""

import os
import json
import pickle
import hashlib
import shutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
import joblib
from enum import Enum

logger = logging.getLogger(__name__)


class ModelStatus(Enum):
    """Model status enumeration"""
    TRAINING = "training"
    READY = "ready"
    DEPRECATED = "deprecated"
    ERROR = "error"


@dataclass
class ModelMetadata:
    """Model metadata for tracking and validation"""
    model_id: str
    model_name: str
    model_type: str
    version: str
    created_at: datetime
    updated_at: datetime
    status: ModelStatus
    accuracy: float
    training_samples: int
    features_count: int
    file_size: int
    checksum: str
    dependencies: List[str]
    hyperparameters: Dict[str, Any]
    performance_metrics: Dict[str, float]


class ModelManager:
    """Robust model management system with proven development techniques"""
    
    def __init__(self, models_dir: str = "models", backup_dir: str = "models/backup"):
        self.models_dir = Path(models_dir)
        self.backup_dir = Path(backup_dir)
        self.metadata_file = self.models_dir / "metadata.json"
        self.models_registry: Dict[str, ModelMetadata] = {}
        
        # Create directories
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing metadata
        self._load_metadata()
        
        logger.info(f"Model Manager initialized with {len(self.models_registry)} models")
    
    def _load_metadata(self):
        """Load model metadata from file"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                    for model_id, metadata_dict in data.items():
                        # Convert string dates back to datetime
                        metadata_dict['created_at'] = datetime.fromisoformat(metadata_dict['created_at'])
                        metadata_dict['updated_at'] = datetime.fromisoformat(metadata_dict['updated_at'])
                        metadata_dict['status'] = ModelStatus(metadata_dict['status'])
                        self.models_registry[model_id] = ModelMetadata(**metadata_dict)
                        
        except Exception as e:
            logger.error(f"Error loading model metadata: {e}")
            # Create backup of corrupted metadata
            if self.metadata_file.exists():
                backup_path = self.metadata_file.with_suffix('.json.backup')
                shutil.copy2(self.metadata_file, backup_path)
                logger.info(f"Corrupted metadata backed up to {backup_path}")
    
    def _save_metadata(self):
        """Save model metadata to file"""
        try:
            # Convert metadata to serializable format
            serializable_data = {}
            for model_id, metadata in self.models_registry.items():
                metadata_dict = asdict(metadata)
                metadata_dict['created_at'] = metadata.created_at.isoformat()
                metadata_dict['updated_at'] = metadata.updated_at.isoformat()
                metadata_dict['status'] = metadata.status.value
                serializable_data[model_id] = metadata_dict
            
            # Save with atomic write
            temp_file = self.metadata_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            
            # Atomic move
            temp_file.replace(self.metadata_file)
            
        except Exception as e:
            logger.error(f"Error saving model metadata: {e}")
            raise
    
    def _generate_model_id(self, model_name: str, model_type: str) -> str:
        """Generate unique model ID"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{model_name}_{model_type}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum for integrity validation"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculating checksum: {e}")
            return ""
    
    def _validate_model_file(self, file_path: Path) -> bool:
        """Validate model file integrity"""
        try:
            if not file_path.exists():
                return False
            
            # Check file size
            if file_path.stat().st_size == 0:
                return False
            
            # Try to load the model
            with open(file_path, 'rb') as f:
                pickle.load(f)
            
            return True
            
        except Exception as e:
            logger.error(f"Model file validation failed: {e}")
            return False
    
    def save_model(self, model: Any, model_name: str, model_type: str, 
                  accuracy: float = 0.0, training_samples: int = 0,
                  features_count: int = 0, hyperparameters: Dict[str, Any] = None,
                  performance_metrics: Dict[str, float] = None) -> str:
        """Save model with comprehensive metadata and validation"""
        try:
            # Generate model ID
            model_id = self._generate_model_id(model_name, model_type)
            
            # Create model file path
            model_file = self.models_dir / f"{model_id}.pkl"
            
            # Prepare model data
            model_data = {
                'model': model,
                'model_name': model_name,
                'model_type': model_type,
                'saved_at': datetime.now(),
                'version': '1.0'
            }
            
            # Save model with atomic write
            temp_file = model_file.with_suffix('.tmp')
            with open(temp_file, 'wb') as f:
                pickle.dump(model_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Atomic move
            temp_file.replace(model_file)
            
            # Calculate file size and checksum
            file_size = model_file.stat().st_size
            checksum = self._calculate_checksum(model_file)
            
            # Create metadata
            metadata = ModelMetadata(
                model_id=model_id,
                model_name=model_name,
                model_type=model_type,
                version='1.0',
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status=ModelStatus.READY,
                accuracy=accuracy,
                training_samples=training_samples,
                features_count=features_count,
                file_size=file_size,
                checksum=checksum,
                dependencies=self._get_model_dependencies(model),
                hyperparameters=hyperparameters or {},
                performance_metrics=performance_metrics or {}
            )
            
            # Store metadata
            self.models_registry[model_id] = metadata
            self._save_metadata()
            
            logger.info(f"Model saved successfully: {model_id} ({model_name})")
            return model_id
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            # Cleanup on failure
            if 'temp_file' in locals() and temp_file.exists():
                temp_file.unlink()
            raise
    
    def load_model(self, model_id: str) -> Optional[Any]:
        """Load model with validation"""
        try:
            if model_id not in self.models_registry:
                logger.error(f"Model {model_id} not found in registry")
                return None
            
            metadata = self.models_registry[model_id]
            model_file = self.models_dir / f"{model_id}.pkl"
            
            # Validate file exists
            if not model_file.exists():
                logger.error(f"Model file not found: {model_file}")
                self._mark_model_error(model_id, "File not found")
                return None
            
            # Validate file integrity
            if not self._validate_model_file(model_file):
                logger.error(f"Model file validation failed: {model_file}")
                self._mark_model_error(model_id, "File validation failed")
                return None
            
            # Verify checksum
            current_checksum = self._calculate_checksum(model_file)
            if current_checksum != metadata.checksum:
                logger.error(f"Model checksum mismatch: {model_id}")
                self._mark_model_error(model_id, "Checksum mismatch")
                return None
            
            # Load model
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            # Update access time
            metadata.updated_at = datetime.now()
            self._save_metadata()
            
            logger.info(f"Model loaded successfully: {model_id}")
            return model_data['model']
            
        except Exception as e:
            logger.error(f"Error loading model {model_id}: {e}")
            self._mark_model_error(model_id, str(e))
            return None
    
    def _mark_model_error(self, model_id: str, error_message: str):
        """Mark model as having an error"""
        if model_id in self.models_registry:
            self.models_registry[model_id].status = ModelStatus.ERROR
            self.models_registry[model_id].updated_at = datetime.now()
            self._save_metadata()
            logger.warning(f"Model {model_id} marked as error: {error_message}")
    
    def _get_model_dependencies(self, model: Any) -> List[str]:
        """Get model dependencies"""
        dependencies = []
        
        # Check for common ML libraries
        if hasattr(model, 'predict_proba'):
            dependencies.append('scikit-learn')
        
        try:
            import tensorflow as tf
            if isinstance(model, tf.keras.Model):
                dependencies.append('tensorflow')
        except ImportError:
            pass
        
        return dependencies
    
    def list_models(self, status: Optional[ModelStatus] = None) -> List[ModelMetadata]:
        """List models with optional status filter"""
        models = list(self.models_registry.values())
        
        if status:
            models = [m for m in models if m.status == status]
        
        return sorted(models, key=lambda x: x.updated_at, reverse=True)
    
    def get_model_info(self, model_id: str) -> Optional[ModelMetadata]:
        """Get detailed model information"""
        return self.models_registry.get(model_id)
    
    def update_model_metadata(self, model_id: str, **kwargs) -> bool:
        """Update model metadata"""
        try:
            if model_id not in self.models_registry:
                logger.error(f"Model {model_id} not found")
                return False
            
            metadata = self.models_registry[model_id]
            
            # Update allowed fields
            allowed_fields = ['accuracy', 'performance_metrics', 'hyperparameters', 'status']
            for field, value in kwargs.items():
                if field in allowed_fields:
                    setattr(metadata, field, value)
            
            metadata.updated_at = datetime.now()
            self._save_metadata()
            
            logger.info(f"Model metadata updated: {model_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating model metadata: {e}")
            return False
    
    def delete_model(self, model_id: str, backup: bool = True) -> bool:
        """Delete model with optional backup"""
        try:
            if model_id not in self.models_registry:
                logger.error(f"Model {model_id} not found")
                return False
            
            metadata = self.models_registry[model_id]
            model_file = self.models_dir / f"{model_id}.pkl"
            
            # Create backup if requested
            if backup and model_file.exists():
                backup_file = self.backup_dir / f"{model_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                shutil.copy2(model_file, backup_file)
                logger.info(f"Model backed up to: {backup_file}")
            
            # Delete model file
            if model_file.exists():
                model_file.unlink()
            
            # Remove from registry
            del self.models_registry[model_id]
            self._save_metadata()
            
            logger.info(f"Model deleted: {model_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting model {model_id}: {e}")
            return False
    
    def cleanup_old_models(self, days_old: int = 30, status: ModelStatus = ModelStatus.DEPRECATED) -> int:
        """Clean up old models"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            deleted_count = 0
            
            models_to_delete = []
            for model_id, metadata in self.models_registry.items():
                if (metadata.status == status and 
                    metadata.updated_at < cutoff_date):
                    models_to_delete.append(model_id)
            
            for model_id in models_to_delete:
                if self.delete_model(model_id, backup=True):
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old models")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old models: {e}")
            return 0
    
    def export_model(self, model_id: str, export_path: str) -> bool:
        """Export model to external location"""
        try:
            if model_id not in self.models_registry:
                logger.error(f"Model {model_id} not found")
                return False
            
            metadata = self.models_registry[model_id]
            model_file = self.models_dir / f"{model_id}.pkl"
            
            if not model_file.exists():
                logger.error(f"Model file not found: {model_file}")
                return False
            
            # Create export package
            export_dir = Path(export_path)
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy model file
            exported_model_file = export_dir / f"{model_id}.pkl"
            shutil.copy2(model_file, exported_model_file)
            
            # Export metadata
            metadata_file = export_dir / f"{model_id}_metadata.json"
            with open(metadata_file, 'w') as f:
                metadata_dict = asdict(metadata)
                metadata_dict['created_at'] = metadata.created_at.isoformat()
                metadata_dict['updated_at'] = metadata.updated_at.isoformat()
                metadata_dict['status'] = metadata.status.value
                json.dump(metadata_dict, f, indent=2)
            
            logger.info(f"Model exported to: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting model {model_id}: {e}")
            return False
    
    def import_model(self, import_path: str) -> Optional[str]:
        """Import model from external location"""
        try:
            import_dir = Path(import_path)
            
            # Find model files
            model_files = list(import_dir.glob("*.pkl"))
            if not model_files:
                logger.error(f"No model files found in: {import_path}")
                return None
            
            model_file = model_files[0]
            model_id = model_file.stem
            
            # Load metadata
            metadata_file = import_dir / f"{model_id}_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata_dict = json.load(f)
                    metadata_dict['created_at'] = datetime.fromisoformat(metadata_dict['created_at'])
                    metadata_dict['updated_at'] = datetime.fromisoformat(metadata_dict['updated_at'])
                    metadata_dict['status'] = ModelStatus(metadata_dict['status'])
                    metadata = ModelMetadata(**metadata_dict)
            else:
                logger.warning(f"No metadata found for {model_id}, creating basic metadata")
                metadata = ModelMetadata(
                    model_id=model_id,
                    model_name=model_id,
                    model_type="unknown",
                    version="1.0",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    status=ModelStatus.READY,
                    accuracy=0.0,
                    training_samples=0,
                    features_count=0,
                    file_size=model_file.stat().st_size,
                    checksum=self._calculate_checksum(model_file),
                    dependencies=[],
                    hyperparameters={},
                    performance_metrics={}
                )
            
            # Copy model file
            target_model_file = self.models_dir / f"{model_id}.pkl"
            shutil.copy2(model_file, target_model_file)
            
            # Store metadata
            self.models_registry[model_id] = metadata
            self._save_metadata()
            
            logger.info(f"Model imported successfully: {model_id}")
            return model_id
            
        except Exception as e:
            logger.error(f"Error importing model from {import_path}: {e}")
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get model management system status"""
        try:
            total_models = len(self.models_registry)
            ready_models = len([m for m in self.models_registry.values() if m.status == ModelStatus.READY])
            error_models = len([m for m in self.models_registry.values() if m.status == ModelStatus.ERROR])
            
            total_size = sum(m.file_size for m in self.models_registry.values())
            
            return {
                'total_models': total_models,
                'ready_models': ready_models,
                'error_models': error_models,
                'total_size_mb': total_size / (1024 * 1024),
                'models_directory': str(self.models_dir),
                'backup_directory': str(self.backup_dir),
                'system_healthy': error_models == 0
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)} 