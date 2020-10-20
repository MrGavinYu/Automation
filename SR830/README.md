# BBD2xx

Package SR830 is used to control Standford SR830.

## Installation

Download SR830-\*.whl from the release page, and run the following command in command line:

```shell
pip install SR830-*.whl
```

## Usage

### Import

```Python
from SR830 import *
```

This will import class SR830, Enum-class Tau and Sen.

### Create an Instance
  
```Python
device = SR830(port)
```

where 
port: the serial port name of SR830, it can be ignored if there is only one GPIB device.

### Control

You can get or set parameter xxx using get_xxx and set_xxx. For example.

```Python
device.set_freq(10e3) # Set Frequency as 10kHz
device.get_freq() # Get Frequency
...
```

There are 2 parameters(sensitivity and time constant) different from others because you can only set some discrete numbers to them.

```Python
device.set_sens(Sen.Sen_2nV) # Set sensitivity as 2nV/fA
device.get_sens() # will return string '2nV'
device.set_tau(Tau.Tau_10mus) # Set time constant as 10mus
device.get_tau() # will return string '10mus'
```

## Document For Developers

Developement document of SR830 is placed in '/documents/SR830' under root folder.

## Feedback

Mail: [Gavin Yu](mailto:jw.yu@zju.edu.cn)
