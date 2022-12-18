from PyQt6 import QtWidgets, uic

# Start app
app = QtWidgets.QApplication([])

# Load UI files
login_screen = uic.loadUi("login.ui")
close_screen = uic.loadUi("close.ui")
data_screen = uic.loadUi("data.ui")
results_screen = uic.loadUi("results.ui")

# Executable
login_screen.show()

login_screen.error_label.hide()
data_screen.error_label.hide()
attempts = 2


def format_bytes(bytes):
    if bytes < 1024:
        return f"{round(bytes, 3)} B"
    elif bytes < 1024 ** 2:
        return f"{round(bytes / 1024, 3)} KB"
    elif bytes < 1024 ** 3:
        return f"{round(bytes / 1024 ** 2, 3)} MB"
    else:
        return f"{round(bytes / 1024 ** 3, 3)} GB"


def calculate_audio_data(
        audio_bits,
        audio_frequency,
        audio_channels,
        audio_compression,
        duration):
    audio_frequency = int(audio_frequency) * 1000 * 2
    audio_bw = audio_frequency * int(audio_bits) * int(audio_channels)
    audio_storage = audio_bw * duration / 8
    audio_storage_compressed = audio_storage * (1 - audio_compression)

    return [audio_bw, audio_storage, audio_storage_compressed]


def calculate_video_data(
        video_color,
        video_resolution,
        video_compression,
        video_fps,
        duration):
    [width, height] = video_resolution.split("x")
    video_bw = int(width) * int(height) * int(video_fps) * int(video_color)
    video_storage = video_bw * duration / 8
    video_storage_compressed = video_storage * (1 - video_compression)

    return [video_bw, video_storage, video_storage_compressed]


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


def display_results(audio_data, video_data):
    data_screen.close()
    results_screen.show()
    total_bw = audio_data[0] + video_data[0]
    total_storage = audio_data[1] + video_data[1]
    total_storage_compressed = audio_data[2] + video_data[2]
    compress_percentage = (total_storage_compressed / total_storage) * 100

    results_screen.audio_bw.setText(
        f"El ancho de banda requerido\nes de: {audio_data[0]} bps")
    results_screen.audio_storage_original.setText(
        f"El espacio de almacenamiento\nrequerido (sin compresión)\nes de: {format_bytes(audio_data[1])}")
    results_screen.audio_storage_compressed.setText(
        f"El espacio de almacenamiento\nrequerido (con compresión)\nes de: {format_bytes(audio_data[2])}")

    results_screen.video_bw.setText(
        f"El ancho de banda requerido\nes de: {video_data[0]} bps")
    results_screen.video_storage_original.setText(
        f"El espacio de almacenamiento\nrequerido (sin compresión)\nes de: {format_bytes(video_data[1])}")
    results_screen.video_storage_compressed.setText(
        f"El espacio de almacenamiento\nrequerido (con compresión)\nes de: {format_bytes(video_data[2])}")

    results_screen.total_bw.setText(
        f"El ancho de banda total\nrequerido es de: {total_bw} bps")
    results_screen.total_storage_original.setText(
        f"El espacio de almacenamiento\ntotal requerido (sin\ncompresión) es de: {format_bytes(total_storage)}")
    results_screen.total_storage_compressed.setText(
        f"El espacio de almacenamiento\ntotal requerido (con\ncompresión) es de: {format_bytes(total_storage_compressed)}")
    results_screen.result_label.setText(
        f"Se ahorro el {round(compress_percentage, 1)}% de espacio de almacenamiento al comprimir ({format_bytes(total_storage - total_storage_compressed)})")


def calculate_again():
    results_screen.close()
    data_screen.show()


def app_exit():
    app.exit()


def gui_data():
    audio_compression = int(
        data_screen.audio_compression.text().split("%")[0]) / 100

    video_compression = int(
        data_screen.video_compression.text().split("%")[0]) / 100
    video_initial_time = data_screen.video_initial_time.text().split(":")
    video_final_time = data_screen.video_final_time.text().split(":")

    if audio_compression == '' or video_compression == '' or video_initial_time[
            0] == '' or video_final_time[0] == '':
        data_screen.error_label.show()
        return

    data_screen.error_label.hide()
    initial_time = int(video_initial_time[0]) * 60 + int(video_initial_time[1])
    final_time = int(video_final_time[0]) * 60 + int(video_final_time[1])
    duration = (final_time - initial_time) * 60

    audio_bits = data_screen.audio_bits.currentText()
    audio_frequency = data_screen.audio_frequency.currentText()
    audio_channels = data_screen.audio_channels.currentText()

    video_color = data_screen.video_color.currentText()
    video_resolution = data_screen.video_resolution.currentText()
    video_fps = data_screen.video_fps.currentText()

    audio_data = calculate_audio_data(
        audio_bits,
        audio_frequency,
        audio_channels,
        audio_compression,
        duration)

    video_data = calculate_video_data(
        video_color,
        video_resolution,
        video_compression,
        video_fps,
        duration)

    display_results(audio_data, video_data)


login_screen.login.clicked.connect(gui_login)
close_screen.btn_close.clicked.connect(app_exit)
data_screen.calculate.clicked.connect(gui_data)
results_screen.calculate_again.clicked.connect(calculate_again)
results_screen.exit.clicked.connect(app_exit)

app.exec()
