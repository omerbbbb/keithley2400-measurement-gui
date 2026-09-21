import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QComboBox
import pyqtgraph as pg
from pymeasure.instruments.keithley.keithley2400 import Keithley2400
from PyQt5.QtCore import QTimer
import numpy as np

from keithley2400CurrentToTime import CurrentToTimeApp
from keithley2400VoltageToCurrent import CurrentToVoltage

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Creating the main window
        self.setWindowTitle("SharoniLab")
        self.setGeometry(100, 100, 1600, 900)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        # Create a QComboBox for From
        self.from_label = QLabel("From: ", self)
        self.from_label.setMaximumWidth(150)
        self.layout.addWidget(self.from_label)
        self.from_box = QComboBox(self)
        self.from_box.addItem("V")
        self.from_box.addItem("I")
        self.from_box.addItem("Time (sec)")
        self.layout.addWidget(self.from_box)
        self.from_box.setMaximumWidth(150)
        # Create a QComboBox for To
        self.to_label = QLabel("To: ", self)
        self.to_label.setMaximumWidth(150)
        self.layout.addWidget(self.to_label)
        self.to_box = QComboBox(self)
        self.to_box.addItem("V")
        self.to_box.addItem("I")
        self.to_box.addItem("Time (sec)")
        self.layout.addWidget(self.to_box)
        self.to_box.setMaximumWidth(150)
        # Creates a button to open the Keithley program
        self.keithley2400_button = QPushButton("Start Keithley 2400 program")
        self.keithley2400_button.clicked.connect(self.Keithley2400App)
        self.layout.addWidget(self.keithley2400_button)
        self.from_label.setMaximumWidth(150)

    def Keithley2400App(self):
        print(self.from_box.currentText())
        if (self.from_box.currentText() == "I" and self.to_box.currentText() == "Time (sec)"):
            self.app_window = CurrentToTimeApp()
            self.app_window.show()
        elif (self.from_box.currentText() == "V" and self.to_box.currentText() == "I"):
            self.app_window = CurrentToVoltage()
            self.app_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())