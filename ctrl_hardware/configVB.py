#! /usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Charles Armstrap <charles@armstrap.org>
# If you like this library, consider donating to: https://bit.ly/armstrap-opensource-dev
# Anything helps.
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

import os, sys

# Caminho para o diretório ctrl_hardware
ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
# Adiciona o diretório ao sys.path
sys.path.append(ctrl_hardware_path)

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, DmmFunction

# You will probably need to replace "myVirtualBench" with the name of your device.
# By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
# You can see the device's name in the VirtualBench Application under File->About
virtualbench = PyVirtualBench('VB8012-30A210F')


'''
The provided script, config_VB_DMM, can be improved to ensure the 
ps = virtualbench.acquire_power_supply() line is executed only once by utilizing the concept of 
lazy initialization.
'''

class VirtualBenchManager:
    """
    This class manages the acquisition and release of virtual bench instruments.
    It utilizes lazy initialization to ensure instruments are acquired only once.
    """
    def __init__(self):
        """
        Initializes the manager with private variables to store instrument references.
        """
        self._ps = None # Power supply instrument (initially None)
        self._dmm = None # Digital multimeter instrument (initially None)

    def acquire_power_supply(self):

        """
        Acquires a power supply instrument from virtualbench.
        Uses lazy initialization to acquire the instrument only if it hasn't been acquired yet.

        Returns:
        The acquired power supply instrument.
        """
        if self._ps is None:
            self._ps = virtualbench.acquire_power_supply() 
        return self._ps

    def acquire_digital_multimeter(self):
        """
        Acquires a digital multimeter instrument from virtualbench.
        Uses lazy initialization to acquire the instrument only if it hasn't been acquired yet.

        Returns:
        The acquired digital multimeter instrument.
        """
        if self._dmm is None:
            self._dmm = virtualbench.acquire_digital_multimeter()
        return self._dmm

    def release_instruments(self):
        """
        Releases the acquired instruments (power supply and multimeter) if they exist.

        """
        if self._ps:
            self._ps.release()
        self._ps = None
        if self._dmm:
            self._dmm.release()
        self._dmm = None

    def configure_voltage_output(self, channel, voltage_level, current_limit):
        """
        Configures the voltage output of the acquired power supply.

        Args:
        channel: The channel to configure.
        voltage_level: The voltage level to set.
        current_limit: The current limit to apply.
        """
        self._ps.configure_voltage_output(channel, voltage_level, current_limit)

    def enable_all_outputs(self):
        """
        Enables all outputs of the acquired power supply.
        """
        self._ps.enable_all_outputs(True)

vb_manager = VirtualBenchManager()  # Create a single instance

def config_VB_DMM (Vcc:int, configMeasure:str):
    try:
        #############################
        # Power Supply Configuration
        #############################

        channel = "ps/+25V"
        voltage_level = Vcc
        current_limit = 0.5
        ps = vb_manager.acquire_power_supply()
        # ... use ps for configuration ...    ps.configure_voltage_output(channel, voltage_level, current_limit)

        ps.configure_voltage_output(channel, voltage_level, current_limit)
        ps.enable_all_outputs(True)
      
        dmm = vb_manager.acquire_digital_multimeter()
        # ... use dmm for configuration ...
        if configMeasure == "voltage":
            dmm.configure_measurement(DmmFunction.DC_VOLTS, True, 10)
        elif configMeasure == "current":
            dmm.configure_measurement(DmmFunction.DC_CURRENT, True, 1) # Verificar Manual Range = 10.0
        
        measurement_result = dmm.read()

    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        vb_manager.release_instruments()

        #virtualbench.release()
    return measurement_result
