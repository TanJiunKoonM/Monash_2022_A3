from __future__ import annotations
from enum import Enum
import random
import geopy
from geopy.distance import great_circle
import math


class CapitalType(Enum):
    """
    The different types of capitals (e.g. "primary").
    """
    primary = "primary"
    admin = "admin"
    minor = "minor"
    unspecified = ""

    # returning string instead of address
    def __str__(self) -> str:
        return self.value


class Country():
    """
    Represents a country.
    """

    countries = dict()  # a dict that associates country names to instances.

    def __init__(self, name: str, iso3: str) -> None:
        """
        Creates an instance with a country name and a country ISO code with 3 characters.
        """
        self.name = name
        self.iso3 = iso3

        # appending to the dictionary
        Country.countries[self.name] = self

    def add_city(self, city: City):
        """
        Adds a city to the country.
        """

        # iterating over dictionary, if the name is found, adding the rest of countries 
        for x in City.cities.values():
            if x.country == self.name:
                City.cities[city.city_id] = self

    def get_cities(self, capital_types: list[CapitalType] = None) -> list[City]:
        """
        Returns a list of cities of this country.

        The argument capital_types can be given to specify a subset of the capital types that must be returned.
        1. Cities that do not correspond to these capital types are not returned.
        2. If no argument is given, all cities are returned.
        """

        self_cities = []

        # appending all the relevant countries into list self_cities
        for x in City.cities.values():
            if x.country == self.name:
                self_cities.append(x)

        # if no argument given, return all the cities
        return_cities = []
        if capital_types == None:
            return self_cities

        # if arguments given, return all the relevant countries
        else:
            for x in self_cities:
                for y in capital_types:
                    if x.capital_type == y.value:
                        return_cities.append(x)
        return return_cities

    def get_city(self, city_name: str) -> City:
        """
        Returns a city of the given name in this country.
        1. Returns None if there is no city by this name.
        2. If there are multiple cities of the same name, returns an arbitrary one.
        """
        self_cities = self.get_cities()
        ret = []

        # appending all the same city name countries into list ret
        for x in self_cities:
            if x.name == city_name:
                ret.append(x)

        # no city is found
        if len(ret) == 0:
            return None

        # # If there are one city of the same name, returns that city.
        elif len(ret) == 1:
            return ret[0]

        # If there are multiple cities of the same name, returns an arbitrary one.
        else:
            return random.choice(ret)

    def __str__(self) -> str:
        """
        Returns the name of the country.
        """
        return self.name


class City():
    """
    Represents a city.
    """

    cities = dict()  # a dict that associates city IDs to instances.

    def __init__(self, name: str, latitude: str, longitude: str, country: str, capital_type: str, city_id: str) -> None:
        """
        Initialises a city with the given data.
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        self.capital_type = capital_type
        self.city_id = city_id

        self.cities[self.city_id] = self

    def distance(self, other_city: City) -> int:
        """
        Returns the distance in kilometers between two cities
        using the great circle method,
        rounded up to an integer.
        """
        self_bearings = (self.latitude, self.longitude)
        other_bearings = (other_city.latitude, other_city.longitude)
        return math.ceil(great_circle(self_bearings, other_bearings).kilometers)

    def __str__(self) -> str:
        """
        Returns the name of the city and the country ISO3 code in parentheses.
        For example, "Melbourne (AUS)".
        """
        country_code = ""
        for capital_country_name in Country.countries.values():
            if str(self.country) == str(capital_country_name):
                country_code = capital_country_name.iso3
                break
            else:
                continue
        return f"{self.name} ({country_code})"


def create_example_countries_and_cities() -> None:
    """
    Creates a few Countries and Cities for testing purposes.
    """
    australia = Country("Australia", "AUS")
    melbourne = City("Melbourne", "-37.8136", "144.9631", "Australia", "admin", "1036533631")
    canberra = City("Canberra", "-35.2931", "149.1269", "Australia", "primary", "1036142029")
    sydney = City("Sydney", "-33.865", "151.2094", "Australia", "admin", "1036074917")

    japan = Country("Japan", "JPN")
    tokyo = City("Tokyo", "35.6839", "139.7744", "Japan", "primary", "1392685764")


def test_example_countries_and_cities() -> None:
    """
    Assuming the correct cities and countries have been created, runs a small test.
    """
    australia = Country.countries['Australia']
    canberra = australia.get_city("Canberra")
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")

    print("The distance between {} and {} is {}km".format(melbourne, sydney, melbourne.distance(sydney)))

    for city in australia.get_cities([CapitalType.admin, CapitalType.primary]):
        print("{} is a {} capital of {}".format(city, city.capital_type, city.country))


if __name__ == "__main__":
    create_example_countries_and_cities()
    test_example_countries_and_cities()