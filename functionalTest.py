import requests
import json
import argparse


class FunctionalTests():
    def __init__(self, rulesFile, hostsFile, secure=False):
        self.filename = rulesFile
        self.hostsfile = hostsFile
        self.edgehostnames = []
        self.hostnames = []
        self.srobject = None
        self.secure = secure
        with open(rulesFile, 'rb') as pmFile:
            self.rules = json.loads(pmFile.read())
        with open(hostsFile, 'rb') as hostsDetails:
            self.hostinfo = json.loads(hostsDetails.read())
        self.setHostNames()
        self.setSRObject()

    def setHostNames(self):
        for entry in self.hostinfo['hostnames']['items']:
            self.hostnames.append( entry['cnameFrom'] )
            self.edgehostnames.append( entry['cnameTo'] )

    def setSRObject(self):
        self.findSRObject(self.rules['rules'])


    def getEdgeHostNames(self):
        return self.edgehostnames

    def getHostNames(self):
        return self.hostnames

    def getSrObject(self):
        pass

    def parseRules(self):
        pass

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


if __name__ == "__main__":
    # fetch the list of arguments. we need at least 2
    parser = argparse.ArgumentParser(description="Simple functional testing tool using requests library")
    parser.add_argument('--rules', help="PAPI rules file that will be parsed and tested", required=True)
    parser.add_argument('--hosts', help="Host details file that will be used to extract host name and edge host names",
                        required=True)
    parser.add_argument('--secure', help="Run all the tests as https instead of http", action="store_true")

    args = parser.parse_args()

    ft = FunctionalTests(args.rules,args.hosts,args.secure)
