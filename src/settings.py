import os

APP = 'Cloud-Group-8'
APP_VERSION = "1.0.0"
LOG_PATTERN = '%(asctime)s.%(msecs)s:%(name)s:%(thread)d:(%(threadName)-10s):%(levelname)s:%(process)d:%(message)s'

# POSTGRESQL
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
PG_HOST = os.getenv('PG_HOST', 'miso-grupo8.cqeaj94zhds3.us-east-1.rds.amazonaws.com')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DATABASE = os.getenv('PG_DATABASE', 'bdconversion')

# S3
BUCKET = os.getenv("BUCKET", "bucket-grupo8-nube")
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', "ASIAQPOUW3HCYOLPLCY4")
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', "/rrxgsOV4eOr2M7upcySW61yMfgcxGlIP2qvXDLU")
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN', "FwoGZXIvYXdzELj//////////wEaDFkdrqRJ9bhd7QXwBCLJAWNLLbzzs0T5WaKCoPcfZPMdTe2wiojBTvbVng7KZuggPWfvE2xt8AZOu7q1yHscXqoEWX3pk+UNYHJF3jKOaIPSHQo4jtbL7Mjg++yDky0imK6Ec6eKPSREYvt1erRgjwAzXe78kL0TXbYMhUYIKVLn4MFJFKsCR03ubrbK2M4WMF/toLbua7EkrH6Z85rPoTIT6vACe6OgQAuufiVKulTJjRhUWNDAuDBcCAZu/2vcSVPs3frrp2xe2oTmpTMCG5W9/ObXXSXoGSi6/rSNBjItLzN1eav1eVdj6wZnufh6f/goq5d/3zRQohhNPvoN5g1s7qRY8YZhNzOchhBI")

# WAITRESS CONFIG
WAITRESS_WORKERS = int(os.getenv('WAITRESS_WORKERS', 8))
WAITRESS_CHANNELS = int(os.getenv('WAITRESS_CHANNELS', 100))
