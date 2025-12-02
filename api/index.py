"""
Vercel serverless function entry point for Flask app

Last Updated: December 2, 2025
Python Version: 3.14+
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the app variable for Python serverless functions
# Flask app is WSGI-compatible and works directly with Vercel

