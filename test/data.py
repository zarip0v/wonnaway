import os
import json


class data:

    @staticmethod
    def upload_airports():
        full_path = os.path.realpath(__file__)
        with open(os.path.dirname(full_path) + '/data/airports.json', 'r') as f:
            airports_clean = json.loads(f.read())
        f.close()
        AIRPORTS = {}
        for airport in airports_clean:
            if "railway" not in airport["name"].lower():
                AIRPORTS[airport["code"]] = {
                    "name": airport["name_translations"]["ru"],
                    "city_code": airport["city_code"],
                    "country_code": airport["country_code"],
                    "coordinates": airport["coordinates"]
                }
        return AIRPORTS

    @staticmethod
    def upload_cities():
        full_path = os.path.realpath(__file__)
        with open(os.path.dirname(full_path) + '/data/cities.json', 'r') as f:
            cities_clean = json.loads(f.read())
        f.close()
        CITIES = {}
        for city in cities_clean:
            CITIES[city["code"]] = {
                "name": city["name_translations"]["ru"],
                "country_code": city["country_code"]
            }
        return CITIES

    @staticmethod
    def upload_countries():
        full_path = os.path.realpath(__file__)
        with open(os.path.dirname(full_path) + '/data/countries.json', 'r') as f:
            countries_clean = json.loads(f.read())
        f.close()
        COUNTRIES = {}
        for country in countries_clean:
            COUNTRIES[country["code"]] = {
                "name": country["name_translations"]["ru"]
            }
        with open(os.path.dirname(full_path) + '/data/country_cases.json', 'r') as f:
            countries_clean = json.loads(f.read())
        f.close()
        for country in countries_clean.keys():
            COUNTRIES[country]["cases"] = countries_clean[country]["cases"]
        return COUNTRIES

