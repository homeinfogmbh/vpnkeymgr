#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='vpnkeymgr',
    requires=['docopt'],
    packages=['vpnkeymgr'],
    data_files=[('/etc', ['files/etc/termgr.conf']),
                ('/usr/bin', ['files/usr/bin/vpnkeymgr']),
                ('/usr/share/terminals',
                 ['files/usr/share/terminals/openvpn.conf.temp'])
                ],
    license=open('LICENSE.txt').read(),
    description=('HOMEINFO OpenVPN key manager')
    )
