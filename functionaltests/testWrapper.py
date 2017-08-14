# -*- coding: utf-8 -*-

import socket
import requests

class TestWrapper:
    def getIPAddress(self, domain):
        result = None
        try:
            result =  socket.gethostbyname(domain)
        except socket.gaierror:
            pass

        return result


    def hostExists(self,host,hostHeader=None):
        result = False
        try:
            if hostHeader==None:
                hostHeader = host
            response = requests.get('http://'+host+'/',{'Host':hostHeader})
            result = True
        except Exception as e:
            pass
        return result

if __name__=="__main__":
    t = TestWrapper()
    print (t.hostExists('a'))