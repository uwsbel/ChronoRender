
from finderabs import FinderAbs
from finderrel import FinderRel

class FinderFactory():
    @staticmethod
    def build(paths, relativeTo=None):
        if relativeTo:
            return FinderRel(paths, relativeTo)
        else:
            return FinderAbs(paths)
