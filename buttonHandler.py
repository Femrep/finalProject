from PyQt5 import QtGui
from noteMapper import NoteMapper
class ButtonHandler:
    def __init__(self, ui):
        self.ui = ui

    def reset_button_color(self):
        for attr in dir(self.ui):
            if attr.startswith('st_'):
                button = getattr(self.ui, attr)
                button.setStyleSheet("")

    def radio_button_clicked(self):
        self.ui.pushButton.setStyleSheet("")
        if self.ui.record.isChecked():
            self.ui.reset()
            self.ui.pushButton.setStyleSheet("")
            self.ui.pushButton.setVisible(False)
            self.ui.pushButton.setText("Record Note")
            for attr in dir(self.ui):
                if attr.startswith('st_'):
                    button = getattr(self.ui, attr)
                    button.setEnabled(True)
        else:
            self.ui.reset()
            self.ui.pushButton.setVisible(True)
            self.ui.pushButton.setText("Play Note")
            for attr in dir(self.ui):
                if attr.startswith('st_'):
                    button = getattr(self.ui, attr)
                    button.setStyleSheet("")
                    button.setEnabled(False)

    def on_click(self, button):
        self.reset_button_color()
        button_name = button.objectName()
        if button_name in self.ui.note_mapper.button_actions:
            for btn_name in self.ui.note_mapper.button_actions[button_name]:
                btn = getattr(self.ui, btn_name)
                btn.setStyleSheet("background-color: green")
        else:
            button.setStyleSheet("background-color: green")

        for key, values in self.ui.note_mapper.button_to_record.items():
            if button_name in values:
                self.ui.record_list.append(key)
                break
        else:
            self.ui.record_list.append(button_name)

        if self.ui.count < 19:
            i = self.ui.count
            image = getattr(self.ui, f"image_{i}")
            image_path = self.ui.note_mapper.button_to_image.get(button_name, "empty.png")
            image.setPixmap(QtGui.QPixmap(self.ui.resource_path(f"image/notas_locations/{image_path}")))
            self.ui.count += 1
            if self.ui.count == 19:
                self.ui.count = 1

    def on_click_PushButton(self):
        name_of_push_button = self.ui.pushButton.text()
        if name_of_push_button == "Play Note":
            if self.ui.button_counter:
                self.ui.pushButton.setStyleSheet("background-color: red")
                self.reset_button_color()
                self.ui.button_counter = False
                self.ui.detector_thread.start()
            else:
                self.ui.pushButton.setStyleSheet("")
                self.reset_button_color()
                self.ui.button_counter = True
                self.ui.detector_thread.quit()
        elif name_of_push_button == "Record Note":
            if self.ui.button_counter:
                self.ui.pushButton.setStyleSheet("background-color: red")
                self.reset_button_color()
                self.ui.count = 1
                self.ui.button_counter = False
            else:
                self.ui.pushButton.setStyleSheet("")
                self.ui.button_counter = True
                self.reset_button_color()

