class RIBStream:
    """This class encapsulates the output stream.

    The version number is automatically placed into the stream before
    any "real" Ri calls are made. Output from RiArchiveRecord() will
    be placed before the version number. (Note: The version line is disabled
    for now).
    """
    
    def __init__(self, outstream, outtype=''):
        self.out = outstream
        self.outtype = outtype
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
        self.out.write(data)

    def writeArchiveRecord(self, data):
        """Same as write() but suppresses the version number.

        This method is used by RiArchiveRecord(), everyone else uses
        write().
        """
        self.out.write(data)

    def getText(self):
        if self.outtype == 'str':
            return self.out.getvalue()
        return ''
