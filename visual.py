from PyQt4 import QtGui

import routes


class Visualiser(QtGui.QMainWindow):

    def __init__(self):
        super(Visualiser, self).__init__()
        self.setGeometry(200, 200, 700, 250)
        self.setWindowTitle('RegioChange')

        self.combo_train_number = QtGui.QComboBox(self)
        self.combo_source = QtGui.QComboBox(self)
        self.combo_target = QtGui.QComboBox(self)
        self.date = QtGui.QDateTimeEdit(self)
        self.btn_search = QtGui.QPushButton(self)
        self.label_result = QtGui.QLabel(self)

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
        self.label_date = QtGui.QLabel(self)
        self.label_date.move(10, 130)
        self.label_date.setFixedWidth(250)
        self.label_date.setText('Dátum a čas odchodu:')

        self.btn_search.move(10, 170)
        self.btn_search.setText('OK')

        self.label_result.move(10, 210)
        self.label_result.setFixedWidth(690)

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
        ans = ''
        if route is None:
            ans = 'Us sa neda najst nic mrzi ma to :('
        else:
            for idx, station in enumerate(route):
                ans += station
                if idx < len(route) - 1:
                    ans += '  -->  '
        self.label_result.setText(ans)
