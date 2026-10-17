"""Service configuration for the collector."""
from vendor.ratelib import RateLimiter

MAX_EVENTS_PER_SEC = 240
BURST_CAPACITY = 500

limiter = RateLimiter(BURST_CAPACITY, MAX_EVENTS_PER_SEC)
