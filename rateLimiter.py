from irate_limiter import IRateLimiter
import time
from log import get_logger

log = get_logger(__name__)

class RateLimiter(IRateLimiter):
    def __init__(self, redis_client, rate_limit, refill_rate):
        self.redis = redis_client
        self.rate_limit= rate_limit
        self.refill_rate = refill_rate
    
    def is_allowed(self, client_ip):
        # check if client is allowed to make a request
        current_time = int(time.time())
        user_data = self.redis.get(client_ip)
        if user_data:
            tokens, last_time = map(int, user_data.decode('utf-8').split(':'))
            elapsed_time = current_time - last_time
            refill_tokens = elapsed_time // self.refill_rate
            if refill_tokens + tokens > 0:
                tokens = min(refill_tokens + tokens - 1, self.rate_limit)
                self.redis.set(client_ip, f'{tokens}:{current_time}')
                return True, None
            else:
                self.redis.set(client_ip, f'{tokens}:{current_time}')
                return False, None
        else:
            self.redis.set(client_ip, f'{self.rate_limit - 1}:{current_time}')
            return False, None