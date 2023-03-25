import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


logging.basicConfig(level="INFO")
sentry_logging = LoggingIntegration(
    level=logging.DEBUG,        
    event_level=logging.INFO  
)
sentry_sdk.init(
    dsn="https://b9ad1f8593304e62bc4149b731a06296@o4504831080333312.ingest.sentry.io/4504831082889216",
    integrations=[
        sentry_logging,
    ],
    traces_sample_rate=1.0,
)

