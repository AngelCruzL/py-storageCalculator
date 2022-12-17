from PyQt6 import QtWidgets, uic

# Start app
app = QtWidgets.QApplication([])

# Load UI files
login_screen = uic.loadUi("login.ui")
close_screen = uic.loadUi("close.ui")
data_screen = uic.loadUi("data.ui")

# Executable
login_screen.show()

login_screen.error_label.hide()
data_screen.error_label.hide()
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
        login_screen.error_label.setText(
            f"Clave incorrecta. Quedan {attempts} intentos")
        attempts -= 1
        login_screen.password.clear()


def app_exit():
    app.exit()


def gui_data():
    audio_compression = data_screen.audio_compression.text().split("%")[0]

    video_compression = data_screen.video_compression.text().split("%")[0]
    video_initial_time = data_screen.video_initial_time.text().split(":")
    video_final_time = data_screen.video_final_time.text().split(":")

    if audio_compression == '' or video_compression == '' or video_initial_time[0] == '' or video_final_time[0] == '':
        data_screen.error_label.show()
        return

    data_screen.error_label.hide()
    initial_time = int(video_initial_time[0]) * 60 + int(video_initial_time[1])
    final_time = int(video_final_time[0]) * 60 + int(video_final_time[1])
    duration = final_time - initial_time

    audio_bits = data_screen.audio_bits.currentText()
    audio_frequency = data_screen.audio_frequency.currentText()
    audio_channels = data_screen.audio_channels.currentText()

    video_color = data_screen.video_color.currentText()
    video_resolution = data_screen.video_resolution.currentText()
    video_fps = data_screen.video_fps.currentText()


login_screen.login.clicked.connect(gui_login)
close_screen.btn_close.clicked.connect(app_exit)
data_screen.calculate.clicked.connect(gui_data)

app.exec()
