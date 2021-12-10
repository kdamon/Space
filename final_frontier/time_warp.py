from datetime import date, datetime, timedelta
import calendar



def get_query_dates(start_date, end_date, max_query_days):
	## Calculate the full date range
	delta = end_date - start_date

	## Get a list of all of the dates in the full date range
	days = []
	for d in range(delta.days + 1):
		days.append(str(start_date + timedelta(days=d)))

	## Split dates into groups of the max amount of query days
	query_dates = [days[i:i+max_query_days] for i in range(0, len(days), max_query_days)]

	## Remove middle dates from the groups since we only need start and end dates
	for query_group in query_dates:
		del query_group[1:-1]
					
	return query_dates



def calculate_query_dates(time_period, max_query_days):
	## Get the days for the user supplied month and year
	if '-' in time_period:
		year_month = time_period.split('-')
		year = int(year_month[0])
		month = int(year_month[1])
		num_days = calendar.monthrange(year, month)[-1]
		start_date = date(year, month, 1)
		end_date = date(year, month, num_days)
		query_dates = get_query_dates(start_date, end_date, max_query_days)

	else:
		## Get today's date, 15 and 30 day deltas
		today = date.today()
		thirty_days = timedelta(days=30)
		fifteen_days = timedelta(days=15)

		## Go into the past 30 days
		if time_period == 'past':
			start_date = today - thirty_days
			end_date = today
			query_dates = get_query_dates(start_date, end_date, max_query_days)

		## Go into the past 15 days and into the future 15 days to get the 30 days surrounding today's date
		elif time_period == 'present':
			start_date = today - fifteen_days
			end_date = today + fifteen_days
			query_dates = get_query_dates(start_date, end_date, max_query_days)

		## Go into the future 30 days
		elif time_period == 'future':
			start_date = today
			end_date = today + thirty_days
			query_dates = get_query_dates(start_date, end_date, max_query_days)

		## If no time period, or it somehow fails to get passes in, use the current month and year
		else:
			year = int(today.year)
			month = int(today.month)
			num_days = calendar.monthrange(year, month)[-1]
			start_date = date(year, month, 1)
			end_date = date(year, month, num_days)
			query_dates = get_query_dates(start_date, end_date, max_query_days)

	return query_dates