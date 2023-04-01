import city_country_csv_reader
from locations import create_example_countries_and_cities
from trip import Trip, create_example_trips
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def plot_trip(trip: Trip, projection='gnom', line_width=2, colour='b') -> None:
    """
    Plots a trip on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.
    """

    # Assuming that the latitude and longitude of the first country has the maximum and minimum latitude and longitude.
    # Storing the latitude and longitude of the first country into each variables
    min_lat = float(trip.trip[0].latitude)
    max_lat = float(trip.trip[0].latitude)
    min_lon = float(trip.trip[0].longitude)
    max_lon = float(trip.trip[0].longitude)

    # Iterating through the nested list trip from class trip
    for city in trip.trip:

        # if we found that the minimum latitude of other country is lower than the first country, we have to change the status.
        if float(city.latitude) < min_lat:
            min_lat = float(city.latitude)

        # if we found that the maximum latitude of other country is higher than the first country, we have to change the status.
        elif float(city.latitude) > max_lat:
            max_lat = float(city.latitude)

        # if we found that the minimum longitude of other country is lower than the first country, we have to change the status.
        if float(city.longitude) < min_lon:
            min_lon = float(city.longitude)

        # if we found that the maximum longitude of other country is higher than the first country, we have to change the status.
        elif float(city.longitude) > max_lon:
            max_lon = float(city.longitude)


    # Calculating the difference between two countries longitudes and latitudes
    lat_diff = max_lat - min_lat
    lon_diff = max_lon - min_lon

    # if the size of map is not at least 50 degrees in each direction, we have to add more degrees according to the amount of difference
    # so that the size of a map will become at least 50 degrees in each direction
    if lat_diff < 50:
        max_lat += (50 - lat_diff) / 2 + 5
        min_lat -= (50 - lat_diff) / 2 + 5

    # if the size of map is at least 50 degrees in each direction, we are just padding the boundary by 5 degrees.
    else:
        max_lat += 5
        min_lat -= 5

    # if the size of map is not at least 50 degrees in each direction, we have to add more degrees according to the amount of difference
    # so that the size of a map will become at least 50 degrees in each direction
    if lon_diff < 50:
        max_lon += (50 - lon_diff) / 2 + 5
        min_lon -= (50 - lon_diff) / 2 + 5

    # if the size of map is at least 50 degrees in each direction, we are just padding the boundary by 5 degrees.
    else:
        max_lon += 5
        min_lon -= 5

    # plotting the map by using mill projection and boundary calculated above.
    world_map = Basemap(projection='mill', llcrnrlat=min_lat, llcrnrlon=min_lon, urcrnrlat=max_lat, urcrnrlon=max_lon)

    # drawing different elements into map
    world_map.drawcoastlines(linewidth=0.5)
    world_map.drawcountries(linewidth=0.5)
    world_map.fillcontinents()

    # List variable to store the relative country longitude and latitude in order to draw the lines(edges) between each other
    latitudes = []
    longitudes = []

    # Iterating through the nested list trip from class trip
    for city in trip.trip:
        # storing the each latitide and longitude to the variables city_lat and city_lon for latter usage
        city_lat, city_lon = float(city.latitude), float(city.longitude)
        lat, lon = world_map(city_lon, city_lat)

        # appending all the position into list latitudes and longitudes
        latitudes.append(lat)
        longitudes.append(lon)

        # draw the vertices(nodes) for each countries, using blue color and markersize 2
        world_map.plot(lat, lon, 'b.', markersize=2)

    # drawing the lines between countries locations using the list stored, using the color and linewidth specified in the function.
    world_map.plot(latitudes, longitudes, color=colour, linewidth=line_width)

    # variable title to store file name, counter and limit variable to check the condition
    title = 'map'

    # Iterating through the list trip in class trip to append the file string.
    for city in trip.trip:
        title += '_' + city.name
    title += ".png"

    # including the title in the map and finally saving the map to a file
    plt.title(title)
    plt.savefig(title)
    plt.clf()


if __name__ == "__main__":
    # reading the csv file
    city_country_csv_reader.create_cities_countries_from_CSV("fit1045_a3_applied05_november6th\worldcities_truncated.csv")

    # creating the countries and cities
    create_example_countries_and_cities()

    # creating the trip
    trips = create_example_trips()

    # Plotting each trip in the nested list trip
    for trip in trips:
        plot_trip(trip)