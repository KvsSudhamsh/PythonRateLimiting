# Define rate limit parameters
RATE_LIMIT = 6  # Requests per minute
TIME_WINDOW = 60  # Time window in seconds
REFILL_RATE = TIME_WINDOW//RATE_LIMIT