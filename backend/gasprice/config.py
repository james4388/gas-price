import os

TESTING = os.environ.get('TESTING') == 'true'

REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CACHE_DEFAULT_EXPIRED = int(os.environ.get('CACHE_DEFAULT_EXPIRED', 86400))
CACHE_PREFIX = os.environ.get('CACHE_PREFIX', 'GP')

CORS_WHITELIST = '*'  # Make a list of white listed domain for prod

GASFEED_API = os.environ.get('GASFEED_API', 'http://devapi.mygasfeed.com')
GASFEED_API_KEY = os.environ.get('GASFEED_API_KEY', '')

CLEARBIT_NAME_API = 'https://autocomplete.clearbit.com/v1/companies/suggest'

GOOGLE_GEOCODING_API_KEY = os.environ.get('GOOGLE_GEOCODING_API_KEY', '')

LOG_TYPE = os.environ.get('LOG_TYPE', 'stream')
LOG_STDOUT = os.environ.get('LOG_STDOUT', 'true') == 'true'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR')
LOG_FORMAT = os.environ.get(
    "LOG_FORMAT",
    "[%(asctime)s][%(levelname)s][%(name)s.%(funcName)s] %(message)s",
)
