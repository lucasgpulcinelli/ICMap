from PyQt5.QtWidgets import QHBoxLayout, QWidget

from ui.roomsearch import RoomSearch


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
