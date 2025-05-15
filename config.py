import os
import tempfile
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory as this file
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

# Get the base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    RADIUS_SERVER = os.getenv('RADIUS_SERVER', '127.0.0.1')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', 'testing123')
    MAX_REQUESTS_PER_10MIN = 30
    # Use system's temp directory instead of /dev/shm
    TEMP_DIR = os.getenv('TEMP_DIR', tempfile.gettempdir())
    
    # Create rate limit directory if it doesn't exist
    RATE_LIMIT_DIR = os.path.join(TEMP_DIR, 'eduroam_rate_limits')
    os.makedirs(RATE_LIMIT_DIR, exist_ok=True)
