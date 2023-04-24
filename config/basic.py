"""Basic config

To set project basic config
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Project path
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

# .env location
DOTENV_PATH = os.path.join(PROJECT_PATH, '.env')
