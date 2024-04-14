from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QLineEdit, QListView

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


class App(QWidget):
    def __init__(self, tensor, rooms):
        super().__init__()
        self.rooms = rooms
        self.tensor = tensor

        layout = QVBoxLayout()
        sub_layout = QHBoxLayout()

        self.room_from = RoomSearch(rooms.keys(), "onde você está")
        self.room_to = RoomSearch(rooms.keys(), "para onde você vai")

        sub_layout.addWidget(self.room_from)
        sub_layout.addWidget(self.room_to)

        layout.addLayout(sub_layout)

        self.button = QPushButton("Encontrar Caminho")
        self.button.clicked.connect(self.genPath)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def genPath(self):
        text_from = self.room_from.selectFirst()
        text_to = self.room_to.selectFirst()

        if text_from is None or text_to is None:
            return

        source = self.rooms[text_from]
        dest = self.rooms[text_to]

        print(maze_solver.solveBFS(self.tensor, source, dest))
