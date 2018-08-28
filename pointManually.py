# -*- coding:utf-8 -*-
import sys
import cv2

if __name__ == '__main__':

    params = sys.argv

    inputname = params[1]
    image = cv2.imread(inputname)
    outputname = params[2]
    logName = params[3]

    height, width = image.shape[:2]
    # image = cv2.resize(image, (500, 520))
    
    draw_img = image.copy()
    
    coordFileName = inputname[:-4] + ".txt"
    coordFile = open(coordFileName, 'r')

    rightEye = coordFile.readline().strip().split(',')
    leftEye = coordFile.readline().strip().split(',')

    R_cx = int(rightEye[0])
    R_cy = int(rightEye[1])

    L_cx = int(leftEye[0])
    L_cy = int(leftEye[1])

    cv2.circle(draw_img, (R_cx, R_cy), 6, (0, 0, 255), -1)
    cv2.circle(draw_img, (L_cx, L_cy), 6, (0, 0, 255), -1)
    
    # # # cv2.imshow("Pupil Detection", draw_img)
    # # # cv2.waitKey(0)
    # logfilename = "Coordinates/" + inputname[:-4] + "_result.txt"
    
    logfile = open(logName, "w")

    logfile.write(str(R_cx))
    logfile.write(" ")
    logfile.write(str(R_cy))
    logfile.write("\n")
    logfile.write(str(L_cx))
    logfile.write(" ")
    logfile.write(str(L_cy))

    logfile.close()

    # cv2.imwrite("result.jpg", draw_img)
    cv2.imwrite(outputname, draw_img)