from redis import Redis
# from datetime import datetime
from flask import Flask, request, jsonify
from irate_limiter import IRateLimiter
from log import get_logger
from rateLimiter import RateLimiter
import constants as const
class RateLimitedApp:
    def __init__(self,rate_limiter:IRateLimiter):
        self.app = Flask(__name__)
        self.rate_limiter = rate_limiter
        self.log  = get_logger(__name__)
    def get_client_ip(self):
        """Get the client's IP address."""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0]
        return request.remote_addr

    def handle_request(self):
        client_ip = self.get_client_ip()
        self.log.info(f"User IP: {client_ip}")
        allowed, retry_after = self.rate_limiter.is_allowed(client_ip)
        if allowed:
            return jsonify({"message":"successful"})
        else:
            return jsonify({"message":f"rate limited retry after: {retry_after} seconds"}), 429
    
    def register_routes(self):
        """Register routes with the Flask app."""
        self.app.add_url_rule("/hello", "handle_request", self.handle_request, methods=["GET"])

    def run(self, debug=True):
        """Run the Flask app."""
        self.app.run(debug=debug)
if __name__ == "__main__":
    redis_client = Redis(host='localhost', port=6379, db=0)
    rate_limiter = RateLimiter(redis_client, const.RATE_LIMIT, const.REFILL_RATE)
    app = RateLimitedApp(rate_limiter)
    app.register_routes()
    app.run()