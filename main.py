from path_finder import PathFinder


if __name__ == '__main__':
    source = 'Praha, hl.n.'  # input('Zaciatocna stanica: ')
    target = 'Košice, žel. st.'  # input('Konecna stanica: ')
    date = '18/08/2017'  # input('Dátum (dd/mm/rrrr): ')
    date = date[6:10] + date[3:5] + date[0:2]  # yyyymmdd
    finder = PathFinder()
    found_route = finder.find_path(source, target, date)
    if found_route is None:
        print('Mozes plakat')
    else:
        first = True
        for station in found_route:
            if not first:
                print(' -> ')
            first = False
            print(station)
