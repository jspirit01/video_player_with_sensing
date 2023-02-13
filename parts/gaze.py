import random
import os
from const import constants
from const.config import PARTICIPANT_MONITOR


from pygaze.logfile import Logfile
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.eyetracker import EyeTracker
import pygame
import pyglet

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (PARTICIPANT_MONITOR[0], PARTICIPANT_MONITOR[1])

class Gaze:
    def __init__(self, ):
        
        # Start a new Display instance to be able to show things on the monitor.
        # The important parameters will automatically be loaded from the constants.
        self.disp = Display()
        
        pygame.display.set_mode((1920,1080), flags=pygame.HIDDEN)


        # pyglet.window.Window(fullscreen=True, screens[1])
        
        # pygame.display.iconify()


        # create keyboard object
        self.keyboard = Keyboard(keylist=['space', 'escape'], timeout=None)

        # Initialise the EyeTracker and let it know which Display instance to use by
        # passing it to the EyeTracker.
        self.tracker = EyeTracker(self.disp)
        print("INIT")
        # create logfile object
        # self.log = Logfile()
        # # log.write(["trialnr", "trialtype", "endpos", "latency", "correct"])
        # self.log.write(['date', 'time', 'trialnr', 'video', 'timestamp'])

        # create screens
        pass 
        # inscreen = Screen()
        # inscreen.draw_text(
        #     text="When you see a cross, look at it and press space. Then make an eye movement to the black circle when it appears.\n\n(press space to start)",
        #     fontsize=24)
        # fixscreen = Screen()
        # fixscreen.draw_fixation(fixtype='cross', pw=3)
        # targetscreens = {}
        # targetscreens['left'] = libscreen.Screen()
        # targetscreens['left'].draw_circle(pos=(int(constants.DISPSIZE[0] * 0.25), constants.DISPSIZE[1] / 2), fill=True)
        # targetscreens['right'] = libscreen.Screen()
        # targetscreens['right'].draw_circle(pos=(int(constants.DISPSIZE[0] * 0.75), constants.DISPSIZE[1] / 2),
        #                                    fill=True)
        # feedbackscreens = {}
        # feedbackscreens[1] = libscreen.Screen()
        # feedbackscreens[1].draw_text(text='correct', colour=(0, 255, 0), fontsize=24)
        # feedbackscreens[0] = libscreen.Screen()
        # feedbackscreens[0].draw_text(text='incorrect', colour=(255, 0, 0), fontsize=24)

        self.recording = False
        self.recorded_path = None

    def calibrate(self, logfile):


        # Open logfile and write initiation report
        self.tracker.initiation_report(logfile)
        # pygame.display.set_mode((PARTICIPANT_MONITOR[0], PARTICIPANT_MONITOR[1]), pygame.FULLSCREEN)
        
        # Calibrate the eye tracker.
        pygame.display.set_mode((1920,1080), flags=pygame.FULLSCREEN)
        calibration_result = self.tracker.calibrate()
        pygame.display.set_mode((1920,1080), flags=pygame.HIDDEN)

        return calibration_result
        

    def ready(self):
        pass
        

    def stream(self):
        # print("Start Gaze Streaming")
        while True:
            pass
        

    def record(self, save_path):
        if not self.recording:
            self.recording = True
            self.tracker.start_recording()
            self.tracker.log("RECORDINGSTART")

    def stop_record(self):
        if self.recording:
            self.recording = False
            self.tracker.log("RECORDINGSTOP")
            self.tracker.stop_recording()
            
    def terminate(self):
        print('terminating Gaze')
        self.tracker.close()
        self.disp.close()
        print("Gaze is terminated.")
        
    def save_data(self, folder):
        pass
    
    def clear(self):
        pass