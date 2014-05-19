# Copyright (c) 2014 Tampere University of Technology,
#                    Intel Corporation,
#                    OptoFidelity,
#                    and authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pylint: disable = C0103, C0111, C0302, C0326
# pylint: disable = R0902, R0903, R0904, R0911, R0912, R0913, R0914, R0915
# pylint: disable = W0212

import unittest
import opentestrobot
import os

try:
    import fmbtgti
    g_fmbtAvailable = True
except ImportError:
    g_fmbtAvailable = False

moduleDir = os.path.dirname(__file__)

class TestSwEmulation(unittest.TestCase):
    def setup(self):
        pass

    def tearDown(self):
        pass

    def _verifyLastEvent(self, gti, event, args):
        lastEvent = gti.connection().history()[-1]
        assert lastEvent[1] == event, ('Wrong event, got "%s" expected "%s"' %
                                       (lastEvent[1], event))
        assert lastEvent[2] == args, ('Wrong args, got "%s" expected "%s"' %
                                      (lastEvent[2], args))

    @unittest.skipIf(not g_fmbtAvailable, "fMBT is not available")
    def testTap(self):
        """Test UserInteraction API with simulated software emulation
        """
        gti = fmbtgti.GUITestInterface()
        gti.setConnection(fmbtgti.SimulatedGUITestConnection(
            [os.path.join(moduleDir, "images", "nexus-s-dial.png")]))

        ui = opentestrobot.UserInteraction(
            opentestrobot.gesture.SwEmulation(gti),
            opentestrobot.vision.SwEmulation(gti))

        ui.tap((0.5, 0.5)) # tap the middle of the screen

        self._verifyLastEvent(gti, "sendTap", (240, 400))

        ui.tapImage("images/call.png")

        self._verifyLastEvent(gti, "sendTap", (239, 751))

        ui.tapText("6:29")

        self._verifyLastEvent(gti, "sendTap", (447, 20))
