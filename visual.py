from PyQt4 import QtGui, QtCore

import routes
import signals


class Visualiser(QtGui.QMainWindow):

    def __init__(self):
        super(Visualiser, self).__init__()
        self.x_coord = 200
        self.y_coord = 200
        self.window_width = 470
        self.window_height = 210
        self.setGeometry(self.x_coord, self.y_coord, self.window_width, self.window_height)
        self.setWindowTitle('RegioChange')

        self.combo_train_number = QtGui.QComboBox(self)
        self.combo_source = QtGui.QComboBox(self)
        self.combo_target = QtGui.QComboBox(self)
        self.date = QtGui.QDateTimeEdit(self)
        self.btn_search = QtGui.QPushButton(self)

        self.combo_train_number.move(200, 10)
        self.label_train_number = QtGui.QLabel(self)
        self.label_train_number.move(10, 10)
        self.label_train_number.setFixedWidth(250)
        self.label_train_number.setText('Číslo vlaku:')

        self.combo_source.move(200, 50)
        self.combo_source.setFixedWidth(250)
        self.label_source = QtGui.QLabel(self)
        self.label_source.move(10, 50)
        self.label_source.setFixedWidth(250)
        self.label_source.setText('Začiatočná stanica:')

        self.combo_target.move(200, 90)
        self.combo_target.setFixedWidth(250)
        self.label_target = QtGui.QLabel(self)
        self.label_target.move(10, 90)
        self.label_target.setFixedWidth(250)
        self.label_target.setText('Konečná stanica:')

        self.date.move(200, 130)
        self.date.setFixedWidth(150)
        self.date.setDate(QtCore.QDate.currentDate())
        self.label_date = QtGui.QLabel(self)
        self.label_date.move(10, 130)
        self.label_date.setFixedWidth(250)
        self.label_date.setText('Dátum a čas odchodu:')

        self.btn_search.move(10, 170)
        self.btn_search.setText('Hľadať')

        self.select_train()
        self.show()

    def select_train(self):
        all_trains = ['', '1003', '1008', '1011', '1012', '1020', '1021']
        self.combo_train_number.addItems(all_trains)
        self.combo_train_number.activated.connect(self.fill_stations)

    def get_train_number(self):
        return str(self.combo_train_number.currentText())

    def fill_stations(self):
        tn = self.get_train_number()
        if tn not in routes.ROUTES_DICT.keys():
            return
        route_key = routes.ROUTES_DICT[self.get_train_number()]
        station_codes = routes.ALL_ROUTES[route_key]
        stations = []
        for code in station_codes:
            stations.append(routes.CODE_STATIONS[code])
        self.combo_source.clear()
        self.combo_target.clear()
        self.combo_source.addItems(stations)
        self.combo_target.addItems(stations)

    def get_datetime(self):
        return self.date.dateTime().toPyDateTime()

    def print_route(self, route):
        err_message = None
        if route is signals.TRAIN_NOT_FOUND:
            err_message = 'Neviem nájsť zvolený vlak'
        elif route is signals.IMPOSSIBLE_ROUTE:
            err_message = 'Týmto vlakom nie je možné cestovať medzi zvolenými stanicami'
        elif route is signals.BROWSER_NOT_FOUND:
            err_message = 'Nenašiel som webový prehliadač. Ak máš nainštalovaný jeden z prehliadačov Firefox, ' \
                           'Chrome, Safari, Opera, alebo PhantomJS, uisti sa, že sú v systémovej premennej PATH'
        elif route is signals.WRONG_DIRECTION:
            err_message = 'Tento vlak medzi zvolenými stanicami premáva v opačnom smere'
        elif route is signals.DATE_IN_PAST:
            err_message = 'Tento vlak si už išiel'
        elif route is signals.BROWSER_CLOSED_UNEXPECTEDLY:
            err_message = 'Prehliadač sa nečakane zatvoril'

        if err_message is None:
            if route is None:
                QtGui.QMessageBox.critical(self, 'Výsledok', 'Skús to neskôr', QtGui.QMessageBox.Ok)
            else:
                ans = ''
                for idx, station in enumerate(route):
                    ans += str(idx + 1) + ') ' + station + '\n'
                QtGui.QMessageBox.information(self, 'Výsledok', ans, QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.critical(self, 'Chyba', err_message, QtGui.QMessageBox.Ok)

