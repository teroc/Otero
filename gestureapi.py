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

class GestureApi(object):
    ###########################
    # tap (and hold) gestures #
    ###########################

    # arguments
    # pos:      position to tap within work area
    # duration: minimum time to hold between press and release, 0.0 indicates ordinary tap

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; tap pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # touchAngle

    def tap(self, pos, duration=0.0, **kwargs):
        raise NotImplementedError

    ###########################################
    # drag gestures                           #
    # (sharp begin, straight move, sharp end) #
    ###########################################

    # arguments
    # beginPos:      beginning position of drag within work area
    # endPos:        ending position of drag within work area
    # beginDuration: minimum duration to hold between press and move
    # endDuration:   minimum duration to hold between move and release

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; drag pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move

    def drag(self, beginPos, endPos, beginDuration=0.0, endDuration=0.0, **kwargs):
        raise NotImplementedError

    #############################################
    # swipe gestures                            #
    # (smooth begin, straight move, smooth end) #
    #############################################

    # arguments
    # beginPos:      beginning position of swipe within work area
    # endPos:        ending position of swipe within work area

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; swipe pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move

    def swipe(self, beginPos, endPos, **kwargs):
        raise NotImplementedError

    ############################################
    # flick gestures                           #
    # (sharp begin, straight move, smooth end) #
    ############################################

    # arguments
    # beginPos:      beginning position of flick within work area
    # endPos:        ending position of flick within work area

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; flick pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move

    def flick(self, beginPos, endPos, **kwargs):
        raise NotImplementedError

