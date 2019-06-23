"""
snmp demo
"""
from parsers.snmp import Snmp
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
    snmp = Snmp(lines=LINES.splitlines())
    result = snmp.parse()
    result['communities'] = result['communities'].values()
    result['communities'] = sorted(result['communities'],
                                   key=lambda k: k['community'])
    result['users'] = result['users'].values()
    result['users'] = sorted(result['users'], key=lambda k: k['username'])

    config = []
    for pname in [
            'aaa_user_cache_timeout', 'contact', 'engine_id_local', 'enable',
            'global_enforce_priv', 'location', 'packet_size',
            'source_interface_informs', 'source_interface_traps'
    ]:
        config.append(snmp.render(result, pname))

    for community in result['communities']:
        for pname in ['communities', 'communities_acl']:
            res = snmp.render(community, pname)
            if res:
                config.append(res)
        for pname in [
                'communities_ipv4acl_ipv6acl', 'communities_ipv4acl',
                'communities_ipv6acl'
        ]:
            res = snmp.render(community, pname)
            if res:
                config.append(res)
                break

    for user in result['users']:
        config.append(snmp.render(user, 'users'))
        if user.get('enforce_priv'):
            config.append(snmp.render(user, 'users_enforce_priv'))
        for pname in [
                'users_ipv4acl_ipv6acl', 'users_ipv4acl', 'users_ipv6acl'
        ]:
            res = snmp.render(user, pname)
            if res:
                config.append(res)
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
