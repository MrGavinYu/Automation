# @Author: Gavin Yu <jw.yu@zju.edu.cn>
"""
This is a module in order to control Stanford SR830.

Reference: https://github.com/ari1127/SR830/blob/master/SR830.py
"""

import pyvisa
from enum import Enum

__all__ = ['Tau', 'Sen', 'SR830']


class Tau(Enum):
    Tau_10mus = 0
    Tau_30mus = 1
    Tau_100mus = 2
    Tau_300mus = 3
    Tau_1ms = 4
    Tau_3ms = 5
    Tau_10ms = 6
    Tau_30ms = 7
    Tau_100ms = 8
    Tau_300ms = 9
    Tau_1s = 10
    Tau_3s = 11
    Tau_10s = 12
    Tau_30s = 13
    Tau_100s = 14
    Tau_300s = 15
    Tau_1ks = 16
    Tau_3ks = 17
    Tau_10ks = 18
    Tau_30ks = 19


class Sen(Enum):
    Sen_2nV = 0
    Sen_5nV = 1
    Sen_10nV = 2
    Sen_20nV = 3
    Sen_50nV = 4
    Sen_100nV = 5
    Sen_200nV = 6
    Sen_500nV = 7
    Sen_1muV = 8
    Sen_2muV = 9
    Sen_5muV = 10
    Sen_10muV = 11
    Sen_20muV = 12
    Sen_50muV = 13
    Sen_100muV = 14
    Sen_200muV = 15
    Sen_500muV = 16
    Sen_1mV = 17
    Sen_2mV = 18
    Sen_5mV = 19
    Sen_10mV = 20
    Sen_20mV = 21
    Sen_50mV = 22
    Sen_100mV = 23
    Sen_200mV = 24
    Sen_500mV = 25
    Sen_1V = 26


class SR830:
    def __init__(self, port=0):
        self._port = port
        self._rm = pyvisa.ResourceManager()
        if port == 0:
            ___devices_list = self._rm.list_resources()
            for s in ___devices_list:
                if s[:4] == 'GPIB':
                    self._port = s
                    break
        if self._port == 0:
            raise Exception('No devices available!')
        self._device = self._rm.open_resource(self._port)

    def reset(self):
        self._device.write('*RST')

    def clear(self):
        self._device.write('*CLS')

    def disable_front_panel(self):
        self._device.write('OVRM 1')

    def enable_front_panel(self):
        self._device.write('OVRM 0')

    def auto_phase(self):
        self._device.write('APHS')

    def auto_gain(self):
        self._device.write('AGAN')

    def auto_reserve(self):
        self._device.write('ARSV')

    def auto_offset(self, channel):
        self._device.write('AOFF %i' % channel)

    # get settings
    def get_tau(self):
        return Tau(int(self._device.query('OFLT?'))).name[4:]

    def get_sens(self):
        return Sen(int(self._device.query('SENS?'))).name[4:]

    def get_trigsource(self):
        return self._device.query('FMOD?')

    def get_trigshape(self):
        return self._device.query('RSLP?')

    def get_harm(self):
        return self._device.query('HARM?')

    def get_input(self):
        return self._device.query('ISRC?')

    def get_ground(self):
        return self._device.query('IGND?')

    def get_couple(self):
        return self._device.query('ICPL?')

    def get_filter(self):
        return self._device.query('ILIN?')

    def get_reserve(self):
        return self._device.query('RMOD?')

    def get_slope(self):
        return self._device.query('OFSL?')

    def get_sync(self):
        return self._device.query('SYNC?')

    def get_disp_rat(self, channel):
        return self._device.query('DDEF? %i' % channel)

    def get_exp_off(self, channel):
        return self._device.query('OEXP? %i' % channel)

    # set settings
    def set_freq(self, freq):
        self._device.write('FREQ %f' % freq)

    def set_ampl(self, ampl):
        self._device.write('SLVL %f' % ampl)

    def set_mode(self, mode):
        self._device.write('FMOD %i' % mode)

    def set_tau(self, tau):
        if tau not in Tau:
            raise IndexError('Invalid tau value!')
        self._device.write('OFLT %i' % tau.value)

    def set_sens(self, sens):
        if sens not in Sen:
            raise IndexError('Invalid sensitivity value!')
        self._device.write('SENS %i' % sens.value)

    def set_phase(self, phase):
        self._device.write('PHAS %f' % phase)

    def set_aux(self, output, value):
        self._device.write('AUXV %(out)i, %(val).3f' % {'out': output, 'val': value})

    def set_trigsource(self, ref):
        self._device.write('FMOD %e' % ref)

    def set_trigshape(self, trigshape):
        self._device.write('RSLP %i' % trigshape)

    def set_disp_rat(self, channel, disp, ratio):
        self._device.write('DDEF %(channel)i, %(disp)i, %(ratio)i' % {'channel': channel, 'disp': disp, 'ratio': ratio})

    def set_exp_off(self, channel, offset, expand):
        self._device.write(
            'OEXP %(channel)i, %(offset)f, %(expand)i' % {'channel': channel, 'offset': offset, 'expand': expand})

    def set_reserve(self, reserve):
        self._device.write('RMOD %i' % reserve)

    def set_filter(self, filt):
        self._device.write('ILIN %i' % filt)

    def set_input(self, inp):
        self._device.write('ISRC %i' % inp)

    def set_ground(self, gnd):
        self._device.write('IGND %i' % gnd)

    def set_couple(self, coup):
        self._device.write('ICPL %i' % coup)

    def set_slope(self, slope):
        self._device.write('OFSL %i' % slope)

    def set_sync(self, sync):
        self._device.write('SYNC %i' % sync)

        # get data

    def get_all(self):
        return self._device.query("SNAP?1,2,3,4")

    def get_X(self):
        return float(self._device.query('OUTP? 1'))

    def get_Y(self):
        return float(self._device.query('OUTP? 2'))

    def get_R(self):
        return float(self._device.query('OUTP? 3'))

    def get_Theta(self):
        return float(self._device.query('OUTP? 4'))

    def get_freq(self):
        return float(self._device.query('FREQ?'))

    def get_ampl(self):
        return float(self._device.query('SLVL?'))

    def get_phase(self):
        return float(self._device.query('PHAS?'))

    def get_harm(self):
        return float(self._device.query('HARM?'))

    def get_oaux(self, value):
        return float(self._device.query('OAUX? %i' % value))

    def read_aux(self, output):
        return float(self._device.query('AUXV? %i' % output))
