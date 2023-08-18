import os
import sys
import asyncio
import edge_tts
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui


sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import you


class TextToSpeechGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setFixedSize(700, 700)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.round_corners()

        self.initUI()

    def mousePressEvent(self, event):
        # This function is called when the user presses a mouse button over the window
        if event.button() == Qt.LeftButton:
            # If the left mouse button is pressed, we calculate the difference between the mouse
            # cursor's position and the top-left corner of the window. This is the amount that the
            # window needs to be moved by when the user drags the mouse.
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # This function is called when the user moves the mouse while holding down a mouse button
        if event.buttons() == Qt.LeftButton:
            # If the left mouse button is being held down, we move the window to the new position
            # of the mouse cursor, minus the offset that we calculated in the mousePressEvent function.
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def round_corners(self):
        radius = 25.0
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def initUI(self):
        # Add minimize button
        self.minimize_button = QPushButton("-")
        self.minimize_button.setObjectName("minimizeButton")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setMinimumSize(30, 30)

        # Add close button
        self.close_button = QPushButton("X")
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)
        self.close_button.setMinimumSize(30, 30)

        self.windowTitle = QLabel(
            f'VerboVoice | by Ahmed Kawa')
        self.windowTitle.setAlignment(Qt.AlignCenter)
        self.windowTitle.setObjectName("windowTitle")

        # Initialize text input field
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Enter prompt here")
        self.input_field.setLineWrapMode(QTextEdit.WidgetWidth)

        # Initialize title input field
        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText("Enter title of MP3 file")

        # Initialize output field
        self.output_field = QLabel(
            f'The answer to your question will be ready soon! <img src="icons/soon.png" width="32" height="32">')
        self.output_field.setAlignment(Qt.AlignCenter)

        # Initialize buttons
        self.play_button = QPushButton("Play")
        self.play_button.setObjectName("Play")
        self.pause_button = QPushButton("Pause")
        self.pause_button.setObjectName("Pause")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("Stop")
        self.delete_button = QPushButton('Delete', self)  # Create the delete button
        self.delete_button.setObjectName("Delete")
        self.generate_button = QPushButton("Generate MP3")
        self.generate_button.setObjectName("MP3")
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        # Create widget for button layout
        button_widget = QWidget()
        button_widget.setObjectName("tb1")
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.generate_button)

        # Create widget for minimize, maximize, and close buttons
        btn_widget = QWidget()
        btn_widget.setObjectName("tb1")
        btn_lay = QHBoxLayout(btn_widget)
        btn_lay.addStretch(1)
        btn_lay.addWidget(self.windowTitle)  # add stretch to push buttons to right
        btn_lay.addWidget(self.minimize_button)
        btn_lay.addWidget(self.close_button)
        btn_lay.setSpacing(3)
        btn_lay.setContentsMargins(0, 0, 30, 0)  # move the close and minimize button to the left

        # Add input and output fields, minimize/maximize/close button widget, and button layout widget to main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(btn_widget)
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.title_field)
        main_layout.addWidget(self.output_field)
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

        # Connect signals and slots for buttons
        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.delete_button.clicked.connect(self.delete_audio)  # Connect the delete button to a new method
        self.generate_button.clicked.connect(self.generate)

        # Set stylesheet
        stylesheet = """
                    @import url("https://fonts.googleapis.com/css2?family=Poppins&display=swap");
                    QWidget {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #2F4C40, stop: 1 #335145);
                        color: #335145;
                        text-align: center;
                        font-family: Montserrat;
                        border-radius: 5px;

                    }
                    QWidget#tb1 {
                        background-color: transparent;
                        color: white;
                    }

                    QLabel {
                        background-color: transparent;
                        font-size: 18px;
                        font-weight: bold;
                        text-align: center;
                        color: #a6c36f;
                        margin-left: 10px;
                        margin-top: 30px;
                        margin-right: 10px;
                        margin-bottom: 30px;

                    }

                    QLabel#windowTitle {
                      background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #87AA47, stop: 1 #a6c36f);
                      font-size: 18px;
                      padding: 10px;
                      font-weight: #C993BB;
                      text-align: center;
                      color: #335145;
                      margin-left: 10px;
                      margin-top: 10px;
                      margin-right: 105%;
                      margin-bottom: 10px;
                      border-radius: 20px;
                    }

                    QLineEdit {
                        border-radius: 15px;
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #87AA47, stop: 1 #a6c36f);
                        padding: 15px;
                        font-size: 16px;
                        color: #335145;
                        height: 17px;
                        margin-left: 10px;
                        margin-top: 10px;
                        margin-right: 10px;
                    }

                    QPushButton#Play,
                    QPushButton#Pause,
                    QPushButton#Stop,
			        QPushButton#Delete,
                    QPushButton#MP3 {
                        border-radius: 15px;
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #a6c36f, stop: 1 #87AA47);
                        border: none;
                        color: #335145;
                        font-size: 16px;
                        padding: 8px 16px;
                        margin-left: 10px;
                        margin-bottom: 10px;
                        margin-right: 10px;
                    }

                    QPushButton#Play:hover,
                    QPushButton#Pause:hover,
                    QPushButton#Stop:hover,
			        QPushButton#Delete:hover,
                    QPushButton#MP3:hover {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #87AA47, stop: 1 #a6c36f);
                    }

                    QPushButton#Play:pressed,
                    QPushButton#Pause:pressed,
                    QPushButton#Stop:pressed,
			        QPushButton#Delete:pressed,
                    QPushButton#MP3:pressed {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #ED9A00, stop: 1 #A86D00);
                    }

                    QTextEdit {
                        border-radius: 20px;
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #87AA47, stop: 1 #a6c36f);
                        padding: 15px;
                        font-size: 16px;
                        color: #335145;
                        margin-left: 10px;
                        margin-top: 10px;
                        margin-right: 10px;
                    }

                    QFileDialog {
                        background-color: #a6c36f;
                        color: #335145;
                    }

                    #delete_button {
                        background-color: #beef9e;
                        color: #335145;
                        border-radius: 10px;
                        border: none;
                        font-size: 16px;
                        padding: 8px 16px;
                        margin-right: 10px;
                    }

                    #delete_button:hover {
                        background-color: #828c51;
                        color: #fff;
                    }

                    #output_field {
                        border-radius: 10px;
                        background-color: #a6c36f;
                        padding: 5px;
                        font-size: 16px;
                        color: #335145;
                        text-align: center;
                    }

                    #output_field::hover {
                        background-color: #beef9e;
                    }

                    #output_field::pressed {
                        background-color: #828c51;
                    }

                    QPushButton#minimizeButton,
                    QPushButton#closeButton {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #a6c36f, stop: 1 #87AA47);
                        color: #335145;
                        font-size: 16px;
                        border: none;
                        outline: none;
                        padding: 4px;
                        padding-left: 5px;
                        margin-right: 0px;
                        margin-left: 0px;
                        margin-top: 10px;
                        margin-bottom: 10px;
                        border-radius: 15px;
                        text-align: center;
                    }

                    QPushButton#minimizeButton:hover,
                    QPushButton#closeButton:hover {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #87AA47, stop: 1 #a6c36f);
                    }

                """
        self.setStyleSheet(stylesheet)

        self.show()

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def generate(self):
        # Set cloudflare clearance cookie and get answer from GPT-4 model
        try:
            result = you.Completion.create(prompt=self.input_field.toPlainText())

            response = result['response']

        except Exception as e:
            # Return error message if an exception occurs
            response = f'An error occurred: {e}. Please make sure you are using a valid cloudflare clearance token and user agent.'

        TEXT_FILE = response
        VOICE = "en-GB-SoniaNeural"
        OUTPUT_FILE = os.path.join("audio", self.title_field.text() + ".mp3")

        async def _main() -> None:
            communicate = edge_tts.Communicate(TEXT_FILE, VOICE)
            await communicate.save(OUTPUT_FILE)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_main())
        finally:
            loop.close()

        # Display output file in output field
        self.output_field.setText(f'The response is ready to be played <img src="icons/success.png" width="24" height="24">')

        # Create media player and set media content
        media_content = QMediaContent(QUrl.fromLocalFile(os.path.abspath(OUTPUT_FILE)))
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(media_content)

        # Enable buttons for playback control
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def delete_audio(self):
        filename = self.title_field.text() + ".mp3"
        if os.path.isfile(filename):
            os.remove(filename)
            self.output_field.setText(f'{filename} deleted! <img src="icons/trash.png" width="24" height="24">')
        else:
            self.output_field.setText(f'{filename} not found! <img src="icons/error.png" width="24" height="24">')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TextToSpeechGUI()
    window.show()

    sys.exit(app.exec_())
