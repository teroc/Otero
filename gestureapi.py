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

class GestureApi(object):
	###########################
	# tap (and hold) gestures #
	###########################
	
	# arguments
	# pos:      position to tap within target area (entire work area for tapPos)
	# duration: minimum time to hold between press and release, 0.0 indicates ordinary tap 
	
	# kwargs recommendations
	# bypassSafety: bool; ignore safety restrictions in movement area
	# pressure:     float; tap pressure (0.0 no pressure, 1.0 greatest safe pressure)
	# fingerRadius: float; finger radius in millimeters
	# touchAngle
	
	def tap(self, pos, duration=0.0, **kwargs):
		raise NotImplementedError

	###########################################
	# scroll (and drag) gestures              #
	# (sharp begin, straight move, sharp end) #
	###########################################
	
	# arguments
	# beginPos:      beginning position of scroll
	# endPos:        ending position of scroll
	# beginDuration: minimum duration to hold between press and move
	# endDuration:   minimum duration to hold between move and release
	
	# kwargs recommendations
	# bypassSafety: bool; ignore safety restrictions in movement area
	# scrollDuration: duration of move
	
	def scroll(self, beginPos, endPos, beginDuration=0.0, endDuration=0.0, *kwargs):
		raise NotImplementedError

