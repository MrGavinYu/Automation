# @Author: Gavin Yu <jw.yu@zju.edu.cn>
""" Controller of Thorlabs Motor BBD2xx and BBD1xx

BBD -- Class of Controller
"""
import clr
import os, sys
import platform

__all__ = ['BBD']

# TODO: Need to add the file Thorlabs-32bit
dll_path = os.path.dirname(os.path.abspath(__file__)) + '\\Thorlabs-' + platform.architecture()[0]
if dll_path not in sys.path:
    sys.path.append(dll_path)

clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("System")

