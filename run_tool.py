#!/usr/bin/env python3
"""
Quick startup script for the Penetration Testing Toolset
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main entry point for the penetration testing tool."""
    print("🔐 Penetration Testing Toolset")
    print("=" * 50)
    
    try:
        # Import the main application
        from penetration_tools.main import app
        
        # Set up basic configuration
        os.environ.setdefault("ENVIRONMENT", "development")
        os.environ.setdefault("DEBUG", "true")
        os.environ.setdefault("SECRET_KEY", "dev-secret-key-change-in-production")
        os.environ.setdefault("DATABASE_URL", "sqlite:///./penetration_tools.db")
        os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
        
        print("✅ Configuration loaded")
        print("🚀 Starting FastAPI server...")
        print("📖 API Documentation will be available at: http://localhost:8000/docs")
        print("🏥 Health check at: http://localhost:8000/health")
        print("=" * 50)
        
        # Import uvicorn and run the server
        import uvicorn
        uvicorn.run(
            "penetration_tools.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Please install dependencies first:")
        print("   pip install -e .")
        return 1
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 