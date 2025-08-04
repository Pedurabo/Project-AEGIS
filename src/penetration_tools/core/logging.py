"""
Structured logging configuration for the penetration testing toolset.
"""

import sys
import logging
from typing import Any, Dict
from datetime import datetime
import structlog
from structlog.stdlib import LoggerFactory
from structlog.processors import JSONRenderer, TimeStamper, add_log_level
from structlog.types import Processor

from ..config import settings


def add_correlation_id(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add correlation ID to log entries."""
    # In a real implementation, you'd get this from context
    # For now, we'll use a simple timestamp-based ID
    if "correlation_id" not in event_dict:
        event_dict["correlation_id"] = f"req_{datetime.now().timestamp()}"
    return event_dict


def setup_logging() -> structlog.stdlib.BoundLogger:
    """Setup structured logging with correlation IDs and JSON output."""
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.monitoring.log_level.upper())
    )
    
    # Configure structlog
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        TimeStamper(fmt="iso"),
        add_correlation_id,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Add JSON renderer for production, console for development
    if settings.environment == "production" or settings.monitoring.log_format == "json":
        processors.append(JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


# Global logger instance
logger = setup_logging()


class SecurityLogger:
    """Specialized logger for security events."""
    
    def __init__(self):
        self.logger = structlog.get_logger("security")
    
    def login_attempt(self, username: str, success: bool, ip_address: str, **kwargs):
        """Log login attempts."""
        self.logger.info(
            "login_attempt",
            username=username,
            success=success,
            ip_address=ip_address,
            event_type="authentication",
            **kwargs
        )
    
    def scan_started(self, scan_id: str, scan_type: str, target: str, user_id: str, **kwargs):
        """Log scan initiation."""
        self.logger.info(
            "scan_started",
            scan_id=scan_id,
            scan_type=scan_type,
            target=target,
            user_id=user_id,
            event_type="scan",
            **kwargs
        )
    
    def vulnerability_found(self, scan_id: str, vulnerability: str, severity: str, target: str, **kwargs):
        """Log discovered vulnerabilities."""
        self.logger.warning(
            "vulnerability_found",
            scan_id=scan_id,
            vulnerability=vulnerability,
            severity=severity,
            target=target,
            event_type="vulnerability",
            **kwargs
        )
    
    def exploit_attempt(self, scan_id: str, exploit: str, target: str, success: bool, **kwargs):
        """Log exploit attempts."""
        self.logger.info(
            "exploit_attempt",
            scan_id=scan_id,
            exploit=exploit,
            target=target,
            success=success,
            event_type="exploit",
            **kwargs
        )
    
    def security_alert(self, alert_type: str, message: str, severity: str, **kwargs):
        """Log security alerts."""
        self.logger.error(
            "security_alert",
            alert_type=alert_type,
            message=message,
            severity=severity,
            event_type="alert",
            **kwargs
        )


# Global security logger instance
security_logger = SecurityLogger() 