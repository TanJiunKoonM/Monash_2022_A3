from locations import City, Country, test_example_countries_and_cities


def create_cities_countries_from_CSV(path_to_csv: str) -> None:
    """
    Reads a CSV file given its path and creates instances of City and Country for each line.
    """

    # opening the file provided by function create_cities_countries_from_CSV
    with open(path_to_csv, encoding="utf8") as file:
        file.readline()

        # iterating through the line in the file, and splitting the line into a list.
        for line in file:
            parsed_line = line.strip().split(',')

            if(len(parsed_line) != 11):
                print(parsed_line)

            # if the list is abnormal, which is len() = 13, which mean we have to combined 3 elements into 1 elements, and then removed the extra elements.
            if len(parsed_line) == 13:
                parsed_line[4] = parsed_line[4] + parsed_line[5] + parsed_line[6]
                parsed_line.remove(parsed_line[5])
                parsed_line.remove(parsed_line[5])

            # if the list is abnormal, which is len() = 12, which mean we have to combined 2 elements into 1 elements, and then removed the extra elements.
            if len(parsed_line) == 12:
                parsed_line[7] = parsed_line[8] + parsed_line[7]
                parsed_line.remove(parsed_line[8])

            country_exists = False

            # iterating through the list of countries in class Country from file location, finding whether the country is exist or not, if the country is exist, break the code.
            for country in Country.countries:
                if parsed_line[4] == country:
                    country_exists = True
                    break

            # if the country is not exist, so we will create a new country by calling the class Country from file location.
            if not country_exists:
                Country(parsed_line[4], parsed_line[6])

            # once everything is done checking, we will create a new city by calling the Class City from file location.
            new_city = City(parsed_line[1], parsed_line[2], parsed_line[3], parsed_line[4], parsed_line[8],
                            parsed_line[10])


if __name__ == "__main__":
    # calling the function of create_cities_countries_from_CSV and test_example_countries_and_cities.
    create_cities_countries_from_CSV("fit1045_a3_applied05_november6th\worldcities_truncated.csv")
    test_example_countries_and_cities()
