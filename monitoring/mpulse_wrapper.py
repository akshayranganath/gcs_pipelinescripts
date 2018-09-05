import sys
import config
if sys.version_info[0] >= 3:
     # python3
     from configparser import ConfigParser
     import http.client as http_client
else:
     # python2.7
     from ConfigParser import ConfigParser
     import httplib as http_client

import argparse
import logging
import requests
import json

#setup logging
logger = logging.getLogger("mpulse_wrapper.py")
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def build_query_string(query_arguments):
	query_string_list = []
	for each_key in query_arguments:
		query_string_list.append(each_key+'='+query_arguments[each_key])
	return query_string_list

def getSummary(token, api_key, timer, timelines={}):
	base_url = "https://mpulse.soasta.com/concerto/mpulse/api/v2/"
	function = "/summary"
	query_arguments = {"format": "json", "timer": timer}
	if timelines=={}:
		#set default as last hour
		query_arguments["date-comparator"] = "LastHour"
	else:
		if "date-comparator" in timelines:
			query_arguments["date-comparator"] = timelines["date-comparator"]
		if "date" in timelines:
			query_arguments["date"] = timelines["date"]
	
	headers = {"Authentication": token["token"]}
	api_endpoint = base_url + api_key + function + "?" + "&".join(build_query_string(query_arguments))
	logging.debug("API URL: " + api_endpoint)
	try:
		response = requests.get(api_endpoint, headers = headers)
		if response.status_code == 200:
			logger.info(json.dumps(response.json(),indent=2))
	except Exception as e:
		logging.error(str(e))



if __name__=="__main__":    

    parser = argparse.ArgumentParser(description='mPulse entry point.' )
    parser.add_argument('--config', help='mPulse configuration file containing the user\'s API key (deault=~/.mpulse)',default="~/.mpulse")
    parser.add_argument('--section', help='Section within the config file containing the credentials (default=[mpulse])',default='mpulse')
    parser.add_argument('--api_key', help='API key of the app',required=True) 
    parser.add_argument('--timer', help='The timer to report (default=page load time)', default='PageLoad')

    args = parser.parse_args()
    logger.debug('Configuration file: ' + args.config)
    logger.debug('Configuration section: ' + args.section)
    settings = config.getCredentials(args.config,args.section)
    token = config.generateToken(settings['apitoken'], settings['tenant'])
    logger.debug(token)
    getSummary(token, args.api_key, args.timer)
