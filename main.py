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
    source = input('Zaciatocna stanica: ')
    target =  input('Konecna stanica: ')
    date = input('Dátum (dd/mm/rrrr): ')
    departure_time = input('Čas (hh:mm)')
    finder = PathFinder(source, target, date, departure_time)
    found_route = finder.find_path()
    print_result(found_route)
