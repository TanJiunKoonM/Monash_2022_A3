from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from vehicles import create_example_vehicles
import math
from locations import City, Country
from locations import create_example_countries_and_cities


class Trip():
    """
    Represents a sequence of cities.
    """

    def __init__(self, departure: City) -> None:
        """
        Initialises a Trip with a departure city.
        """
        self.trip = []
        self.departure_city = departure
        self.trip.append(departure)

    def add_next_city(self, city: City) -> None:
        """
        Adds the next city to this trip.
        """
        self.trip.append(city)

    def total_travel_time(self, vehicle: Vehicle) -> float:
        """
        This function will determine the total travel time

        Arguments:
            - vehicle : a instance variable from class Vehicle

        Returns the total travel time of the vehicle.
        """
        total_time = 0

        # iterating through the elements of the list self trip.
        for x in range(len(self.trip) - 1):

            # if the travel time between two countries is not math.inf, which means there is a path between two countries, so we will sum all the travel time
            if vehicle.compute_travel_time(self.trip[x], self.trip[x + 1]) != math.inf:
                total_time += vehicle.compute_travel_time(self.trip[x], self.trip[x + 1])

            # Returns math.inf if any leg (i.e. part) of the trip is not possible.
            else:
                return math.inf
        return total_time

    def find_fastest_vehicle(self, vehicles: list[Vehicle]):
        """
        This function will determine the fastest vehicle between two countries

        Arguments:
            - vehicles : a list of vehicles from class Vehicle

        Returns the Vehicle for which this trip is fastest, and the duration of the trip.
        """

        # Assuming that the first vehicle in the list vehicles is the fastest vehicle.
        fastest_vehicle = vehicles[0]

        # Iterating through the list vehicles to find the fastest vehicle between two countries given.
        # Aware that if there is a tie, we would not change the fastest vehicle on variable fastest_vehicle which means we do not have to create a list.
        for vehicle in vehicles:
            if self.total_travel_time(vehicle) < self.total_travel_time(fastest_vehicle):
                fastest_vehicle = vehicle

        # If the trip is not possible for any of the vehicle, return (None, math.inf).
        if self.total_travel_time(fastest_vehicle) == math.inf:
            return None, self.total_travel_time(fastest_vehicle)

        # If the trip is possible for any of the vehicle, return the Vehicle for which this trip is fastest, and the duration of the trip.
        else:
            return fastest_vehicle, self.total_travel_time(fastest_vehicle)

    def __str__(self) -> str:
        """
        Returns a representation of the trip as a sequence of cities:
        City1 -> City2 -> City3 -> ... -> CityX
        """
        return_string = ''

        # iterating based on the length of trip.
        for x in range(len(self.trip)):

            # if the element is not the last one, we have to add ' -> ' to indicate the next trip.
            if x != len(self.trip) - 1:
                return_string += str(self.trip[x]) + ' -> '

            # if the element (x) is last one, we just don't add anything since there is no more location added after this location.
            else:
                return_string += str(self.trip[x])
        return return_string


def create_example_trips() -> list[Trip]:
    """
    Creates examples of trips.
    """

    # first we create the cities and countries
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    # then we create trips
    trips = []

    # Iterating through the elements in the list given.
    for cities in [(melbourne, sydney), (canberra, tokyo), (melbourne, canberra, tokyo), (canberra, melbourne, tokyo)]:
        trip = Trip(cities[0])

        # Iterating through all the rest elements in the list cities and appending all the alements into variable list trips.
        for city in cities[1:]:
            trip.add_next_city(city)

        trips.append(trip)

    return trips


if __name__ == "__main__":
    vehicles = create_example_vehicles()
    trips = create_example_trips()

    # Iterating through the list trips
    for trip in trips:
        # finding the fastest vehicle between two countries given, and then store the fastest vehicle and the travel duration into variable vehicle, duration.
        vehicle, duration = trip.find_fastest_vehicle(vehicles)
        print("The trip {} will take {} hours with {}".format(trip, duration, vehicle))