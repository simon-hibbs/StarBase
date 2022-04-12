# my_logger.py

"""This is 'my_logger' module, which is imported into all
   the other modules of my application."""

import logging
import logging.handlers
from functools import wraps

# Create a global logger

_vs_logger = None

# Set default DEBUG_ON True - in which case debug messages
# are saved to the log file.  Or set it to False - in which
# case only INFO and ERROR messages are saved to the log file

_DEBUG_ON = True

def set_logger():
    "Set up the logger"
    global _vs_logger
    _vs_logger = logging.getLogger("my_logger")
    # Set the logger level
    if _DEBUG_ON:
        _vs_logger.setLevel(logging.DEBUG)
    else:
        _vs_logger.setLevel(logging.INFO)

    # Set the format
    form = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Add the log message handler to the logger
    # The location of the logfile is given here as 'logfile.txt'
    # in an actual application I would take a bit of care
    # where this is located

    file_handler = logging.handlers.RotatingFileHandler("logfile.txt",
                                                    maxBytes=10000000,
                                                    backupCount=5)
    console_handler = logging.StreamHandler()

    file_handler.setFormatter(form)
    console_handler.setFormatter(form)
    
    _vs_logger.addHandler(file_handler)
    _vs_logger.addHandler(console_handler)

def info_log(message):
    "Log message with level info"
    if _vs_logger:
        _vs_logger.info(str(message))

def debug_log(message):
    "Log message with level debug"
    if _DEBUG_ON and _vs_logger:
        _vs_logger.debug(str(message))

def logmethod(f):
    "Creates a decorator to log a method"
    @wraps(f)
    def wrapper(self, *args, **kwds):
        debug_log("%s in %s called" % (f.__name__, self.__class__.__name__))
        return f(self, *args, **kwds)
    return wrapper

def exception_log(message):
    "Log message with level error plus exception traceback"
    if _vs_logger:
        _vs_logger.exception(str(message))
