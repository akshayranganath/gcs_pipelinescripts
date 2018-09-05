def build_query_string(query_arguments):
	query_string_list = []
	for each_key in query_arguments:
		query_string_list.append(each_key+'='+query_arguments[each_key])
	return query_string_list

def get_query_date(arguments, query_arguments):
	if 'date-comparator' not in arguments and 'date' not in arguments:
		#nothing specific is given. simply use LastHour
		query_arguments["date-comparator"] = "LastHour"
	else:
		#only date is provided
		if 'date' in arguments:
			query_arguments["date"] = arguments["date"]
		else:
			if 'date-compartor' in arguments['date-comparator']:
				query_arguments['date-comparator'] = arguments['date-comparator']
	return query_arguments