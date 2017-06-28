#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='vpnkeymgr',
    requires=['docopt'],
    packages=['vpnkeymgr'],
    data_files=[('/usr/bin', ['files/vpnkeymgr'])],
    description=('HOMEINFO OpenVPN key manager'))
