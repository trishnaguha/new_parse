"""
snmp demo
"""
from parsers.snmp import SnmpTemplate
from templator.pretty import jsonify

LINES = '''
snmp-server aaa-user cache-timeout 7200
snmp-server contact brad
snmp-server location some string with a space
snmp-server community communitya group network-operator
snmp-server community communityb group network-admin
snmp-server community communityc group network-admin
snmp-server community communityd group network-admin
snmp-server engineID local 00:00:00:00:01
no snmp-server enable traps entity entity_mib_change
no snmp-server enable traps entity entity_module_status_change
snmp-server enable traps aaa server-state-change
snmp-server enable traps bridge newroot
snmp-server enable traps bridge topologychange
snmp-server globalEnforcePriv
snmp-server packetsize 1376
no snmp-server protocol enable
snmp-server source-interface traps Ethernet1/1
snmp-server source-interface informs Ethernet1/1
snmp-server user m01 network-operator auth md5 password
snmp-server user m02 network-operator auth md5 password priv password
snmp-server user m03 network-operator auth md5 password priv aes-128 password
snmp-server user m04 auth md5 password engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user m05 network-operator auth md5 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey
snmp-server user m06 auth md5 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user m07 network-operator auth md5 password priv password
snmp-server user m08 network-operator auth md5 password priv aes-128 password
snmp-server user m09 network-operator auth md5 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey
snmp-server user m10 network-operator auth md5 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv aes-128 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey
snmp-server user m11 auth md5 password priv password engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user m12 auth sha password priv aes-128 password engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user m13 auth md5 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user m14 auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv aes-128 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user s01 network-operator auth sha password
snmp-server user s02 network-operator auth sha password priv password
snmp-server user s03 network-operator auth sha password priv aes-128 password
snmp-server user s04 auth sha password engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user s05 network-operator auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey
snmp-server user s06 auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user s07 network-operator auth sha password priv password
snmp-server user s08 network-operator auth sha password priv aes-128 password
snmp-server user s09 network-operator auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey
snmp-server user s10 network-operator auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv aes-128 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey
snmp-server user s11 auth sha password priv password engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user s12 auth sha password priv aes-128 password engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user s13 auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server user s14 auth sha 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 priv aes-128 0x73fd9a2cc8c53ed3dd4ed8f4ff157e69 localizedkey engineID 0:0:0:63:0:1:0:10:20:15:10:3
snmp-server community communitya use-acl 5
snmp-server community communityb use-ipv4acl 6
snmp-server community communityc use-ipv6acl 7
snmp-server community communityd use-ipv4acl 6 use-ipv6acl 7
snmp-server user s01 use-ipv4acl 10
snmp-server user s02 use-ipv6acl 15
snmp-server user s03 use-ipv4acl 10 use-ipv6acl 15
snmp-server user s08 enforcePriv
'''


def run():
    """
    run
    """
    snmp = SnmpTemplate(lines=LINES.splitlines())
    result = snmp.parse()
    result['communities'] = result['communities'].values()
    result['communities'] = sorted(result['communities'],
                                   key=lambda k: k['community'])
    result['users'] = result['users'].values()
    result['users'] = sorted(result['users'], key=lambda k: k['username'])

    config = []
    pnames = ['aaa_user.cache_timeout', 'contact', 'engine_id.local', 'enable',
              'global_enforce_priv', 'location', 'packet_size',
              'source_interface.informs', 'source_interface.traps']
    config.extend(snmp.render(result, pnames))

    for community in result['communities']:
        pnames = ['communities', 'communities.acl']
        config.extend(snmp.render(community, pnames))
        for pname in [
                'communities.ipv4acl_ipv6acl', 'communities.ipv4acl',
                'communities.ipv6acl'
        ]:
            res = snmp.render(community, pname)
            if res:
                config.extend(res)
                break

    for user in result['users']:
        config.extend(snmp.render(user, 'users'))
        if user.get('enforce_priv'):
            config.extend(snmp.render(user, 'users.enforce_priv'))
        for pname in [
                'users.ipv4acl_ipv6acl', 'users.ipv4acl', 'users.ipv6acl'
        ]:
            res = snmp.render(user, pname)
            if res:
                config.extend(res)
                break

    trimmed = [line.strip() for line in LINES.splitlines() if line]
    return config, result, trimmed


def main():
    """
    main
    """
    config, result, trimmed = run()
    print('#' * 60, "original config")
    print(LINES)
    print('#' * 60, "structed data")
    print(jsonify(result))
    print('#' * 60, "recreated config\n")
    print('\n'.join(trimmed))
    print()
    print('#' * 60, "recreated == original")
    print(config.sort() == trimmed.sort())


if __name__ == '__main__':
    main()
