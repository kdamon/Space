import requests, pytest, vcr, json

class asteroids:
	## Set some shared variables for the functions
	base_url = 'https://api.nasa.gov/neo/rest/v1/'
	shuttle_payload = {'api_key': 'DEMO_KEY'}
	nearest_object_misses = {}



	## Function to gather the asteroid closest approach data, then format and output the data
	@vcr.use_cassette('final_frontier/captains_log/aca.yaml')
	def asteroid_closest_approach(self):
		total_element_count = 0

		## Request the NeoWs astroid data from Nasa's API
		asteroid_closest_approach_response = requests.get(self.base_url + 'neo/browse', params=self.shuttle_payload)

		## If we get a valid response, get the JSON data
		if asteroid_closest_approach_response.status_code == 200:
			asteroid_data = asteroid_closest_approach_response.json()

			## Iterate through the near earth objects on the first page of data
			for earth_object in range(0, len(asteroid_data['near_earth_objects'])):
				## Sort the close approach data by lunar miss distance
				sorted_approach_list = sorted(asteroid_data['near_earth_objects'][earth_object]['close_approach_data'], key=lambda d: float(d['miss_distance']['lunar']))
				## Keep only the closest approach data
				del sorted_approach_list[1:]
				## Replace the close approach data list with only the closest approach
				asteroid_data['near_earth_objects'][earth_object]['close_approach_data'] = sorted_approach_list
				## Record the closest approach asteroid ID and lunar miss distance to be used later for the top ten closest approaches
				self.nearest_object_misses[asteroid_data['near_earth_objects'][earth_object]['id']] = float(sorted_approach_list[0]['miss_distance']['lunar'])

			## Define some variables for the next pages of data
			next_page_base_url = 'http://www.neowsapp.com/rest/v1/neo/browse'
			self.shuttle_payload['size'] = '20'
			pages = asteroid_data['page']['total_pages']

			## Iterate through the pages of data to collect the closest approach for the remaining near earth objects
			for page in range(1, pages + 1):
				self.shuttle_payload['page'] = str(page)

				## Request next page of NeoWs data
				with vcr.use_cassette('final_frontier/captains_log/page_' + str(page) + '.yaml'):
					page_response = requests.get(next_page_base_url, params=self.shuttle_payload)

				## If we get a valid response, get the JSON data
				if page_response.status_code == 200:
					page_data = page_response.json()

					## Iterate through the near earth objects
					for earth_object in range(0, len(page_data['near_earth_objects'])):
						if len(page_data['near_earth_objects'][earth_object]['close_approach_data']) > 1:
							## Add to the total element count
							total_element_count += 1
							## Sort the close approach data by lunar miss distance
							sorted_approach_list = sorted(page_data['near_earth_objects'][earth_object]['close_approach_data'], key=lambda d: float(d['miss_distance']['lunar']))
							## Keep only the closest approach data
							del sorted_approach_list[1:]
							## Replace the close approach data list with only the closest approach
							page_data['near_earth_objects'][earth_object]['close_approach_data'] = sorted_approach_list
							## Record the closest approach asteroid ID and lunar miss distance to be used later for the top ten closest approaches
							self.nearest_object_misses[page_data['near_earth_objects'][earth_object]['id']] = float(sorted_approach_list[0]['miss_distance']['lunar'])
							## Append the near earth object data to the data we collected from the previous pages
							asteroid_data['near_earth_objects'].append(page_data['near_earth_objects'][earth_object])

						## If there's only one record of close approach data, no need to sort it
						elif len(page_data['near_earth_objects'][earth_object]['close_approach_data']) == 1:
							## Add to the total element count
							total_element_count += 1
							## Collect the close approach data
							sorted_approach_list = page_data['near_earth_objects'][earth_object]['close_approach_data']
							## Record the close approach asteroid ID and lunar miss distance to be used later for the top ten closest approaches
							self.nearest_object_misses[page_data['near_earth_objects'][earth_object]['id']] = float(sorted_approach_list[0]['miss_distance']['lunar'])
							## Append the near earth object data to the data we collected from the previous pages
							asteroid_data['near_earth_objects'].append(page_data['near_earth_objects'][earth_object])

				## If we get an invalid response
				else:
					asteroid_data['near_earth_objects'].append({'failed_to_get_page': str(page), 'status_code': page_response.status_code})

			## Sort the asteroid IDs by the lunar miss distance for all of the asteroids collected
			nearest_ten_object_misses = dict(sorted(self.nearest_object_misses.items(), key=lambda item: float(item[1])))
			## Get a list of the asteroid IDs
			nearest_ten_object_misses_keys = list(nearest_ten_object_misses.keys())
			## Delete the top ten closest approaches from the list of IDs because those are the ones we want to keep in the record
			del nearest_ten_object_misses_keys[:10]
			## Delete all of the asteroid records in the list above, thus keeping the top ten
			for nearest_miss in nearest_ten_object_misses_keys:
				del nearest_ten_object_misses[nearest_miss]

			## Cleanup the output JSON a bit
			del asteroid_data['links']
			del asteroid_data['page']

			## set the total element count in the JSON and the record of the top ten closest approaches
			asteroid_data['total_elements'] = str(total_element_count)
			self.nearest_object_misses = nearest_ten_object_misses

		## If we get an invalid response
		else:
			asteroid_data = {'failed_to_get_page': '0', 'status_code': asteroid_closest_approach_response.status_code}

		return asteroid_data, total_element_count, nearest_ten_object_misses




	## Function to gather the closest approach data for a given month
	def month_closest_approaches(self, query_dates):
		## Create an empty dictionary to collect the data
		month_closest_approaches_data = {}
		total_element_count = 0

		## Iterate through each set of seven days to query for the whole month
		for query in query_dates:
			## Define the start and end dates
			self.shuttle_payload['start_date'] = query[0]
			self.shuttle_payload['end_date'] = query[1]

			## Request the NeoWs asteroid data from Nasa's API
			with vcr.use_cassette('final_frontier/captains_log/month_query_' + query[0] + '_' + query[1] + '.yaml', record_mode='new_episodes'):
				query_closest_approaches_response = requests.get(self.base_url + 'feed', params=self.shuttle_payload)

				## If we get a valid response, get the JSON data
				if query_closest_approaches_response.status_code == 200:
					query_closest_approaches_data = query_closest_approaches_response.json()

					## If this is the first query, record all of the data to the empty dictionary
					if len(month_closest_approaches_data) == 0:
						month_closest_approaches_data = query_closest_approaches_data
					## Otherwise, append the data to the existing dictionary
					else:
						for response_date in query_closest_approaches_data['near_earth_objects'].keys():
							month_closest_approaches_data['near_earth_objects'][response_date] = query_closest_approaches_data['near_earth_objects'][response_date]

					## Add the number of query elements to the total element count
					total_element_count += int(query_closest_approaches_data['element_count'])

				## If we get an invalid response
				else:
					if not 'near_earth_objects' in month_closest_approaches_data.keys():
						month_closest_approaches_data['near_earth_objects'] = {}
					month_closest_approaches_data['near_earth_objects']['failed_to_get_date_range'] = {'dates': query, 'status_code': query_closest_approaches_response.status_code}

		## Cleanup the output JSON a bit
		del month_closest_approaches_data['links']

		## Set the total element count in the JSON
		month_closest_approaches_data['element_count'] = str(total_element_count)

		return month_closest_approaches_data, total_element_count




	## Function to gather the nearest miss asteroids
	@vcr.use_cassette('final_frontier/captains_log/nm.yaml')
	def nearest_misses(self, nearest_ten_object_misses=None):
		## Set the base url for collecting information about single asteroids
		near_object_base_url = 'http://www.neowsapp.com/rest/v1/neo/'

		## Create an empty dictionary to collect the data
		nearest_misses_data = {'near_earth_objects': []}

		## If the nearest ten object misses are passed in from the asteroid_closest_approach function, or if there are ten records in the nearest_object_misses dictionary, proceed with gathering their data
		if nearest_ten_object_misses != None or len(self.nearest_object_misses) == 10:
			if nearest_ten_object_misses == None:
				nearest_ten_object_misses = self.nearest_object_misses

			## Iterate through the nearest ten object misses
			for near_object in nearest_ten_object_misses.keys():
				## Request the asteroid's information from Nasa's API
				with vcr.use_cassette('final_frontier/captains_log/near_object_' + near_object + '.yaml', record_mode='new_episodes'):
					nearest_object_response = requests.get(near_object_base_url + near_object, params=self.shuttle_payload)

					## If we get a valid response, get the JSON data
					if nearest_object_response.status_code == 200:
						nearest_object_data = nearest_object_response.json()

						## If there is more than one close approach, sort the data to get the closest
						if len(nearest_object_data['close_approach_data']) > 1:
							sorted_approach_list = sorted(nearest_object_data['close_approach_data'], key=lambda d: float(d['miss_distance']['lunar']))
							del sorted_approach_list[1:]

							## Append the near earth object to the nearest misses dictionary
							nearest_object_data['close_approach_data'] = sorted_approach_list
							nearest_misses_data['near_earth_objects'].append(nearest_object_data)

					## If we get an invalid response
					else:
						nearest_misses_data['near_earth_objects'].append({'failed_to_get_data_for_asteroid': near_object, 'status_code': nearest_object_response.status_code})

		## If the nearest ten object misses aren't passed and aren't in the records,
		else:
			## then run the asteroid_closest_approach function to gather the information
			self.asteroid_closest_approach()

			## Make sure we have 10 records
			if len(self.nearest_object_misses) == 10:
				nearest_ten_object_misses = self.nearest_object_misses

				## Iterate through the nearest ten object misses
				for near_object in nearest_ten_object_misses.keys():
					## Request the asteroid's information from Nasa's API
					with vcr.use_cassette('final_frontier/captains_log/near_object_' + near_object + '.yaml', record_mode='new_episodes'):
						nearest_object_response = requests.get(near_object_base_url + near_object, params=self.shuttle_payload)

						## If we get a valid response, get the JSON data
						if nearest_object_response.status_code == 200:
							nearest_object_data = nearest_object_response.json()

							## If there is more than one close approach, sort the data to get the closest
							if len(nearest_object_data['close_approach_data']) > 1:
								sorted_approach_list = sorted(nearest_object_data['close_approach_data'], key=lambda d: float(d['miss_distance']['lunar']))
								del sorted_approach_list[1:]

								## Append the near earth object to the nearest misses dictionary
								nearest_object_data['close_approach_data'] = sorted_approach_list
								nearest_misses_data['near_earth_objects'].append(nearest_object_data)

						## If we get an invalid response
						else:
							nearest_misses_data['near_earth_objects'].append({'failed_to_get_data_for_asteroid': near_object, 'status_code': nearest_object_response.status_code})

		return nearest_misses_data