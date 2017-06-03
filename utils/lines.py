import numpy as np
from methods import curvature_measurement as cm

class Lines():
    def __init__(self, detected, recent_xfitted_left, recent_xfitted_right):
            # was the line detected in the last iteration?
            self.last_detected = detected
            self.detected = False

            # x values of the last n fits of the line
            self.recent_xfitted_left = recent_xfitted_left
            # x values of the last n fits of the line
            self.recent_xfitted_right = recent_xfitted_right
            
            #polynomial coefficients for the most recent fit
            self.current_fit_left = [np.array([False])]  
            #polynomial coefficients for the most recent fit
            self.current_fit_right = [np.array([False])] 
            

    def setCurrentFit(self, left_fitx, right_fitx):
        self.detected = True
        self.current_fit_left = left_fitx
        self.current_fit_right = right_fitx

    def evaluate(self):
        correct = True
        if self.detected == True:
            if self.last_detected == True:
                #sanity checks
                if (self.__lanes_in_right_distance(self.current_fit_left[-1], self.current_fit_right[-1])
                        and self.__lanes_parallel(self.current_fit_left[-2:], self.current_fit_right[-2:])):
                    self.recent_xfitted_left.append(self.current_fit_left)
                    self.recent_xfitted_right.append(self.current_fit_right)
                else:
                    self.recent_xfitted_left.append(self.recent_xfitted_left[-1])
                    self.recent_xfitted_right.append(self.recent_xfitted_right[-1])
                    correct = False
            else:
                return self.current_fit_left, self.current_fit_right, correct
        else:
            correct = False
        
        return (np.mean((self.recent_xfitted_left), axis=0),
                np.mean((self.recent_xfitted_right), axis=0), correct)

    def measure(self, ploty):
        return cm.measure(ploty, self.current_fit_left, self.current_fit_right)

    def __lanes_in_right_distance(self, x1, x2):
        if x2-x1 > 350 and x2-x1 < 750:
            return True
        return False

    def __lanes_parallel(self, x1, x2):
        if abs((x1[0]-x2[0]) - (x1[1]-x2[1])) < 0.35:
            return True
        return False
