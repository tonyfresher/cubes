import json
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from model import GameState, CubeColor


CUBE_SIZE = 30
FONT = QtGui.QFont('Roboto', 10)
COLORS = {
    None: '#FFFFFF',
    CubeColor.RED: '#DB4C40',
    CubeColor.YELLOW: '#FFEE75',
    CubeColor.LIME: '#00A878',
    CubeColor.BLUE: '#5B8DC6',
    CubeColor.ORANGE: '#FF783A',
    CubeColor.VIOLET: '#9B3096'
}
SIZES = ['10', '15', '20', '25', '30']
COLOR_COUNTS = ['3', '4', '5', '6']


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.field_size, self.colors, self.sound = self.get_params()
        self._game_state = GameState(self.field_size, self.colors)

        self.bg_music = QtMultimedia.QSound(r'resources/bg_music.wav')
        self.bg_music.setLoops(QtMultimedia.QSound.Infinite)
        if self.sound:
            self.bg_music.play()
        self.init_ui()

    def init_ui(self):
        window = QtWidgets.QWidget()
        self.game_field = GameField(self._game_state, self, parent=window)
        self.score = Score(self._game_state, parent=window)
        self.block_score = BlockScore(self._game_state, parent=window)
        self.cubes_left = CubesLeft(self._game_state, parent=window)
        scores = self.get_scores()[str(self.field_size)][str(self.colors)]
        self.scoreboard = ScoreBoard(scores, parent=window)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.game_field, 0, 0, 4, 1)
        layout.addWidget(self.score, 0, 1)
        layout.addWidget(self.block_score, 1, 1)
        layout.addWidget(self.cubes_left, 2, 1)
        layout.addWidget(self.scoreboard, 3, 1)
        window.setLayout(layout)

        self.setCentralWidget(window)
        self.setWindowTitle('Cubes')
        self.setWindowIcon(QtGui.QIcon(r'resources/cube.png'))

    def get_params(self):
        options_dialog = OptionsWindow(parent=self)
        options_dialog.setModal(True)
        options_dialog.exec_()
        if options_dialog.result() == 0:
            exit()
        else:
            return (int(options_dialog.field_size.currentText()),
                    int(options_dialog.colors.currentText()),
                    options_dialog.music.isChecked())

    def game_over(self):
        self.save_score()
        go_window = GameOver(self._game_state, parent=self)
        go_window.setModal(True)
        go_window.exec_()
        if go_window.result() == 0:
            exit()
        else:
            self._game_state = GameState(self.field_size, self.colors)
            self.init_ui()

    @staticmethod
    def clear_scores():
        records = {size: {color: [0] * 5 for color in range(3, 7)}
                   for size in range(10, 35, 5)}
        with open('resources/scoreboard', 'w') as f:
            json.dump(records, f)

    @staticmethod
    def get_scores():
        with open('resources/scoreboard', 'r', encoding='utf-8') as f:
            scoreboard = json.load(f)
        return scoreboard

    def save_score(self):
        records = self.get_scores()
        with open('resources/scoreboard', 'r+') as f:
            current = records[str(self.field_size)][str(self.colors)]
            l = len(current)
            score = self._game_state.score
            for i in range(l):
                if score >= current[i]:
                    current.insert(i, score)
                    break
            records[str(self.field_size)][str(self.colors)] = current[:l]
            json.dump(records, f)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self, 'Quit', 'Are you sure to quit?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class OptionsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.field_size = QtWidgets.QComboBox()
        self.field_size.addItems(SIZES)
        self.field_size.setCurrentIndex(1)
        self.colors = QtWidgets.QComboBox()
        self.colors.addItems(COLOR_COUNTS)
        self.colors.setCurrentIndex(3)
        self.music = QtWidgets.QRadioButton()
        self.music.setChecked(True)
        ok_button = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        layout2 = QtWidgets.QGridLayout()
        layout2.setSpacing(5)
        layout2.addWidget(QtWidgets.QLabel('Field size: '), 1, 0)
        layout2.addWidget(self.field_size, 1, 1)
        layout2.addWidget(QtWidgets.QLabel('Colors: '), 2, 0)
        layout2.addWidget(self.colors, 2, 1)
        layout2.addWidget(QtWidgets.QLabel('Music: '), 3, 0)
        layout2.addWidget(self.music, 3, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)
        layout.addLayout(layout2)
        layout.addWidget(ok_button)

        ok_button.accepted.connect(self.accept)
        ok_button.rejected.connect(self.reject)

        self.setLayout(layout)
        self.setWindowTitle('Options')
        self.setWindowIcon(QtGui.QIcon(r'resources/cube.png'))
        self.setFixedSize(200, 120)


class GameOver(QtWidgets.QDialog):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)

        text = 'Game Over!\nYou score {}'.format(game_state.score)
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        ok_button = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Retry | QtWidgets.QDialogButtonBox.Cancel)

        layout = QtWidgets.QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label)
        layout.addWidget(ok_button)

        ok_button.accepted.connect(self.accept)
        ok_button.rejected.connect(self.reject)

        self.setLayout(layout)
        self.setWindowTitle(' ')
        self.setWindowIcon(QtGui.QIcon(r'resources/cube.png'))
        self.setFixedSize(140, 80)


class GameField(QtWidgets.QWidget):
    def __init__(self, game_state, main_window, parent=None):
        super().__init__(parent)
        self._game_state = game_state
        self._main_window = main_window
        self._painter = QtGui.QPainter()

        self.setMouseTracking(True)
        self.setFixedSize(self._game_state.field_size * CUBE_SIZE + 1,
                          self._game_state.field_size * CUBE_SIZE + 1)

    def paintEvent(self, event):
        self._painter.begin(self)
        for x in range(self._game_state.field_size):
            for y in range(self._game_state.field_size):
                color = self._game_state.get_color(x, y)
                self._painter.setBrush(QtGui.QColor(COLORS[color]))
                self._painter.drawRect(x * CUBE_SIZE, y * CUBE_SIZE,
                                       CUBE_SIZE, CUBE_SIZE)
        self._painter.end()

    def mousePressEvent(self, event):
        x = event.pos().x() // CUBE_SIZE
        y = event.pos().y() // CUBE_SIZE
        if (x < self._game_state.field_size and
                y < self._game_state.field_size and
                self._game_state.get_color(x, y) and
                self._game_state.count_block_value(x, y) > 0):
            self._game_state.exterminate(x, y)
            self.update()
            self._main_window.score.update()
            self._main_window.cubes_left.update()
        if self._game_state.is_game_over():
            self._main_window.game_over()

    def mouseMoveEvent(self, event):
        x = event.pos().x() // CUBE_SIZE
        y = event.pos().y() // CUBE_SIZE
        if (x < self._game_state.field_size and
                y < self._game_state.field_size):
            score = self._game_state.count_block_value(x, y)
            self._main_window.score.block_score = score
            self._main_window.block_score.block_score = score
            self._main_window.score.update()
            self._main_window.block_score.update()


class Score(QtWidgets.QLabel):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self._game_state = game_state
        self.block_score = 0
        self.setFixedSize(100, 40)
        self._painter = QtGui.QPainter()
        self._pen = QtGui.QPen()
        self._pen.setColor(QtGui.QColor(230, 0, 0))

    def paintEvent(self, event):
        self._painter.begin(self)
        self._painter.setFont(QtGui.QFont('Roboto', 10, QtGui.QFont.Bold))
        self._painter.setPen(self._pen)
        predict = self._game_state.score + self.block_score
        self._painter.drawText(
            self.rect(), QtCore.Qt.AlignLeft,
            ' Score:\n {} -> {}'.format(self._game_state.score,
                                        predict))
        self._painter.end()


class BlockScore(QtWidgets.QLabel):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self._game_state = game_state
        self.block_score = 0
        self.setFixedSize(100, 40)
        self._painter = QtGui.QPainter()

    def paintEvent(self, event):
        self._painter.begin(self)
        self._painter.setFont(FONT)
        self._painter.drawText(self.rect(), QtCore.Qt.AlignLeft,
                               ' Block score:\n %s' % self.block_score)
        self._painter.end()


class CubesLeft(QtWidgets.QLabel):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self._game_state = game_state
        self.setFixedSize(100, 115)
        self._painter = QtGui.QPainter()

    def paintEvent(self, event):
        self._painter.begin(self)
        self._painter.setFont(FONT)
        text = ''
        items = list(self._game_state.count_cubes().items())
        for i in range(len(items)):
            if items[i][0] is not None:
                text += ' {}: {}\n'.format(str(items[i][0])[10:], items[i][1])
        self._painter.drawText(self.rect(), QtCore.Qt.AlignLeft,
                               ' Cubes left:\n%s' % text)
        self._painter.end()


class ScoreBoard(QtWidgets.QLabel):
    def __init__(self, scores, parent=None):
        super().__init__(parent)
        self.setFixedWidth(100)
        text = ' Records:'
        for score in scores:
            text += '\n %s' % score
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setFont(FONT)
        self.setText(text)
