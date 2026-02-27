from prometheus_client import Counter, Histogram, start_http_server
import time

REQUEST_COUNT = Counter("sentinel_requests_total", "Total API Requests")
REQUEST_LATENCY = Histogram("sentinel_request_latency_seconds", "Request latency")

def start_metrics_server():
    start_http_server(9100)

def track_request(func):
    def wrapper(*args, **kwargs):
        REQUEST_COUNT.inc()
        start = time.time()
        result = func(*args, **kwargs)
        REQUEST_LATENCY.observe(time.time() - start)
        return result
    return wrapper
