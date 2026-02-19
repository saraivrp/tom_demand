"""
TOM Demand Management System

A demand prioritization system for CTT based on three proportional allocation methods:
Sainte-Laguë (default), D'Hondt, and WSJF (Weighted Shortest Job First).
"""

import os
import sys

# Keep legacy flat imports working when package is imported as `src.*`.
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

__version__ = "3.0.0"
__author__ = "Lean Portfolio Management Specialist"
