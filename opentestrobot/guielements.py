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

# coordinate handler helpers

import math

# returns pos
def getPos(bbox, pos=(0.5, 0.5)):
    return (bbox[0][0] + pos[0] * (bbox[1][0] - bbox[0][0]), bbox[0][1] + pos[1] * (bbox[1][1] - bbox[0][1]))

def getClockwiseArcAngle(arcAngle=360):
    return abs(arcAngle)

def getCounterclockwiseArcAngle(arcAngle=360):
    return -abs(arcAngle)

def _maxDistInDirection(area, beginPos, angle):
    angle = angle % 360
    rad = math.radians(angle)
    x, y = beginPos
    top = area.getBbox()[0][1]
    left = area.getBbox()[0][0]
    bottom = area.getBbox()[1][1]
    right = area.getBbox()[1][0]
    if 0 < angle < 180:
        maxDistY = (bottom - y) / math.sin(rad)
    elif 180 < angle < 360:
        maxDistY = (top-y) / math.sin(rad)
    else:
        maxDistY = float('inf')

    if 90 < angle < 270:
        maxDistX = (left - x) / math.cos(rad)
    elif 270 < angle or angle < 90:
        maxDistX = (right - x) / math.cos(rad)
    else:
        maxDistX = float('inf')

    return min(maxDistX, maxDistY)

def angleDistToPos(area, beginPos, angle, distance):
    distanceToEdge = _maxDistInDirection(area, beginPos, angle)
    rad = math.radians(angle)

    endPosX = beginPos[0] + math.cos(rad) * distanceToEdge * distance
    endPosY = beginPos[1] + math.sin(rad) * distanceToEdge * distance
    return (endPosX, endPosY)

# all element objects are immutable

class Element(object):
    def __init__(self):
        super(Element, self).__init__()

    def getPos(self, pos=(0.5, 0.5)):
        raise NotImplementedError

    def getBbox(self):
        raise NotImplementedError

class Location(Element):
    def __init__(self, pos):
        super(Location, self).__init__()
        self._pos = pos

    def getPos(self, pos=(0.5, 0.5)):
        return self._pos

    def getBbox(self):
        return (self._pos, self._pos)

class Rectangle(Element):
    def __init__(self, upperLeftPos, lowerRightPos):
        super(Rectangle, self).__init__()
        self._bbox = (upperLeftPos, lowerRightPos)

    def getPos(self, pos=(0.5, 0.5)):
        return getPos(self._bbox, pos)

    def getBbox(self):
        return self._bbox

class ImageRectangle(Rectangle):
    def __init__(self, upperLeftPos, lowerRightPos, imageUri):
        super(ImageRectangle, self).__init__(upperLeftPos, lowerRightPos)
        self._imageUri = imageUri

    def getImageUri(self):
        return self._imageUri

    def __repr__(self):
        return "%s(%s, %s, %s)" % (
            (self.__class__.__name__,) + self.getBbox() + (repr(self._imageUri),))

# consequtive words that may occupy non-rectangular area (i.e. there is no guarantee that any particular position within bounding box has a word at it)
class TextRectangle(Rectangle):
    def __init__(self, upperLeftPos, lowerRightPos, text):
        super(TextRectangle, self).__init__(upperLeftPos, lowerRightPos)
        self._text = text

    def getText(self):
        return self._text

    def getWords(self):
        # TODO
        pass

# single word occupying rectangular area
class Word(TextRectangle):
    def __init__(self, upperLeftPos, lowerRightPos, word):
        super(Word, self).__init__(upperLeftPos, lowerRightPos, word)

    def getWords(self):
        return (self,)

