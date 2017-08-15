import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

import routes
from dates import Dates


class PathFinder:

    def find_path(self, source, target, date):
        source_id = routes.STATION_CODES[source]
        target_id = routes.STATION_CODES[target]
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
        full_route = self.get_changes(route, source_index, target_index, date)
        if full_route is None:
            return None
        full_path = []
        for station in full_route:
            full_path.append(routes.CODE_STATIONS[route[station]])
        return full_path

    # Returns list of changes (indices of stations on path)
    # If there is no way to get to target, returns None
    @staticmethod
    def get_changes(route, source_index, target_index, date):
        full_route = [source_index]
        dater = Dates()
        next_day = dater.add_one_day(date, readable=True)
        where = source_index
        tarif = 'REGULAR'  # TODO let user choose tarif
        driver = webdriver.Firefox()  # TODO let user choose browser
        search_counter = 1
        while where != target_index:
            for partial_target in range(where + 1, target_index + 1):
                url = 'https://cestovnelistky.regiojet.sk/Booking/from/' + str(route[where]) +\
                      '/to/' + str(route[partial_target]) +'/tarif/' + tarif +\
                      '/departure/' + date + '/retdep/' + date + '/return/false?' + str(search_counter) + '#search-results'
                search_counter += 1
                driver.get(url)
                time.sleep(2)
                results = driver.execute_script("return document.documentElement.innerHTML")
                end_of_interesting = results.find(next_day)
                results[end_of_interesting:].replace('free', 'full')
                soup = BeautifulSoup(results, 'html.parser')
                found = False
                full = results.find('full')
                free = results.find('free')
                if full == -1 or free < full:
                    for _ in soup.find_all('div', {'class': 'free'}):
                        found = True
                        break
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
