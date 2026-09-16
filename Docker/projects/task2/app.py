import os
from flask import Flask

app = Flask(__name__)

# Read config from environment variables (not hardcoded) -> "secure config"
APP_NAME = os.getenv("APP_NAME", "ProgreeApp")
APP_ENV = os.getenv("APP_ENV", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret") 

@app.route('/')
def home():
    return f"Hello from {APP_NAME} running in {APP_ENV} mode!"

@app.route('/health')
def health():
    return {"status": "ok"} , 200

if __name__ == '__main__':
    # port also from env var
    port = int(os.getenv("PORT", 6767))
    app.run(host='0.0.0.0', port=port)

