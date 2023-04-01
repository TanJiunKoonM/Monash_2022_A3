import city_country_csv_reader
from locations import City, Country
from trip import Trip, create_example_trips
from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley, create_example_vehicles
from path_finding import find_shortest_path
from map_plotting import plot_trip
import time


class OnboardNavigation:
    def __init__(self):

        # Reading the csv file, creating vehicles examples, creating trips examples
        city_country_csv_reader.create_cities_countries_from_CSV("fit1045_a3_applied05_november6th\worldcities_truncated.csv")
        example_vehicles = create_example_vehicles()
        example_trips = create_example_trips()

        # A list variable to store the vehicles instances
        fleet = []
        end = False

        # while boolean end is not true, so iteration will keep looping
        while not end:

            # Prompt the users to enter the options create a fleet of vehicles
            print('Add a vehicle to your fleet: ')
            print('1. Choose from example vehicles')
            print('2. Create custom vehicle')

            # while the code is not break, which means the user do not give a valid input, so the code will keep looping
            while True:
                try:
                    user_input = int(input('Select your option: '))

                    # Assuming the user gives the valid input otherwise the string will be shown
                    assert user_input in [1, 2], 'Please enter an integer to select your option'
                    break

                # while the user give invalid input, the warming string below will be shown
                except Exception as e:
                    print(f'Error - {e}')

            # if the input is 1, the user will create the vehicles by the examples given.
            if user_input == 1:
                fleet.append(self.choose_from_example_vehicles(example_vehicles))

            # if the input is 2, which means the user want to create a custom vehicle.
            elif user_input == 2:
                fleet.append(self.create_vehicle())

            print('Do you wish to continue adding vehicles?\n1. Yes\n2. No')
            while True:
                try:
                    # Prompt the users to enter the options
                    # if the input is 1, which means the user want to create more vehicles
                    user_input = int(input('Select your option: '))
                    assert user_input in [1, 2], 'Please enter an integer to select your option'

                    # the break code will stop execution of this block, and then go back the beginning and start code again
                    break

                # while the user give invalid input, the warming string below will be shown
                except Exception as e:
                    print(f'Error - {e}')

            # if the input is 2, which means the user do not want to create more vehicles, so the boolean end will turn into True, and stop execution
            if user_input == 2:
                end = True

        # Prompt the users to enter the options create a trip
        print('Create a trip: ')
        print('1. Choose from example trips')
        print('2. Create a custom trip')
        print('3. Find the shortest path between 2 cities for a given vehicle in your fleet')

        # if the user do not give valid options, the break statement will not be executed and teh code below will keep looping.
        while True:
            try:
                user_input = int(input('Select your option: '))

                #  Prompt the users to enter the options they want
                assert user_input in [1, 2, 3], 'Please enter an integer to select your option'
                break
            except Exception as e:
                print(f'Error - {e}')

        # if the input of the user is 1, which means user want to create the trip from trips examples
        if user_input == 1:
            trip = self.choose_from_example_trips(example_trips)

        # if the input of the user is 2, which means user want to create the custom trip by manually adding all cities
        elif user_input == 2:
            trip = self.create_trips()

        # if the input of the user is 3, which means the user want to find a shortest path between two given cities given by users for one vehicle or a fleet of vehicles.
        elif user_input == 3:
            trip = self.find_shortest_path_for_given_vehicle(fleet)[0]

        # a nested list to store the travel times for each vehicles in the fleets for travel time comparison usage.
        vehicle_travel_times = []

        # Iterating over the length of fleet, which means the length of vehicle_travel_times will depend on how many vehicles created
        # appending empty list into variable vehicle_travel_times
        for _ in range(len(fleet)):
            vehicle_travel_times.append([])

        # Iterating over the length of list fleet and the length of list trip
        for x in range(len(fleet)):
            for y in range(len(trip.trip) - 1):
                # the code here will compute the travel time for each vehicles and store the travel time between two countries provided by trip
                # the position of nested list vehicle_travel_times represent each travel time between two specific countries and different vehicles
                vehicle_travel_times[x].append(find_shortest_path(fleet[x], trip.trip[y], trip.trip[y + 1])[1])

        # variable list vehicle_total_travel_times will store the total travel time for each vehicles
        vehicle_total_travel_times = []

        # Iterating over vehicle_travel_times and sum up all the travel time into variable vehicle_total_travel_times
        for array in vehicle_travel_times:
            vehicle_total_travel_times.append(sum(array))

        # storing the index of fastest vehicle into variable fastest_vehicle_index, which means the minumum travel used to travel from departure to destination
        fastest_vehicle_index = vehicle_total_travel_times.index(min(vehicle_total_travel_times))

        # finding the fastest vehicle and store into variable fastest_vehicle, and store tge fastest time into variable fastest_time.
        fastest_vehicle = fleet[fastest_vehicle_index]
        fastest_time = min(vehicle_total_travel_times)

        # Output the result
        print(f'Trip: {trip}')
        print(f'Fastest vehicle: {fastest_vehicle} ({fastest_time} hrs)')

        # call the plot_trip function from file map_plotting to show the map produced
        print('Map creation is in progress....')
        plot_trip(trip)

        # calling simulate_trip function to start travelling
        self.simulate_trip(fleet, trip, vehicle_travel_times, vehicle_total_travel_times)


    def simulate_trip(self, fleet, trip, vehicle_travel_times, vehicle_total_travel_times):
        """
        This function will simulate the trip.

        Arguments:
            - fleet : a list of vehicles instances created so far
            - trip : a list of countries instances
            - vehicle_travel_times : a nested list of travel times for each vehicles in the fleets.
            - vehicle_total_travel_times : a list of total travel time for each vehicles

        Returning nothing.
        """

        print('Simulate the trip for a vehicle in your fleet:')

        # Iterating through the list fleet, and print all the vehicles for user to choose
        for x in range(len(fleet)):
            print(f'{x + 1}. {fleet[x]}')

        # while the code is not break, the code below will keep looping
        while True:

            # Prompt the user to give option
            try:
                user_input = int(input('Please select a vehicle for your trip: '))

                # storing the index of user given into variable vehicle_selected_index
                vehicle_selected_index = user_input - 1
                break

            # Showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        # total bar size will be printed
        bar_size = 50
        travel_speed = 1

        # defining the updating speed by divide 10
        progress_between_updates = travel_speed 

        # variable travel_length represent total travel time
        travel_length = vehicle_total_travel_times[vehicle_selected_index]

        travel_progress = 0
        pointer = 0

        # while the status is not over, which means the updated travel_progress is still less than travel_length
        while travel_progress < travel_length:

            # pausing the code by 0.1 seconds
            time.sleep(0.1)

            # updating the status
            travel_progress = min(travel_length, travel_progress + progress_between_updates)

            # if the code is not over, updating the pointer by adding 1
            if travel_progress >= sum(vehicle_travel_times[vehicle_selected_index][:pointer + 1]):
                pointer += 1

            # fraction_traveled represent the progress status
            fraction_traveled = travel_progress / travel_length

            # determining how many * need to be printed and store the value into variable progress
            progress = int(fraction_traveled * bar_size)

            # different string format to indicate the status
            display_string = 'Current traveling: {:<40}'
            display_string2 = 'Reached destination: {:<40}'

            # when it is not the end of the progress bar, the code below will be executed
            if pointer < len(vehicle_travel_times[vehicle_selected_index]):
                print(display_string.format(f'{trip.trip[pointer]} -> {trip.trip[pointer + 1]}') + "{:3.0f}".format(
                    100 * fraction_traveled) + '% [' + '*' * progress + ' ' * (bar_size - progress) + ']', flush=True,
                      end='\r')

            # when it is the end of the progress bar, the code below will be executed to indicate the ending
            else:
                print(display_string2.format(f'{trip.trip[pointer]}') + "{:3.0f}".format(
                    100 * fraction_traveled) + '% [' + '*' * progress + ' ' * (bar_size - progress) + ']', flush=True,
                      end='\r')


    def choose_from_example_vehicles(self, example_vehicles: list[Vehicle]):
        """
        This function will create the same vehicle instance that already stored in the variable example_vehicles.

        Arguments:
            - example_vehicles : a list of vehicles instances created so far

        Returning vehicle instances.
        """

        print('Example vehicles:')

        # Prompts the user to select the options given
        for x in range(len(example_vehicles)):
            print(f'{x + 1}. {example_vehicles[x]}')

        # while the user do not give valid option, the code below will keep executing
        while True:
            try:
                user_input = int(input('Please select your option: '))

                # storing the instances that already created into variable vehicle
                vehicle = example_vehicles[user_input - 1]
                break

            # Showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        print('Vehicle added successfully')

        return vehicle

    def create_vehicle(self):
        """
        This function will create the custom vehicle that specified by the user.

        Arguments:
            - nothing

        Returning vehicle instances.
        """

        print('Example vehicles:')
        print('1. Crappy Crepe Car\n2. Diplomacy Donut Dinghy\n3. Teleporting Tarte Trolley')
        while True:
            try:
                user_input = int(input('Choose a vehicle: '))

                # if the input of user is not valid, the error message will be shown, the prompt the user to give the input again.
                assert user_input in [1, 2, 3], 'Please enter an integer to select your option'
                break

            #  showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        # if the input is 1, which means the user want to create CrappyCrepeCar vehicle
        if user_input == 1:
            speed = int(input('Please enter a speed for your vehicle (km/h): '))

            # creating the vehicle instance by calling the class CrappyCrepeCar by using the parameter speed provided by user
            vehicle = CrappyCrepeCar(speed)

        # if the input is 2, which means the user want to create DiplomacyDonutDinghy vehicle
        elif user_input == 2:
            speed = int(input('Please enter the in-country speed for your vehicle (km/h): '))
            speed2 = int(input('Please enter the between-primary speed for your vehicle (km/h): '))

            # creating the vehicle instance by calling the class DiplomacyDonutDinghy by using the parameters speed and speed2 provided by user
            vehicle = DiplomacyDonutDinghy(speed, speed2)


        # if the input is 3, which means the user want to create DiplomacyDTeleportingTarteTrolleyonutDinghy vehicle
        elif user_input == 3:
            travel_time = int(input('Please enter the travel time for your vehicle (hr): '))
            max_distance = int(input('Please enter a max distance for your vehicle (km): '))

            # creating the vehicle instance by calling the class TeleportingTarteTrolley by using the parameters travel_time and max_distance provided by user
            vehicle = TeleportingTarteTrolley(travel_time, max_distance)

        print('Vehicle added successfully')
        return vehicle

    def choose_from_example_trips(self, example_trips):
        """
        This function will choose the trip based on the trip examples

        Arguments:
            - example_trips: a nested list that represent different countries for the trip

        Returning vehicle instances.
        """
        print('Example trips:')


        # Showing the trips available for users to select
        for x in range(len(example_trips)):
            print(f'{x + 1}. {example_trips[x]}')
        while True:
            try:
                user_input = int(input('Please select your option: '))

                # storing the trip instances that already created into variable trip
                trip = example_trips[user_input - 1]
                break

            #  showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        print('Trip created successfully')

        return trip

    def create_trips(self):
        """
        This function will create the custom trip that specified by the user

        Arguments:
            - nothing

        Returning trip instances
        """

        while True:
            try:
                user_input = input(
                    'Please enter an ordered list of cities you would like to add to your trip (e.g. Melbourne, Tokyo, Sydney): ').lower()

                # Splitting the value given by user and store into variable cities
                cities = user_input.split(', ')

                # boolean variable to indicate the countries existence
                city_exists = False

                # iterating over class variable cities to find the country is exist or not.
                for city in City.cities.values():

                    # if the country is exist, create the trip
                    if city.name.lower() == cities[0]:
                        trip = Trip(city)
                        city_exists = True
                        break

                #  showing the error message and prompt the user give the option again
                assert city_exists == True, 'One or more cities in entered list does not exist'

                # the code below is used to handle the rest of the input provided by the user
                for input_city in cities[1:]:
                    city_exists = False

                    # itera
                    for city in City.cities.values():

                        # if the country is exist, appending the countries into trip
                        if city.name.lower() == input_city:
                            trip.add_next_city(city)
                            city_exists = True
                            break

                    assert city_exists == True, 'One or more cities in entered list does not exist'

                # If all the checking is done, break the code and stop iterating to check again
                break

            #  showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        print('Trip created successfully, map creation is in the progress....')

        return trip

    def find_shortest_path_for_given_vehicle(self, fleet):
        """
        This function will find the shortest path for a given vehicle

        Arguments:
            - fleet: a list of instance vehicles that created for far.

        Returning string representation of shortest path for a trip and length
        """

        while True:
            try:

                # prompt the user to give the country name for departure city and turn it into lowercase string and store into variable user_input
                user_input = input('Please enter the departure city for your trip: ').lower()
                city_exists = False

                # iterating over the class variable cities to find whether the country is exist or not.
                for city in City.cities.values():
                    if city.name.lower() == user_input:
                        departure = city
                        city_exists = True
                        break

                # check whether city_exists is true or not, if not give error message and keep looping
                assert city_exists == True, 'City does not exist'
                break

            #  showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        while True:
            try:
                user_input = input('Please enter the destination city for your trip: ').lower()
                city_exists = False

                # iterating over the class variable cities to find whether the country is exist or not.
                for city in City.cities.values():
                    if city.name.lower() == user_input:
                        destination = city
                        city_exists = True
                        break

                # check whether city_exists is true or not, if not give error message and keep looping
                assert city_exists == True, 'City does not exist'

                #  If all the checking is done, break the code and stop iterating to check again
                break

            #  showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        print('Please select a vehicle (selected vehicle will be used to calculate the shortest path): ')

        # show all the vehicles that created in the list fleet so far and prompt the user to give the option
        for x in range(len(fleet)):
            print(f'{x + 1}. {fleet[x]}')
        print(f'{len(fleet) + 1}. All vehicles')

        while True:
            try:
                user_input = int(input('Please select a vehicle for your trip: '))

                # if the user want all the vehicles, store the list fleet into variable vehicle_selected
                if user_input == len(fleet) + 1:
                    vehicle_selected = fleet

                # is the user only want to check a specific vehicle, select the specified vehicle and store into variable vehicle_selected
                else:
                    vehicle_selected = fleet[user_input - 1]
                break

            # showing the error message and prompt the user give the option again
            except Exception as e:
                print(f'Error - {e}')

        # if type of variable vehicle_selected, which means the user want all the vehicles, so the code below will be executed
        if type(vehicle_selected) == list:
            print('Shortest paths for each vehicle in fleet: ')
            print("Please wait a while...")

            # iterating over based on the length of list vehicle_selected
            for x in range(len(vehicle_selected)):
                # print all the calculated shortest path time for each vehicles by calling function find_shortest_path from path_finding
                print(
                    f'{x + 1}. {vehicle_selected[x]}: {find_shortest_path(vehicle_selected[x], departure, destination)[1]} hours')
            while True:
                try:
                    user_input = int(input('Please select your option: '))

                    # store the string representation of shortest path for a trip and length into variable shortest_path by using the vehicles specified by user
                    # calling function find_shortest_path from path_finding
                    shortest_path = find_shortest_path(vehicle_selected[user_input - 1], departure, destination)
                    break
                except Exception as e:
                    print(f'Error - {e}')

        else:
            print('Shortest paths for selected vehicle in fleet: ')
            print("Please wait a while...")

            # calling function find_shortest_path from path_finding and store the string representation of shortest path for a trip and length into variable shortest_path
            shortest_path = find_shortest_path(vehicle_selected, departure, destination)

        print('Trip created successfully, map creation is in the progress....')
        return shortest_path


OnboardNavigation()