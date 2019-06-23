from templator import Templator
import re


def tmplt_user(user):
    command = []
    command.append('snmp-server user')
    command.append(user['username'])
    command.append('auth')
    command.append(user['algorithm'])
    command.append(user['password'])
    if user.get('privacy_password', False):
        command.append('priv')
        if user.get('aes_128', False):
            command.append('aes-128')
        command.append(user['privacy_password'])
    if user.get('localized_key', False):
        command.append('localizedKey')
    if user.get('engine_id', False):
        command.append('engineID')
        command.append(user['engine_id'])
    return " ".join(command)


class Snmp(Templator):

    PARSERS = {
        'aaa_user_cache_timeout': {
            'getval': r'^snmp-server aaa-user cache-timeout (?P<cache_val>\S+)$',
            'setval':
            'snmp-server aaa-user cache-timeout {aaa_user[cache_timeout]}',
            'result': {
                'aaa_user': {
                    'cache_timeout': '{cache_val}'
                }
            },
            'cast': {
                'cache_val': 'to_int'
            }
        },
        'communities': {
            'getval':
            r'^snmp-server community (?P<community>\S+) group (?P<group>\S+)$',
            'setval': 'snmp server community {community} group {group}',
            'result': {
                'communities': {
                    '{community}': {
                        'community': '{community}',
                        'group': '{group}'
                    }
                }
            }
        },
        'communities_acl': {
            'getval':
            r'^snmp-server community (?P<community>\S+) use-acl (?P<acl>\S+)$',
            'setval': 'snmp server community {community} use-acl {acl}',
            'result': {
                'communities': {
                    '{community}': {
                        'community': '{community}',
                        'acl': '{acl}'
                    }
                }
            }
        },
        'communities_ipv4acl': {
            'getval':
            r'^snmp-server community (?P<community>\S+) use-ipv4acl (?P<ipv4acl>\S+)$',
            'setval': 'snmp server community {community} use-ipv4acl {ipv4acl}',
            'result': {
                'communities': {
                    '{community}': {
                        'community': '{community}',
                        'ipv4acl': '{ipv4acl}'
                    }
                }
            }
        },
        'communities_ipv6acl': {
            'getval':
            r'^snmp-server community (?P<community>\S+) use-ipv6acl (?P<ipv6acl>\S+)$',
            'setval': 'snmp server community {community} use-ipv6acl {ipv6acl}',
            'result': {
                'communities': {
                    '{community}': {
                        'community': '{community}',
                        'ipv6acl': '{ipv6acl}'
                    }
                }
            }
        },
        'communities_ipv4acl_ipv6acl': {
            'getval':
            re.compile(
                r'''
              ^snmp-server\scommunity
              \s(?P<community>\S+)
              \suse-ipv4acl
              \s(?P<ipv4acl>\S+)
              \suse-ipv6acl
              \s(?P<ipv6acl>\S+)$''', re.VERBOSE),
            'setval':
            'snmp server community {community} use-ipv4acl {ipv4acl} use-ipv6acl {ipv6acl}$',
            'result': {
                'communities': {
                    '{community}': {
                        'community': '{community}',
                        'ipv4acl': '{ipv4acl}',
                        'ipv6acl': '{ipv6acl}'
                    }
                }
            }
        },
        'contact': {
            'getval': '^snmp-server contact (?P<contact>.*)$',
            'setval': 'snmp-server contact {contact}',
            'result': {
                'contact': '{contact}'
            }
        },
        'engine_id_local': {
            'getval': '^snmp-server engineID local (?P<engine_id>\\S+)$',
            'setval': 'snmp-server engineID local {engine_id[local]}',
            'result': {
                'engine_id': {
                    'local': '{engine_id}'
                }
            }
        },
        'enable': {
            'getval': '^((?P<no>no)\s)?snmp-server protocol enable$',
            'setval': 'snmp-server protocol enable',
            'result': {
                'enable': '{no}'
            },
            'cast': {
                'no': 'default_not_no'
            }
        },
        'global_enforce_priv': {
            'getval': r'^((?P<no>no)\s)?snmp-server globalEnforcePriv$',
            'setval': 'snmp-server globalEnforcePriv',
            'result': {
                'global_enforce_priv': '{no}'
            },
            'cast': {
                'no': 'default_is_no'
            }
        },
        'location': {
            'getval': '^snmp-server location (?P<location>.*)$',
            'setval': 'snmp-server location {location}',
            'result': {
                'location': '{location}'
            }
        },
        'packet_size': {
            'getval': '^snmp-server packetsize (?P<packetsize>.*)$',
            'setval': 'snmp-server packetsize {packetsize}',
            'result': {
                'packetsize': '{packetsize}'
            },
            'cast': {
                'packetsize': 'to_int'
            }
        },
        'source_interface_informs': {
            'getval': '^snmp-server source-interface informs (?P<int>\\S+)$',
            'setval':
            'snmp-server source-interface informs {source_interface[informs]}',
            'result': {
                'source_interface': {
                    'informs': '{int}'
                }
            }
        },
        'source_interface_traps': {
            'getval': '^snmp-server source-interface traps (?P<int>\\S+)$',
            'setval':
            'snmp-server source-interface traps {source_interface[traps]}',
            'result': {
                'source_interface': {
                    'traps': '{int}'
                }
            },
        },
        'users': {
            'getval':
            re.compile(
                r'''
              ^snmp-server\suser\s
              (?P<username>\S+)
              (\s(?P<group>\S+))?
              \sauth
              \s(?P<algorithm>(md5|sha))
              \s(?P<password>\S+)
              (\spriv(\s(?P<aes_128>aes-128))?\s(?P<privacy_password>\S+))?
              (\s(?P<localized_key>localizedkey))?
              (\sengineID\s(?P<engine_id>\S+))?$''', re.VERBOSE),
            'setval': tmplt_user,
            'result': {
                'users': {
                    '{username}': {
                        'aes_128': '{aes_128}',
                        'algorithm': '{algorithm}',
                        'engine_id': '{engine_id}',
                        'group': '{group}',
                        'localized_key': '{localized_key}',
                        'password': '{password}',
                        'privacy_password': '{privacy_password}',
                        'username': '{username}'
                    }
                }
            },
            'cast': {
                'aes_128': 'to_bool',
                'localized_key': 'to_bool'
            },
        },
        'users_enforce_priv': {
            'getval':
            re.compile(
                r'''
              ^snmp-server\suser\s
              (?P<username>\S+)
              \s(?P<enforce_priv>enforcePriv)$''', re.VERBOSE),
            'setval':
            'snmp server user {username} enforcePriv',
            'result': {
                'users': {
                    '{username}': {
                        'username': '{username}',
                        'enforce_priv': '{enforce_priv}'
                    }
                }
            },
            'cast': {
                'enforce_priv': 'to_bool'
            }
        },
        'users_ipv4acl': {
            'getval':
            re.compile(
                r'''
              ^snmp-server\suser\s
              (?P<username>\S+)
              \suse-ipv4acl
              \s(?P<ipv4acl>\S+)$''', re.VERBOSE),
            'setval':
            'snmp server user {username} use-ipv4acl {ipv4acl}',
            'result': {
                'users': {
                    '{username}': {
                        'username': '{username}',
                        'ipv4acl': '{ipv4acl}'
                    }
                }
            }
        },
        'users_ipv6acl': {
            'getval':
            re.compile(
                r'''
                  ^snmp-server\suser\s
                  (?P<username>\S+)
                  \suse-ipv6acl
                  \s(?P<ipv6acl>\S+)$''', re.VERBOSE),
            'setval':
            'snmp server user {username} use-ipv6acl {ipv6acl}',
            'result': {
                'users': {
                    '{username}': {
                        'username': '{username}',
                        'ipv6acl': '{ipv6acl}'
                    }
                }
            }
        },
        'users_ipv4acl_ipv6acl': {
            'getval':
            re.compile(
                r'''
              ^snmp-server\suser\s
              (?P<username>\S+)
              \suse-ipv4acl
              \s(?P<ipv4acl>\S+)
              \suse-ipv6acl
              \s(?P<ipv6acl>\S+)$''', re.VERBOSE),
            'setval':
            'snmp server user {username} use-ipv4acl {ipv4acl} use-ipv6acl {ipv6acl}',
            'result': {
                'users': {
                    '{username}': {
                        'username': '{username}',
                        'ipv4acl': '{ipv4acl}',
                        'ipv6acl': '{ipv6acl}'
                    }
                }
            }
        },
    }
