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

System = dict(
	gestures="OTRP.fMBT_gestures",
	visual="OTRP.fMBT_gestures",
	user_interaction="OTRP.UI_api",
	)
gesture_module = do_import(System, 'gestures')
visual_module = do_import(System, 'visual')
user_interaction_module = do_import(System, 'user_interaction')
gestures = gesture_module.GestureApi(gesture_parameter_1, gesture_parameter2)
visual = gestures
user_interaction = user_interaction_module.UiApi(gestures, visual)

import OTRP.fMBT_gestures
import OTRP.UI_api
gestures = OTRP.fMBT_gestures.GestureApi(gesture_parameter_1, gesture_parameter2)
visual = gestures
user_interaction = OTRP.UiApi(gestures, visual)

System = dict(
	robot="Gadgets.robot_delta",
	gestures="OTRP.generic_robot_gestures",
	camera="Gadgets.camera_v4l2",
	visual="OTRP.generic_camera_visual",
	user_interaction="OTRP.UI_api",
	)
robot_module = do_import(System, 'robot')
gesture_module = do_import(System, 'gestures')
camera_module = do_import(System, 'camera')
visual_module = do_import(System, 'visual')
user_interaction_module = do_import(System, 'user_interaction')
robot = robot_module.RobotApi()
gestures = gesture_module.GestureApi(robot, gesture_parameter_1, gesture_parameter2)
camera = camera_module.CameraApi()
visual = visual_module.VisualApi(camera)
user_interaction = user_interaction_module.UiApi(gestures, visual)

import Gadgets.robot_delta
import OTRP.generic_robot_gestures
import OTRP.generic_camera_visual
import Gadgets.camera_v4l2
import OTRP.UI_api
robot = Gadgets.robot_delta.RobotApi()
gestures = OTRP.generic_robot_gestures.GestureApi(robot, gesture_parameter_1, gesture_parameter2)
camera = Gadgets.camera_v4l2.CameraApi()
visual = OTRP.generic_camera_visual.VisualApi(camera)
user_interaction = OTRP.UiApi(gestures, visual)
