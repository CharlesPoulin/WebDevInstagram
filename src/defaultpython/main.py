import logging
import os

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main entry point for the defaultpython application.
    """
    load_dotenv()

    app_env: str = os.getenv("APP_ENV", "development")

    logger.info("Starting defaultpython in %s mode", app_env)
    logger.info("Hello from defaultpython! Environment: %s", app_env)


if __name__ == "__main__":
    main()
