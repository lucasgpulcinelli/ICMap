import os

from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout


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
