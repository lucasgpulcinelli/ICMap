import os

from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtCore import QTimer, QUrl, Qt
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QSlider, QWidget, QVBoxLayout


class PathShower(QWidget):
    '''
    class PathShower creates and shows an interactive video based on a maze
    solving path.
    '''

    def __init__(self, path):
        super().__init__()

        self.video = QVideoWidget()

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setMedia(QMediaContent(
            QUrl.fromLocalFile(os.path.join(os.getcwd(), "res", "path.webm"))))

        self.player.setVideoOutput(self.video)

        self.playpausebt = QPushButton("Pause")
        self.playpausebt.clicked.connect(self.playpause)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.sliderUpdate)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderPressed.connect(self.sliderPressed)
        self.slider.sliderReleased.connect(self.sliderReleased)

        l = QVBoxLayout()
        l.addWidget(self.video)

        hb = QHBoxLayout()
        hb.addWidget(self.playpausebt)
        hb.addWidget(self.slider)

        l.addLayout(hb)

        self.setLayout(l)

        self.timer.start()
        self.player.play()

    def playpause(self):
        '''
        playpause toggles the video playback based on its current state.
        '''

        action_pause = self.player.state() == self.player.PlayingState
        self.playpausebt.setText("Play" if action_pause else "Pause")

        if action_pause:
            self.player.pause()
        else:
            self.player.play()

    def sliderUpdate(self):
        '''
        sliderUpdate runs every second to update the slider position to match 
        video playback.
        '''

        if self.player.state() != self.player.PlayingState:
            return

        if self.player.duration() == 0:
            return

        self.slider.setSliderPosition(
            int(self.player.position()/self.player.duration()*100))

    def sliderPressed(self):
        '''
        sliderPressed pauses the video and stops the slider timed updates 
        while the user is dragging the slider to a new position.
        '''

        self.unpauseAfter = self.player.state() == self.player.PlayingState
        self.player.pause()
        self.timer.stop()

    def sliderReleased(self):
        '''
        sliderReleased is the counterpart to sliderPressed, restaring playback
        at the new slider position and the slider timed updates after the user 
        stops dragging the slider.
        '''

        self.player.setPosition(
            int(self.slider.sliderPosition()/100*self.player.duration()))

        if self.unpauseAfter:
            self.player.play()
        self.timer.start()
