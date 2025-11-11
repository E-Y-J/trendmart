import os
import sys

# Ensure the BACKEND directory is on sys.path so 'ai_recom_system' resolves
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))

# Also ensure the REPO ROOT (parent of 'backend') is on sys.path so 'backend.*'
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")))
