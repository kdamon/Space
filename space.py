import sys
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
# a.asteroid_closest_approach()

# Call the closest approaches for the given month
# a.month_closest_approaches(query_dates)

# call the nearest misses function
# a.nearest_misses()