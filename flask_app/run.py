import os
from main import app

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['PYTHONPATH'] = BASE_DIR
    app.run(host='localhost', port=8080, debug=True)
