import sys
from PySide6 import QtCore, QtWidgets, QtGui
from main_window import MainWindow

if __name__ == "__main__":
    # Force software rendering if needed or ensure correct GL profile
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    app = QtWidgets.QApplication(sys.argv)

    # Set surface format for ModernGL compatibility
    fmt = QtGui.QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
