import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout
import pyqtgraph as pg
from pymeasure.instruments.keithley.keithley2400 import Keithley2400
from PyQt5.QtCore import QTimer
import numpy as np


class CurrentToTimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Creating the main window
        self.setWindowTitle("Keithley Data Logger")
        self.setGeometry(100, 100, 1600, 900)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.instrument_2400 = Keithley2400("GPIB0::28::INSTR")  # Change "COM2" to your Keithley 2400 address

        # Create PyQtGraph plots
        self.plot_widget_2400 = pg.PlotWidget(self)
        self.layout.addWidget(self.plot_widget_2400)
        self.curve_2400 = self.plot_widget_2400.plot(pen='r')
        # self.plot_widget_2400.setYRange(0, 1)  # Adjust the range as needed
        self.plot_widget_2400.setLabel('left', 'Current', units='A')
        self.plot_widget_2400.setLabel('bottom', 'Time', units='s')


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000)

        # Create button to update Keithley2400 settings
        self.button_update_settings = QPushButton("Update Settings")
        self.button_update_settings.clicked.connect(self.update_settings)
        self.layout.addWidget(self.button_update_settings)

        # Current compliance insert box and label
        self.current_compliance = QLineEdit(self)
        self.current_compliance_label = QLabel("Current Compliance")
        self.current_compliance.setMaximumWidth(150)
        self.layout.addWidget(self.current_compliance_label)
        self.layout.addWidget(self.current_compliance)

        # Voltage source insert box and label
        self.voltage_source_label = QLabel("Voltage Source")
        self.voltage_source = QLineEdit(self)
        self.layout.addWidget(self.voltage_source_label)
        self.layout.addWidget(self.voltage_source)
        self.voltage_source.setMaximumWidth(150)

        # On and Off button
        self.on_off_switch = QPushButton("Toggle On/Off")
        self.on_off_switch.clicked.connect(self.on_off)
        self.layout.addWidget(self.on_off_switch)

        # Plot data
        self.current_measurement = 0
        self.max_data_points = 100
        self.x_data = np.array([])
        self.y_data = np.array([])
    def update_plots(self):
        # Read data from Keithley 2400
        if (self.instrument_2400.source_enabled == True):
            self.current_measurement = self.instrument_2400.current
            # Update plots data
            self.x_data = np.append(self.x_data, len(self.x_data) + 1)
            self.y_data = np.append(self.y_data, self.current_measurement)
            if len(self.x_data) > self.max_data_points:
                self.x_data = self.x_data[-self.max_data_points:]
                self.y_data = self.y_data[-self.max_data_points:]
            self.curve_2400.setData(x=self.x_data, y=self.y_data)

    # update settings action
    def update_settings(self):
        self.instrument_2400.source_voltage = float(self.voltage_source.text())
        self.instrument_2400.compliance_current = float(self.current_compliance.text())

    # On and off action
    def on_off(self):
        print(self.instrument_2400.source_enabled)
        if (self.instrument_2400.source_enabled == False):
            self.instrument_2400.enable_source()
        else:
            self.instrument_2400.disable_source()

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrentToTimeApp()
    window.show()
    sys.exit(app.exec_())
