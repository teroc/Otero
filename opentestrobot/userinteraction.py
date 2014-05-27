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

"""
Example: Control robot with Optofidelity's HTTP API, use a
Video4Linux2 camera as machine vision image source.

>>> from opentestrobot import UserInteraction, vision, gesture
>>> ui = UserInteraction(
...     vision.V4l2(device="/dev/video0", format=(1920, 1080)),
...     gesture.OptoHttp("http://192.168.33.99:8080/"))
>>> ui.vision().refresh()
>>> ui.tapImage("homescreen-browser.png")

Example: Use the same USB connection to an Android device for both
taking screenshots and synthesizing user events.

>>> import fmbtandroid
>>> device = fmbtandroid.Device()
>>> from opentestrobot import UserInteraction
>>> ui = UserInteraction(
...     vision.SwEmulation(device),
...     gesture.SwEmulation(device))
>>> ui.vision().refresh()
>>> ui.tapImage("homescreen-browser.png")
"""

from guielements import *

class UserInteraction(object):
    """UserInteraction provides convenience API on top of gesture and vision
    """

    # argument types
    # pos:       tuple of two floats;   x, y coordinates, by default unity coordinates with origin at upper left corner of target area and (1.0, 1.0) at lower right corner, x increasing right and y increasing down
    # imageUri:  str;                   URI; with file URI, extension may be left out and default determined by observation module will be used
    # text:      str;                   text
    # element:   element object;        work area subpart
    # angle:     float;                 angle in degrees, clockwise from top unless otherwise indicated
    # distance:  float;                 length of gesture as proportion of maximal possible, maximum depends on gesture
    # duration:  float;                 time in seconds
    # timeout:   float;                 time in seconds

    WORK_AREA = Rectangle((0, 0), (1, 1))

    ANGLE_UP = 0.0
    ANGLE_RIGHT = 90.0
    ANGLE_DOWN = 180.0
    ANGLE_LEFT = 270.0

    def __init__(self, visionInstance, gestureInstance, locateTimeout=0):
        self._vision = visionInstance
        self._gesture = gestureInstance
        self._locateTimeout = locateTimeout

    # confirmed methods

    ###########################
    # tap (and hold) gestures #
    ###########################

    # arguments
    # element:       element to tap
    # image:         image to tap
    # text:          text to tap
    # pos:           position to tap within target area (entire work area for tapPos)
    # duration:      minimum time to hold between press and release, 0.0 indicates ordinary tap
    # locateTimeout: time to poll the system before giving up if item to be located is not found

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; tap pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # touchAngle

    def tap(self, pos, duration=0.0, **kwargs):
        return self._gesture.tap(pos, duration, **kwargs)

    def tapElement(self, element=WORK_AREA, pos=(0.5, 0.5), duration=0.0, **kwargs):
        return self.tap(element.getPos(pos), duration, **kwargs)

    def tapImage(self, imageUri, pos=(0.5, 0.5), duration=0.0, locateTimeout=None, **kwargs):
        # TODO: split kwargs to locateImage and tap
        locations = self.locateImage(imageUri, locateTimeout)
        if not locations:
            raise ImageNotRecognizedError(imageUri)
        return self._gesture.tap(locations[0].getPos(), duration)

    def tapText(self, text, pos=(0.5, 0.5), duration=0.0, locateTimeout=None, **kwargs):
        locations = self.locateText(text, locateTimeout)
        if not locations:
            raise TextNotRecognizedError(text)
        return self._gesture.tap(locations[0].getPos(), duration)

    ###########################################
    # drag gestures                           #
    # (sharp begin, straight move, sharp end) #
    ###########################################

    # arguments
    # beginElement:  element within which drag begins
    # endElement:    element within which drag ends (if angle is not given)
    # beginImage:    image within which drag begins
    # endImage:      image within which drag ends (if angle is not given)
    # beginText:     text within which drag begins
    # endText:       text within which drag ends (if angle is not given)
    # beginPos:      beginning position of drag within target area (entire work area for drag)
    # endPos:        ending position of drag within target area (entire work area for drag)
    # angle:         direction of drag gesture, if given pre-empts parameters for end position
    # distance:      distance to drag as proportion of distance from begin towards edge of work area, effective only if angle is given
    # beginDuration: minimum duration to hold between press and move
    # endDuration:   minimum duration to hold between move and release
    # locateTimeout: time to poll the system before giving up if item to be located is not found

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; drag pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move

    def drag(self, beginPos, endPos, beginDuration=0.25, endDuration=0.25, **kwargs):
        self._gesture.drag(beginPos, endPos, beginDuration, endDuration, **kwargs)

    def dragElement(self, beginElement=WORK_AREA, endElement=WORK_AREA, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, beginDuration=0.0, endDuration=0.0, **kwargs):
        raise NotImplementedError

    def dragImage(self, beginImageUri, endImageUri=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, beginDuration=0.0, endDuration=0.0, locateTimeout=None, **kwargs):
        raise NotImplementedError

    def dragText(self, beginText, endText=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, beginDuration=0.0, endDuration=0.0, locateTimeout=None, **kwargs):
        raise NotImplementedError


    #############################################
    # swipe gestures                            #
    # (smooth begin, straight move, smooth end) #
    #############################################

    # arguments
    # beginElement:  element within which swipe begins
    # endElement:    element within which swipe ends (if angle is not given)
    # beginImage:    image within which swipe begins
    # endImage:      image within which swipe ends (if angle is not given)
    # beginText:     text within which swipe begins
    # endText:       text within which swipe ends (if angle is not given)
    # beginPos:      beginning position of swipe within target area (entire work area for swipe)
    # endPos:        ending position of swipe within target area (entire work area for swipe)
    # angle:         direction of swipe gesture, if given pre-empts parameters for end position
    # distance:      distance to swipe as proportion of distance from begin towards edge of work area, effective only if angle is given
    # locateTimeout: time to poll the system before giving up if item to be located is not found

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; swipe pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move

    def swipe(self, beginPos, endPos, **kwargs):
        return self._gesture.swipe(beginPos, endPos, **kwargs)

    def swipeElement(self, beginElement=WORK_AREA, endElement=WORK_AREA, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError

    def swipeImage(self, beginImageUri, endImageUri=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, locateTimeout=None, **kwargs):
        raise NotImplementedError

    def swipeText(self, beginText, endText=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, locateTimeout=None, **kwargs):
        locations = self.locateText(beginText, locateTimeout)
        if not locations:
            raise TextNotRecognizedError(beginText)
        if angle != None:
            endPos = angleDistToPos(UserInteraction.WORK_AREA, locations[0].getPos(), angle, distance)
        return self._gesture.swipe(locations[0].getPos(), endPos)

    ############################################
    # flick gestures                           #
    # (sharp begin, straight move, smooth end) #
    ############################################

    # arguments
    # beginElement:  element within which flick begins
    # endElement:    element within which flick ends (if angle is not given)
    # beginImage:    image within which flick begins
    # endImage:      image within which flick ends (if angle is not given)
    # beginText:     text within which flick begins
    # endText:       text within which flick ends (if angle is not given)
    # beginPos:      beginning position of flick within target area (entire work area for flick)
    # endPos:        ending position of flick within target area (entire work area for flick)
    # angle:         direction of flick gesture, if given pre-empts parameters for end position
    # distance:      distance to flick as proportion of distance from begin towards edge of work area, effective only if angle is given
    # locateTimeout: time to poll the system before giving up if item to be located is not found

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; flick pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters
    # dragDuration: duration of move

    def flick(self, beginPos, endPos, **kwargs):
        raise NotImplementedError

    def flickElement(self, beginElement=WORK_AREA, endElement=WORK_AREA, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, **kwargs):
        raise NotImplementedError

    def flickImage(self, beginImageUri, endImageUri=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, locateTimeout=None, **kwargs):
        raise NotImplementedError

    def flickText(self, beginText, endText=None, beginPos=(0.5, 0.5), endPos=(0.5, 0.5), angle=None, distance=1.0, locateTimeout=None, **kwargs):
        raise NotImplementedError


    #########################################
    # rotate gestures                       #
    # (sharp begin, curved move, sharp end) #
    #########################################

    # arguments
    # element:      element which determines the center of rotation
    # beginElement: element which determines the starting point of rotation, by default the same as element
    # centerPos:    center of rotation
    # beginPos:     beginning position of rotation; for element variant, by default at top middle of element, just within it
    # arcAngle:     angle of arc drawn by rotation

    # kwargs recommendations
    # bypassSafety: bool; ignore safety restrictions in movement area
    # pressure:     float; flick pressure (0.0 no pressure, 1.0 greatest safe pressure)
    # fingerRadius: float; finger radius in millimeters

    def rotate(self, centerPos, beginPos, arcAngle=360, *kwargs):
        raise NotImplementedError

    def rotateElement(self, element=WORK_AREA, beginElement=None, centerPos=(0.5, 0.5), beginPos=None, arcAngle=360, *kwargs):
        raise NotImplementedError

    ############################
    # image and text retrieval #
    ############################

    # arguments
    # imageUri:    Uri to the image to be located; file system URIs always work; file extensions need not given, implementation searches for images in suitable formats; exception is raised if image is not found
    # text:        text to be located
    # locateTimeout: time to poll the system before giving up if item to be located is not found
    # forceReload: image must be reloaded from scratch without caches

    # rotated images may be found depending on implementation

    # kwargs recommendations
    # <namespace>_confidence: implementation-specific confidence of match

    # returns tuple of elements
    def locateImage(self, imageUri, locateTimeout=None, forceReload=False, **kwargs):
        if locateTimeout == None:
            locateTimeout = self._locateTimeout
        return self._vision.locateImage(imageUri, locateTimeout,
                                        forceReload, **kwargs)

    # returns tuple of elements
    def locateText(self, text, locateTimeout=None, **kwargs):
        if locateTimeout == None:
            locateTimeout = self._locateTimeout
        return self._vision.locateText(text, locateTimeout, **kwargs)

class OpentestrobotError(Exception):
    pass

class ImageNotRecognizedError(OpentestrobotError):
    pass

class TextNotRecognizedError(OpentestrobotError):
    pass
