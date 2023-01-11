# Copyright (C) 2022 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from adi.context_manager import context_manager
from adi.jesd import jesd
from adi.rx_tx import tx
from adi.sync_start import sync_start


class ad9162(tx, context_manager, sync_start):
    """ AD9162 16-Bit, 12 GSPS, RF DAC """

    _complex_data = False
    # _complex_data = True
    _tx_channel_names = ["voltage0_i", "voltage0_q"]
    _device_name = ""

    def __init__(self, uri="", username="root", password="analog"):

        context_manager.__init__(self, uri, self._device_name)

        self._jesd = jesd(uri, username=username, password=password)
        self._txdac = self._ctx.find_device("axi-ad9162-hpc")

        tx.__init__(self)

    @property
    def fir85_enable(self):
        return self._get_iio_attr("voltage0_i", "fir85_enable", True, self._txdac)

    @fir85_enable.setter
    def fir85_enable(self, value):
        self._set_iio_attr("voltage0_i", "fir85_enable", True, value, self._txdac)

    @property
    def sample_rate(self):
        """sample_rate: Sample frequency rate TX path in samples per second."""
        return self._get_iio_attr("voltage0_i", "sampling_frequency", True, self._txdac)

    @property
    def scale(self):
        return self._get_iio_attr("voltage0_i", "scale", True, self._txdac)

    @property
    def frequency_nco(self):
        return self._get_iio_attr("altvoltage4", "frequency_nco", True, self._txdac)

    @frequency_nco.setter
    def frequency_nco(self, value):
        self._set_iio_attr("altvoltage4", "frequency_nco", True, value, self._txdac)

    @property
    def jesd204_statuses(self):
        return self._jesd.get_all_statuses()