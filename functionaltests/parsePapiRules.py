# -*- coding: utf-8 -*-
import json
import argparse
import subprocess

class FunctionalTests():

    def __init__(self, rulesFile, hostsFile, secure=False):
        """
        A slightly longer init function, this code will parse the PM property file,
        the hosts file and then extract the following:
        1. Host names
        2. Edge hostnames associated with the host name
        3. Sureroute object names
        """
        self.filename = rulesFile
        self.hostsfile = hostsFile
        self.edgehostnames = []
        self.hostnames = []
        self.origins = []
        self.srobject = None
        self.srForceSSL = None
        self.secure = secure
        with open(rulesFile, 'r') as pmFile:
            self.rules = json.loads(pmFile.read())
        if hostsFile != None:
            with open(hostsFile, 'r') as hostsDetails:
                self.hostinfo = json.loads(hostsDetails.read())
        else:
            self.hostinfo = self.fetchHostDetails(self.rules['propertyId'], self.rules['propertyVersion'],\
                                                  self.rules['contractId'],self.rules['groupId'])
        self.setHostNames()
        self.setSRObject()
        self.setOrigins()

    def fetchHostDetails(self, propertyId, propertyVersion,contractId,groupId):
        endPoint = ":/papi/v1/properties/" + propertyId + "/versions/" + str(propertyVersion) + \
            "/hostnames/?contractId=" + contractId + "&groupId=" + groupId
        result = json.loads(subprocess.check_output(['http','--auth','edgegrid','-a','papi:','-b',endPoint]).decode('utf-8'))
        #print (json.dumps(result,indent=2))
        return result



    def setHostNames(self):
        """A simple function to extract the host name and edge host name information"""
        for entry in self.hostinfo['hostnames']['items']:
            self.hostnames.append( entry['cnameFrom'] )
            self.edgehostnames.append( entry['cnameTo'] )

    def setSRObject(self):
        """A shell function that will invoke a recursive call to find the sureroute object path"""
        self.findSRObject(self.rules['rules'])

    def setOrigins(self):
        self.findOrigins(self.rules['rules'])

    # A recursive function to find the sr object behavior
    def findSRObject(self, rules):
        if 'children' in rules:
            for child in rules['children']:
                self.findSRObject(child)

        if 'behaviors' in rules:
            for behavior in rules['behaviors']:
                if 'children' in behavior:
                    self.findSRObject(behavior)

                if behavior['name'] == 'sureRoute':
                    self.srobject =  behavior['options']['testObjectUrl']
                    self.srForceSSL = behavior['options']['forceSslForward']

                    # A recursive function to find the sr object behavior

    def findOrigins(self, rules):
        if 'children' in rules:
            for child in rules['children']:
                self.findSRObject(child)

        if 'behaviors' in rules:
            for behavior in rules['behaviors']:
                if 'children' in behavior:
                    self.findSRObject(behavior)

                if behavior['name'] == 'origin':
                   origin_object = {
                        'host': behavior['options']['hostname'],
                        'hostHeader': behavior['options']['customForwardHostHeader'] if 'customForwardHostHeader' in behavior['options']  else  None
                   }
                   self.origins.append(origin_object)


    def getEdgeHostNames(self):
        return self.edgehostnames


    def getHostNames(self):
        return self.hostnames


    def getSrObject(self):
        return self.srobject


    def getOriginDetals(self):
        return self.origins

if __name__ == "__main__":
    # fetch the list of arguments. we need at least 2
    parser = argparse.ArgumentParser(description="Simple functional testing tool using requests library")
    parser.add_argument('--rules', help="PAPI rules file that will be parsed and tested", required=True)
    parser.add_argument('--hosts', help="Host details file that will be used to extract host name and edge host names",
                        required=True)
    parser.add_argument('--secure', help="Run all the tests as https instead of http", action="store_true")

    args = parser.parse_args()

    ft = FunctionalTests(args.rules,args.hosts,args.secure)
