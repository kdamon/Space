import os, sys, json
from final_frontier import asteroids, time_warp

## Define arguments
## Usage: python space.py [past|present|future|4_digit_year-month]
valid_time_periods = ['past', 'present', 'future']
valid_years = range(1800, 2101)
valid_months = range(1, 13)
today = time_warp.date.today()
if len(sys.argv) < 2:
	print("\nUsage: python space.py [past|present|future|4_digit_year-month\n")



## Record the start time
start_time = time_warp.datetime.now()
print("Process Start Time:", start_time.strftime("%x %I:%M:%S %p\n"))



## Max amount of query days as specified by Nasa's API
max_query_days = 7



## Make a 'captains_log' folder for our cassetts if one doesn't exist
if not os.path.exists('final_frontier/captains_log'):
	os.mkdir('final_frontier/captains_log')

## Make a 'json_data' folder to store the json data if one doesn't exist
if not os.path.exists('final_frontier/json_data'):
	os.mkdir('final_frontier/json_data')



## Get the time period argument and format it. If none given, set to this year and month
try:
	time_period = sys.argv[1]
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



## Calculate the date ranges to query
query_dates = time_warp.calculate_query_dates(time_period, max_query_days)



## Abbreviate the asteroids class
a = asteroids.asteroids()



## Call the closest approach function
print("Gathering closest approach data for all asteroids...", end="", flush=True)
asteroid_data, total_element_count, nearest_ten_object_misses = a.asteroid_closest_approach()

## Write out the closest approach JSON file
closest_approach_file = open('final_frontier/json_data/asteroid_closest_approach.json', 'w')
closest_approach_file.write(json.dumps(asteroid_data))
closest_approach_file.close()

## Calculate how long the closest approach process took
closest_approach_end_time = time_warp.datetime.now()
closest_approach_duration = closest_approach_end_time - start_time
print(" Collected [", str(total_element_count), "] objects, taking", closest_approach_duration)



## Call the closest approaches for the given month
print("Gathering closest approach data for", query_dates[0][0], "through", query_dates[-1][-1] + "...", end="", flush=True)
month_closest_approaches_data, total_element_count = a.month_closest_approaches(query_dates)

## Write out the closest approaches for the month JSON file
month_closest_file = open('final_frontier/json_data/month_closest_approaches.json', 'w')
month_closest_file.write(json.dumps(month_closest_approaches_data))
month_closest_file.close()

## Calculate how long the closest approaches for the month process took
month_closest_end_time = time_warp.datetime.now()
month_closest_duration = month_closest_end_time - closest_approach_end_time
print(" Colleced [", str(total_element_count), "] objects, taking", month_closest_duration)



## call the nearest misses function
print("Gathering the ten closest approaches...", end="", flush=True)
if len(nearest_ten_object_misses) == 10:
	nearest_misses_data = a.nearest_misses(nearest_ten_object_misses)
else:
	nearest_misses_data = a.nearest_misses()

## Write out the top ten nearest misses JSON file
nearest_misses_file = open('final_frontier/json_data/nearest_misses.json', 'w')
nearest_misses_file.write(json.dumps(nearest_misses_data))
nearest_misses_file.close()

## Calculate how long the nearest misses process took
nearest_misses_end_time = time_warp.datetime.now()
nearest_misses_duration = nearest_misses_end_time - month_closest_end_time
print(" Collected [ 10 ] objects, taking", nearest_misses_duration)



## Record the end time and calculate the duration
end_time = time_warp.datetime.now()
duration = end_time - start_time

print("\nProcess Start Time:", start_time.strftime("%x %I:%M:%S %p"))
print("Process End Time:", end_time.strftime("%x %I:%M:%S %p"))
print("Process Duration:", duration)

## Show the user where to find the output files
print("\nProcess complete. Please see this directory for the results:")
print(os.getcwd() + '/final_frontier/json_data/')