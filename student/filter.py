# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        self.F = self.F()
        self.Q = self.Q()

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############
        dt = params.dt

        F = np.matrix([
            [1, 0, 0, dt, 0, 0],
            [0, 1, 0, 0, dt, 0],
            [0, 0, 1, 0, 0, dt],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        return F
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############

        t = params.dt
        q = params.q

        t3q = pow(t, 3) * q / 3
        t2q = pow(t, 2) * q / 2
        tq = t * q

        Q = np.matrix([
            [t3q, 0, 0, t2q, 0, 0],
            [0, t3q, 0, 0, t2q, 0],
            [0, 0, t3q, 0, 0, t2q],
            [t2q, 0, 0, tq, 0, 0],
            [0, t2q, 0, 0, tq, 0],
            [0, 0, t2q, 0, 0, tq]
        ])
        return Q
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############

        x = self.F * track.x
        P = self.F * track.P * self.F.transpose() + self.Q
        track.set_x(x)
        track.set_P(P)
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############

        H = meas.sensor.get_H(track.x)  # Measurement Jacobian
        gamma = self.gamma(track, meas)  # Residual
        S = self.S(track, meas, H) # Residual Covariance

        P = track.P

        K = P * H.transpose()*np.linalg.inv(S) # Kalman Gain

        x = track.x + K*gamma  # State Update
        I = np.identity(params.dim_state)
        P = (I - K*H) * P  # Covariance Update

        track.set_x(x)
        track.set_P(P)
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        hx = meas.sensor.get_hx(track.x)
        gamma = meas.z - hx
        return gamma
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############

        S = H * track.P * H.transpose() + meas.R
        return S
        
        ############
        # END student code
        ############ 