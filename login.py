from PyQt6 import QtWidgets, uic

# Start app
app = QtWidgets.QApplication([])

# Load UI files
login = uic.loadUi("login.ui")
close_screen = uic.loadUi("close.ui")

# Executable
login.show()

# def init():
login.error_label.hide()
attempts = 2


def gui_login():
    global attempts
    login.error_label.show()
    password = login.password.text()

    if password == "str-2022":
        login.error_label.hide()
        login.error_label.setText("")

    elif attempts == 0:
        close_screen.show()
        login.close()

    else:
        login.error_label.setText(f"Clave incorrecta. Quedan {attempts} intentos")
        attempts -= 1
        login.password.clear()


def gui_close():
    close_screen.close()


login.login.clicked.connect(gui_login)
close_screen.btn_close.clicked.connect(gui_close)

app.exec()
