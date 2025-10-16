## Objectives
This project is an integral part of the Master’s Dissertation entitled "LaRE – Expandable Remote Laboratory".
It implements and manages a remote laboratory for electronics education, designed as a viable alternative to VISIR, with the additional commitment of being an open-source project, accessible to any educational institution regardless of geographical location.

The board matrix, the core element of the system, was developed based on a software-controlled architecture, independent of proprietary platforms, thereby ensuring that the system can be used without the need for commercial licenses. However, due to the current lack of support for the pyVirtualBench library on Linux systems and ARM architectures, the implementation of LaRE remains, at this stage, dependent on Windows systems — a factor that limits its adoption in more versatile and low-cost educational platforms.
Nevertheless, the modular architecture of LaRE enables future expansions and adaptations to different pedagogical contexts.

This dissertation partially fulfills the requirements defined in the Course Unit of Dissertation/Thesis of the 2nd year of the Master’s Degree in Electrical and Computer Engineering, specialization area in Automation and Systems.


## Helpful Resources
The original Flask structure was simplified and adapted to better suit the project’s requirements.
Some of the Flask features were inspired by a YouTube tutorial, which served as a reference for understanding the basic setup of routes, templates, and frontend communication - https://www.youtube.com/watch?v=dam0GPOAvVI
The pyVirtualBench library can be found here: https://github.com/armstrap/armstrap-pyvirtualbench
Additional information: http://armstrap.org/2015/07/27/pyvirtualbench-controlling-five-instruments-from-a-single-python-application/

## Requirements (Windows Only)
* [NI VirtualBench hardware](http://www.ni.com/virtualbench/)
* [VirtualBench driver >= 1.1.0](https://www.ni.com/en-us/support/downloads/drivers/download.virtualbench-software.html#324215)
  Be sure to check "ANSI C Support" during installation.
    ![NiInstaller](https://github.com/armstrap/armstrap-pyvirtualbench/raw/master/images/ni-virtualbench-installer.png)
* [Python >= 3.4](https://www.python.org/downloads/).  You will need 32-bit Python support to work with the NI-provided drivers.

## Dependencies
Refer to the requirements.txt file: pip install -r requirements.txt