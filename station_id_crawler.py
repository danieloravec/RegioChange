import requests
from bs4 import BeautifulSoup


class Crawler:

    @staticmethod
    def crawl():
        stations = {}
        urls = [
            'https://www.regiojet.sk/cestovne-poriadky-a-zastavky/cestovne-poriadky/index.html?timetableId=3252012012',
            'https://www.regiojet.sk/cestovne-poriadky-a-zastavky/cestovne-poriadky/index.html?stationId=2370298000',
        ]
        for url in urls:
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'html.parser')
            for station in soup.findAll('div', {'class': 'sa-stationLabel'}):
                name = station.string
                station_string = str(station)
                station_id = ''
                for char in station_string:
                    if '9' >= char >= '0':
                        station_id += char
                stations[name] = station_id
        return stations

    @staticmethod
    def transform_to_string(stations):
        return str(stations)
