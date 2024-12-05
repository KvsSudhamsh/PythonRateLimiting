import redis
import time
from datetime import datetime
from flask import Flask, request, jsonify

# Initialize Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Initialize Flask app
app = Flask(__name__)

# Define rate limit parameters
RATE_LIMIT = 6  # Requests per minute
TIME_WINDOW = 60  # Time window in seconds
REFILL_RATE = TIME_WINDOW//RATE_LIMIT
def get_client_ip():
    """Get the client's IP address."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@app.route("/hello", methods=["GET"])
def function():
    client_ip = get_client_ip()
    print("user ip:",client_ip)
    current_time = int(time.time())
    user = r.get(client_ip)
    if user:
        flag = False
        tokens, curr_time = map(int,user.decode('utf-8').split(':'))
        diff_time = current_time - curr_time
        refill_tokens = diff_time//REFILL_RATE
        if refill_tokens + tokens>0:
            flag = True
            tokens = min(refill_tokens+tokens-1,RATE_LIMIT)
            r.set(client_ip,f'{tokens}:{current_time}')
        else:
            r.set(client_ip,f'{tokens}:{current_time}')
    else:
        r.set(client_ip,f'{RATE_LIMIT-1}:{current_time}')
    if flag:
        return jsonify({"message":"successful"})
    else:
        return jsonify({"message":f"rate limited retry after: {REFILL_RATE - diff_time} seconds"})

if __name__ == "__main__":
    app.run(debug=True)