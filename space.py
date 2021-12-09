from final_frontier import asteroids, time_warp

# print(dir(asteroids.asteroids))
print()

# Define arguments

# Calculate the date range to query
time_warp.calculate_query_dates()

# Abbreviate the asteroids class
a = asteroids.asteroids()

# Call the closest approach function
a.asteroid_closest_approach()

# Call the closest approaches for the given month
# a.month_closest_approaches()

# call the nearest misses function
# a.nearest_misses()