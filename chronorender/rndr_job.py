import datetime

import meta_data as md
import rndr_doc as rd

# represent a render job
class RndrJobException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrJob():
    def __init__(self, inxml, factories):

        self._metadata      = md.MetaData(inxml)
        self._rndrdoc       = rd.RndrDoc(factories, self._metadata)
        self._datecreated   = datetime.date

    def run(self):
        self._rndrdoc.render()
