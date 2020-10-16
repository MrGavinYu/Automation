# BBD2xx

Package BBD2xx is used to control Thorlabs BBD201、BBD202 and BBD203.
It depends on the Thorlabs .NET library kinesis(which is already in the package) and pythonnet.

## Installation

Download BBD2xx-\*.whl from the release page, and run the following command in command line:

```shell
pip install BBD2xx-*.whl
```

## Usage

### Import

```Python
from BBD2xx imprt BBD
```

### Create an Instance
  
```Python
device = BBD.BBD(serial_number=73000001, channel_no=1, is_simulator=False)
```

where 
serial_number: the serial number of your BBD2xx device, if your only connect 1 device, you don`t have to pass the parameter.
channel_no: the channel number of the device you want to control.
is_simulator: pass True to run on the simulator, you need to start the Kinesis Simulator and create a BBD device first.

### Control

```Python
device.move_to(0.1)
#Move to absolute coordinate 0.1mm, the precision of the BBD is 0.2um.
device.move_relative(0.001)
#Move forward for 0.001mm, pass a negative number to move backward.
device.home()
#Move home 
device.get_position()
#Return an absolute position in unit mm.
```
There is one thing need to point out that the BBD201 in our lab has a defect resulting a forbidden area under coordinate 17mm. If you move to a forbidden area, the kinesis function will throw an error, and our package will ignore it.

### Exception Handling

All moving method such as move_to, move_relative, home etc. has a default parameter called timeout(unit:ms), if the moving operation cannot be done within timeout, it will throw an MoveTimeoutException(you can import the exception from BBD2xx.BBD)

For example,
```Python
try:
    device.move_relative(0.001)
except MoveTimeoutException as e:
    # Done some reset operation
    device.reset()
    print('Some Unknown Reason', e)
```

From our experience, the BBD201 motor will be stuck if you move continuously more than 10000 steps, so I recommend you to use reset_if_stuck method. You need to pass some continuous positions you sampled from the device, and the method will automatically detect whether these positions is same, if they are same, it will reset the motor and return True. The following code is an example.

```Python
while device.get_position() < 100:
	data.append(device.get_position())
	if len(data) % 100 == 0:
		if device.reset_if_stuck(data[-100:]):
			print('Stuck At %f' % data[-1])
		device.move_to(data[-1])
```

## Test

A test script is placed in '/test' folder.

## Document For Developers

Developement document of Kinesis is placed in '/documents/BBD2xx' under root folder.

## Feedback

Mail: [Gavin Yu](mailto:jw.yu@zju.edu.cn)
