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
import mpulse_helper

#setup logging
logger = logging.getLogger("mpulse_wrapper.py")
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def getSummary(token, api_key, timer, arguments):
	base_url = "https://mpulse.soasta.com/concerto/mpulse/api/v2/"
	function = "/summary"
	query_arguments = {"format": "json", "timer": timer}
	
	query_arguments = mpulse_helper.get_query_date(arguments, query_arguments)
	
	headers = {"Authentication": token["token"]}
	api_endpoint = base_url + api_key + function + "?" + "&".join(mpulse_helper.build_query_string(query_arguments))
	logging.debug("API URL: " + api_endpoint)
	response = {}

	try:
		response = requests.get(api_endpoint, headers = headers)
		if response.status_code == 200:
			logger.info(json.dumps(response.json(),indent=2))	
			response = response.json()		
	except Exception as e:
		logging.error(str(e))
	
	return response

def getHistogram(token, api_key, timer, arguments):
	base_url = "https://mpulse.soasta.com/concerto/mpulse/api/v2/"
	function = "/histogram"
	query_arguments = {"format": "json", "timer": timer}

	query_arguments = mpulse_helper.get_query_date(arguments, query_arguments)
	headers = {"Authentication": token["token"]}
	api_endpoint = base_url + api_key + function + "?" + "&".join(mpulse_helper.build_query_string(query_arguments))
	
	logging.debug("API URL: " + api_endpoint)
	response = {}

	try:
		response = requests.get(api_endpoint, headers = headers)
		if response.status_code == 200:
			logger.info(json.dumps(response.json(),indent=2))	
			response = response.json()		
	except Exception as e:
		logging.error(str(e))
	
	return response	

def getApiResponse(token, args):
	base_url = "https://mpulse.soasta.com/concerto/mpulse/api/v2/"

	arguments = {}
	if 'args' in args and args.args != None or args.args!="":		
		for each_argument in args.args:
			params = each_argument.strip().split("=")
			if len(params) == 2:
				arguments[params[0]] = params[1]
	if 'type' not in arguments:
		arguments['type'] = "summary"

	function = '/' + arguments['type']
	
	query_arguments = mpulse_helper.get_query_date(arguments)
	query_arguments['format'] = 'json'
	#now remove the 'type' dictionary entry
	mpulse_helper.cleanup_arguments(arguments)	
	query_arguments.update(arguments)
	logger.debug("Arguments currently in list: " + str(query_arguments))
	headers = {"Authentication": token["token"]}
	api_endpoint = base_url + args.api_key + function + "?" + "&".join(mpulse_helper.build_query_string(query_arguments))
	
	logging.debug("API URL: " + api_endpoint)
	response = {}

	try:
		response = requests.get(api_endpoint, headers = headers)
		if response.status_code == 200:
			logger.info(json.dumps(response.json(),indent=2))	
			response = response.json()		
	except Exception as e:
		logging.error(str(e))
	
	return response		


if __name__=="__main__":    

    parser = argparse.ArgumentParser(description='CLI for mPulse Query API. For more information about the API, please refer to https://developer.akamai.com/api/web_performance/mpulse_query/v2.html' )
    parser.add_argument('--config', help='mPulse configuration file containing the user\'s API key (deault=~/.mpulse)',default="~/.mpulse")
    parser.add_argument('--section', help='Section within the config file containing the credentials (default=[mpulse])',default='mpulse')
    parser.add_argument('--api_key', help='API key of the app',required=True) 
    parser.add_argument('--timer', help='The timer to report (default=page load time)', default='PageLoad')
    #gather up reminder
    parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    logger.debug('Configuration file: ' + args.config)
    logger.debug('Configuration section: ' + args.section)
    logger.debug(args)
    settings = config.getCredentials(args.config,args.section)
    token = config.generateToken(settings['apitoken'], settings['tenant'])
    logger.debug(token)
    getApiResponse(token, args)
    #getSummary(token, args.api_key, args.timer)
