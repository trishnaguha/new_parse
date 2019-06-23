"""
interface demo
"""
from parsers.interfaces import Interfaces
from templator.pretty import jsonify

LINES = '''
interface Ethernet1/128
  description foo
  no switchport
  no ip redirects
  ip address 192.168.1.1/24 route-preference 2 tag 5
  ip address 10.1.1.1/24 secondary
interface mgmt0
  description mgmt
  vrf member management
  ip address 192.168.101.14/24
'''


def run():
    """
    run
    """
    interfaces = Interfaces(lines=LINES.splitlines())
    result = interfaces.parse()
    for name, val in result.items():
        if 'ipv4' in val:
            result[name]['ipv4'] = list(val['ipv4'].values())
    result = list(result.values())

    config = []
    for interface in result:
        config.append(interfaces.render(interface, 'interface'))
        for optional in ['description', 'vrf']:
            res = interfaces.render(interface, optional)
            if res:
                config.append(res)
        if interface.get('switchport') is False:
            config.append(interfaces.render(interface, 'switchport',
                                            negate=True))
        if interface.get('ip', {}).get('redirects') is False:
            config.append(interfaces.render(interface, 'ip_redirects',
                                            negate=True))
        for ipv4 in interface.get('ipv4', []):
            config.append(interfaces.render(ipv4, 'ip_address'))

    trimmed = [line.strip() for line in LINES.splitlines() if line]
    return config, result, trimmed


def main():
    """
    do it
    """
    config, result, trimmed = run()
    print('#'*60, "original config")
    print(LINES)
    print('#'*60, "structed data")
    print(jsonify(result))
    print('#'*60, "recreated config\n")
    print('\n'.join(trimmed))
    print()
    print('#'*60, "recreated == original")
    print(config == trimmed)


if __name__ == '__main__':
    main()
