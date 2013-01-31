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

    def build(self, manager=''):
        if self._bDrmaa:
            from dist_drmaa import DRMAA
            return DRMAA()
        elif self._bPBS:
            from dist_pbs import PBS
            return PBS()
        else:
          raise DistributedFactoryException('no supported distributed manager installed on system')

    def _validateSystemDistributedManagers(self):
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
