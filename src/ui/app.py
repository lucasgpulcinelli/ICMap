from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QSizePolicy, QStackedLayout, QWidget, QVBoxLayout

from ui.fromtosearch import FromToSearch
from ui.pathshower import PathShower

import maze_solver


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
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.algorithms = QComboBox()
        self.algorithms.addItem("Resolver usando BFS")
        self.algorithms.addItem("Resolver Usando A*")

        self.stacked_layout.addWidget(self.search)
        execute_layout.addWidget(self.button)
        execute_layout.addWidget(self.algorithms)

        layout.addLayout(self.stacked_layout)
        layout.addLayout(execute_layout)

        self.setLayout(layout)
        self.stacked_layout.setCurrentIndex(1)

    def buttonToggle(self):
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            self.button.setText("Gerar Caminho")
            return

        path = self.genPath()
        if path is None:
            return

        self.button.setText("Fazer um Novo Trajeto")

        try:
            self.stacked_layout.removeWidget(self.path_shower)
        except AttributeError:
            pass

        self.path_shower = PathShower(path)

        self.stacked_layout.addWidget(self.path_shower)
        self.stacked_layout.setCurrentIndex(1)

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
