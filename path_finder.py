import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time

import routes
from dates import Dates


class PathFinder:

    def __init__(self, _source, _target, _date, _departure_time, _max_waiting_time):
        self.source = _source
        self.target = _target
        self.date = datetime.datetime(
            int(_date[6:10]),
            int(_date[3:5]),
            int(_date[0:2]),
            int(_departure_time[0:2]),
            int(_departure_time[3:]),
            0
        )
        self.max_waiting_time = _max_waiting_time

    def find_path(self):
        source_id = routes.STATION_CODES[self.source]
        target_id = routes.STATION_CODES[self.target]
        source_index = None
        target_index = None
        route = None
        for current_route in routes.ALL_ROUTES:
            found_source = False
            found_target = False
            for index, station in enumerate(current_route):
                if (not found_source) and (station == source_id):
                    found_source = True
                    source_index = index
                elif found_source and (not found_target) and (station == target_id):
                    found_target = True
                    target_index = index
                    route = current_route
                    break
            if found_target:
                break
        full_route = self.get_changes(route, source_index, target_index)
        if full_route is not None:
            full_path = []
            for station in full_route:
                full_path.append(routes.CODE_STATIONS[route[station]])
            return full_path
        return None

    # Returns list of changes (indices of stations on path)
    # If there is no way to get to target, returns None
    def get_changes(self, route, source_index, target_index):
        full_route = [source_index]
        where = source_index
        tarif = 'REGULAR'  # TODO let user choose tarif. [UPDATE -> is it really necessary?]
        driver = webdriver.Firefox()  # TODO let user choose browser
        search_counter = 1
        partial_arrival = None
        while where != target_index:
            for partial_target in range(where + 1, target_index + 1):
                url = self.build_url(
                    source=route[where], target=route[partial_target], tarif=tarif, search_counter=search_counter
                )
                search_counter += 1
                driver.get(url)
                time.sleep(1)
                results = driver.execute_script("return document.documentElement.innerHTML")
                soup = BeautifulSoup(results, 'html.parser')
                found = False

                # full = results.find('full')
                # free = results.find('free')
                # if full == -1 or free < full:
                #     for _ in soup.find_all('div', {'class': 'free'}):
                #         found = True
                #         break

                for train in soup.find_all('div', {'class': 'free'}):
                    departure = train.find('div', {'class': 'col_depart'}).string
                    if dater.earlier(last_arrival, departure):
                        waiting_time = dater.difference(last_arrival, departure)
                        if waiting_time <= self.max_waiting_time:
                            found = True
                            partial_arrival = train.find('div', {'class': 'col_arival'}).string

                if not found:
                    if where == partial_target - 1:
                        return None
                    else:
                        full_route.append(partial_target - 1)
                        where = partial_target - 1
                elif partial_target == target_index:
                    where = target_index
                    break
        full_route.append(target_index)
        driver.close()
        return full_route

    def build_url(self, source, target, tarif, search_counter):
        url = 'https://cestovnelistky.regiojet.sk/Booking/from/' + str(source) + \
              '/to/' + str(target) + '/tarif/' + tarif + \
              '/departure/' + self.date + '/retdep/' + self.date + \
              '/return/false?' + str(search_counter) + '#search-results'
        return url
