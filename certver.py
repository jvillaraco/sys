#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
certver.py v170314
Test certificate end
IN: URL: for certificate to test,
    time: time (in days) to check for cert end
OUT: Number of days untill cets ends
Distributed under Apache 2.0 License
(http://www.apache.org/licenses/LICENSE-2.0.txt)
"""


import ssl
import sys
from datetime import datetime
from OpenSSL import crypto


def main(debug=False):
    cert = crypto.load_certificate(crypto.FILETYPE_PEM,
                                   ssl.get_server_certificate((sys.argv[1],
                                                              443)))
    sCertEnds = cert.get_notAfter()
    dtCertEnds = datetime.strptime(sCertEnds, '%Y%m%d%H%M%SZ')
    if debug:
        print(dtCertEnds)
        print(cert)
        print("Ends: %s" % dtCertEnds)
    now = datetime.now()
    rest = dtCertEnds - now
    if debug:
        # print(datetime_object)
        print(now)
        print("Days before cert ends: %s" % rest)
    print(rest.days)


if __name__ == '__main__':
    main()
