import sys
import random
import tempfile
from time import sleep

from pymeasure.display.inputs import ScientificInput
from pymeasure.experiment import Procedure, IntegerParameter, Parameter, FloatParameter, ListParameter
from pymeasure.experiment import Results
from pymeasure.display.console import ManagedConsole
from pymeasure.display.Qt import QtWidgets
from pymeasure.display.windows import ManagedWindow
import logging

from pymeasure.instruments import list_resources
from pymeasure.instruments.keithley.keithley2400 import Keithley2400

log = logging.getLogger('')
log.addHandler(logging.NullHandler())
resources = list_resources()


class TestProcedure(Procedure):
    iterations = IntegerParameter('Loop Iterations', default=100)
    delay = FloatParameter('Delay Time', units='s', default=0.2)
    seed = Parameter('Random Seed', default='12345')
    resource_list = ListParameter("Choose Device", resources)
    DATA_COLUMNS = ['Iteration', 'Random Number']
    def startup(self):
        log.info("Setting up random number generator")
        Keithley2400(resources[1])
        random.seed(self.seed)

    def execute(self):
        log.info("Starting to generate numbers")
        for i in range(self.iterations):
            data = {
                'Iteration': i,
                'Random Number': random.random()
            }
            log.debug("Produced numbers: %s" % data)
            self.emit('results', data)
            self.emit('progress', 100 * (i + 1) / self.iterations)
            sleep(self.delay)
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super(MainWindow, self).__init__(
            procedure_class=TestProcedure,
            inputs=['iterations', 'delay', 'seed', 'resource_list'],
            displays=['iterations', 'delay', 'seed', 'resource_list'],
            x_axis='Iteration',
            y_axis='Random Number'
        )
        self.setWindowTitle('GUI Example')

    def queue(self):
        filename = tempfile.mktemp()

        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())