#!/usr/bin/env python3

import sys
import json
import typing

from PyQt5.QtWidgets import QApplication

from ui.app import App
import image_reader


def loadRoomsFile(
        filename: str) -> typing.Dict[str, typing.Tuple[int, int, int]]:
    '''
    loadRoomsFile reads a file and returns a dictionary containing room 
    numbers and description as key and the rooms coordinates as values.
    '''

    rooms_file = open(filename)
    rooms = json.load(rooms_file)
    rooms_file.close()

    # transform the room coordinate array to a tuple because json does not
    # have tuples
    for k in rooms:
        rooms[k] = tuple(rooms[k])

    return rooms


def main():
    app = QApplication(sys.argv)

    rooms = loadRoomsFile("res/rooms.json")
    tensor = image_reader.dirToWalkTensor("res/map")

    widget = App(tensor, rooms)
    widget.setWindowTitle("Mapa do Maroto do ICMC")
    widget.resize(1024, 684)
    widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
