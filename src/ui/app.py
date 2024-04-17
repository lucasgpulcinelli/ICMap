from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QSizePolicy, QStackedLayout, QWidget, QVBoxLayout

from ui.fromtosearch import FromToSearch
from ui.pathshower import PathShower

import maze_solver


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
        self.stacked_layout = QStackedLayout()
        execute_layout = QHBoxLayout()

        # the search bars to the rooms
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
        '''
        buttonToggle either generates the path from a room to another and shows
        it to the user or goes back to the room selection screen, depending on 
        the state of the application.
        '''

        # if we are in the path view area, switch back to room selection
        if self.stacked_layout.currentIndex() != 0:
            self.stacked_layout.setCurrentIndex(0)
            self.button.setText("Gerar Caminho")
            return

        # if we are in the room selection area, create the path to the rooms
        # provided, if the user has given both rooms.

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
        else:
            solver = maze_solver.solveAStar

        return solver(self.tensor, source, dest)
