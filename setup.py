#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='vpnkeymgr',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    requires=['docopt'],
    packages=['vpnkeymgr'],
    scripts=['files/vpnkeymgr'],
    description=('OpenVPN key manager for easyrsa3.'))
