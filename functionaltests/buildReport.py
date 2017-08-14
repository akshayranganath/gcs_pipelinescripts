# -*- coding: utf-8 -*-
import csv
from testWrapper import TestWrapper
from parsePapiRules import FunctionalTests
import argparse


if __name__ == "__main__":
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

    for hostname in ft.getHostNames():
        #print (hostnamewrapper.getIPAddress(hostname))
        print(hostname + ', ' + str( wrapper.getIPAddress(hostname) ))



