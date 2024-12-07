from redis import Redis
# from datetime import datetime
from flask import Flask, request, jsonify
from log import get_logger
from rateLimiter import RateLimiter
import constants as const
import time

log = get_logger(__name__)

# Initialize Redis
r = Redis(host='localhost', port=6379, db=0)

# Initialize Flask app
app = Flask(__name__)

def get_client_ip():
    """Get the client's IP address."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


@app.route("/hello", methods=["GET"])
def handle_request():
    client_ip = get_client_ip()
    log.info(f"User IP: {client_ip}")
    # return jsonify({"message":"successful"})

    rate_limiter = RateLimiter(r, const.RATE_LIMIT, const.REFILL_RATE)
    allowed, retry_after = rate_limiter.is_allowed(client_ip)
    if allowed:
        return jsonify({"message":"successful"})
    else:
        return jsonify({"message":f"rate limited retry after: {retry_after} seconds"}), 429

if __name__ == "__main__":
    app.run(debug=True)