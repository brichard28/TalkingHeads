# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:13:25 2023

@author: maana
"""

import matlab.engine
eng = matlab.engine.start_matlab()

eng.test21(nargout=0)

