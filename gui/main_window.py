from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QTableWidget, QTableWidgetItem, QFrame, QMessageBox,
    QMenu, QLineEdit
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import json
import os

from gui.addaccountform import AddAccountForm
from gui.generator import PasswordGeneratorDialog
from config import DATA_FILE_PATH

class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeyNest - 密碼管理器")
        self.resize(1200, 900)
        self.setWindowIcon(QIcon("icon.ico"))
        self.accounts = [] 
        self.load_accounts()
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        

        main_layout = QHBoxLayout()

        self.menu_frame = QFrame()
        self.menu_frame.setStyleSheet("background-color: #f0f0f0; border-right: 1px solid #ddd;")
        self.menu_frame.setFixedWidth(200)
        
        menu_layout = QVBoxLayout()
        
        self.add_button = QPushButton("➕ 添加帳號")
        self.add_button.setFixedHeight(50)
        self.add_button.clicked.connect(self.show_add_account_form)
        
        self.generator_button = QPushButton("🔑 密碼生成器")
        self.generator_button.setFixedHeight(50)
        self.generator_button.clicked.connect(self.show_password_generator) 
        
        for btn in [self.add_button, self.generator_button]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
            """)
        
        menu_layout.addWidget(self.add_button)
        menu_layout.addWidget(self.generator_button)
        menu_layout.addStretch()
        
        self.menu_frame.setLayout(menu_layout)
        

        content_layout = QVBoxLayout()


        self.account_table = QTableWidget()
        self.account_table.setColumnCount(6)
        self.account_table.setHorizontalHeaderLabels(["服務名稱", "用戶名", "密碼", "Email", "手機號", "備註"])  # 顯示新增的欄位
        self.account_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)

  
        self.account_table.setColumnWidth(0, 150)
        self.account_table.setColumnWidth(1, 200)
        self.account_table.setColumnWidth(2, 350)
        self.account_table.setColumnWidth(3, 200)


        self.account_table.setSortingEnabled(True)

        self.account_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.account_table.customContextMenuRequested.connect(self.show_context_menu)

        self.status_label = QLabel("🔒 已加載 0 個帳號")
        self.status_label.setStyleSheet("font-size: 12px; color: #555; padding: 10px;")
        
        content_layout.addWidget(self.account_table)
        content_layout.addWidget(self.status_label)
        
        main_layout.addWidget(self.menu_frame)
        main_layout.addLayout(content_layout)

        main_widget.setLayout(main_layout)

        # 更新界面
        self.update_account_table()

    def show_add_account_form(self):
        self.add_account_form = AddAccountForm(self)
        self.add_account_form.setWindowModality(Qt.ApplicationModal)  # 禁止操作其他窗口
        self.add_account_form.show()

    def show_password_generator(self):
        self.password_generator_dialog = PasswordGeneratorDialog()
        self.password_generator_dialog.setWindowModality(Qt.ApplicationModal)
        self.password_generator_dialog.show()

    def update_account_table(self):
        self.account_table.setRowCount(len(self.accounts))
        for row, account in enumerate(self.accounts):
            self.account_table.setItem(row, 0, QTableWidgetItem(account['site']))
            self.account_table.setItem(row, 1, QTableWidgetItem(account['username']))
            
            password_widget = QWidget()
            password_layout = QHBoxLayout(password_widget)
            password_layout.setContentsMargins(0, 0, 0, 0)
            
            password_input = QLineEdit(account['password'])
            password_input.setEchoMode(QLineEdit.Password)
            password_input.setReadOnly(True)
            password_input.setStyleSheet("border: none;")

            toggle_button = QPushButton("👁️")
            toggle_button.setFixedWidth(30)
            toggle_button.setCheckable(True)
            toggle_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                    font-size: 18px;
                }
                QPushButton:checked {
                    color: #0078D7;
                }
            """)
            
            toggle_button.clicked.connect(lambda _, p=password_input: self.toggle_password_visibility(p))
            
            password_layout.addWidget(password_input)
            password_layout.addWidget(toggle_button)
            
            self.account_table.setCellWidget(row, 2, password_widget)

            self.account_table.setItem(row, 3, QTableWidgetItem(account.get('email', '')))
            self.account_table.setItem(row, 4, QTableWidgetItem(account.get('phone', '')))
            self.account_table.setItem(row, 5, QTableWidgetItem(account.get('notes', '')))

        self.status_label.setText(f"🔒 已加載 {len(self.accounts)} 個帳號")

    def load_accounts(self):
        if os.path.exists(DATA_FILE_PATH):
            try:
                with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
                    self.accounts = json.load(file)
                print("帳號數據已加載成功")
            except json.JSONDecodeError:
                QMessageBox.warning(self, "警告", "儲存的數據格式錯誤，無法加載帳號！", QMessageBox.Ok)
                self.accounts = []
        else:
            self.accounts = []

    def save_accounts(self):
        """將帳號數據保存到JSON文件"""
        os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        try:
            with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump(self.accounts, file, ensure_ascii=False, indent=4)
            print("帳號數據已保存")
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"儲存帳號數據時出錯：{e}", QMessageBox.Ok)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        
        row = self.account_table.rowAt(pos.y())
        col = self.account_table.columnAt(pos.x())
        
        if row >= 0 and col >= 0:
            copy_action = context_menu.addAction("複製")
            copy_action.triggered.connect(lambda: self.copy_to_clipboard(row, col))

            delete_action = context_menu.addAction("刪除")
            delete_action.triggered.connect(lambda: self.delete_account(row))
        
        context_menu.exec_(self.account_table.mapToGlobal(pos))

    def delete_account(self, row):
        confirm = QMessageBox.question(
            self, "確認刪除", "確定要刪除這個帳號嗎？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            del self.accounts[row]
            self.save_accounts()

            self.update_account_table()
            QMessageBox.information(self, "刪除成功", "帳號已成功刪除！")

    def closeEvent(self, event):
        self.scan_and_save_table_data()
        event.accept()

    def scan_and_save_table_data(self):
        accounts = []
        for row in range(self.account_table.rowCount()):
            account_data = {
                "site": self.account_table.item(row, 0).text() if self.account_table.item(row, 0) else "",
                "username": self.account_table.item(row, 1).text() if self.account_table.item(row, 1) else "",
                "password": self.account_table.cellWidget(row, 2).findChild(QLineEdit).text() if self.account_table.cellWidget(row, 2) else "",  # 這裡抓取密碼
                "email": self.account_table.item(row, 3).text() if self.account_table.item(row, 3) else "",
                "phone": self.account_table.item(row, 4).text() if self.account_table.item(row, 4) else "",
                "notes": self.account_table.item(row, 5).text() if self.account_table.item(row, 5) else "",
            }
            accounts.append(account_data)
        
        self.accounts = accounts
        self.save_accounts()
        self.update_account_table()

    def toggle_password_visibility(self, password_input):
        if password_input.echoMode() == QLineEdit.Password:
            password_input.setEchoMode(QLineEdit.Normal)
        else:
            password_input.setEchoMode(QLineEdit.Password)