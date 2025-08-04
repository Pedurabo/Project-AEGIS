"""
DEVELOPMENTAL SILO - Error Handling System
Comprehensive error handling with proven development techniques
"""

import logging
import traceback
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
import threading
from contextlib import contextmanager


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification"""
    VALIDATION = "validation"
    NETWORK = "network"
    MODEL = "model"
    DATA = "data"
    SYSTEM = "system"
    USER = "user"
    UNKNOWN = "unknown"


@dataclass
class ErrorInfo:
    """Structured error information"""
    timestamp: datetime
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    module: str
    function: str
    line_number: int
    stack_trace: str
    context: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class ErrorHandler:
    """Comprehensive error handling system"""
    
    def __init__(self, log_file: str = "logs/errors.log", max_errors: int = 1000):
        self.log_file = log_file
        self.max_errors = max_errors
        self.error_history: List[ErrorInfo] = []
        self.error_callbacks: Dict[ErrorCategory, List[Callable]] = {
            category: [] for category in ErrorCategory
        }
        self.recovery_strategies: Dict[ErrorCategory, Callable] = {}
        
        # Create logs directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Register default recovery strategies
        self._register_default_recovery_strategies()
        
        logger.info("Error Handler initialized")
    
    def _setup_logging(self):
        """Setup error logging"""
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.ERROR)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to root logger
        logging.getLogger().addHandler(file_handler)
    
    def _register_default_recovery_strategies(self):
        """Register default error recovery strategies"""
        self.register_recovery_strategy(ErrorCategory.NETWORK, self._recover_network_error)
        self.register_recovery_strategy(ErrorCategory.MODEL, self._recover_model_error)
        self.register_recovery_strategy(ErrorCategory.DATA, self._recover_data_error)
        self.register_recovery_strategy(ErrorCategory.VALIDATION, self._recover_validation_error)
    
    def handle_error(self, error: Exception, severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                    category: ErrorCategory = ErrorCategory.UNKNOWN, context: Dict[str, Any] = None,
                    user_id: Optional[str] = None, session_id: Optional[str] = None) -> ErrorInfo:
        """Handle an error with comprehensive logging and recovery"""
        try:
            # Get error information
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # Create error info
            error_info = ErrorInfo(
                timestamp=datetime.now(),
                error_type=type(error).__name__,
                error_message=str(error),
                severity=severity,
                category=category,
                module=error.__module__ if hasattr(error, '__module__') else 'unknown',
                function=traceback.extract_tb(exc_traceback)[-1].name if exc_traceback else 'unknown',
                line_number=traceback.extract_tb(exc_traceback)[-1].lineno if exc_traceback else 0,
                stack_trace=traceback.format_exc(),
                context=context or {},
                user_id=user_id,
                session_id=session_id
            )
            
            # Log error
            self._log_error(error_info)
            
            # Store in history
            self._store_error(error_info)
            
            # Execute callbacks
            self._execute_callbacks(error_info)
            
            # Attempt recovery
            self._attempt_recovery(error_info)
            
            return error_info
            
        except Exception as e:
            # Fallback error handling
            logger.error(f"Error in error handler: {e}")
            return None
    
    def _log_error(self, error_info: ErrorInfo):
        """Log error with appropriate level"""
        log_message = (
            f"[{error_info.severity.value.upper()}] {error_info.category.value}: "
            f"{error_info.error_type}: {error_info.error_message} "
            f"in {error_info.module}.{error_info.function}:{error_info.line_number}"
        )
        
        if error_info.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error_info.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
        
        # Log stack trace for high severity errors
        if error_info.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            logger.debug(f"Stack trace: {error_info.stack_trace}")
    
    def _store_error(self, error_info: ErrorInfo):
        """Store error in history with size limit"""
        self.error_history.append(error_info)
        
        # Maintain size limit
        if len(self.error_history) > self.max_errors:
            self.error_history = self.error_history[-self.max_errors:]
    
    def _execute_callbacks(self, error_info: ErrorInfo):
        """Execute registered callbacks for error category"""
        callbacks = self.error_callbacks.get(error_info.category, [])
        for callback in callbacks:
            try:
                callback(error_info)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")
    
    def _attempt_recovery(self, error_info: ErrorInfo):
        """Attempt error recovery"""
        recovery_strategy = self.recovery_strategies.get(error_info.category)
        if recovery_strategy:
            try:
                recovery_strategy(error_info)
            except Exception as e:
                logger.error(f"Error in recovery strategy: {e}")
    
    def register_callback(self, category: ErrorCategory, callback: Callable[[ErrorInfo], None]):
        """Register error callback for specific category"""
        if category not in self.error_callbacks:
            self.error_callbacks[category] = []
        self.error_callbacks[category].append(callback)
    
    def register_recovery_strategy(self, category: ErrorCategory, strategy: Callable[[ErrorInfo], None]):
        """Register recovery strategy for error category"""
        self.recovery_strategies[category] = strategy
    
    def _recover_network_error(self, error_info: ErrorInfo):
        """Recovery strategy for network errors"""
        logger.info("Attempting network error recovery...")
        # Implement network retry logic
        # For now, just log the attempt
    
    def _recover_model_error(self, error_info: ErrorInfo):
        """Recovery strategy for model errors"""
        logger.info("Attempting model error recovery...")
        # Implement model reload/retrain logic
        # For now, just log the attempt
    
    def _recover_data_error(self, error_info: ErrorInfo):
        """Recovery strategy for data errors"""
        logger.info("Attempting data error recovery...")
        # Implement data validation/cleanup logic
        # For now, just log the attempt
    
    def _recover_validation_error(self, error_info: ErrorInfo):
        """Recovery strategy for validation errors"""
        logger.info("Attempting validation error recovery...")
        # Implement input sanitization logic
        # For now, just log the attempt
    
    @contextmanager
    def error_context(self, category: ErrorCategory = ErrorCategory.UNKNOWN,
                     severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                     context: Dict[str, Any] = None):
        """Context manager for error handling"""
        try:
            yield
        except Exception as e:
            self.handle_error(e, severity, category, context)
            raise
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        if not self.error_history:
            return {"message": "No errors recorded"}
        
        # Count by severity
        severity_counts = {}
        for severity in ErrorSeverity:
            severity_counts[severity.value] = len([
                e for e in self.error_history if e.severity == severity
            ])
        
        # Count by category
        category_counts = {}
        for category in ErrorCategory:
            category_counts[category.value] = len([
                e for e in self.error_history if e.category == category
            ])
        
        # Recent errors
        recent_errors = self.error_history[-10:] if len(self.error_history) >= 10 else self.error_history
        
        return {
            'total_errors': len(self.error_history),
            'severity_distribution': severity_counts,
            'category_distribution': category_counts,
            'recent_errors': [
                {
                    'timestamp': e.timestamp.isoformat(),
                    'type': e.error_type,
                    'message': e.error_message,
                    'severity': e.severity.value,
                    'category': e.category.value
                }
                for e in recent_errors
            ],
            'system_health': self._calculate_system_health()
        }
    
    def _calculate_system_health(self) -> str:
        """Calculate system health based on error patterns"""
        if not self.error_history:
            return "excellent"
        
        # Get recent errors (last hour)
        recent_cutoff = datetime.now().timestamp() - 3600
        recent_errors = [
            e for e in self.error_history 
            if e.timestamp.timestamp() > recent_cutoff
        ]
        
        # Count critical errors
        critical_count = len([
            e for e in recent_errors 
            if e.severity == ErrorSeverity.CRITICAL
        ])
        
        # Count high severity errors
        high_count = len([
            e for e in recent_errors 
            if e.severity == ErrorSeverity.HIGH
        ])
        
        if critical_count > 0:
            return "critical"
        elif high_count > 5:
            return "poor"
        elif high_count > 2:
            return "fair"
        elif len(recent_errors) > 10:
            return "good"
        else:
            return "excellent"
    
    def clear_error_history(self):
        """Clear error history"""
        self.error_history.clear()
        logger.info("Error history cleared")
    
    def export_error_report(self, file_path: str = None) -> str:
        """Export error report to file"""
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"logs/error_report_{timestamp}.json"
        
        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'statistics': self.get_error_statistics(),
                'error_history': [
                    {
                        'timestamp': e.timestamp.isoformat(),
                        'error_type': e.error_type,
                        'error_message': e.error_message,
                        'severity': e.severity.value,
                        'category': e.category.value,
                        'module': e.module,
                        'function': e.function,
                        'line_number': e.line_number,
                        'context': e.context
                    }
                    for e in self.error_history
                ]
            }
            
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Error report exported to: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error exporting error report: {e}")
            return ""


# Global error handler instance
error_handler = ErrorHandler()


def handle_error_decorator(category: ErrorCategory = ErrorCategory.UNKNOWN,
                          severity: ErrorSeverity = ErrorSeverity.MEDIUM):
    """Decorator for automatic error handling"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_error(e, severity, category, {
                    'function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                })
                raise
        return wrapper
    return decorator


def safe_execute(func: Callable, *args, default_return=None, **kwargs):
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler.handle_error(e, ErrorSeverity.MEDIUM, ErrorCategory.UNKNOWN, {
            'function': func.__name__,
            'args': str(args),
            'kwargs': str(kwargs)
        })
        return default_return 