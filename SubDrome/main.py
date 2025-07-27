from SubDrome import resource_rc  # noqa: F401
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import sys

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('SubDrome/main.qml')

sys.exit(app.exec())
