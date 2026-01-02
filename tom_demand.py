#!/usr/bin/env python3
"""
Main entry point for TOM Demand Management System.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli import cli

if __name__ == '__main__':
    cli()
