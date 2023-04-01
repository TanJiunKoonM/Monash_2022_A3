import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles
import networkx
from itertools import combinations
import math


def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:
    """
    Returns a shortest path between two cities for a given vehicle,
    or None if there is no path.
    """
    world_map = networkx.Graph()

    # creating a nested list by appending all the cities from the list City from class Country into the variable all_paths.
    all_paths = combinations(City.cities, 2)            # country name

    # Iterating through all the elements in the nested list variable all_paths.
    for path in all_paths:
        # Adding the edges betweem two countries, and adding the weight (smallest travel time) on the edges by invoking the function compute_travel_time.
        world_map.add_edge(City.cities[path[0]], City.cities[path[1]],
                           weight=(City.cities[path[0]], City.cities[path[1]]))

    # we use the module networkx to find the smallest weight between two countries and store into variable shortest_path
    shortest_path = networkx.shortest_path(world_map, source=from_city, target=to_city, weight='weight')

    # we use the module networkx to find the length between two countries and store into variable length
    length = networkx.shortest_path_length(world_map, source=from_city, target=to_city, weight='weight')

    # if the length is math.inf, which means there is no path between two countries, so we will return None
    if length == math.inf:
        return None

    # if there is no path, returning the shortest path between two cities for a given vehicle
    else:

        # creating instance variables by calling class Trip using the country in the list shortest_path on index 0
        trip = Trip(shortest_path[0])

        # appending all the rest of the elements in the list shortest_path into the variable list trip.
        for city in shortest_path[1:]:
            trip.add_next_city(city)
        return trip


if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("fit1045_a3_applied05_november6th\worldcities_truncated.csv")

    vehicles = create_example_vehicles()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    # Showing the shortest path between two countries for 3 different vehicles.
    for vehicle in vehicles:
        print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo,
                                                                    find_shortest_path(vehicle, melbourne, tokyo)))