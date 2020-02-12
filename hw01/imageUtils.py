import cv2

#Utilities for opencv-based image processing.

# Class to select a region of interest (ROI)
# USAGE: Create the object, and execute it: SelectROI("image",im)()

class SelectROI(object):
    def __init__(self, name, im):
        '''Params: window name and image'''
        self.image = im
        self.winname = name

        #cv2.namedWindow(name)
        self.coords = []
        self.dragging = False
        self._update()

    def _mouse_cb(self, event, x, y, flags, parameters):
        '''Record starting (x,y) coordinates on left mouse button click'''
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coords[:] = [(x, y)]
            self.dragging = True

        elif event == 0 and self.dragging:
            self.coords[1:] = [(x, y)]

        # Record ending (x,y) coords when mouse released
        elif event == cv2.EVENT_LBUTTONUP:
            self.coords[1:] = [(x, y)]
            self.dragging = False
            xs, ys = list(zip(*self.coords))
            self.coords = [(min(xs), min(ys)),
                           (max(xs), max(ys))]
            print('roi:', self.coords)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.coords = []
            self.dragging = False

        self._update()

    def _update(self):
        im = self.image.copy()
        if len(self.coords) == 2:
            cv2.rectangle(im, self.coords[0], self.coords[1], (0, 255, 0), 2)

        cv2.imshow(self.winname, im)

    def __call__(self):
        cv2.setMouseCallback(self.winname, self._mouse_cb)
        cv2.waitKey()
        cv2.destroyWindow(self.winname)
        return self.coords if self.coords else None

if __name__ == '__main__' :
    '''for testing'''
    im=cv2.imread("tcone-1.jpg")
    #cv2.namedWindow('image',cv2.WINDOW_NORMAL) # Can be resized
    s=SelectROI("image", im)
    print('region of interest',s())
