import logging

LOG_LEVEL_VAR = 'LOG_LEVEL'

# Check if .env file exists in parent directory
try:
    # Read environment variables from .env file
    with open('../.env') as f:
        for line in f:
            key_values = line.strip().split('=')
            key = key_values[0].strip()
            value = key_values[1].strip()
            if key == LOG_LEVEL_VAR:
                if str.isdigit(value):
                    log_level = int(value)
                else:
                    log_level = logging.getLevelName(value)
                break
except:
    # If .env file does not exist, use default logging level
    log_level = logging.CRITICAL + 1

# Set up basic configuration with default logging level
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)