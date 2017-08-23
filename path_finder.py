from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time

import routes


class PathFinder:

    def __init__(self, _route_key, _source, _target, _date):
        self.route_key = _route_key
        self.source = _source
        self.target = _target
        self.date = _date
        self.last_arrival = _date

    def find_path(self):
        source_id = routes.STATION_CODES[self.source]
        target_id = routes.STATION_CODES[self.target]
        source_index = None
        target_index = None
        route = routes.ALL_ROUTES[routes.ROUTES_DICT[self.route_key]]
        for index, station in enumerate(route):
            if station == source_id:
                source_index = index
            elif station == target_id:
                target_index = index
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
        arrival_to = [datetime.datetime.now() - datetime.timedelta(days=365) for _ in range(len(route))]
        arrival_to[source_index] = self.date
        driver = self.get_browser()
        search_counter = 1
        in_next_day = date_incremented = False
        arrival = None
        while where != target_index:
            pass
            for partial_target in range(where + 1, target_index + 1):
                url = self.build_url(route[where], route[partial_target], search_counter)
                search_counter += 1
                driver.get(url)
                html = driver.execute_script('return document.documentElement.innerHTML')
                soup = BeautifulSoup(html, 'html.parser')
                found = False
                prev_train_departure = None
                for train in soup.find_all('div', {'class': ['free', 'full']}):
                    departure = [int(t) for t in train.find('div', {'class': 'col_depart'}).string.split(':')]
                    # Are we crossing to next day?
                    if prev_train_departure is not None and \
                        (prev_train_departure[0] > departure[0] or
                         (prev_train_departure[0] == departure[0] and prev_train_departure[1] >= departure[1])):
                        if in_next_day:
                            found = False
                            break
                        else:
                            in_next_day = True
                    prev_train_departure = departure
                    departure = datetime.datetime(
                        self.date.year, self.date.month, self.date.day, departure[0], departure[1], 0
                    )
                    if in_next_day and not date_incremented:
                        departure += datetime.timedelta(days=1)
                    time_diff = self.minutes(departure - arrival_to[where])
                    # I assume that train can stay for 0 minutes. Is it risky?
                    if self.is_train(train) and 'free' in train['class'] and arrival_to[where] <= departure and \
                            0 <= time_diff <= routes.MAX_STATION_TIME:
                        found = True
                        arrival = [int(t) for t in train.find('div', {'class': 'col_arival'}).string.split(':')]
                        break
                    elif arrival_to[where] <= departure and time_diff > routes.MAX_STATION_TIME:
                        break

                if not found:
                    if where == partial_target - 1:
                        driver.close()
                        return None
                    else:
                        where = partial_target - 1
                        full_route.append(partial_target - 1)
                        if in_next_day:
                            self.date += datetime.timedelta(days=1)
                            date_incremented = True
                        self.date = datetime.datetime(
                            self.date.year, self.date.month, self.date.day, arrival[0], arrival[1], 0
                        )
                        arrival_to[partial_target - 1] = self.date  # TODO do we need arrival_to and not only self.date?
                        break
                elif partial_target == target_index:
                    where = target_index
                    break
        full_route.append(target_index)
        driver.close()
        return full_route

    def build_url(self, source, target, search_counter):
        url = 'https://cestovnelistky.regiojet.sk/Booking/from/' + str(source) +\
              '/to/' + str(target) + '/tarif/REGULAR/departure/' +\
              self.regio_date() + '/retdep/' + self.regio_date() +\
              '/return/false?' + str(search_counter) + '#search-results'
        return url

    def regio_date(self):
        date = str(self.date.year)
        if self.date.month < 10:
            date += '0'
        date += str(self.date.month)
        if self.date.day < 10:
            date += '0'
        date += str(self.date.day)
        return date

    @staticmethod
    def minutes(difference):
        return difference.days * 3600 if difference.days > 0 else 0 + (difference.seconds + 59) // 60

    @staticmethod
    def is_train(train):
        vehicle_div = train.find('div', {'class': 'col_icon'})
        vehicle_img = vehicle_div.find('img')
        return vehicle_img['title'] == 'Vlak'

    @staticmethod
    def get_browser():
        try:
            browser = webdriver.PhantomJS()
        except:
            try:
                browser = webdriver.Firefox()
            except:
                try:
                    browser = webdriver.Chrome()
                except:
                    try:
                        browser = webdriver.Safari()
                    except:
                        try:
                            browser = webdriver.Opera()
                        except:
                            raise FileNotFoundError(
                                'Browser not found. Do you have Firefox, Chrome, Safari, Opera or PhantomJS installed'
                                'and is at least one of them in PATH variable?'
                            )
        return browser

