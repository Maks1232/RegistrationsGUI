from __future__ import annotations

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from .Constants import (
    APP_LOGO_IMAGE_PATH,
    REG_TEMPLATE_IMAGE_PATH,
    VOIVODESHIPS_ALL,
    Level,
    Voivodeship,
)
from .Game import Game
from .UI.MainWindow import Ui_MainWindow
from .Utils import get_resource_path


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup_images()
        self.setup_actions()
        self.setup_game_options()
        self.setup_regplate()

    def setup_game_options(self):
        # Voivodeships combobox
        self.comboBox.removeItem(0)
        for voivodeship_name in [
            *[voivodeship.value for voivodeship in Voivodeship],
            VOIVODESHIPS_ALL,
        ]:
            self.comboBox.addItem(voivodeship_name)
        # Difficulty combobox
        self.comboBox_2.removeItem(0)
        for difficulty_name in [level.value for level in Level]:
            self.comboBox_2.addItem(difficulty_name)

    def setup_actions(self):
        # Start game
        self.pushButton_6.clicked.connect(self.start_game)
        # Exit game
        self.pushButton_5.clicked.connect(self.exit_game_if_confirmed)
        # Answer buttons
        self.pushButton.clicked.connect(self.answered_1)
        self.pushButton_2.clicked.connect(self.answered_2)
        self.pushButton_3.clicked.connect(self.answered_3)
        self.pushButton_4.clicked.connect(self.answered_4)

    def setup_regplate(self):
        self.label_plate = QtWidgets.QLabel(self.page)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(48)
        font.setWeight(50)
        self.label_plate.setFont(font)
        self.label_plate.setText("XYZ")
        self.label_plate.setScaledContents(False)
        self.label_plate.setAlignment(QtCore.Qt.AlignCenter)
        self.label_plate.setObjectName("label")
        self.label.setRelatedLabel(self.label_plate)

    def setup_images(self):
        self.label.setPixmap(QtGui.QPixmap(get_resource_path(REG_TEMPLATE_IMAGE_PATH)))
        self.label_5.setPixmap(QtGui.QPixmap(get_resource_path(APP_LOGO_IMAGE_PATH)))

    def update_game_ui(self):
        if not self.game.isRunning:
            self.exit_game()
        else:
            self.label_plate.setText(self.game.current_question[0])
            self.pushButton.setText(self.game.current_question[2][0])
            self.pushButton_2.setText(self.game.current_question[2][1])
            self.pushButton_3.setText(self.game.current_question[2][2])
            self.pushButton_4.setText(self.game.current_question[2][3])
            self.label_9.setText(str(self.game.questions_left_count))
            self.label_4.setText(str(self.game.get_score_text()))
            self.label_8.setVisible(not self.game.repeating_mode)
            self.label_9.setVisible(not self.game.repeating_mode)

    def exit_game_if_confirmed(self):
        # End game button action
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Potwierdzenie")
        dlg.setText("Czy napewno chcesz wyjść?")
        dlg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        dlg.setIcon(QMessageBox.Warning)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            self.exit_game()

    def exit_game(self):
        self.stackedWidget.setCurrentIndex(1)
        # Delete game object
        del self.game

    def start_game(self):
        try:
            self.game = Game(
                level=Level(self.comboBox_2.currentText()),
                voivodeship=(
                    VOIVODESHIPS_ALL
                    if self.comboBox.currentText() == VOIVODESHIPS_ALL
                    else Voivodeship(self.comboBox.currentText())
                ),
                repeating=self.checkBox.isChecked(),
            )
        except ValueError as e:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Błędna konfiguracja")
            dlg.setText(str(e))
            dlg.exec()
            return
        self.stackedWidget.setCurrentIndex(0)
        self.update_game_ui()

    def answered_1(self):
        self.game.register_answer(0)
        self.update_game_ui()

    def answered_2(self):
        self.game.register_answer(1)
        self.update_game_ui()

    def answered_3(self):
        self.game.register_answer(2)
        self.update_game_ui()

    def answered_4(self):
        self.game.register_answer(3)
        self.update_game_ui()
