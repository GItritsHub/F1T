import cv2
import numpy as np
import datetime
import time
from threading import Thread, Lock
import pickle

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

def gstreamer_pipeline(
        sensor_id = 0, 
        capture_width=VIDEO_WIDTH,
        capture_heigt=VIDEO_HEIGHT,
        display_width=int(VIDEO_WIDTH),
        display_height=int(VIDEO_HEIGHT),
        framerate=30,
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
    def __init__(self, sensor_id=0, calibration_pickle=None):
        self.sensor_id = sensor_id
        self.gstreamer_pipeline = gstreamer_pipeline(sensor_id=self.sensor_id)
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline)
        self.ret, self.frame = self.cap.read()
        self.started = False
        self.read_lock = Lock()
        self.cameraMatrix, self.dist, self.newCameraMatrix, self.roi = self.read_pickle(calibration_pickle)

    def read_pickle(self, calibration_pickle):
        with open(calibration_pickle, 'rb') as file:
            cameraMatrix, dist = pickle.load(file)
        
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (VIDEO_WIDTH,VIDEO_HEIGHT), 1, (VIDEO_WIDTH,VIDEO_HEIGHT))
        
        return cameraMatrix, dist, newCameraMatrix, roi

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
    cap0 = VideoStream(0, './F1T/IMX219_StereoModule/calibration0.pkl').start()
    cap1 = VideoStream(1, './F1T/IMX219_StereoModule/calibration1.pkl').start()

    while cap0.isOpened() and cap1.isOpened():
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
    
        if ret0 and ret1:
            mapx0, mapy0 = cv2.initUndistortRectifyMap(cap0.cameraMatrix, cap0.dist, None, cap0.newCameraMatrix, (VIDEO_WIDTH,VIDEO_HEIGHT), 5)
            mapx1, mapy1 = cv2.initUndistortRectifyMap(cap1.cameraMatrix, cap1.dist, None, cap1.newCameraMatrix, (VIDEO_WIDTH,VIDEO_HEIGHT), 5)
            undistorted_frame0 = cv2.remap(frame0, mapx0, mapy0, cv2.INTER_LINEAR)
            undistorted_frame1 = cv2.remap(frame1, mapx1, mapy1, cv2.INTER_LINEAR)
            x0, y0, w0, h0 = cap0.roi
            
            undistorted_frame0 = undistorted_frame0[y0:y0+h0, x0:x0+w0]
            undistorted_frame1 = undistorted_frame1[y0:y0+h0, x0:x0+w0]

            synced_frames = np.hstack((undistorted_frame0, undistorted_frame1))
            cv2.imshow('undist1', synced_frames)
            
                            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    #release capture
    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    show_dual_camera()