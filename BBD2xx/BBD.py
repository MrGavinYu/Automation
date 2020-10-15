"""
This file contains a global function get_all_BBD_sn and class BBD
get_all_BBD_sn: used to get all BBD devices` serial number.
BBD: mainly to control single channel of BBD201、BBD202、BBD203.

TODO: Need to modify the code from 1 channel to 3 channel
"""

import clr
import time

clr.AddReference('Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI')
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI import *
from System import Decimal
import numpy as np

# TODO: An Example.
# TODO: Automatically find the net dll.

def get_all_BBD_sn():
    try:
        DeviceManagerCLI.BuildDeviceList()
    except Exception as e:
        raise RuntimeError('Exception raise by BuildDeviceList ', e)
    return DeviceManagerCLI.GetDeviceList(BenchtopBrushlessMotor.DevicePrefix)


class BBD:
    """
    Control class of BBD device, all distance unit is mm and time unit is s.
    """
    def __init__(self, serial_number=0, channel_no=1, is_simulator=False):
        """
        :param serial_number: Serial Number of Device
        :param channel_no: No. of channel
        :param is_simulator: Decide if running a simulator
        """
        self.__device = None
        self.__channel_no = channel_no
        self.__channel = None
        self.__is_simulator = is_simulator
        self.__sn = str(serial_number)

        if is_simulator:
            SimulationManager.Instance.InitializeSimulations()

        sn_list = get_all_BBD_sn()
        if len(sn_list) == 0:
            raise ModuleNotFoundError('No devices connected')
        if serial_number == 0:
            self.__sn = sn_list[0]
        self.connect()

    def __del__(self):
        self.disconnect()
        if self.__is_simulator:
            SimulationManager.Instance.UninitializeSimulations()

    def is_connect(self):
        """
        :return: Is device connected.
        """
        if self.__device is not None:
            return self.__device.GetConnectionState() != ThorlabsConnectionManager.ConnectionStates.Disconnected

    def get_device_info(self):
        """
        :return: Return a channel device info
        """
        if self.is_connect():
            return self.__channel.GetDeviceInfo()

    def get_settings(self):
        """
        :return: Return a channel device motor settings.
        """
        if self.is_connect():
            return self.__channel.MotorDeviceSettings

    def get_position(self):
        """
        :return: Return a position(unit:mm) with 4 decimals due to BBD201 have max precision of 200nm
        """
        # The max precision is 200nm and unit is mm, so we keep 4 decimals.
        return float(self.__channel.DevicePosition.ToString("f4"))

    def disconnect(self):
        """
        Disconnect the channel and control device.
        """
        if self.is_connect():
            self.channel_disconnect()
            self.__device.Disconnect(False)
            self.__device.ShutDown()
        self.__device = None
        self.__channel = None

    def channel_disconnect(self):
        if self.is_channel_connect():
            self.__channel.StopPolling()
            self.__channel.Disconnect(False)
            self.__channel.ShutDown()

    def connect(self):
        """
        Connect a device and a channel
        """
        self.disconnect()
        serial_numbers = get_all_BBD_sn()
        if self.__sn not in serial_numbers:
            raise RuntimeError('%s is not a valid serial number' % self.__sn)

        self.__device = BenchtopBrushlessMotor.CreateBenchtopBrushlessMotor(self.__sn)
        if self.__device is None:
            raise RuntimeError('%s is not a BenchtopBrushlessMotor' % self.__sn)

        try:
            self.__device.Connect(self.__sn)
        except Exception as e:
            raise RuntimeError('Failed to open device %s' % self.__sn, e)

        self.__channel = self.__device.GetChannel(self.__channel_no)

        if self.__channel is None:
            raise RuntimeError('Channel unavailable')

        if self.__channel.IsSettingsInitialized():
            try:
                self.__channel.WaitForSettingsInitialized(5000)
            except Exception as e:
                raise RuntimeError('Settings failed to initialize', e)
        self.enable_channel()
        self.home()
        self.move_to(20)

    def enable_channel(self):
        if self.is_connect():
            self.__channel.StartPolling(250)
            time.sleep(0.5)
            self.__channel.EnableDevice()
            time.sleep(0.5)
            self.__channel.LoadMotorConfiguration(self.__channel.DeviceID)

    def home(self, timeout=30000):
        if self.__channel is not None:
            try:
                self.__channel.Home(timeout)
            # The BBD201 in our laboratory has a defect resulting a forbidden area under coordinate 17mm.
            # Solution is ignore it.
            except MoveTimeoutException as e:
                self.__ignore_error()
            except Exception as e:
                raise RuntimeError('Failed to home device', e)

    def is_channel_enable(self):
        if self.is_channel_connect():
            return self.__channel.IsEnabled
        return False

    def is_channel_connect(self):
        if self.is_connect():
            return self.__channel is not None and self.__channel.IsConnected
        return False

    def get_channel(self):
        return self.__channel

    def move_to(self, position, time_out=60000):
        """
        :param position: New position(unit:mm)
        :param time_out: Timeout of this Routine
        :return:
        """
        if self.is_channel_enable():
            try:
                self.__channel.MoveTo(Decimal(position), time_out)
            except MoveTimeoutException as e:
                self.ignore_error()
            except Exception as e:
                raise RuntimeError('Failed to move to position', e)

    def move_relative(self, distance, time_out=60000):
        """
        :param distance: Relative distance(unit:mm) to move, if it is negative moving backward and forward if positive.
        :param time_out: Timeout of this method
        """
        if self.is_channel_enable():
            try:
                if distance < 0:
                    self.__channel.MoveRelative(MotorDirection.Backward, Decimal(abs(distance)), time_out)
                else:
                    self.__channel.MoveRelative(MotorDirection.Forward, Decimal(distance), time_out)
            except MoveTimeoutException as e:
                self.ignore_error()
            except Exception as e:
                raise RuntimeError('Failed to move to position', e)

    def is_homed(self):
        if self.is_channel_enable():
            return self.__channel.IsHomed

    def set_v(self, v, **kwargs):
        """
        :param v: Max Velocity
        :param kwargs:
        Acceleration:
        MinVelocity:
        :return:
        """
        if self.__channel is not None:
            vel_pars = self.__channel.GetVelocityParams()
            vel_pars.MaxVelocity = v
            if 'Acceleration' in kwargs.keys():
                vel_pars.Acceleration = kwargs['Acceleration']
            if 'MinVelocity' in kwargs.keys():
                vel_pars.MinVelocity = kwargs['MinVelocity']
            self.__channel.SetVelocityParams(vel_pars)

    def __ignore_error(self):
        if self.get_position() < 17:
            self.enable_channel()
        else:
            raise MoveTimeoutException('Unknown Exception at %fmm' % self.get_position())

    def reset_if_stuck(self, position_list):
        """
        We have done some tests showing that if you move more than 10000 times in single connection,
        the device would be stuck in a point.
        Solution is test if the position is still there for long time, if it is, reset the connection.
        :param position_list: Position list you get from the device.
        :return: Return True if it is stuck otherwise False.
        """
        dif = np.diff(position_list)
        dif = np.round(dif, 5)
        if sum(dif > 0.00001) == 0:
            self.disconnect()
            self.connect()
            return True
        return False

