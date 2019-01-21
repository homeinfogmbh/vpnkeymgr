"""Configuration file parser."""

from configparser import ConfigParser


__all__ = ['CONFIG']


CONFIG = ConfigParser()
CONFIG.read('/etc/vpnkeymgr.conf')
