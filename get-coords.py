# -*- coding:utf-8 -*-
import dlib
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys

import extract
import pupil

extract = extract.extract()
pupil = pupil.pupil()

def getPointList(pointList, x):
    """
    @ param1[in] pointList      
    @ param2[in] x              
    @ param[out] xPointList     
    """
    
    xPointList = []
    for i in range(len(pointList)):
        if x == 0 or x == 1:
            xPointList.append(pointList[i][x])
        else:
            print("x is out of range. x = 0 or 1")
            sys.exit()
    return xPointList

if __name__ == '__main__':

    params = sys.argv

    facedetector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # if (len(params) != 3):
    #     print ("Run as: python face.py <inputfile.jpg> <outputfile.jpg>")
    #     exit(1)

    inputname = params[1]
    image = cv2.imread(inputname)
    outputname = params[2]
    wrongList = params[3]
    written = False

    height, width = image.shape[:2]
    # image = cv2.resize(image, (500, 520))
    
    gray_img = image.copy()
    draw_img = image.copy()
    
    eye_mask = np.zeros((height, width, 1), dtype = np.uint8)
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)

    faces = facedetector(gray_img, 1)

    wrongListFile = open(wrongList, "a")

    if len(faces) == 0:
        if (not written):
            wrongListFile.write(inputname + "\n")
            written = True
        print("Can not detect face, using fallback bounding box.")

        # CFE
        # top = 204
        # bottom = 675
        # left = 247
        # right = 846

        # RPack - straight
        # top = 937
        # bottom = 1895
        # left = 723
        # right = 1682

        #Rafd
        # top = 313
        # bottom = 634
        # left = 170
        # right = 491

        # # CFD - WF
        # top = 511
        # bottom = 1469
        # left = 723
        # right = 1682

        # CFD - BF
        # top = 511
        # bottom = 1469
        # left = 723
        # right = 1682

        # CFD - BM
        # top = 511
        # bottom = 1469
        # left = 723
        # right = 1682
        
        # BIM
        # top = 204
        # bottom = 675
        # left = 118
        # right = 504

        # CFD - WM
        top = 511
        bottom = 1469
        left = 723
        right = 1682

    else:
        face = faces[0]         # we have only one face always
        top, bottom, left, right = face.top(), face.bottom(), face.left(), face.right()
    # print (face)
    # print (face.top())
    # print (face.bottom())
    # print (face.left())
    # print (face.right())

    #     R_cx = None
    #     R_cy = None
    #     L_cx = None
    #     L_cy = None

    # else:
    # for i, face in enumerate(faces):
    #     print (face)
    #     print (face.top())
    #     print (face.bottom())
    #     print (face.left())
    #     print (face.right())
    
    # RPack - straight
    # top = 937
    # bottom = 1895
    # left = 723
    # right = 1682

    # BIM
    # top = 204
    # bottom = 675
    # left = 118
    # right = 504

    # CFD - AF
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # CFD - AM
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # # CFD - BF
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # # CFD - BM
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # # CFD - LF
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # # CFD - LM
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # # CFD - WF
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682

    # # CFD - WM
    # top = 511
    # bottom = 1469
    # left = 723
    # right = 1682


    # Check if values seem correct
    # cv2.line(draw_img, (left, top), (left, bottom), (255, 0, 0), 1)
    # cv2.line(draw_img, (left, bottom), (right, bottom), (255, 0, 0), 1)
    # cv2.line(draw_img, (right, bottom), (right, top), (255, 0, 0), 1)
    # cv2.line(draw_img, (right, top), (left, top), (255, 0, 0), 1)

    face = dlib.rectangle(left, top, right, bottom)
    # if min(top, height - bottom - 1, left, width - right -1) < 0:
    #     continue

    r_eye_contour, l_eye_contour = extract.getEyeContour(image, predictor, face)
    
    # x and y points of right eye contour
    r_xpoints = getPointList(r_eye_contour, 0)
    r_ypoints = getPointList(r_eye_contour, 1)
    
    # x and y points of left eye contour
    l_xpoints = getPointList(l_eye_contour, 0)
    l_ypoints = getPointList(l_eye_contour, 1)

    # fill eye_mask with contours of eye
    cv2.drawContours(eye_mask, [r_eye_contour], -1, (255, 255, 255), -1)
    cv2.drawContours(eye_mask, [l_eye_contour], -1, (255, 255, 255), -1)

    # if len(r_eye_contour) != 6:
    #     continue
            
    # rate = 0.25, to calculate the threshold
    R_cx, R_cy = pupil.getPupilPoint(r_xpoints, r_ypoints, gray_img, eye_mask, 0.25)

    if  R_cx != None and R_cy != None:
        cv2.circle(draw_img, (R_cx, R_cy), 6, (0, 0, 255), -1)
    else:
        if (not written):
            wrongListFile.write(inputname + "\n")
            written = True
        print("Can not detect R pupil")
    
    L_cx, L_cy = pupil.getPupilPoint(l_xpoints, l_ypoints, gray_img, eye_mask, 0.25)

    if L_cx != None and L_cy != None:
        cv2.circle(draw_img, (L_cx, L_cy), 6, (0, 0, 255), -1)
    else:
        if (not written):
            wrongListFile.write(inputname + "\n")
            written = True
        print("Can not detect L pupil")

    # # cv2.imshow("Pupil Detection", draw_img)
    # # cv2.waitKey(0)
    logfilename = "Coordinates/" + inputname[:-4] + "_result.txt"
    
    logfile = open(logfilename, "w")

    logfile.write(str(R_cx))
    logfile.write(" ")
    logfile.write(str(R_cy))
    logfile.write("\n")
    logfile.write(str(L_cx))
    logfile.write(" ")
    logfile.write(str(L_cy))

    logfile.close()
    # wrongListFile.close()

    # cv2.imwrite("result.jpg", draw_img)
    cv2.imwrite(outputname, draw_img)

