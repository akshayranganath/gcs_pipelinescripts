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


    def hostExists(self,host,hostHeader=None, proxy=None):
        result = False
        try:
            url = 'http://'
            if hostHeader==None:
                hostHeader = host

            headers = {
                'Host' : hostHeader
            }

            if proxy!=None:
                url += proxy + '/'
                headers['Host'] = host
            else:
                url += host + '/'

            response = requests.get(url,headers)
            result = True
        except Exception as e:
            pass
        return result

if __name__=="__main__":
    t = TestWrapper()
    print (t.hostExists('a'))