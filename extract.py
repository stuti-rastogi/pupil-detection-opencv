# -*- coding:utf-8 -*-
import dlib
import numpy as np

class extract:

    def cutArea(self, x_list, y_list):
        """
        @ param1[in] x_list                     X points
        @ param2[in] y_list                     Y points
        @ param[out] top, bottom, left, right
        """

        # get boundary values of the area

        top = min(y_list)
        bottom = max(y_list)
        
        left = min(x_list)
        right = max(x_list)
        
        return top, bottom, left, right

    def getEyeContour(self, image, predictor, face):
        """
        @ param1[in] image              
        @ param2[in] predictor
        @ param3[in] face               
        @ param[out] r_eye_contour      
        @ param[out] l_eye_contour      
        """

        r_eye_contour = []
        l_eye_contour = []
        
        # print (face)
        
        shape = predictor(image, face)

        # https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/
        # Left eye  : 36, 37, 38, 39, 40, 41
        # Right eye : 42, 43, 44, 45, 46, 47

        for i in range(shape.num_parts):
            if i >= 36 and i <= 41:
                r_eye_point = []
                r_eye_point.append(shape.part(i).x)
                r_eye_point.append(shape.part(i).y)
                r_eye_point = np.array(r_eye_point)
                r_eye_contour.append(r_eye_point)
            
            elif i >= 42 and i <= 47:
                l_eye_point = []
                l_eye_point.append(shape.part(i).x)
                l_eye_point.append(shape.part(i).y)
                l_eye_point = np.array(l_eye_point)
                l_eye_contour.append(l_eye_point)

        r_eye_contour = np.array(r_eye_contour)
        l_eye_contour = np.array(l_eye_contour)
        return r_eye_contour, l_eye_contour
