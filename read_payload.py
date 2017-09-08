import sys
import json
import logging

FORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)
#logging.basicConfig()
logger = logging.getLogger('filecleaner')
logger.setLevel(logging.DEBUG)

merge_request = False
raw_data = sys.stdin.read()
payload = json.loads(raw_data)
logger.info('Loaded the payload data successfully')
if 'action' in payload and payload['action']=='closed':
	logger.debug('Found a close action')
	if 'pull_request' in payload and 'merged_at' in payload['pull_request']:
		logger.debug('Found a merged_at within a pull_request')
		merge_request = True
if merge_request == True:	
	logger.info('Found a successful merge request.')
else:
	logger.info('Merge request was not found.')
assert merge_request