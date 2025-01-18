import sys

from loguru import logger


def setup_logging():
    """
    Configures the loguru logger to handle service errors and other logs with color and graceful error handling.
    """
    # Remove default logger to avoid duplicate logs
    logger.remove()

    # Add a new logger with custom format and color
    logger.add(sys.stdout, 
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
               level="INFO",
               colorize=True)

    # Add a file handler to save logs to a file
    logger.add("logs/app.log", 
               rotation="10 MB", 
               retention="10 days", 
               level="DEBUG", 
               format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}")

    # Graceful error handling
    def exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = exception_handler
    
    return logger

