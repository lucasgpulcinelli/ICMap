import os

from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QWidget, QVBoxLayout


class PathShower(QWidget):
    '''
    class PathShower creates and shows an interactive video based on a maze
    solving path.
    '''

    def __init__(self, path):
        super().__init__()

        self.w = QVideoWidget()

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setMedia(QMediaContent(
            QUrl.fromLocalFile(os.path.join(os.getcwd(), "res", "path.webm"))))

        self.player.setVideoOutput(self.w)

        l = QVBoxLayout()
        l.addWidget(self.w)
        self.setLayout(l)
        self.player.play()
