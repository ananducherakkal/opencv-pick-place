import cv2
from MyObjectDetector import *
import numpy as np
import os
from trackbar import *
from color import get_color
    
def get_coordinates (color="all", trackbar_type="all"):
    # Load Aruco detector
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    parameters =  cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # Load your Object Detector
    detector = NewObjectDetector()
    # Load Cap
    ###uncomment for web or other camera connected###
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    ###uncomment for using saved images###
    #current_dir = os.path.dirname(os.path.abspath(__file__))

    trackbar_values = [20, 33, 31, 50]
    if trackbar_type == "ellipse":
         trackbar_values = [20, 31, 31, 50]
    elif trackbar_type == "hexagon":
         trackbar_values = [33, 40, 31, 41]
    elif trackbar_type == "rectangle":
         trackbar_values = [15, 19, 33, 44]

    trackbar = Trackbar({
        "W1": [1,100,trackbar_values[0],True],
        "W2": [1,100,trackbar_values[1],True],
        "H1": [1,100,trackbar_values[2],True],
        "H2": [1,100,trackbar_values[3],True],
    })


    # trackbar = Trackbar({
    #     "W1": [1,100,20,True],
    #     "W2": [1,100,35,True],
    #     "H1": [1,100,31,True],
    #     "H2": [1,100,50,True],
    # })

    # # Ellips
    # trackbar = Trackbar({
    #     "W1": [1,100,20,True],
    #     "W2": [1,100,31,True],
    #     "H1": [1,100,31,True],
    #     "H2": [1,100,50,True],
    # })
    # # Hexogan
    # trackbar = Trackbar({
    #     "W1": [1,100,33,True],
    #     "W2": [1,100,40,True],
    #     "H1": [1,100,31,True],
    #     "H2": [1,100,41,True],
    # })

    # # rectangle
    # trackbar = Trackbar({
    #     "W1": [1,100,15,True],
    #     "W2": [1,100,19,True],
    #     "H1": [1,100,33,True],
    #     "H2": [1,100,44,True],
    # })


    trackbar.showTrackbar()

    while True:
        _,img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.flip(img, 0)
        target_height = 960
        # img=cv2.imread(os.path.join(current_dir, 'Pictures/test_image.jpg'))
        original_height, original_width, _ = img.shape
        aspect_ratio = original_height / original_width
        target_width = int(target_height * aspect_ratio)
        img=cv2.resize(img, (target_height, target_width))
        # Get Aruco marker corner and id
        corners, ids, _ = arucoDetector.detectMarkers(img)
        

        client_message = []
        
        if corners:
            # Draw polygon around the marker
            int_corners = np.intp(corners)#convert to ints since polylines does not accept array
            cv2.polylines(img, int_corners, True, (0, 255, 0), 2)
            aruco_perimeter = cv2.arcLength(corners[0], True)
            # Pixel to cm ratio
            pixel_cm_ratio = aruco_perimeter / 58
            
            # Aruco corners
            aruco_origin = corners[0][0][0]
            aruco_x = corners[0][0][1] - corners[0][0][0]
            aruco_y = corners[0][0][3] - corners[0][0][0]

            # aruco vector
            aruco_x_norm = np.linalg.norm(aruco_x)
            aruco_y_norm = np.linalg.norm(aruco_y)

            aruco_x_dir = aruco_x / aruco_x_norm
            aruco_y_dir = aruco_y / aruco_y_norm
            
            #use Script to extract contours
            contours = detector.My_detector(img)

            # Draw objects boundaries
            for cnt in contours:
                    # Get bounding rectangel of objects found
                    rect = cv2.minAreaRect(cnt)
                    (x, y), (w, h), angle = rect
                
                    
                    box = cv2.boxPoints(rect)

                    object_center = (x - aruco_origin[0], y - aruco_origin[1])

                    # Convert object center to the new coordinate system
                    object_x = np.dot(object_center, aruco_x_dir) / pixel_cm_ratio
                    object_y = np.dot(object_center, aruco_y_dir) / pixel_cm_ratio
                    
                    # Get Width and Height of the Objects by applying the Ratio pixel to cm
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio

                    # # Get Width and Height of the Objects by applying the Ratio pixel to cm
                    box = np.intp(box)
                    #sort out qualifed shapes and keep center coords

                    ## all small shpae size
                    
                    getTrackbarValue = trackbar.getTrackbarValue
                    width_range = [getTrackbarValue("W1")/10, getTrackbarValue("W2")/10]
                    height_range = [getTrackbarValue("H1")/10, getTrackbarValue("H2")/10]
                    
                    ## wood block size
                    # width_range = [1.5, 4]
                    # height_range = [11, 14]
                    type = 0
                    if (width_range[0] < object_width < width_range[1] and height_range[0] < object_height < height_range[1]):
                         type = 1
                    elif (height_range[0] < object_width < height_range[1] and width_range[0] < object_height < width_range[1]):
                         type = 2

                    angle = angle if type == 1 else angle - 90

                    if type:
                        found_color = True
                        #check color in center of shape
                        b,g,r = img[int(y),int(x)]
                        print(get_color(r, g, b), color)
                        if color != "all" and color != get_color(r, g, b):
                            found_color = False
                        
                        if found_color:
                            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                            cv2.polylines(img, [box], True, (255, 0, 0), 2)
                            cv2.putText(img, "Position {} mm".format((int(object_x), int(object_y))), (int(x - 100), int(y)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                            cv2.putText(img, "Orinetation is {} degrees".format(int(angle)), (int(x - 100), int(y + 50)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                            cv2.circle(img,(int(x), int(y)),1,(255,255,0),1)
                            client_message.append({
                                "y": object_x * 10,
                                "x": object_y * 10,
                                "angle": -angle
                            })
        cv2.imshow("win", img)
        key = cv2.waitKey(200)
        if key == 27:
            cv2.destroyAllWindows()
            return None
        elif key == 13:
            cv2.destroyAllWindows()
            return client_message

print(get_coordinates(color="black", trackbar_type="all"))