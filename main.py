import sys
from PyQt5.QtWidgets import QApplication
from view import MainWindow


HELP = """Правила:
Кликни по группе, состоящей из минимум двух кубиков
одинакового цвета, чтобы они исчезли. Чем больше группа,
тем больше очков."""

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in {'-h', '--help', "/?"}:
        exit(HELP)

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
