import multiprocessing
import os

# Binding
bind = "0.0.0.0:8000"

# Worker Formula: (2 x $num_cores) + 1
# On small EC2 instances, this ensures maximum CPU utilization without context switch overhead.
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4

# Timeouts
timeout = 300
graceful_timeout = 30
keepalive = 2

# Operational Resilience
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-" # Stdout for Docker log collection
errorlog = "-"  # Stderr
loglevel = os.getenv("LOG_LEVEL", "info")

# Process Naming
proc_name = "ictapoc-backend"
