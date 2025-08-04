"""
Main FastAPI application for the penetration testing toolset.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import structlog

from .config import settings
from .core.logging import logger, security_logger
from .core.monitoring import metrics
from .api.v1.router import api_router
from .core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting penetration testing toolset", version=settings.api.version)
    
    # Initialize database
    await init_db()
    
    # Initialize monitoring
    if settings.monitoring.prometheus_enabled:
        metrics.start_server(settings.monitoring.prometheus_port)
        logger.info("Prometheus metrics server started", port=settings.monitoring.prometheus_port)
    
    yield
    
    # Shutdown
    logger.info("Shutting down penetration testing toolset")


# Create FastAPI application
app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
    description=settings.api.description,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1", "your-domain.com"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.security.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.security.allowed_methods,
    allow_headers=settings.security.allowed_headers,
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests with correlation ID."""
    start_time = time.time()
    
    # Generate correlation ID
    correlation_id = f"req_{int(start_time * 1000)}"
    
    # Log request
    logger.info(
        "incoming_request",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        correlation_id=correlation_id
    )
    
    # Add correlation ID to request state
    request.state.correlation_id = correlation_id
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        "request_completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time,
        correlation_id=correlation_id
    )
    
    # Add headers
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(
        "validation_error",
        errors=exc.errors(),
        correlation_id=getattr(request.state, "correlation_id", None)
    )
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "correlation_id": getattr(request.state, "correlation_id", None)
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(
        "http_error",
        status_code=exc.status_code,
        detail=exc.detail,
        correlation_id=getattr(request.state, "correlation_id", None)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "correlation_id": getattr(request.state, "correlation_id", None)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(
        "unhandled_exception",
        exception_type=type(exc).__name__,
        exception_message=str(exc),
        correlation_id=getattr(request.state, "correlation_id", None),
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "correlation_id": getattr(request.state, "correlation_id", None)
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.api.version,
        "environment": settings.environment,
        "timestamp": time.time()
    }


# Metrics endpoint
@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint."""
    if not settings.monitoring.prometheus_enabled:
        raise HTTPException(status_code=404, detail="Metrics not enabled")
    
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.api.title,
        "version": settings.api.version,
        "description": settings.api.description,
        "docs": "/docs" if settings.debug else None,
        "health": "/health",
        "metrics": "/metrics" if settings.monitoring.prometheus_enabled else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "penetration_tools.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.monitoring.log_level.lower()
    ) 