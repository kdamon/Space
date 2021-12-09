import requests, pytest, vcr, json

class asteroids:
	# Set some shared variables for the functions
	base_url = 'https://api.nasa.gov/neo/rest/v1/'
	shuttle_payload = {'api_key': 'DEMO_KEY'}

	# Function to gather the asteroid closest approach data, then format and output the data
	@vcr.use_cassette('final_frontier/captains_log/aca.yaml')
	def asteroid_closest_approach(self):
		asteroid_closest_approach_response = requests.get(self.base_url + 'neo/browse', params=self.shuttle_payload)
		print('Status:', asteroid_closest_approach_response.status_code)
		print(asteroid_closest_approach_response.headers['X-RateLimit-Remaining'], 'api calls remaining')
		# print(asteroid_closest_approach_response.json())

		asteroid_data = asteroid_closest_approach_response.json()
		print(asteroid_data['near_earth_objects'][0]['close_approach_data'][0]['miss_distance']['lunar'])
		asteroid_approach_list = asteroid_data['near_earth_objects'][0]['close_approach_data']
		for earth_object in range(0, len(asteroid_data['near_earth_objects'])):
			print(earth_object)
			sorted_approach_list = sorted(asteroid_data['near_earth_objects'][earth_object]['close_approach_data'], key=lambda d: float(d['miss_distance']['lunar']))
			del sorted_approach_list[1:]
			print(sorted_approach_list)
			asteroid_data['near_earth_objects'][earth_object]['close_approach_data'] = sorted_approach_list
		next_page_base_url = 'http://www.neowsapp.com/rest/v1/neo/browse'
		self.shuttle_payload['size'] = '20'
		elements = asteroid_data['page']['total_elements']
		print(elements, 'total elements')
		pages = asteroid_data['page']['total_pages']
		print(pages, 'pages')
		for page in range(1, pages + 1):
			self.shuttle_payload['page'] = str(page)

		return asteroid_data

	# Function to gather the closest approach data for a given month
	@vcr.use_cassette('final_frontier/captains_log/mca.yaml')
	def month_closest_approaches(self, query_dates, only_return_closest_approach=False):
		self.shuttle_payload['start_date'] = '2021-12-01'
		self.shuttle_payload['end_date'] = '2021-12-07'
		print(self.shuttle_payload)
		print(query_dates)
		month_closest_approaches_response = requests.get(self.base_url + '/feed', params=self.shuttle_payload)
		print(month_closest_approaches_response.status_code)
		print(month_closest_approaches_response.headers['X-RateLimit-Remaining'], 'api calls remaining')
		# print(month_closest_approaches_response.json())
		month_closest_approaches_data = month_closest_approaches_response.json()

		return month_closest_approaches_data

	# Function to gather the nearest miss asteroids
	@vcr.use_cassette('final_frontier/captains_log/nm.yaml')
	def nearest_misses(self):
		nearest_misses_response = requests.get(self.base_url + 'neo/browse', params = self.shuttle_payload)
		print(nearest_misses_response.status_code)
		print(nearest_misses_response.headers['X-RateLimit-Remaining'], 'api calls remaining')
		# print(nearest_misses_response.json())
		nearest_misses_data = nearest_misses_response.json()

		return nearest_misses_data