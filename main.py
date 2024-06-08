from PyQt5 import QtCore, QtGui, QtWidgets
from guitar import NoteDetector
from buttonHandler import ButtonHandler
from noteMapper import NoteMapper

import sys
import os

class Ui_MainWindow(object):
    def __init__(self):
        self.note_mapper = NoteMapper()
        self.button_counter = True
        self.count = 1
        self.list_image = []
        self.list_imageButton = []
        self.array_position = 1
        self.flag_of_note = False
        self.flag_array = False
        self.record_list = []
        self.detector = NoteDetector()
        self.detector.note_detected.connect(self.on_note_detected)
        self.detector_thread = QtCore.QThread()
        self.detector.moveToThread(self.detector_thread)
        self.detector_thread.started.connect(self.detector.detect_notes)
        self.button_handler = ButtonHandler(self)

    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Guitar Learning Application")
        MainWindow.resize(1104, 654)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1101, 611))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.bottom_frame = QtWidgets.QFrame(self.frame)
        self.bottom_frame.setGeometry(QtCore.QRect(0, 310, 1111, 251))
        self.bottom_frame.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame.setObjectName("bottom_frame")
        
        self.label = QtWidgets.QLabel(self.bottom_frame)
        self.label.setGeometry(QtCore.QRect(70, 20, 981, 221))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(self.resource_path("image/empty_fret.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.setupLabels()
        self.setupButtons()
        self.setupImages()
        self.setupMenuBar(MainWindow)
        self.setupOtherWidgets(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupLabels(self):
        label_names = ["label_2", "label_3", "label_4", "label_5", "label_6", "label_7"]
        label_positions = [(60, 50), (60, 75), (60, 100), (60, 125), (60, 150), (60, 175)]
        label_texts = ["1.", "2.", "3.", "4.", "5.", "6."]

        for name, position, text in zip(label_names, label_positions, label_texts):
            label = QtWidgets.QLabel(self.bottom_frame)
            label.setGeometry(QtCore.QRect(*position, 47, 13))
            label.setObjectName(name)
            label.setText(text)

        perde_names = [f"perde_{i+1}" for i in range(14)]
        
        font = QtGui.QFont()
        font.setPointSize(11)

        for name, position in zip(perde_names, self.note_mapper.perde_positions):
            label = QtWidgets.QLabel(self.bottom_frame)
            label.setGeometry(QtCore.QRect(*position, 16, 31))
            label.setFont(font)
            label.setScaledContents(True)
            label.setObjectName(name)
            label.setText(str(perde_names.index(name) + 1))

    def setupButtons(self):
        self.play = QtWidgets.QRadioButton(self.frame)
        self.play.setGeometry(QtCore.QRect(360, 570, 82, 17))
        self.play.setObjectName("play")
        self.play.setText("Play")
        self.play.clicked.connect(self.button_handler.radio_button_clicked)
        
        self.record = QtWidgets.QRadioButton(self.frame)
        self.record.setGeometry(QtCore.QRect(590, 570, 82, 17))
        self.record.setObjectName("record")
        self.record.setText("Record")
        self.record.clicked.connect(self.button_handler.radio_button_clicked)

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(1000, 570, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Play Note")
        self.pushButton.setVisible(False)
        self.pushButton.clicked.connect(self.button_handler.on_click_PushButton)

        button_names = [f"st_{string}_{fret}" for fret in range(15) for string in range(1, 7)]
        
        for name, position in zip(button_names, self.note_mapper.button_positions):
            button = QtWidgets.QPushButton(self.bottom_frame)
            button.setGeometry(QtCore.QRect(*position, 16, 16))
            button.setAutoFillBackground(True)
            button.setText("")
            button.setObjectName(name)
            button.setEnabled(False)
            button.clicked.connect(lambda _, b=button: self.button_handler.on_click(b))
            setattr(self, name, button)

    def setupImages(self):
        self.top_frame = QtWidgets.QFrame(self.frame)
        self.top_frame.setGeometry(QtCore.QRect(0, 0, 1101, 301))
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName("top_frame")

        self.bos_note= QtWidgets.QLabel(self.top_frame)
        self.bos_note.setGeometry(QtCore.QRect(50, 0, 1101, 301))
        self.bos_note.setText("")
        self.bos_note.setPixmap(QtGui.QPixmap(self.resource_path("image/bos_note.png")))
        self.bos_note.setScaledContents(False)
        self.bos_note.setObjectName("bos_note")

        self.bos_note2= QtWidgets.QLabel(self.top_frame)
        self.bos_note2.setGeometry(QtCore.QRect(350, 0, 1101, 301))
        self.bos_note2.setText("")
        self.bos_note2.setPixmap(QtGui.QPixmap(self.resource_path("image/bos_note.png")))
        self.bos_note2.setScaledContents(False)
        self.bos_note2.setObjectName("bos_note")
        
        self.Sol_anahtari = QtWidgets.QLabel(self.top_frame)
        self.Sol_anahtari.setGeometry(QtCore.QRect(40, 10, 651, 271))
        self.Sol_anahtari.setText("")
        self.Sol_anahtari.setPixmap(QtGui.QPixmap(self.resource_path("image/sol_anahtari.png")))
        self.Sol_anahtari.setScaledContents(False)
        self.Sol_anahtari.setObjectName("Sol_anahtari")

        for i in range(1, 19):
            image = QtWidgets.QLabel(self.top_frame)
            image.setGeometry(QtCore.QRect(-250 + 50 * i, 0, 371, 301))
            image.setText("")
            image.setPixmap(QtGui.QPixmap(self.resource_path(f"image/notas_locations/empty.png")))
            image.setScaledContents(False)
            image.setObjectName(f"image_{i}")
            setattr(self, f"image_{i}", image)

    def setupMenuBar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1104, 21))
        self.menubar.setObjectName("menubar")

        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menufile.setTitle("File")

        MainWindow.setMenuBar(self.menubar)

        self.about = QtWidgets.QAction(MainWindow)
        self.about.setObjectName("about")
        self.about.setText("About")
        self.about.setStatusTip("About Application")
        self.about.triggered.connect(self.about_application)

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setText("Save")
        self.actionSave.setStatusTip("Save Record")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(self.save_record)

        self.actionOpen_Record = QtWidgets.QAction(MainWindow)
        self.actionOpen_Record.setObjectName("actionOpen_Record")
        self.actionOpen_Record.setText("Open Record")
        self.actionOpen_Record.triggered.connect(self.open_record)

        self.menufile.addAction(self.about)
        self.menufile.addAction(self.actionSave)
        self.menufile.addAction(self.actionOpen_Record)

        self.menubar.addAction(self.menufile.menuAction())

    def setupOtherWidgets(self, MainWindow):
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Guitar Learning Application", "Guitar Learning Application"))
        MainWindow.setWindowIcon(QtGui.QIcon(self.resource_path("image/guitar.png")))

    def reset(self):
        self.reset_other()
        for i in range(1, 19):
            image = getattr(self, f"image_{i}")
            image.setPixmap(QtGui.QPixmap(self.resource_path(f"image/notas_locations/empty.png")))

    def reset_other(self):
        self.button_handler.reset_button_color()
        self.array_position = 1
        self.count = 1
        self.flag_of_note = False
        self.pushButton.setStyleSheet("")
        self.button_counter = True
        self.detector_thread.quit()
        self.list_image = []
        self.list_imageButton = []
        self.record_list = []

    def on_note_detected(self, position):
        if self.pushButton.text() == "Play Note":
            if self.button_counter == False:
                button_name = f"st_{position[0]}_{position[1]}"
                list_image = self.list_image
                size_list_image = len(list_image)
                if self.flag_array:
                    if self.array_position <= len(list_image):
                        btn = self.list_imageButton[self.array_position-1]
                        for btn_name in self.note_mapper.button_actions[btn]:
                            btn = getattr(self, btn_name)
                            btn.setStyleSheet("background-color: green")
                        if list_image[self.array_position-1] == self.note_mapper.button_to_image.get(button_name, "empty.png"):
                            if self.count < 19:
                                self.flag_of_note = False
                                image = getattr(self, f"image_{self.count}")
                                image.setPixmap(QtGui.QPixmap(self.resource_path(f"image/correct/{self.note_mapper.button_to_image.get(button_name, 'empty.png')}")))
                                self.array_position += 1
                                self.count += 1
                                self.button_handler.reset_button_color()
                                if self.count >= 19:
                                    arr_ps = self.array_position
                                    for i in range(1, 19):
                                        image = getattr(self, f"image_{i}")
                                        if arr_ps <= size_list_image:
                                            image.setPixmap(QtGui.QPixmap(self.resource_path(f"image/notas_locations/{list_image[arr_ps-1]}")))
                                            arr_ps += 1
                                        else:
                                            image.setPixmap(QtGui.QPixmap(self.resource_path(f"image/notas_locations/empty.png")))
                                    self.count = 1
                        else:
                            if self.flag_of_note == False:
                                self.flag_of_note = True
                                print("False")
                    else:
                        if self.array_position > len(list_image):
                            self.reset()
                else:
                    self.reset()
        else:
            print("nota detected")

    def update_images_from_file(self, file_path):
        if self.play.isChecked():
            with open(file_path, 'r') as file:
                buttons = file.read().strip().split(',')
                count = self.count
            for button_name in buttons:
                if count < 19:
                    image = getattr(self, f"image_{count}")
                    image_path = self.note_mapper.button_to_image.get(button_name, "empty.png")
                    self.list_imageButton.append(button_name)
                    self.list_image.append(image_path)
                    image.setPixmap(QtGui.QPixmap(self.resource_path(f"image/notas_locations/{image_path}")))
                    count += 1
                    self.flag_array = True
                else:
                    image_path = self.note_mapper.button_to_image.get(button_name, "empty.png")
                    self.list_image.append(image_path)

    def save_record(self):
        if self.record.isChecked():
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Record File", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(','.join(self.record_list))

    def open_record(self):
        if self.play.isChecked():
            self.reset()
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Record File", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_name:
                self.update_images_from_file(file_name)

    def about_application(self):
        QtWidgets.QMessageBox.about(None, "About Application", "This application is a guitar learning application.\n You can record the notes by clicked button and play the notes you recorded.\n Fahrettin Emre Pabuscu \n no:20190702010  \n Made in 2024 \n contact: fahrettinemrepab@gmail.com")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
