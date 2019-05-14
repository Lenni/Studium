#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:06:09 2019

@author: lennart
"""

import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import special

# Create a sphere
r = 3
pi = np.pi
cos = np.cos
sin = np.sin
phi, theta = np.mgrid[0:pi:200j, 0:2*pi:200j]


x = r * sin(phi) * cos(theta)
y = r * sin(phi) * sin(theta)
z = r * cos(phi)

colorfunction=special.sph_harm(2,1,theta,phi).imag

norm=colors.Normalize()


fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(x, y, z)
ax.plot_surface(x, y, z, cmap=cm.jet, facecolors=cm.jet(norm(colorfunction)))
plt.show()