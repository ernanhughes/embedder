import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QTextEdit,
    QTextEdit,
    QComboBox,
    QFileDialog,
    QVBoxLayout
)

from PyQt6.QtGui import QGuiApplication

class EmbedderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 800, 200
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle("Embedder Application")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options = (
            "getOpenFileName()",
            "getOpenFileNames()",
            "getExistingDirectory()",
            "getSaveFileName()",
        )

        self.combo = QComboBox()
        self.combo.addItems(self.options)
        layout.addWidget(self.combo)

        btn = QPushButton("Launch")
        btn.clicked.connect(self.launchDialog)
        layout.addWidget(btn)

        self.textbox = QTextEdit()
        layout.addWidget(self.textbox)

    def launchDialog(self):
        option = self.options.index(self.combo.currentText())
        if option == 0:
            response = self.getFileName()
        elif option == 1:
            response = self.getFileNames()
        elif option == 2:
            response = self.getDirectory()
        elif option == 3:
            response = self.getSaveFileName()
        else:
            print("Got Nothing")

    def getFileName(self):
        file_filter = "Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Image File (*.png *.jpg)"
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file",
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter="Excel File (*.xlsx *.xls)",
        )
        self.textbox.setText(str(response))

    def getFileNames(self):
        file_filter = "Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Image File (*.png *.jpg)"
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption="Select file(s)",
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter="Excel File (*.xlsx *.xls)",
        )
        self.textbox.setText(str(response))

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(
            self,
            # caption='Select a folder'
        )
        self.textbox.setText(str(response))

    def getSaveFileName(self):
        file_filter = "Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)"
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption="Select a data file",
            directory="Data File.dat",
            filter=file_filter,
            initialFilter="Excel File (*.xlsx *.xls)",
        )
        self.textbox.setText(str(response))

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QGuiApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget {
            font-size: 20px;
        }
    """
    )

    myApp = EmbedderApp()
    myApp.center()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing Window...")
