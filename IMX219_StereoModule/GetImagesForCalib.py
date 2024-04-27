import cv2
from SyncedCameraFeed import gstreamer_pipeline

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
sensor_id = 0

cap = cv2.VideoCapture(gstreamer_pipeline(sensor_id=sensor_id)) #Specify sensor_id 

cnt = 0

while cap.isOpened():

    succes, img = cap.read()

    k = cv2.waitKey(10)

    if k == 27: #press esc if enough images have been taken
        break
    elif k == ord('c'): 
        cv2.imwrite(f'./F1T/IMX219_StereoModule/images_sensorid{sensor_id}/img' + str(cnt) + '.png', img) #If this doesn't work - paste full path to the images_sensorid{sensor_id}
        print("image saved!")
        cnt += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()