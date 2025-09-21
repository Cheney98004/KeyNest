from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QGroupBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class AddAccountForm(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(500, 400)
        self.setWindowTitle("添加帳號")

        self.setWindowFlags(Qt.Dialog)

        self.drag_position = None
        
        layout = QVBoxLayout(self)

        form_group = QGroupBox()
        form_layout = QFormLayout(form_group)

        self.site_name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.notes_input = QLineEdit()

        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(15)

        form_layout.addRow("服務名稱:", self.site_name_input)
        form_layout.addRow("用戶名:", self.username_input)
        form_layout.addRow("密碼:", self.password_input)
        form_layout.addRow("Email (選填):", self.email_input)
        form_layout.addRow("手機號 (選填):", self.phone_input)
        form_layout.addRow("備註 (選填):", self.notes_input)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet("background-color: #f44336;")
        self.cancel_button.clicked.connect(self.close)

        self.save_button = QPushButton("保存")
        self.save_button.setStyleSheet("background-color: #4CAF50;")
        self.save_button.clicked.connect(self.save_account)

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def save_account(self):
        if not self.site_name_input.text() or not self.username_input.text() or not self.password_input.text():
            QMessageBox.warning(self, "錯誤", "網站名稱、用戶名和密碼是必填項目！", QMessageBox.Ok)
            return

        account_data = {
            "site": self.site_name_input.text(),
            "username": self.username_input.text(),
            "password": self.password_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "notes": self.notes_input.text()
        }
        self.parent().accounts.append(account_data)
        self.parent().update_account_table()
        self.parent().save_accounts()  # 保存
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None
