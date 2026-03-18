import sys
import os

# Add your project directory to the path
project_home = '/home/YOUR_USERNAME/ai_teacher_platform'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

from app import create_app
application = create_app()
