from templator import Templator
import re

def tmplt_ipv4(address):
    command = []
    command.append('ip address')
    command.append(address['address'])
    if address.get('route_preference'):
        command.append('route-preference')
        command.append(str(address['route_preference']))
    if address.get('tag'):
        command.append('tag')
        command.append(address['tag'])
    if address.get('secondary') and address['secondary']:
        command.append('secondary')
    return " ".join(command)


class Interfaces(Templator):

    PARSERS = {
        'interface': {
            'getval': r'^interface (?P<name>\S+)$',
            'setval': 'interface {name}',
            'result': {
                '{name}': {
                    'name': '{name}'
                }
            },
            'shared': True
        },
        'description': {
            'getval': r'\s+description (?P<description>\S+)$',
            'setval': 'description {description}',
            'result': {
                '{name}': {
                    'description': '{description}'
                }
            }
        },
        'ip_address': {
            'getval': re.compile(r'''
                 ^\s+ip\saddress\s(?P<address>(\d{1,3}.){3}\d{1,3}/\d{1,2})
                 (\s(?P<secondary>secondary))?
                 (\sroute-preference\s(?P<route_preference>\S+))?
                 (\stag\s(?P<tag>\S+))?$''', re.VERBOSE),
            'setval': tmplt_ipv4,
            'result': {
                '{name}': {
                    'ipv4': {
                        '{address}': {
                            'address': '{address}',
                            'route_preference': '{route_preference}',
                            'secondary': '{secondary}',
                            'tag': '{tag}'
                        }
                    }
                }
            },
            'cast': {
                'secondary': 'to_bool',
                'route_preference': 'to_int'
            }
        },
        'ip_redirects': {
            'getval': r'\s+((?P<no>no)\s)?ip redirects$',
            'setval': 'ip redirects',
            'result': {
                '{name}': {
                    'ip': {
                        'redirects': '{no}',
                    }
                }
            },
            'cast': {
                'no': 'no_means_false'
            }
        },
        'switchport': {
            'getval': r'\s+((?P<no>no)\s)?switchport$',
            'setval': 'switchport',
            'result': {
                '{name}': {
                    'switchport': '{no}',
                }
            },
            'cast': {
                'no': 'no_means_false'
            }
        },
        'vrf': {
            'getval': r'\s+vrf\smember\s(?P<vrf>\S+)$',
            'setval': 'vrf member {vrf}',
            'result': {
                '{name}': {
                    'vrf': '{vrf}',
                }
            },
        },
    }
