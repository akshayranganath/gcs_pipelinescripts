# -*- coding: utf-8 -*-
import csv
from testWrapper import TestWrapper
from parsePapiRules import FunctionalTests
import argparse
import logging

logger = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printHeader(header):
    print ()
    print (bcolors.BOLD  + header)
    print("-------------------------------------------------------------------------------------------" + bcolors.ENDC)

def printLine(name, value):
    if value != None and value!=False:
        print (name + ', ' + bcolors.OKGREEN + str(value) + bcolors.ENDC)
    else:
        print(name + ', ' + bcolors.FAIL + str(value) + bcolors.ENDC)


if __name__ == "__main__":

    # get a logger
    FORMAT = '%(asctime)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('FunctionalTester')

    # fetch the list of arguments. we need at least 2
    parser = argparse.ArgumentParser(description="Simple functional testing tool using requests library")
    parser.add_argument('--rules', help="PAPI rules file that will be parsed and tested", required=True)
    parser.add_argument('--hosts', help="Host details file that will be used to extract host name and edge host names",
                        required=True)
    parser.add_argument('--secure', help="Run all the tests as https instead of http", action="store_true")

    args = parser.parse_args()

    ft = FunctionalTests(args.rules,args.hosts,args.secure)

    # now check if the host names exist
    wrapper = TestWrapper()

    printHeader("Host Resolution Report")
    for hostname in ft.getHostNames():
        printLine(hostname, wrapper.getIPAddress(hostname) )

    printHeader("Origin Resolution Report")
    for origin in ft.getOriginDetals():
        printLine(origin['host'], wrapper.getIPAddress(origin['host']))

    printHeader("Edge Host Names Report for host names")
    for edgeHostName in ft.getEdgeHostNames():
        printLine(edgeHostName ,wrapper.getIPAddress(edgeHostName))

    printHeader("Host Accessibility Report - No Spoofing")
    for hostname in ft.getHostNames():
        printLine(hostname, wrapper.hostExists(hostname) )

    printHeader("Host Accessibility with Spoofing")
    for hostname in ft.getHostNames():
        printLine(hostname, wrapper.hostExists(hostname, hostname, 'a1.b.akamai-staging.net' ) )

    printHeader("Origin Accessibility Report")
    for origin in ft.getOriginDetals():
        printLine(origin['host'], wrapper.hostExists(origin['host'], origin['hostHeader']))