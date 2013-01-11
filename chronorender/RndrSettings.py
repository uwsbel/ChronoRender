import Object 
import copy

class RndrSettingsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrSettings(Object.Object):

    def __init__(self, *args, **kwargs):
        super(RndrSettings, self).__init__(args, kwargs)

        self._initFromNamedArgs(kwargs)
        self._getAddtParams(kwargs)

    def __str__(self):
        out = []
        out.append(super(RndrSettings, self).__str__())
        out.append(self._dataDelim)
        return str(out)

    def _initFromNamedArgs(self, args):
        self._dataDelim = args['delim']         if ('delim' in args) else ','
        self._writeFileExp = args['write']      if ('write' in args) else './out_####.tif'
        self._dataFileExp = args['data']        if ('data'in args) else './*.dat'
        self._scaling = float(args['scaling'])  if ('scaling' in args) else 1.0
        self._radians = bool(args['radians'])   if ('radians' in args) else False
        self._searchPath = args['searchpath']   if ('searchpath' in args) else './'
        self._frameRange = args['framerange']   if ('framerange' in args) else '0 0'
        self._dataFormat = args['dataformat'].split(',')   if ('dataformat' in args) else ['ID', 'POS_X', 'POS_Y', 'POS_Z']

    def _getAddtParams(self, args):
        p = copy.deepcopy(args)

        if ('delim' in args): del p['delim']
        if ('write' in args): del p['write']
        if ('scaling' in args): del p['scaling']
        if ('data' in args): del p['data']
        if ('radians' in args): del p['radians']
        if ('searchpath' in args): del p['searchpath']
        if ('framerange' in args): del p['framerange']
        if ('dataformat' in args): del p['dataformat']

        self._params = p
