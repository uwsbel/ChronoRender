import sys
from ri_constants import *
from ri_types import *

def RiErrorIgnore(code, severity, message):
    """Standard error handler.

    Ignores error messages."""
    
    pass

def RiErrorPrint(code, severity, message):
    """Standard error handler.

    Prints the message to stderr."""

    if severity==RIE_WARNING:
        print >> sys.stderr, "WARNING:",
    elif severity==RIE_ERROR or severity==RIE_SEVERE:
        print >> sys.stderr, "ERROR (%d):"%(code),        
    print >> sys.stderr, message

def RiErrorAbort(code, severity, message):
    """Standard error handler.

    Prints the message to stderr and aborts if it was an error."""

    RiErrorPrint(code, severity, message)
    if severity>=RIE_ERROR:
        sys.exit(1)


class RIException(Exception):
    """RenderMan Interface exception

    This exception is thrown by the error handler RiErrorException()."""
    pass

def RiErrorException(code, severity, message):
    """This error handler raises an exception when an error occurs.

    If the "error" is only an info or warning message the message is
    printed to stderr, otherwise the exception RIException is thrown.
    The actual error message is given as an argument to the constructor of
    RIException (the line with the file name, line number and offending
    Ri call is removed. You will have that information in the Traceback).
    """
    if severity<RIE_ERROR:
        RiErrorPrint(code, severity, message)
    else:
        if message[:7]=="In file":
            n=message.find("\n")
            message=message[n+1:]
        raise RIException(message)
