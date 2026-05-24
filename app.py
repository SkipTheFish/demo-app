import logging
import time
import random
from flask import Flask, request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    cost = random.randint(10, 200)
    user = request.args.get('user', 'anonymous')
    logger.info(f"Request processed: method=GET path=/ user={user} cost={cost}ms status=200")
    return f'Hello from demo-app v1! user={user}\n'

@app.route('/error')
def error():
    user = request.args.get('user', 'anonymous')
    logger.error(f"Request failed: method=GET path=/error user={user} cost=5000ms status=500")
    return 'Internal Server Error\n', 500

@app.route('/health')
def health():
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
