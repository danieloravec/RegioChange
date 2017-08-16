from path_finder import PathFinder


def print_result(route):
    if route is None:
        print('Mozes plakat')
    else:
        first = True
        for station in route:
            if not first:
                print(' -> ')
            first = False
            print(station)

if __name__ == '__main__':
    source = 'Praha, hl.n.'  # input('Zaciatocna stanica: ')
    target = 'Košice, žel. st.'  # input('Konecna stanica: ')
    date = '18/08/2017'  # input('Dátum (dd/mm/rrrr): ')
    departure_time = '07:00'  # input('Čas (hh:mm)')
    max_waiting_time = 30 #  input('Prípustná doba čakania (minúty): ')
    finder = PathFinder(source, target, date, departure_time, max_waiting_time)
    found_route = finder.find_path()
    print_result(found_route)
