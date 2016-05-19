#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='vpnkeymgr',
    requires=['docopt'],
    packages=['vpnkeymgr'],
    data_files=[
        ('/usr/bin', [
            'files/usr/bin/vpnkeymgr']),
        ('/usr/share/terminals', [
            'files/usr/share/terminals/openvpn.conf.temp'])],
    description=('HOMEINFO OpenVPN key manager'))
