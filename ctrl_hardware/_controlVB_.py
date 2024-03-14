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

import os, sys, requests
from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, DmmFunction

# Caminho para o diretório ctrl_hardware
ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
# Adiciona o diretório ao sys.path
sys.path.append(ctrl_hardware_path)

# You will probably need to replace "myVirtualBench" with the name of your device.
# By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
# You can see the device's name in the VirtualBench Application under File->About
virtualbench = PyVirtualBench('VB8012-30A210F')

#from shift_register import SRoutput

# This examples demonstrates how to make measurements using the Power
    
def config_Parameters (Vcc:int, Resistence:int):
    #Vcc = int(Vcc) # É passado o parâmetro em forma de string mas é necessária a conversão para int
    #Resistence = int(Resistence)

    #############################
    # Power Supply Configuration
    #############################
    channel = "ps/+25V"
    voltage_level = Vcc
    current_limit = 0.5

    ps = virtualbench.acquire_power_supply()

    ps.configure_voltage_output(channel, voltage_level, current_limit)
    ps.enable_all_outputs(True)

    dmm = virtualbench.acquire_digital_multimeter();
    dmm.configure_measurement(DmmFunction.DC_VOLTS, True, 10.0)

    measurement_result = dmm.read()

    print("MeasurementV: %f V" % (measurement_result))
    print("MeasurementR: %f KOhm" % (Resistence))
   
    dmm.release()
    ps.release()    

    return measurement_result
