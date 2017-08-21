from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time

import routes


class PathFinder:

    def __init__(self, _route_key, _source, _target, _date, _departure_time):
        self.route_key = _route_key
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
        self.last_arrival = None

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
        driver = self.get_browser()
        #driver.set_window_size('10', '10')
        search_counter = 1
        in_next_day = False  # To know, if we can go to next day, or we are already there and can't go further

        while where != target_index:
            for partial_target in range(where + 1, target_index + 1):
                url = self.build_url(
                    source=route[where], target=route[partial_target], search_counter=search_counter
                )
                search_counter += 1  # URL needs to have this in it
                driver.get(url)
                time.sleep(2)  # We can't send requests too often
                results = driver.execute_script("return document.documentElement.innerHTML")  # Dynamic HTML (from JS)
                soup = BeautifulSoup(results, 'html.parser')
                found = False
                next_day = False  # There is a chance of crossing to next day while we are in train
                prev_train_departure = None  # [hours, minutes]
                current_date = self.date

                for train in soup.find_all('div', {'class': ['free', 'full']}):
                    departure = train.find('div', {'class': 'col_depart'}).string
                    train_departure = [int(t) for t in departure.split(':')]
                    # Crossing to next day, or just earlier train that day?
                    if(prev_train_departure is not None) and (train_departure[0] < prev_train_departure[0] or
                            (train_departure[0] == prev_train_departure[0] and
                             train_departure[1] < prev_train_departure[1])):
                        if next_day:
                            if in_next_day:  # We are already in next day, can't go further
                                break
                            current_date += datetime.timedelta(days=1)
                            current_date = datetime.datetime(
                                current_date.year,
                                current_date.month,
                                current_date.day,
                                train_departure[0],
                                train_departure[1],
                                0
                            )
                            in_next_day = True
                        else:
                            next_day = True
                    prev_train_departure = train_departure

                    departure = datetime.datetime(
                        current_date.year,
                        current_date.month,
                        current_date.day,
                        train_departure[0],
                        train_departure[1],
                        0
                    )

                    if self.is_train(train) and 'free' in train['class'] and\
                            (self.last_arrival is None and departure >= self.date and
                                     self.minutes(departure - self.date) <= routes.MAX_STATION_TIME) or\
                            (self.last_arrival is not None
                                and self.last_arrival <= departure and
                                    self.minutes(departure - self.last_arrival) <= routes.MAX_STATION_TIME):
                        found = True
                        arrival = train.find('div', {'class': 'col_arival'}).string
                        arrival = [int(t) for t in arrival.split(':')]
                        break

                if not found:
                    if where == partial_target - 1:
                        return None
                    else:
                        full_route.append(partial_target - 1)
                        where = partial_target - 1
                        self.date = current_date
                        self.last_arrival = datetime.datetime(
                            current_date.year, current_date.month, current_date.day, arrival[0], arrival[1], 0
                        )
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
              self.regio_date() + '/retdep/' + self.regio_date() + \
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
        vehicle_a = vehicle_div.find('a')
        vehicle_img = vehicle_a.find('img')
        vehicle_title = vehicle_img['title']
        return vehicle_title == 'Vlak'

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
                            raise LookupError(
                                'Browser not found. Do you have Firefox, Chrome, Safari, Opera or PhantomJS installed?'
                            )
        return browser

