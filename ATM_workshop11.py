import sys
import json
from PyQt6.QtWidgets import (
    QLabel, QWidget, QLineEdit, QPushButton, QHBoxLayout, QApplication,
    QStackedWidget, QVBoxLayout, QMessageBox)
class Customer:
    def __init__(self, name, password, balance=0):
        self.name = name
        self.password = password
        self.balance = balance

    def to_dict(self):
        return {"name": self.name,
            "password": self.password,
            "balance": self.balance}
    @staticmethod
    def from_dict(data):
        return Customer(data['name'], data['password'], data['balance'])

customers = {'ap_student': Customer('ap_student','1234',1000)}

def save_customers_to_file(filename="customers.json"):
    with open(filename, 'w') as file:
        json.dump({name: customer.to_dict() for name, customer in customers.items()}, file, indent=4)

def load_customers_from_file(filename="customers.json"):
    global customers
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            customers = {name: Customer.from_dict(info) for name, info in data.items()}
            customers['ap_student']= Customer('ap_student','1234',1000)
    except FileNotFoundError:
        customers = {'ap_student': Customer('ap_student','1234',1000)}


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATM App")
        self.setGeometry(300, 300, 400, 300)

        self.stacked_widgets = QStackedWidget(self)
        self.current_user = None
        self.language = 'eng'
        self.bg_color = "white"

        self.init_pages()
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widgets)
        self.setLayout(layout)

    def tr(self, en, fa):
        if self.language == 'eng':
            return en
        else:
            return fa

    def init_pages(self):
        self.start_page = self.create_start_page()
        self.login_signup_page = self.create_login_signup_page()
        self.main_menu_page = self.create_main_menu_page()
        self.balance_page = self.create_balance_page()
        self.withdraw_page = self.create_withdraw_page()
        self.transfer_page = self.create_transfer_page()
        self.change_pass_page = self.create_change_password_page()

        self.stacked_widgets.addWidget(self.start_page)
        self.stacked_widgets.addWidget(self.login_signup_page)
        self.stacked_widgets.addWidget(self.main_menu_page)
        self.stacked_widgets.addWidget(self.balance_page)
        self.stacked_widgets.addWidget(self.withdraw_page)
        self.stacked_widgets.addWidget(self.transfer_page)
        self.stacked_widgets.addWidget(self.change_pass_page)

    def create_start_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Welcome to ATM App / به برنامه خودپرداز خوش آمدید")
        layout.addWidget(label)

        eng_button = QPushButton("English")
        fa_button = QPushButton("فارسی")
        eng_button.setStyleSheet("background: teal")
        fa_button.setStyleSheet("background: darkturquoise")
        layout2 = QHBoxLayout()
        layout2.addWidget(eng_button)
        layout2.addWidget(fa_button)

        eng_button.clicked.connect(lambda: self.show_login_signup_page('eng'))
        fa_button.clicked.connect(lambda: self.show_login_signup_page('fa'))

        layout.addLayout(layout2)
        page.setLayout(layout)
        return page

    def show_login_signup_page(self, lang):
        self.language = lang
        self.bg_color = "teal" if lang == 'eng' else "darkturquoise"
        self.apply_background_color()
        self.refresh_ui_texts()
        self.stacked_widgets.setCurrentWidget(self.login_signup_page)

    def apply_background_color(self):
        for i in range(self.stacked_widgets.count()):
            widget = self.stacked_widgets.widget(i)
            widget.setStyleSheet(f"background-color: {self.bg_color};")

    def create_login_signup_page(self):
        page = QWidget()
        self.login_layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")

        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)

        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")

        self.login_layout.addWidget(self.username_label)
        self.login_layout.addWidget(self.username_input)
        self.login_layout.addWidget(self.password_label)
        self.login_layout.addWidget(self.password_input)
        self.login_layout.addWidget(self.login_button)
        self.login_layout.addWidget(self.signup_button)

        page.setLayout(self.login_layout)
        return page

    def login(self):
        name = self.username_input.text()
        password = self.password_input.text()

        if name in customers and customers[name].password == password:
            self.current_user = customers[name]
            self.show_message("Login successful!")
            self.stacked_widgets.setCurrentWidget(self.main_menu_page)
        else:
            self.show_message("Invalid credentials")

    def signup(self):
        name = self.username_input.text()
        password = self.password_input.text()

        if name in customers:
            self.show_message("Username already exists.")
        else:
            customers[name] = Customer(name, password, 1000) #it is assumed that all initial balances are 1000 currency units
            save_customers_to_file()
            self.show_message("Account created. You can now log in.")

    def create_main_menu_page(self):
        page = QWidget()
        self.menu_layout = QVBoxLayout()

        self.menu_label = QLabel("Select Action")
        self.balance_btn = QPushButton("Check Balance")
        self.withdraw_btn = QPushButton("Withdraw Cash")
        self.transfer_btn = QPushButton("Transfer Money")
        self.change_pass_btn = QPushButton("Change Password")
        self.logout_btn = QPushButton("Logout")

        self.balance_btn.clicked.connect(self.show_balance_page)
        self.withdraw_btn.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.withdraw_page))
        self.transfer_btn.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.transfer_page))
        self.change_pass_btn.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.change_pass_page))
        self.logout_btn.clicked.connect(self.logout)

        self.menu_layout.addWidget(self.menu_label)
        self.menu_layout.addWidget(self.balance_btn)
        self.menu_layout.addWidget(self.withdraw_btn)
        self.menu_layout.addWidget(self.transfer_btn)
        self.menu_layout.addWidget(self.change_pass_btn)
        self.menu_layout.addWidget(self.logout_btn)

        page.setLayout(self.menu_layout)
        return page

    def show_balance_page(self):
        self.balance_number_label.setText(f"{self.current_user.balance}")
        self.stacked_widgets.setCurrentWidget(self.balance_page)

    def create_balance_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.balance_label = QLabel(f"Current Balance:")
        self.balance_number_label = QLabel("")
        layout.addWidget(self.balance_label)
        layout.addWidget(self.balance_number_label)
        self.back_button_balance = QPushButton("New Mission")
        self.back_button_balance.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.main_menu_page))
        layout.addWidget(self.back_button_balance)
        page.setLayout(layout)

        return page

    def create_withdraw_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.withdraw_input = QLineEdit()
        self.withdraw_input.setPlaceholderText("Amount to withdraw")
        self.withdraw_btn2 = QPushButton("Withdraw")
        self.back_button_withdraw = QPushButton("New Mission")
        self.withdraw_50_btn = QPushButton('50')
        self.withdraw_100_btn = QPushButton('100')
        self.withdraw_150_btn = QPushButton('150')
        self.withdraw_200_btn = QPushButton('200')

        button_layout.addWidget(self.withdraw_50_btn)
        button_layout.addWidget(self.withdraw_100_btn)
        button_layout.addWidget(self.withdraw_150_btn)
        button_layout.addWidget(self.withdraw_200_btn)

        self.withdraw_btn2.clicked.connect(self.withdraw_cash)
        self.back_button_withdraw.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.main_menu_page))
        self.withdraw_50_btn.clicked.connect(lambda: self.withdraw_money_btn_based(50))
        self.withdraw_100_btn.clicked.connect(lambda: self.withdraw_money_btn_based(100))
        self.withdraw_150_btn.clicked.connect(lambda: self.withdraw_money_btn_based(150))
        self.withdraw_200_btn.clicked.connect(lambda: self.withdraw_money_btn_based(200))

        layout.addWidget(self.withdraw_input)
        layout.addWidget(self.withdraw_btn2)
        layout.addWidget(self.back_button_withdraw)
        layout.addLayout(button_layout)
        page.setLayout(layout)
        return page
    def withdraw_money_btn_based(self, amount):
        if self.current_user.balance >= amount:
            self.current_user.balance -= amount
            save_customers_to_file()
            self.show_message(f"Withdrawal successful. New balance: ${self.current_user.balance}")
        else:
            self.show_message("Insufficient balance or invalid amount.")
    def withdraw_cash(self):
        try:
            amount = float(self.withdraw_input.text())
            if amount > 0 and self.current_user.balance >= amount:
                self.current_user.balance -= amount
                save_customers_to_file()
                self.show_message(f"Withdrawal successful. New balance: ${self.current_user.balance}")
            else:
                self.show_message("Insufficient balance or invalid amount.")
        except ValueError:
            self.show_message("Please enter a valid number.")

    def create_transfer_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.transfer_user_input = QLineEdit()
        self.transfer_amount_input = QLineEdit()
        self.transfer_user_input.setPlaceholderText("Recipient username")
        self.transfer_amount_input.setPlaceholderText("Amount to transfer")

        self.transfer_btn2 = QPushButton("Transfer")
        self.back_button_transfer = QPushButton("New Mission")

        self.transfer_btn2.clicked.connect(self.transfer_money)
        self.back_button_transfer.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.main_menu_page))

        layout.addWidget(self.transfer_user_input)
        layout.addWidget(self.transfer_amount_input)
        layout.addWidget(self.transfer_btn2)
        layout.addWidget(self.back_button_transfer)

        page.setLayout(layout)
        return page

    def transfer_money(self):
        recipient = self.transfer_user_input.text()
        try:
            amount = float(self.transfer_amount_input.text())
            if recipient not in customers:
                self.show_message("Recipient does not exist.")
            elif amount <= 0 or self.current_user.balance < amount:
                self.show_message("Invalid or insufficient funds.")
            else:
                self.current_user.balance -= amount
                customers[recipient].balance += amount
                save_customers_to_file()
                self.show_message(f"Transferred ${amount} to {recipient}.")
        except ValueError:
            self.show_message("Please enter a valid amount.")

    def create_change_password_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.new_pass_input = QLineEdit()
        self.new_pass_input.setPlaceholderText("Enter new password")
        self.new_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_label = QLabel('Confirm Password')
        self.confirm_label.setFixedHeight(40)
        self.repeat_password = QLineEdit()
        self.change_btn2 = QPushButton("Change Password")
        self.back_button_change_pass = QPushButton("New Mission")

        self.change_btn2.clicked.connect(self.change_password)
        self.back_button_change_pass.clicked.connect(lambda: self.stacked_widgets.setCurrentWidget(self.main_menu_page))

        layout.addWidget(self.new_pass_input)
        layout.addWidget(self.confirm_label)
        layout.addWidget(self.repeat_password)
        layout.addWidget(self.change_btn2)
        layout.addWidget(self.back_button_change_pass)

        page.setLayout(layout)
        return page

    def change_password(self):
        new_password = self.new_pass_input.text()
        if new_password:
            self.current_user.password = new_password
            save_customers_to_file()
            self.show_message("Password changed successfully.")
        else:
            self.show_message("Password cannot be empty.")

    def logout(self):
        self.current_user = None
        self.username_input.clear()
        self.password_input.clear()
        self.stacked_widgets.setCurrentWidget(self.start_page)

    def show_message(self, msg):
        QMessageBox.information(self, self.tr("Info", "اطلاع"), msg)

    def refresh_ui_texts(self):
        self.login_button.setText(self.tr("Login", "ورود"))
        self.signup_button.setText(self.tr("Sign Up", "ثبت نام"))
        self.username_label.setText(self.tr("Username:", "نام کاربری:"))
        self.password_label.setText(self.tr("Password:", "رمز عبور:"))
        self.menu_label.setText(self.tr("Select Action", "عملیات مورد نظر را انتخاب کنید"))
        self.balance_btn.setText(self.tr("Check Balance", "مشاهده موجودی"))
        self.withdraw_btn.setText(self.tr("Withdraw Cash", "برداشت وجه"))
        self.transfer_btn.setText(self.tr("Transfer Money", "انتقال وجه"))
        self.change_pass_btn.setText(self.tr("Change Password", "تغییر رمز عبور"))
        self.logout_btn.setText(self.tr("Logout", "خروج"))
        self.withdraw_input.setPlaceholderText(self.tr("Amount to withdraw", "مبلغ برداشت"))
        self.transfer_user_input.setPlaceholderText(self.tr("Recipient username", "نام کاربری گیرنده"))
        self.transfer_amount_input.setPlaceholderText(self.tr("Amount to transfer", "مبلغ انتقال"))
        self.new_pass_input.setPlaceholderText(self.tr("Enter new password", "رمز عبور جدید را وارد کنید"))
        self.confirm_label.setText(self.tr("Confirm Password:", "تایید رمز عبور:"))
        self.balance_label.setText(self.tr(f"Current Balance: ", f"موجودی :"))
        self.back_button_balance.setText(self.tr("New Mission","عملیات جدید"))
        self.back_button_change_pass.setText(self.tr("New Mission","عملیات جدید"))
        self.back_button_transfer.setText(self.tr("New Mission", "عملیات جدید"))
        self.back_button_withdraw.setText(self.tr("New Mission", "عملیات جدید"))
        self.withdraw_btn2.setText(self.tr("Withdraw ","برداشت "))
        self.transfer_btn2.setText(self.tr("Transfer","انتقال"))
        self.change_btn2.setText(self.tr("Change Password","تعویض رمز عبور"))
        
if __name__ == "__main__":
    load_customers_from_file()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

