import subprocess
import os
from const.config import *
from subprocess import PIPE
import signal

import time
import psutil

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

# proc = subprocess.Popen(args=['ffmpeg', '-f', 'dshow', '-y', '-rtbufsize', '100M', "-f", 'gdigrab', '-framerate', '60',
#           '-probesize', '10M', '-draw_mouse', '1', '-offset_x', '0', '-offset_y',
#           '0', '-video_size', '1920x1080', '-itsoffset', '1', '-i', 'desktop',
#           '-c:v', 'libx264', '-r', '30', '-preset', 'ultrafast', '-tune',
#           'zerolatency', '-crf', '25', '-pix_fmt', 'yuv420p', SAVE_PATH + '/screen_record.mp4',
#           ], startupinfo=startupinfo)


proc = subprocess.Popen(args=['ffmpeg.exe', '-f', 'dshow', '-y', '-rtbufsize', '100M', "-f", 'gdigrab', '-framerate', '60',
                              '-probesize', '10M', '-draw_mouse', '1', '-offset_x', '0', '-offset_y',
                              '0', '-video_size', '1920x1080', '-itsoffset', '1', '-i', 'desktop',
                              '-c:v', 'libx264', '-r', '30', '-preset', 'ultrafast', '-tune',
                              'zerolatency', '-crf', '25', '-pix_fmt', 'yuv420p', SAVE_PATH + '/' + 'test.mp4',
                              ], startupinfo=startupinfo, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

time.sleep(5)
# os.kill(proc.pid, signal.CTRL_C_EVENT)
# os.system('taskkill /IM "ffmpeg.exe" /F')
proc.communicate(input=b'q')
time.sleep(1)

proc2 = subprocess.Popen(args=['ffmpeg.exe', '-f', 'dshow', '-y', '-rtbufsize', '100M', "-f", 'gdigrab', '-framerate', '60',
                              '-probesize', '10M', '-draw_mouse', '1', '-offset_x', '0', '-offset_y',
                              '0', '-video_size', '1920x1080', '-itsoffset', '1', '-i', 'desktop',
                              '-c:v', 'libx264', '-r', '30', '-preset', 'ultrafast', '-tune',
                              'zerolatency', '-crf', '25', '-pix_fmt', 'yuv420p', SAVE_PATH + '/' + 'test2.mp4',
                              ], startupinfo=startupinfo, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

time.sleep(5)
proc2.communicate(input=b'q')