#!/usr/bin/env python3
"""
Development server runner for the auth backend.

This script starts the FastAPI development server with hot reload enabled.
"""

import os
import sys
from pathlib import Path
import uvicorn

# Change to the script's directory to ensure correct imports
script_dir = Path(__file__).parent
os.chdir(script_dir)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )
