import os
import sys
import logging

# These placeholders (%(asctime)s, %(levelname)s, etc.) are automatically provided by Python's logging module
"""
Captures the current timestamp (asctime)
Identifies the log level (levelname) (INFO, ERROR, etc.)
Detects the module (module) where logging was called
Inserts the actual log message (message)
"""
logging_str = "[%(asctime)s: %(levelname)s: %(module)s : %(message)s]"

# create a logs directory with file path
log_dir = "logs"
log_filepath = os.path.join(log_dir,"logging.log")
os.makedirs(log_dir,exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
    logging.FileHandler(log_filepath),   # Save logs to a file
    logging.StreamHandler(sys.stdout)    # Print logs to console
]
)

# creates an instance with name DataScienceWorkflowLogger
logger = logging.getLogger("NetworkSecurity")