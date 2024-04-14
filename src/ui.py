from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QSizePolicy, QStackedLayout, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QListView

import maze_solver


class RoomSearch(QWidget):
    def __init__(self, options, search_placeholder):
        super().__init__()
        self.options = options

        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText(search_placeholder)

        self.options_list = QListView(self)
        self.model = QStandardItemModel()
        self.options_list.setModel(self.model)

        layout.addWidget(self.search_input)
        layout.addWidget(self.options_list)

        self.setLayout(layout)

        self.search_input.textChanged.connect(self.filterOptions)
        self.search_input.returnPressed.connect(self.selectFirst)

        self.updateOptions(self.options)

    def updateOptions(self, options):
        self.model.clear()
        for option in options:
            item = QStandardItem(option)
            self.model.appendRow(item)

    def filterOptions(self, text):
        filtered_options = [
            option for option in self.options if text.lower() in option.lower()]
        self.updateOptions(filtered_options)

    def selectFirst(self):
        if self.search_input.text() == "":
            return None

        item = self.model.item(0, 0)
        if item is None:
            self.search_input.setText("")
            return None
        t = item.text()
        self.search_input.setText(t)
        return t


class FromToSearch(QWidget):
    def __init__(self, rooms):
        super().__init__()
        self.rooms = rooms

        layout = QHBoxLayout()

        self.room_from = RoomSearch(rooms.keys(), "onde você está")
        self.room_to = RoomSearch(rooms.keys(), "para onde você vai")

        layout.addWidget(self.room_from)
        layout.addWidget(self.room_to)

        self.setLayout(layout)


class App(QWidget):
    def __init__(self, tensor, rooms):
        super().__init__()

        self.tensor = tensor
        self.rooms = rooms

        layout = QVBoxLayout()
        self.stacked_layout = QStackedLayout()
        execute_layout = QHBoxLayout()

        self.search = FromToSearch(rooms)

        self.button = QPushButton("Gerar Caminho")
        self.button.clicked.connect(self.buttonToggle)
        self.button.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.algorithms = QComboBox()
        self.algorithms.addItem("Resolver usando BFS")
        self.algorithms.addItem("Resolver Usando A*")

        self.image_label = QLabel()

        self.stacked_layout.addWidget(self.search)
        self.stacked_layout.addWidget(self.image_label)
        execute_layout.addWidget(self.button)
        execute_layout.addWidget(self.algorithms)

        layout.addLayout(self.stacked_layout)
        layout.addLayout(execute_layout)

        self.setLayout(layout)

    def buttonToggle(self):
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            self.button.setText("Gerar Caminho")
            return

        path = self.genPath()
        if path is None:
            return

        img = QPixmap('res/map/0.png')

        self.image_label.setPixmap(img.scaledToHeight(750))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setWordWrap

        self.stacked_layout.setCurrentIndex(1)
        self.button.setText("Fazer um Novo Trajeto")

    def genPath(self):
        text_from = self.search.room_from.selectFirst()
        text_to = self.search.room_to.selectFirst()

        if text_from is None or text_to is None:
            return None

        source = self.rooms[text_from]
        dest = self.rooms[text_to]

        if self.algorithms.currentIndex() == 0:
            solver = maze_solver.solveBFS
        else:
            solver = maze_solver.solveAStar

        return solver(self.tensor, source, dest)
