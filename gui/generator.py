from PyQt5.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout,
    QDialog, QSpinBox, QLineEdit
)
import random
import string

class PasswordGeneratorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("密碼生成器")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.length_label = QLabel("選擇密碼長度:")
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 128) 
        self.length_spinbox.setValue(12)

        self.generated_password_label = QLabel("生成的密碼:")
        self.generated_password_display = QLineEdit()
        self.generated_password_display.setReadOnly(True)

        self.generate_button = QPushButton("生成密碼")
        self.generate_button.clicked.connect(self.generate_password)

        layout.addWidget(self.length_label)
        layout.addWidget(self.length_spinbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.generated_password_label)
        layout.addWidget(self.generated_password_display)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spinbox.value()
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        self.generated_password_display.setText(password)