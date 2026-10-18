# Vercel entrypoint: expose the Flask app from main.py as the serverless
# function. All routes are rewritten here by vercel.json.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: E402,F401
