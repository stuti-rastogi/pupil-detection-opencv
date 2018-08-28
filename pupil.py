# -*- coding:utf-8 -*-
import numpy as np
import cv2
import extract
import iris

extract = extract.extract()
iris = iris.iris()

class pupil:

    def detectPupil(self, iris_points):
        """
        @ param1[in]  iris_points(np.array)    
        @ param1[out] cx                       
        @ param2[out] cy                                       
        """
        iris_hull = cv2.convexHull(iris_points)
        
        M = cv2.moments(iris_hull)

        # center of mass
        if (M['m00'] != 0.0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        
        else:
            cx = None
            cy = None
        return cx, cy

    def getPupilPoint(self, xpoints, ypoints, gray_img, eye_mask, rate):
        """
        @ param1[in]  xpoints                
        @ param2[in]  ypoints                
        @ param3[in]  gray_img              
        @ param4[in]  eye_mask              
        @ param5[in]  rate                  
        
        @ param1[out] eye_roi               
        @ param2[out] threshold             
        @ param3[out] eye_luminance         
        @ param4[out] iris_mask             
        @ param5[out] cx                    
        @ param6[out] cy                    
        @ param7[out] iris_hull             
        """

        top, bottom, left, right = extract.cutArea(xpoints, ypoints)
        
        # get region of interest from the eye and the contour
        eye_roi = gray_img[top:bottom, left:right]
        eye_mask_roi = eye_mask[top:bottom, left:right]

        # rows and cols of eye_mask used for iris_mask
        iris_mask = np.zeros((eye_mask_roi.shape[0], eye_mask_roi.shape[1], 1), dtype=np.uint8)
        
        threshold, eye_luminance = iris.defineThreshold(eye_roi, eye_mask_roi, rate)
        
        iris_points = iris.detectIris(left, top, eye_roi, eye_mask_roi, threshold, abso=True)
        iris_points_relative = iris.detectIris(left, top, eye_roi, eye_mask_roi, threshold, abso=False)
        
        if len(iris_points) == 0:
            cx = None
            cy = None
        else:        
            cx, cy = self.detectPupil(iris_points)
        
        return cx, cy

