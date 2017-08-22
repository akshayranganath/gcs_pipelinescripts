import csv
import os

def getTestCases(fileName, header=True):
    testCases = []
    if os.path.isfile(fileName):
        with open(fileName,'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if header == True:
                    header = False
                else:
                    #read everything after the header
                    (url, response_code, ttl, message) = row
                    testCases.append((url, response_code, ttl, message))

    return testCases


if __name__=="__main__":
    openFile('scenario.csv')