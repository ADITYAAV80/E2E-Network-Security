import os
import sys
import logging
import socket

# Custom filter to add IP address
class IPFilter(logging.Filter):
    def filter(self, record):
        record.ip = socket.gethostbyname(socket.gethostname())
        return True

# Define log format with IP at start
logging_str = "[%(ip)s] [%(asctime)s: %(levelname)s: %(module)s : %(message)s]"

# Log file setup
log_dir = "logs"
log_filepath = os.path.join(log_dir, "logging.log")
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger and add IP filter
logger = logging.getLogger("NetworkSecurity")
logger.addFilter(IPFilter())
