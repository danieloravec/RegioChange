from path_finder import PathFinder


def print_result(route):
    print('\nVýsledok:\n')
    if route is None:
        print('Môžeš plakať')
    else:
        print('Niečo som našiel: \n')
        first = True
        for station in route:
            if not first:
                print(' -> ')
            first = False
            print(station)

if __name__ == '__main__':
    print('Informácie o linke')
    route_source = 'Košice, žel. st.'  # input('Linka začína v stanici: ')
    route_target = 'Praha, hl.n.'  # input('Linka končí v stanici: ')
    source = 'Ružomberok, žel. st.'  # input('Ty ideš zo stanice: ')
    target = 'Praha, hl.n.'  # input('Do stanice: ')
    date = '17/08/2017'  # input('Dátum (dd/mm/rrrr): ')
    departure_time = '23:45'  # input('Čas (hh:mm): ')
    print('\n------- Idem cestovať... -------\n')
    finder = PathFinder(route_source + ' ' + route_target, source, target, date, departure_time)
    found_route = finder.find_path()
    print_result(found_route)
