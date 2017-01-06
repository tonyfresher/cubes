import sys
from PyQt5.QtWidgets import QApplication
from view import MainWindow


HELP = """Click on the group consists of minimum two cubes
of the same color to exterminate it. Have fun!"""

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in {'-h', '--help', "/?"}:
        exit(HELP)

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
