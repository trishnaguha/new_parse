
import re
from copy import deepcopy
from ansible.module_utils.network.common.utils import dict_merge

class Templator():

    PARSERS = {}

    def __init__(self, lines=None):
        self._lines = lines

    @staticmethod
    def to_bool(string):
        if string:
            return True
        return False

    @staticmethod
    def to_int(string):
        if string:
            return int(string)
        return None

    @staticmethod
    def no_means_true(string):
        if string == 'no':
            return True
        return False

    @staticmethod
    def no_means_false(string):
        if string == 'no':
            return False
        return True

    def _deepformat(self, tmplt, data):
        wtmplt = deepcopy(tmplt)
        for tkey, tval in tmplt.items():
            ftkey = tkey.format(**data)
            if ftkey != tkey:
                wtmplt.pop(tkey)
            if isinstance(tval, dict):
                wtmplt[ftkey] = self._deepformat(tval, data)
            elif isinstance(tval, list):
                wtmplt[ftkey] = [self._deepformat(x, data)
                                 for x in tval]
            elif isinstance(tval, str):
                done = False
                for dkey, dval in data.items():
                    if tval == "{{{x}}}".format(x=dkey):
                        wtmplt[ftkey] = dval
                        done = True
                        break
                if not done:
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
                    # cast all the values
                    for key, val in capdict.items():
                        if key in parser.get('cast', {}):
                            capdict[key] = getattr(self,
                                                   parser['cast'][key])(val)

                    if parser.get('shared'):
                        shared = capdict
                    vals = dict_merge(capdict, shared)
                    res = self._deepformat(deepcopy(parser['result']), vals)
                    result = dict_merge(result, res)
        return result

    def render(self, data, parser_names, negate=False):
        if not isinstance(parser_names, list):
            parser_names = [parser_names]
        commands = []
        for pname in parser_names:
            try:
                setval = self.PARSERS[pname]['setval']
                if callable(setval):
                    res = setval(data)
                else:
                    res = setval.format(**data)
                if negate:
                    res = 'no ' + res
                commands.append(res)
            except KeyError:
                pass
        return commands
