import os

from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtCore import QTimer, QUrl, Qt
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QSlider, QWidget, QVBoxLayout

import video


class PathShower(QWidget):
    '''
    class PathShower creates and shows an interactive video based on a maze
    solving path.
    '''

    def __init__(self, solution):
        super().__init__()

        video.generate_video(solution)

        self.video = QVideoWidget()

        self.media = QMediaContent(
            QUrl.fromLocalFile(os.path.join(os.getcwd(), "res", "path.avi")))

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setMedia(self.media)
        self.player.setVideoOutput(self.video)

        self.playpausebt = QPushButton("Pause")
        self.playpausebt.clicked.connect(self.playpause)

        self.sliderTimer = QTimer(self)
        self.sliderTimer.setInterval(1000)
        self.sliderTimer.timeout.connect(self.sliderUpdate)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderPressed.connect(self.sliderPressed)
        self.slider.sliderReleased.connect(self.sliderReleased)

        self.pauseTimer = QTimer()
        self.pauseTimer.timeout.connect(self.pauseOnEnd)

        l = QVBoxLayout()
        l.addWidget(self.video)

        buttonback = QPushButton("back one frame")
        buttonback.clicked.connect(self.backframe)

        buttonfwd = QPushButton("forward one frame")
        buttonfwd.clicked.connect(self.fwdframe)

        hb = QHBoxLayout()
        hb.addWidget(self.playpausebt)
        hb.addWidget(self.slider)
        hb.addWidget(buttonback)
        hb.addWidget(buttonfwd)

        l.addLayout(hb)

        self.setLayout(l)

        self.pauseTimer.start()
        self.sliderTimer.start()
        self.player.play()

    def backframe(self):
        self.player.pause()
        self.player.setPosition(self.player.position()-1000//20)

    def fwdframe(self):
        self.player.pause()
        self.player.setPosition(self.player.position()+1000//20)

    def playpause(self):
        '''
        playpause toggles the video playback based on its current state.
        If the video is near its end, also restarts it from the beginning.
        '''

        action_pause = self.player.state() == self.player.PlayingState
        self.playpausebt.setText("Play" if action_pause else "Pause")

        if self.player.position() >= self.player.duration() - 60:
            self.player.setPosition(0)
            self.slider.setSliderPosition(0)

        if action_pause:
            self.player.pause()
        else:
            self.player.play()

    def pauseOnEnd(self):
        '''
        pauseOnEnd runs on a timer to pause the video on its last few frames.
        '''

        if self.player.duration() == 0:
            return

        if self.player.position() < self.player.duration() - 50:
            return

        self.player.pause()
        self.playpausebt.setText("Play")

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
        self.sliderTimer.stop()

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
        self.sliderTimer.start()
