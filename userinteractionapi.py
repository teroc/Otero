# coordinate handler helpers

# returns pos
def getPos(bbox, pos=(0.5, 0.5)):
	return (bbox[0][0] + pos[0] * (bbox[1][0] - bbox[0][0]), bbox[0][1] + pos[1] * (bbox[1][1] - bbox[0][1]))


# all element objects are immutable

class Element(object):
	def getPos(self, pos):
		raise NotImplementedError

class Location(Element):
	def __init__(self, pos):
		self._pos = pos
	
	def getPos(self, pos):
		return self._pos

class Area(Element):
	def __init__(self, upperLeftPos, lowerRightPos):
		self._bbox = (upperLeftPos, lowerRightPos)
	
	def getPos(self, pos):
		return getPos(self._bbox, pos)

	def getBbox(self):
		return self._bbox

class Image(Area):
	def __init__(self, image):
		# TODO
		pass

# consequtive words that may occupy non-rectangular area (i.e. there is no guarantee that any particular position within bounding box has a word at it)
class Text(Area):
	def __init__(self, text):
		# TODO
		pass
	
	def getWords(self):
		# TODO
		pass

# single word occupying rectangular area
class Word(Text):
	def __init__(self, word):
		# TODO
		pass
	
	def getWords(self):
		return (self,)


class UserInteractionApi(object):
	# argument types
	# pos:       tuple of two floats;   x, y coordinates, by default unity coordinates with origin at upper left corner of target area and (1.0, 1.0) at lower right corner, x increasing right and y increasing down
	# image:     reference to an image; exact format tbd., possibly path to image file
	# text:      str;                   text
	# element:   element object;        work area subpart
	# angle:     float;                 angle in degrees, clockwise from top unless otherwise indicated
	# direction: int;                   direction of gesture, either 1 (clockwise) or -1 (counterclockwise)
	# length:    float;                 length of gesture as proportion of maximal length possible within target area, taking into account gesture's position and angle
	# duration:  float;                 time in seconds
	
	WORK_AREA = Area((0, 0), (1, 1))
	
	ANGLE_UP = 0.0
	ANGLE_RIGHT = 90.0
	ANGLE_DOWN = 180.0
	ANGLE_LEFT = 270.0
	
	DIR_CLOCKWISE = 1
	DIR_COUNTERCLOCKWISE = -1
	
	
	# confirmed methods
	
	###########################
	# tap (and hold) gestures #
	###########################
	
	# arguments
	# element:  element to tap
	# image:    image to tap
	# text:     text to tap
	# pos:      position to tap within target area (entire work area for tapPos)
	# duration: minimum time to hold between press and release, 0.0 indicates ordinary tap 
	
	# kwargs recommendations
	# pressure:     float; tap pressure (0.0 no pressure, 1.0 greatest safe pressure)
	# fingerRadius: float; finger radius in millimeters
	# touchAngle
	
	def tapPos(self, pos, duration=0.0, **kwargs):
		raise NotImplementedError
	
	def tapElement(self, element=WORK_AREA, pos=(0.5, 0.5), duration=0.0, **kwargs):
		raise NotImplementedError
	
	def tapImage(self, image, pos=(0.5, 0.5), duration=0.0, **kwargs):
		raise NotImplementedError
	
	def tapText(self, text, pos=(0.5, 0.5), duration=0.0, **kwargs):
		raise NotImplementedError
	
	
	# unconfirmed methods
	
	###########################################
	# scroll (and drag) gestures              #
	# (sharp begin, straight move, sharp end) #
	###########################################
	
	# arguments
	# beginPos:      beginning position of scroll
	# endPos:        ending position of scroll
	# bbox:          bounding box through whose center scroll is performed
	# angle:         direction of scroll gesture
	# length:        length of scroll gesture
	# beginDuration: minimum duration to hold between press and move
	# endDuration:   minimum duration to hold between move and release
	
	def scrollPos(self, beginPos, endPos, beginDuration=0.0, endDuration=0.0, *kwargs):
		raise NotImplementedError
	
	# is offset needed?
	
	def scrollElement(self, element=WORK_AREA, angle=ANGLE_UP, length=0.8, beginDuration=0.0, endDuration=0.0, *kwargs):
		raise NotImplementedError
	
	# is this variant needed?
	def scrollImage(self, image, angle=ANGLE_UP, length=0.8, beginDuration=0.0, endDuration=0.0, *kwargs):
		raise NotImplementedError
	
	# is this variant needed?
	def scrollText(self, text, angle=ANGLE_UP, length=0.8, beginDuration=0.0, endDuration=0.0, *kwargs):
		raise NotImplementedError
	
	#############################################
	# swipe gestures                            #
	# (smooth begin, straight move, smooth end) #
	#############################################
	
	# identical to scroll except for smooth beginning and ending; implement as extra parameter?
	
	#####################################################################
	# flick gestures                                                    #
	# (sharp begin, short (constant length?) straight move, smooth end) #
	#####################################################################
	
	# arguments
	# pos:      beginning position of flick
	# bbox:     bounding box to flick
	# angle:    direction of flick gesture
	# flickPos: beginning position to flick within target area 
	
	def flickPos(self, pos, angle=ANGLE_UP, *kwargs):
		raise NotImplementedError
	
	def flickElement(self, element=WORK_AREA, angle=ANGLE_UP, flickPos=(0.5, 0.5), *kwargs):
		raise NotImplementedError
	
	def flickImage(self, image, angle=ANGLE_UP, flickPos=(0.5, 0.5), *kwargs):
		raise NotImplementedError
	
	def flickText(self, text, angle=ANGLE_UP, flickPos=(0.5, 0.5), *kwargs):
		raise NotImplementedError
	
	#########################################
	# rotate gestures                       #
	# (sharp begin, curved move, sharp end) #
	#########################################
	
	# arguments
	# centerPos:  center of rotation
	# beginPos:   beginning position of rotation
	# element:    element within which rotation is performed
	# image:      image within which rotation is performed
	# text:       text within which rotation is performed
	# radius:     float; radius of rotation as proportion of distance from center of target area to nearest edge
	# beginAngle: beginning angle of rotation
	# direction:  direction of rotation
	# arcAngle:   angle of arc drawn by rotation
	
	def rotatePos(self, centerPos, beginPos, direction=DIR_COUNTERCLOCKWISE, arcAngle=360, *kwargs):
		raise NotImplementedError
	
	# is offset needed?
	
	def rotateElement(self, element=WORK_AREA, radius=0.8, beginAngle=ANGLE_UP, direction=DIR_COUNTERCLOCKWISE, arcAngle=360, *kwargs):
		raise NotImplementedError
	
	def rotateImage(self, image, radius=0.8, beginAngle=ANGLE_UP, direction=DIR_COUNTERCLOCKWISE, arcAngle=360, *kwargs):
		raise NotImplementedError
	
	# is this variant needed?
	def rotateText(self, text, radius=0.8, beginAngle=ANGLE_UP, direction=DIR_COUNTERCLOCKWISE, arcAngle=360, *kwargs):
		raise NotImplementedError
	
	############################
	# image and text retrieval #
	############################
	
	# are these needed, or are element objects enough?
	
	# returns bbox
	def locateImage(self, image, **kwargs):
		raise NotImplementedError
	
	# returns bbox
	def locateText(self, text, **kwargs):
		raise NotImplementedError


d = UserInteractionApi()

# tap coordinate
d.tapPos((0.5, 0.7))                # pos
d.tapElement(Location(0.5, 0.7))    # element
d.tapElement(pos=(0.5, 0.7))        # element

# tap center of text
d.tapPos(d.getPos(d.locateText("abc"))) # pos w. bboxes
d.tapPos(Text("abc").getPos())          # pos w. elements
d.tapElement(Text("abc"))               # element
d.tapText("abc")                        # text

# tap beginning of text
d.tapPos(d.getPos(d.locateText("abc"), (0.1, 0.5))) # pos w. bboxes
d.tapPos(Text("abc").getPos(0.1, 0.5))              # pos w. elements
d.tapElement(Text("abc"), (0.1, 0.5))               # element
d.tapText("abc", (0.1, 0.5))                        # text


# hold coordinate
d.tapPos((0.5, 0.7), holdTime=2.0) # parameter in tap


# rotate image full circle counterclockwise from top with pos
bbox = d.locateImage(imageId)
x, y = d.getPos(bbox)
d.rotatePos((x, y), (x, y + 0.8*(bbox[0][1] - y)))
# rotate image full circle counterclockwise from top with image
d.rotateImage(imageId)

# rotate image quarter circle clockwise from left with pos
bbox = d.locateImage(imageId)
x, y = d.getPos(bbox)
d.rotatePos((x, y), (x + 0.8*(bbox[0][0] - x, y)), direction=DIR_CLOCKWISE, arcAngle=90)
# rotate image quarter circle clockwise from left with bbox
d.rotateImage(image, beginAngle=ANGLE_LEFT, direction=DIR_CLOCKWISE, arcAngle=90)

