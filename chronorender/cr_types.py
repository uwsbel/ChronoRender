
class floatlist(object):
    def __new__(cls, vals):
        if isinstance(vals, list):
            return [float(x) for x in vals]
        elif isinstance(vals, dict):
            return [float(x) for x in vals.items()]
        elif isinstance(vals, tuple):
            return map(lambda x: float(x), vals)
        else:
            return [float(vals)]
