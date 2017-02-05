
from PIL import Image
import numpy as np
import sys
import math
import os
import datetime

import matplotlib.pyplot as plt
from random import randint

import statistics
import numpy as np
from scipy.misc import imsave

import scipy

def find_dist(x1,y1,z1,x2,y2,z2):
    sum =0
    sum += (x1-x2)* (x1-x2)
    sum += (y1-y2) * (y1 - y2)
    sum += (z1 - z2) * (z1 - z2)
    return math.sqrt(sum)


big = Image.open("1.jpg")
small = Image.open("sub.jpg")
small_1 = scipy.misc.imresize(small, 0.05)
big_1 = scipy.misc.imresize(big, 0.05)
imsave('small.jpg', small_1)
imsave('big.jpg', big_1)
small = Image.open("small.jpg")
big = Image.open("big.jpg")


pix_big = big.load()
pix_small = small.load()

min_val = 10000000
x_min = 0
y_min = 0

for x in range(0, big.size[0]):
    for y in range(0, big.size[1]):
        #for each pixel look at left 5 pixels
        big_arr = []
        small_arr = []
        sum = 0
        for i in range(0, small.size[0]):
        	for j in range(0, small.size[1]):
        		if i+x < big.size[0] and j+y < big.size[1]:
        			dist = find_dist(pix_small[i,j][0],pix_small[i,j][1],pix_small[i,j][2],pix_big[i+x,j+y][0],pix_big[i+x,j+y][1],pix_big[i+x,j+y][2])
        		sum += dist
  
        if sum < min_val :
        	min_val = sum
        	x_min = x
        	y_min = y

print x_min
print y_min

print big.size[0]
print big.size[1]



