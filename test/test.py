from data import data
from api import api

def test_upload_cities():
    assert data.upload_cities() == {'AAA': {'name': 'Анаа', 'country_code': 'PF'},
                                    'AAB': {'name': 'Аррабури', 'country_code': 'AU'},
                                    'AAC': {'name': 'Эль-Ариш', 'country_code': 'EG'}}

def test_upload_airports():
    assert data.upload_cities() == {'AAA': {'name': 'Анаа', 'city_code': 'AAA', 'country_code': 'PF',
                                            'coordinates': {'lon': -145.41667, 'lat': -17.05}},
                                    'AAB': {'name': 'Arrabury', 'city_code': 'AAB', 'country_code': 'AU',
                                            'coordinates': {'lon': 141.04167, 'lat': -26.7}},
                                    'AAC': {'name': 'El Arish International Airport', 'city_code': 'AAC', 'country_code': 'EG',
                                            'coordinates': {'lon': 33.75, 'lat': 31.133333}}}

def test_upload_countries():
    assert data.upload_countries() == {'DM': {'name': 'Доминика', 'cases': {'ro': 'Доминики', 'da': 'Доминике',
                                                                            'vi': 'в Доминику', 'tv': 'Доминикой',
                                                                            'pr': 'о Доминике'}},
                                       'CW': {'name': 'Кюрасао', 'cases': {'ro': 'Кюрасао', 'da': 'Кюрасао',
                                                                           'vi': 'в Кюрасао', 'tv': 'Кюросао',
                                                                           'pr': 'о Кюрасао'}},
                                       'GL': {'name': 'Гренландия', 'cases': {'ro': 'Гренландии', 'da': 'Гренландии',
                                                                              'vi': 'в Гренландию', 'tv': 'Гренландией',
                                                                              'pr': 'о Гренландии'}}}

def test_get_data_by_location():
    assert api.getDataByLocation(55.591141, 37.320492) == {'name': 'Vnukovo International Airport',
                                                            'code': 'VKO', 'IATA': 'VKO', 'ICAO': 'UUWW',
                                                            'distance_meters': '3832'}
def test_get_name_by_code():
    assert api.getNameByCode("VKO") == 'Vnukovo International Airport'
