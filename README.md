# Keithley 2400 Measurement GUI

A small Python desktop tool I wrote for a university physics lab to control a **Keithley 2400 SourceMeter** and plot measurements live, instead of reading values off the instrument by hand.

## What it measures

| Mode | File | What it does |
|---|---|---|
| I–V (current vs. voltage) | `keithley2400VoltageToCurrent.py` | You set a source voltage and a current compliance limit; the app reads voltage and current about once per second and plots I against V as you change the voltage. |
| Current vs. time | `keithley2400CurrentToTime.py` | Holds a fixed source voltage and plots the measured current over time (about one sample per second, last 100 points). |
| Automated I–V sweep | `appTest.py` | Sweeps the voltage from a start value to a stop value in fixed steps, records current at each step and saves the data to a file. Adapted from the PyMeasure IV example (license header kept). |

`mainApp.py` is the launcher: choose the "From" and "To" quantities (V to I, or I to Time) and it opens the matching window.
`test.py` is an early PyMeasure GUI test used to check the instrument connection; it does not measure anything physical.

## How it works

- **Instrument control:** [PyMeasure](https://pymeasure.readthedocs.io/)'s `Keithley2400` driver over GPIB (VISA address `GPIB0::28::INSTR`).
- **GUI and live plotting:** PyQt5 and pyqtgraph; a `QTimer` polls the instrument every second.
- **Safety:** every mode sets a compliance limit before the source is turned on, and there is an explicit on/off toggle.

## Running it

```bash
pip install -r requirements.txt
python mainApp.py
```

You need a Keithley 2400 connected via GPIB and a VISA backend (NI-VISA, or `pyvisa-py`). If your instrument uses a different address, change `GPIB0::28::INSTR` in the two instrument files.

## Limitations

This was a working lab tool, not a polished package: settings are typed in as plain numbers without validation, the address is hard-coded, and there are no automated tests because everything depends on the physical instrument.
