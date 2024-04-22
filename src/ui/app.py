import time
from PySide2.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QLabel
from PySide2.QtWidgets import QSizePolicy, QStackedLayout, QWidget, QVBoxLayout, QApplication
from PySide2.QtCore import Qt

from ui.fromtosearch import FromToSearch
from ui.pathshower import PathShower

import maze_solver
import utils


class App(QWidget):
    '''
    class App defines the main Qt5 window application.
    It has an interactive interface to generate paths from a room to another 
    with different algorithms and show them to the user.
    '''

    def __init__(self, tensor, rooms):
        super().__init__()

        # tensor is the boolean walk numpy array that shows if a path is
        # walkable or not
        self.tensor = tensor
        self.rooms = rooms

        layout = QVBoxLayout()
        message_layout = QHBoxLayout()
        self.stacked_layout = QStackedLayout()
        execute_layout = QHBoxLayout()

        # the search bars to the rooms
        self.search = FromToSearch(rooms)

        self.message_label = QLabel("RESULTS")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.hide()

        self.button = QPushButton("Gerar Caminho")
        self.button.clicked.connect(self.buttonToggle)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.algorithms = QComboBox()
        self.algorithms_names = ["BFS", "A* Euclidean", "A* Partitioned"]
        for name in self.algorithms_names:
            self.algorithms.addItem(f"Resolver usando {name}")

        message_layout.addWidget(self.message_label)
        self.stacked_layout.addWidget(self.search)
        execute_layout.addWidget(self.button)
        execute_layout.addWidget(self.algorithms)

        layout.addLayout(message_layout)
        layout.addLayout(self.stacked_layout)
        layout.addLayout(execute_layout)

        self.setLayout(layout)

    def message(self, text, color):
        self.message_label.setText(text)
        self.message_label.setStyleSheet(f"color: {color}")
        self.message_label.show()
        QApplication.processEvents()

    def buttonToggle(self):
        '''
        buttonToggle either generates the path from a room to another and shows
        it to the user or goes back to the room selection screen, depending on 
        the state of the application.
        '''

        # if we are in the path view area, switch back to room selection
        self.message_label.hide()
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            self.button.setText("Gerar Caminho")
            return

        # if we are in the room selection area, create the path to the rooms
        # provided, if the user has given both rooms.


        start = time.time()
        solution = self.genPath()
        if solution[0][-1] is None:
            self.message("Não foi possível encontrar um caminho!", "red")
            return
        delta = round((time.time() - start)*100, 2)
        distance = utils.path_cost(solution[0][-1])
        algo = self.algorithms_names[self.algorithms.currentIndex()]

        self.message(f"Caminho encontrado em {delta} ms! Gerando video...", "black")
        self.button.setText("Fazer um Novo Trajeto")

        try:
            self.stacked_layout.removeWidget(self.path_shower)
        except AttributeError:
            pass

        self.path_shower = PathShower(solution) # code freezes here while path shower computes

        self.stacked_layout.addWidget(self.path_shower)
        self.stacked_layout.setCurrentIndex(1)

        self.message(f"{algo}: Passos: {len(solution[0])} | Tempo de execução: {delta} ms | Custo do caminho: {distance}m", "black")

    def genPath(self):
        '''
        genPath gets the inputs from the UI to trigger path generation with 
        the user selected algorithms. It returns the path found as in the 
        maze_solver function definitions.
        '''

        text_from = self.search.room_from.selectFirst()
        text_to = self.search.room_to.selectFirst()

        if text_from is None or text_to is None:
            return None

        source = self.rooms[text_from]
        dest = self.rooms[text_to]

        if self.algorithms.currentIndex() == 0:
            solver = maze_solver.solveBFS
        elif self.algorithms.currentIndex() == 1:
            solver = maze_solver.solveAStarEuclidean
        else:
            solver = maze_solver.solveAStarPartitioned


        return solver(self.tensor, source, dest)
