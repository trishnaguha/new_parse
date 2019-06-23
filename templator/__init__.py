
import re
from copy import deepcopy
from ansible.module_utils.network.common.utils import dict_merge, dict_diff

class Templator():

    PARSERS = {}

    def __init__(self, lines):
        self._lines = lines

    @staticmethod
    def to_int(string):
        if string:
            return int(string)
        return None

    @staticmethod
    def to_bool(string):
        if string:
            return True
        return None

    @staticmethod
    def default_not_no(string):
        if string == 'no':
            return False
        return None

    @staticmethod
    def default_is_no(string):
        if string != 'no':
            return True
        return None

    def _deepformat(self, tmplt, data, cast):
        if not cast:
            cast = {}
        wtmplt = deepcopy(tmplt)
        for tkey, tval in tmplt.items():
            ftkey = tkey.format(**data)
            if ftkey != tkey:
                wtmplt.pop(tkey)
            if isinstance(tval, dict):
                wtmplt[ftkey] = self._deepformat(tval, data, cast)
            elif isinstance(tval, list):
                wtmplt[ftkey] = [self._deepformat(x, data, cast) for x in tval]
            elif isinstance(tval, str):
                casted = False
                for dkey, dval in data.items():
                    if tval == "{{{x}}}".format(x=dkey) and dkey in cast:
                        res = getattr(self, cast[dkey])(dval)
                        wtmplt[ftkey] = res
                        casted = True
                if not casted:
                    try:
                        wtmplt[ftkey] = tval.format(**data)
                    except KeyError:
                        wtmplt.pop(tkey)
                if wtmplt[ftkey] == 'None' or wtmplt[ftkey] is None:
                    wtmplt.pop(ftkey)
        return wtmplt

    def parse(self):
        result = {}
        shared = {}
        for line in self._lines:
            for _pname, parser in self.PARSERS.items():
                cap = re.match(parser['getval'], line)
                if cap:
                    capdict = cap.groupdict()
                    if parser.get('shared'):
                        shared = capdict
                    vals = dict_merge(capdict, shared)
                    res = self._deepformat(deepcopy(parser['result']), vals,
                                           parser.get('cast'))
                    result = dict_merge(result, res)
        return result

    def render(self, data, parser_name, negate=False):
        try:
            setval = self.PARSERS[parser_name]['setval']
            if callable(setval):
                res = setval(data)
            else:
                res = setval.format(**data)
        except KeyError:
            res = None
        if negate:
            return 'no ' + res
        return res
