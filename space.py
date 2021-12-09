import os, sys, json
from final_frontier import asteroids, time_warp

# print(dir(asteroids.asteroids))
# print(dir(time_warp))
print()

# Define arguments
# Usage: python space.py [past|present|future|year-month]
valid_time_periods = ['past', 'present', 'future']
valid_years = range(1800, 2101)
valid_months = range(1, 13)
today = time_warp.date.today()

# Make a 'captains_log' folder for our cassetts if one doesn't exist
if not os.path.exists('final_frontier/captains_log'):
	os.mkdir('final_frontier/captains_log')

# Make a 'json_data' folder to store the json data if one doesn't exist
if not os.path.exists('final_frontier/json_data'):
	os.mkdir('final_frontier/json_data')

try:
	time_period = sys.argv[1]
	# print(time_period)
	if time_period.lower() in valid_time_periods:
		time_period = time_period.lower()
	else:
		if '-' in time_period:
			year_month = time_period.split('-')
			year = int(year_month[0])
			month = int(year_month[1])
			if not year in valid_years:
				print("Invalid year")
				year = today.year
			year = str(year)
			if not month in valid_months:
				print("Invalid month")
				month = today.month
			month = str(month)
			if len(month) == 1:
				month = '0' + month
			time_period = year + '-' + month
		else:
			print("Invalid time period")
			time_period = str(today.year) + '-' + str(today.month)
except:
	time_period = str(today.year) + '-' + str(today.month)

# Calculate the date ranges to query
query_dates = time_warp.calculate_query_dates(time_period)
print(query_dates)

# Abbreviate the asteroids class
a = asteroids.asteroids()

# Call the closest approach function
asteroid_data = a.asteroid_closest_approach()

closest_approach_file = open('final_frontier/json_data/asteroid_closest_approach.json', 'w')
closest_approach_file.write(json.dumps(asteroid_data))
closest_approach_file.close()

# Call the closest approaches for the given month
# month_closest_approaches_data = a.month_closest_approaches(query_dates)

# month_closest_file = open('final_frontier/json_data/month_closest_approaches.json', 'w')
# month_closest_file.write(json.dumps(month_closest_approaches_data))
# month_closest_file.close()

# call the nearest misses function
# nearest_misses_data = a.nearest_misses()

# nearest_misses_file = open('final_frontier/json_data/nearest_misses.json', 'w')
# nearest_misses_file.write(json.dumps(nearest_misses_data))
# nearest_misses_file.close()