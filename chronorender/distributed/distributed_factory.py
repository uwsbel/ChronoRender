class DistributedFactoryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DistributedFactory():
    def __init__(self):
        self._bDrmaa = False
        self._bPBS   = False

        self._validateSystemDistributedManagers()

    def build(self, typename=None, **kwargs):

        if self._bDrmaa:
            from dist_drmaa import DRMAA
            if typename and typename != DRAMM.getTypeName():
                pass
            else:
                return DRMAA(**kwargs)

        if self._bPBS:
            from dist_pbs import PBS
            if typename and typename != PBS.getTypeName():
                pass
            else:
                return PBS(**kwargs)

        raise DistributedFactoryException('distributed manager is not supported OR not installed on system')

    def _buildFromTypeName(self, name):
        return

    def _validateSystemDistributedManagers(self):
        self._validateDRMAA()
        self._validatePBS()

    def _validatePBS(self):
        try:
            import pbs
            self._bPBS = True
        except ImportError:
            self._bPBS = False
            pass

    def _validateDRMAA(self):
        try:
            import drmaa
            self._bDrmaa = True
        except ImportError:
            self._bDrmaa = False
            pass
