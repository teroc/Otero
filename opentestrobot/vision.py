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

"""

import urlparse
import camera
import oir
import ocr
import time

class Interface(object):
    """API required from Vision implementations

    Observation module
    """
    def __init__(self, cameraInstance=None, oirInstance=None, ocrInstance=None):
        super(Interface, self).__init__()
        self.setCamera(cameraInstance)
        self.setOir(oirInstance)
        self.setOcr(ocrInstance)

    def setCamera(self, cameraInstance):
        self._camera = cameraInstance
        if self._camera:
            self._cameraFrameOutput = self._camera.features()["frame"]

    def setOir(self, oirInstance):
        self._oir = oirInstance

    def setOcr(self, ocrInstance):
        self._ocr = ocrInstance

    def locateImage(self, imageUri, locateTimeout=0, forceReload=False, **kwargs):
        if self._cameraFrameOutput == "filename":
            return self._locate(self._camera.frame,
                                lambda frame: self._oir.oirLocate(frame, imageUri),
                                locateTimeout, **kwargs)
        else:
            raise Exception('unsupported camera frame output: "%s"' %
                            self._cameraFrameOutput)

    def locateText(self, text, locateTimeout=0, forceReload=False, **kwargs):
        if self._cameraFrameOutput == "filename":
            return self._locate(self._camera.frame,
                                lambda frame: self._ocr.ocrLocate(frame, text),
                                locateTimeout, **kwargs)
        else:
            raise Exception('unsupported camera frame output: "%s"' %
                            self._cameraFrameOutput)

    def _locate(self, newFrameFileFunc, locateFunc, locateTimeout, **kwargs):
        if locateTimeout == None:
            locateTimeout = 0
        startTime = time.time()
        currentTime = startTime
        endTime = startTime + locateTimeout
        results = ()

        while currentTime <= endTime:
            results = locateFunc(newFrameFileFunc())
            if results:
                break
            currentTime = time.time()

        return results


class SwEmulation(Interface):
    """Software emulation of Vision API and components behind it

    This Vision implementation uses software emulation of Camera,
    that is, takes screenshots with fMBT GUITestInterface.

    fMBT's default OCR and OIR engines are used for text and image
    recognition.
    """
    def __init__(self, guiTestInterface):
        super(SwEmulation, self).__init__()
        self._gti = guiTestInterface
        self.setCamera(camera.SwEmulation(self._gti))
        self.setOir(oir.FmbtOir(self._gti))
        self.setOcr(ocr.FmbtOcr(self._gti))
