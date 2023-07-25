#! /usr/bin/env python3

from setuptools import setup

setup(
    name="vpnkeymgr",
    use_scm_version={"local_scheme": "node-and-timestamp"},
    setup_requires=["setuptools_scm"],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info@homeinfo.de>",
    maintainer="Richard Neumann",
    maintainer_email="<r.neumann@homeinfo.de>",
    packages=["vpnkeymgr"],
    entry_points={"console_scripts": ["vpnkeymgr = vpnkeymgr.cli:main"]},
    description="OpenVPN key manager for easyrsa3.",
)
