# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:50:15 2023

@author: Benjamin Richardson and Maanasa Guru Adimurthy
"""

import matlab.engine
eng = matlab.engine.start_matlab()

eng.test21(nargout=0)
