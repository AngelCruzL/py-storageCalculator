from PyQt6 import QtWidgets, uic

# Start app
app = QtWidgets.QApplication([])

# Load UI files
login_screen = uic.loadUi("login.ui")
close_screen = uic.loadUi("close.ui")
data_screen = uic.loadUi("data.ui")

# Executable
login_screen.show()

# def init():
login_screen.error_label.hide()
attempts = 2


def gui_login():
    global attempts
    login_screen.error_label.show()
    password = login_screen.password.text()

    if password == "str-2022":
        data_screen.show()
        login_screen.close()

    elif attempts == 0:
        close_screen.show()
        login_screen.close()

    else:
        login_screen.error_label.setText(f"Clave incorrecta. Quedan {attempts} intentos")
        attempts -= 1
        login_screen.password.clear()


def gui_close():
    close_screen.close()


login_screen.login.clicked.connect(gui_login)
close_screen.btn_close.clicked.connect(gui_close)

app.exec()
