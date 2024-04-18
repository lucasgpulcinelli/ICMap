from PySide2.QtWidgets import QHBoxLayout, QWidget

from ui.roomsearch import RoomSearch


class FromToSearch(QWidget):
    '''
    class FromToSearch defines a widget with two search bars with the same 
    options, one for the user to select a room to go to, and another to select
    the room the user is coming from.
    '''

    def __init__(self, rooms):
        super().__init__()
        self.rooms = rooms

        layout = QHBoxLayout()

        self.room_from = RoomSearch(rooms.keys(), "onde você está")
        self.room_to = RoomSearch(rooms.keys(), "para onde você vai")

        layout.addWidget(self.room_from)
        layout.addWidget(self.room_to)

        self.setLayout(layout)
