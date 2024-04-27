import cv2
import numpy as np
import datetime
import time
from threading import Thread, Lock

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080

def gstreamer_pipeline(
        sensor_id = 0, 
        capture_width=VIDEO_WIDTH,
        capture_heigt=VIDEO_HEIGHT,
        display_width=int(VIDEO_WIDTH/4),
        display_height=int(VIDEO_HEIGHT/4),
        framerate=20,
        flip_method=2
    ):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_heigt,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

class VideoStream:
    def __init__(self, sensor_id=0):
        self.sensor_id = sensor_id
        self.gstreamer_pipeline = gstreamer_pipeline(sensor_id=self.sensor_id)
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline)
        self.ret, self.frame = self.cap.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self
        
    def update(self):
        while self.started:
            ret, frame = self.cap.read()
            self.read_lock.acquire()
            self.ret, self.frame = ret,frame
            self.read_lock.release()
    
    def isOpened(self):
        return self.cap.isOpened()
                
    def read(self):
        self.read_lock.acquire()
        ret = self.ret
        frame = self.frame.copy()
        self.read_lock.release()
        return ret, frame
        
    def release(self):
        self.started = False
        self.thread.join()
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
    

def show_dual_camera():
    cap0 = VideoStream(0).start()
    cap1 = VideoStream(1).start()

    while cap0.isOpened() and cap1.isOpened():
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
    
        if ret0 and ret1:
            synced_frames = np.hstack((frame0, frame1))
            cv2.imshow('Synced Frames', synced_frames)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    #release capture
    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    show_dual_camera()