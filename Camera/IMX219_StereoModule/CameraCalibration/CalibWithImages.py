import numpy as np
import cv2
import glob, pickle

chessboardSize = (9,6) #e.g. on an IPad measure https://www.longervision.github.io/2017/03/16/ComputerVision/OpenCV/opencv-internal-calibration-chessboard/ s.t. 20mm
frameSize = (1280,720)
sensor_id = 0 #CHANGE w.r.t. id

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 25 #If you use an IPhone or real paper, simply measure with a ruler a decent size and change accordingly
objp = objp * size_of_chessboard_squares_mm

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob(f'./F1T/Camera/IMX219_StereoModule/images_sensorid{sensor_id}/*.png')

for image in images:

    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(1000)


cv2.destroyAllWindows()
ret, cameraMatrix, dist, rot_vector, trans_vector = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

# Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
pickle.dump((cameraMatrix, dist), open( f"calibration{sensor_id}.pkl", "wb" )) #If this doesn't automatically create the calib pickle in the directory drag and drop it to IMX219_StereoModule