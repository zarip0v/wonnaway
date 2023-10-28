import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

class api:

    AVIASALES_TOKEN = os.getenv('AVIASALES_TOKEN')
    AVIASALES_URL = 'https://api.travelpayouts.com'
    IATAGEO_URL = 'https://iatageo.com'
    CURRENCY_URL = 'https://yasen.aviasales.ru/adaptors/currency.json'

    @staticmethod
    def getNameByCode(code):
        response = requests.get(f"{api.IATAGEO_URL}/getLatLng/{code}")
        data = json.loads(response.text)
        if "name" in data:
            return data["name"]
        return False

    @staticmethod
    def getDataByLocation(latitude, longitude):
        response = requests.get(f"{api.IATAGEO_URL}/getCode/{latitude}/{longitude}")
        data = json.loads(response.text)
        if "code" in data:
            return data
        return False

    @staticmethod
    def getTopDirections(code):
        query_params = {
            "origin": code,
            "token": api.AVIASALES_TOKEN
        }
        response = requests.get(f"{api.AVIASALES_URL}/v1/city-directions", params=query_params)
        data = json.loads(response.text)
        if "data" in data:
            return data
        return False

    @staticmethod
    def getTopCompanies(code):
        query_params = {
            "airline_code": code,
            "limit": 10,
            "token": api.AVIASALES_TOKEN
        }
        response = requests.get(f"{api.AVIASALES_URL}/v1/airline-directions", params=query_params)
        data = json.loads(response.text)
        if "data" in data:
            return data
        return False

    @staticmethod
    def getWhen(origin, destination):
        query_params = {
            "origin": origin,
            "destination": destination,
            "token": api.AVIASALES_TOKEN
        }
        response = requests.get(f"{api.AVIASALES_URL}/v1/prices/cheap", params=query_params)
        data = json.loads(response.text)
        if "success" in data and data["success"]:
            return data
        return False

    @staticmethod
    def getWhere(origin, datefrom, dateto):
        query_params = {
            "origin": origin,
            "departure_at": datefrom,
            "return_at": dateto,
            "limit": 10,
            "unique": "true",
            "token": api.AVIASALES_TOKEN
        }
        response = requests.get(f"{api.AVIASALES_URL}/aviasales/v3/prices_for_dates", params=query_params)
        data = json.loads(response.text)
        if "success" in data and data["success"]:
            return data
        return False

    @staticmethod
    def getCurrencies():
        response = requests.get(f"{api.CURRENCY_URL}")
        data = json.loads(response.text)
        if "usd" in data:
            return data
        return False