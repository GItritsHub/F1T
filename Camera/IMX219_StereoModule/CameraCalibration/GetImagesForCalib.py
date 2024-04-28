import cv2
import sys
from Camera.IMX219_StereoModule.SyncedCameraFeed import gstreamer_pipeline
from pathlib import Path

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1020
path = Path(__file__).parent

def run_calibration(sensor_id=0):
    cap = cv2.VideoCapture(gstreamer_pipeline(int(sensor_id))) #Specify sensor_id
    cnt = 0

    while cap.isOpened():

        succes, img = cap.read()

        k = cv2.waitKey(10)

        if k == 27: #press esc if enough images have been taken
            break
        elif k == ord('c'): 
            cv2.imwrite(f'{path}/images_sensorid{sensor_id}/img' + str(cnt) + '.png', img) #If this doesn't work - paste full path to the images_sensorid{sensor_id}
            print("image saved!")
            cnt += 1

        cv2.imshow('Img',img)

    # Release and destroy all windows before termination
    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_calibration(0)