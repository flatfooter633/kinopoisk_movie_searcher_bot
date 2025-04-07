# Import necessary modules
import asyncio
from logging import config, getLogger
from utils.logger import user_config

from os import name as os_name
from loader import main


# Main function to be run when the application starts
if __name__ == "__main__":
    # Configure logging using the provided configuration
    config.dictConfig(user_config)
    # Get the root logger
    logger = getLogger()
    try:
        # Set the event loop policy to WindowsSelectorEventLoopPolicy if the operating system is Windows
        # Event loop is closed is a known issue on Windows:
        # https://stackoverflow.com/questions/63860576/asyncio-event-loop-is-closed-when-using-asyncio-run
        if os_name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Log that the application has started
        logger.info("...Application started")
        # Run the main function from the loader module
        asyncio.run(main())
    except KeyboardInterrupt:
        # Log that the application is stopping
        logger.info("Application stopping...")
