import threading
from tracemalloc import stop
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
import pygame
import os
import cv2

try:
	from pygaze import libwebcam
# if importing from PyGaze fails, we try to import from the current directory
except:
	import libwebcam


class CamThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        camlist = libwebcam.available_devices()
        print(camlist)
        self.camDev = camlist[camID]
        self.camID = camID
        self.stopped = False
    def run(self):
        print("Starting " + self.previewName)
        self.camPreview()

    def camPreview(self,):
        cv2.namedWindow(self.previewName)
        cam = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
        self.file_num = 0
        while not self.stopped:
            self.file_num+=1
            rval, frame = cam.read()
            frame = cv2.flip(frame,1)
            img = cv2.imshow(self.previewName, frame) 
            # cv2.imwrite("examples/eyetracking_for_video_stimuli/Snaps/%04d.png" % self.file_num, frame)
            key = cv2.waitKey(1)
            if key == 27:  # exit on ESC
                break
        cam.release()
        cv2.destroyWindow(self.previewName)
