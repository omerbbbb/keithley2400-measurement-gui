#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2023 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
This example demonstrates how to make a graphical interface to preform
IV characteristic measurements. There are a two items that need to be
changed for your system:

1) Correct the GPIB addresses in IVProcedure.startup for your instruments
2) Correct the directory to save files in MainWindow.queue

Run the program by changing to the directory containing this file and calling:

python iv_keithley.py

"""

import logging
import sys
from time import sleep
import numpy as np

from pymeasure.instruments.keithley import Keithley2000, Keithley2400
from pymeasure.display.Qt import QtWidgets
from pymeasure.display.windows import ManagedWindow
from pymeasure.experiment import (
    Procedure, FloatParameter, unique_filename, Results
)

log = logging.getLogger('')
log.addHandler(logging.NullHandler())


class IVProcedure(Procedure):

    # max_current = FloatParameter('Maximum Current', units='mA', default=10)
    # min_current = FloatParameter('Minimum Current', units='mA', default=-10)
    # current_step = FloatParameter('Current Step', units='mA', default=0.1)
    current_range = FloatParameter('Current Range', units='mA', default= 1)
    voltage_step = FloatParameter('Voltage Step', units='mV', default=1)
    delay = FloatParameter('Delay Time', units='ms', default=20)
    start_voltage = FloatParameter('Start Voltage', units='mV', default=0)
    stop_voltage = FloatParameter("Stop Voltage", units='mV', default=10)

    DATA_COLUMNS = ['Current (A)', 'Voltage (V)']

    def startup(self):
        log.info("Setting up instruments")
        self.source = Keithley2400("GPIB::28")
        self.source.reset()
        self.source.apply_voltage()
        self.source.measure_current(nplc=0.1)
        self.source.source_voltage_range = self.stop_voltage * 1e-3  # V
        self.source.compliance_current = self.current_range * 1e-3  # A
        self.source.enable_source()
        sleep(2)

    def execute(self):
        volts_up = np.arange(self.start_voltage, self.stop_voltage, self.voltage_step)
        # volts_down = np.arange(self.stop_voltage, self.start_voltage, -self.voltage_step)
        # volts = np.concatenate((volts_up, volts_down))  # Include the reverse
        # volts *= 1e-3  # to mA from A
        volts_up *= 1e-3
        # steps = len(volts)
        steps = len(volts_up)

        log.info("Starting to sweep through current")
        # for i, voltage in enumerate(volts):
        for i, voltage in enumerate(volts_up):
            log.debug("Measuring voltage: %g mV" % voltage)

            # self.source.source_current = current
            self.source.source_voltage = voltage
            # Or use self.source.ramp_to_current(current, delay=0.1)
            sleep(self.delay * 1e-3)
            log.info("Current = " + str(self.source.current))
            current = self.source.current
            data = {
                'Current (A)': current,
                'Voltage (V)': voltage
            }
            self.emit('results', data)
            self.emit('progress', 100. * i / steps)
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        self.source.shutdown()
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super().__init__(
            procedure_class=IVProcedure,
            inputs=[
                 'voltage_step', 'current_range',
                'delay', 'start_voltage', 'stop_voltage'
            ],
            displays=[
                'voltage_step', 'current_range',
                'delay', 'start_voltage', 'stop_voltage'
            ],
            x_axis='Voltage (V)',
            y_axis='Current (A)'
        )
        self.setWindowTitle('IV Measurement')

    def queue(self):
        directory = "./"  # Change this to the desired directory
        filename = unique_filename(directory, prefix='IV')

        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
