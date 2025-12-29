
"""Module for configuring the logger."""
import logging
from logging import Logger
import sys


def configure_logger(name) -> Logger:
    """Configure and return a logger with the given name."""
    logger = logging.getLogger(name)

    ## To avoid duplicate logs, check if the logger already has handlers
    if logger.handlers:
        return logger

    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    format_str = "%(asctime)s [%(module)s] " ": %(levelname)-8s [%(process)d] %(message)s"
    formatter = logging.Formatter(format_str)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    ## Write Azure SDK logs to same handler
    azure_logger_names  = [
        "azure",
        "azure.identity",
        "azure.core.pipeline.policies.http_logging_policy",
        "msal"
    ]
    
    for lname in azure_logger_names:
        l = logging.getLogger(lname)
        l.setLevel(logging.DEBUG)
        l.propagate = False  # prevent duplication to root
        # ensure we only add our handler once
        if not any(isinstance(h, logging.StreamHandler) for h in l.handlers):
            l.addHandler(stream_handler)

    return logger