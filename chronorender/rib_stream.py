
class RIBStream:
    """This class encapsulates the output stream.

    The version number is automatically placed into the stream before
    any "real" Ri calls are made. Output from RiArchiveRecord() will
    be placed before the version number. (Note: The version line is disabled
    for now).
    """
    
    def __init__(self, outstream):
        self.out = outstream
        self.output_version = 1

    def close(self):
        """Close the stream, unless it's stdout."""
        if self.out!=sys.stdout:
            self.out.close()

    def flush(self):
        """Flush the internal buffer."""
        self.out.flush()

    def write(self, data):
        """Write data into the stream."""
        if self.output_version:
            # The binding contains newer calls, so this version number
            # might not be accurate anyway.
#            self.out.write('version 3.03\n')
            self.output_version = 0
        self.out.write(data)

    def writeArchiveRecord(self, data):
        """Same as write() but suppresses the version number.

        This method is used by RiArchiveRecord(), everyone else uses
        write().
        """
        self.out.write(data)
