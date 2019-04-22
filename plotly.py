# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 00:58:50 2019

@author: Calvin
"""

import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
uniform_data = np.random.rand(10, 12)
ax = sns.heatmap(uniform_data)