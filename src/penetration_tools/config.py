"""
Configuration management for the penetration testing toolset.
"""

from typing import Optional, List
from pydantic import BaseSettings, Field, validator
from pydantic_settings import BaseSettings as PydanticBaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: str = Field(default="postgresql://user:pass@localhost/penetration_tools", env="DATABASE_URL")
    pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")
    echo: bool = Field(default=False, env="DB_ECHO")


class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    
    url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    max_connections: int = Field(default=10, env="REDIS_MAX_CONNECTIONS")


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS settings
    allowed_origins: List[str] = Field(default=["http://localhost:3000"], env="ALLOWED_ORIGINS")
    allowed_methods: List[str] = Field(default=["GET", "POST", "PUT", "DELETE"], env="ALLOWED_METHODS")
    allowed_headers: List[str] = Field(default=["*"], env="ALLOWED_HEADERS")


class ScanSettings(BaseSettings):
    """Scan configuration settings."""
    
    max_concurrent_scans: int = Field(default=10, env="MAX_CONCURRENT_SCANS")
    scan_timeout_minutes: int = Field(default=60, env="SCAN_TIMEOUT_MINUTES")
    max_hosts_per_scan: int = Field(default=1000, env="MAX_HOSTS_PER_SCAN")
    
    # Nmap settings
    nmap_timing_template: str = Field(default="-T4", env="NMAP_TIMING_TEMPLATE")
    nmap_script_timeout: int = Field(default=300, env="NMAP_SCRIPT_TIMEOUT")
    
    # Web scan settings
    web_scan_threads: int = Field(default=10, env="WEB_SCAN_THREADS")
    web_scan_timeout: int = Field(default=30, env="WEB_SCAN_TIMEOUT")


class MonitoringSettings(BaseSettings):
    """Monitoring and logging configuration."""
    
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Prometheus settings
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    
    # Elasticsearch settings
    elasticsearch_url: Optional[str] = Field(default=None, env="ELASTICSEARCH_URL")
    elasticsearch_index: str = Field(default="penetration-tools", env="ELASTICSEARCH_INDEX")


class APISettings(BaseSettings):
    """API configuration settings."""
    
    title: str = Field(default="Penetration Testing Toolset API", env="API_TITLE")
    version: str = Field(default="0.1.0", env="API_VERSION")
    description: str = Field(default="A comprehensive penetration testing framework", env="API_DESCRIPTION")
    
    # Rate limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")


class Settings(PydanticBaseSettings):
    """Main application settings."""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # Database
    database: DatabaseSettings = DatabaseSettings()
    
    # Redis
    redis: RedisSettings = RedisSettings()
    
    # Security
    security: SecuritySettings = SecuritySettings()
    
    # Scanning
    scan: ScanSettings = ScanSettings()
    
    # Monitoring
    monitoring: MonitoringSettings = MonitoringSettings()
    
    # API
    api: APISettings = APISettings()
    
    @validator("environment")
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    @validator("debug")
    def validate_debug(cls, v, values):
        if values.get("environment") == "production" and v:
            raise ValueError("Debug mode cannot be enabled in production")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings() 