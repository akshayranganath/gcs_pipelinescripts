from csvhelper import getTestCases
import sys
import argparse
import logging


sys.path.append('unittest');sys.path.append('../unittest');
from unittest_runCheck import RunCheck

messsages = []
def runtests(testCaseFile, baseDomain):
    success = True
    testCases = getTestCases(testCaseFile)
    for testCase in testCases:
        try:
            runCheck = RunCheck()
            runCheck.setUp()
            runCheck.test_check_resonse(testCase, baseDomain)
            print ('.', end="")
        except AssertionError as e:
            print ('F', end="")
            #messages = global.messsages
            messsages.append(str(e))
            success = False
        finally:
            sys.stdout.flush()
    return success


if __name__ == "__main__":

    # get a logger
    FORMAT = '%(asctime)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('FunctionalTester')

    # fetch the list of arguments. we need at least 2
    description = "Functionation testing using data driven framework\n"
    description += "-------------------------------------------------\n"
    description += "Using this function, you can run any number of tests defined in your functional testing document. Specify all your requirements in a csv file of the following format: \n"
    description += "Relative URL, Expected Response Code (optional),Expected TTL (optional), Error message to be printed\n"
    description += "Of this, either the expected response code or the expected TTL has to be present. By passing the domain name, we can then run a check against the domain.\n"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--tests', help="CSV file containing test cases", required=True)
    parser.add_argument('--domain', help="Base domain to run the tests", required=True)
    args = parser.parse_args()
    success = runtests(args.tests, args.domain)

    if success == False:
        print ()
        print ('Tests failed')
        for message in messsages:
            print(message)
        sys.exit(1)



