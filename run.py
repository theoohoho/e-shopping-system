import os
from main import app


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.environ['PYTHONPATH'] = BASE_DIR
API_PORT = os.environ.get('API_PORT') or 80
DEBUG_MODE = os.environ.get('DEBUG_MODE') or False
app.run(host='localhost', port=API_PORT, debug=DEBUG_MODE)
