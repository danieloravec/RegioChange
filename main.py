import sys
from PyQt4 import QtGui

from path_finder import PathFinder
from visual import Visualiser


def get_route(train_number, source, target, date):
    finder = PathFinder(train_number, source, target, date)
    found_route = finder.find_path()
    visualiser.print_route(found_route)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    visualiser = Visualiser()
    visualiser.btn_search.clicked.connect(
        lambda: get_route(
            visualiser.combo_train_number.currentText(),
            visualiser.combo_source.currentText(),
            visualiser.combo_target.currentText(),
            visualiser.get_datetime()
        )
    )

    sys.exit(app.exec_())
