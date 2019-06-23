```
############################################################ original config

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

############################################################ structed data
[
    {
        "name": "Ethernet1/128",
        "description": "foo",
        "switchport": false,
        "ip": {
            "redirects": false
        },
        "ipv4": [
            {
                "address": "192.168.1.1/24",
                "route_preference": 2,
                "tag": "5"
            },
            {
                "address": "10.1.1.1/24",
                "secondary": true
            }
        ]
    },
    {
        "name": "mgmt0",
        "description": "mgmt",
        "vrf": "management",
        "ipv4": [
            {
                "address": "192.168.101.14/24"
            }
        ]
    }
]

############################################################ recreated config

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

############################################################ recreated == original
True
```
