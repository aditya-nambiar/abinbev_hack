
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

import numpy as np

def runningMean(x, N):
    y = np.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = np.sum(x[ctr:(ctr+N)])
    return y/N

im = Image.open("bud.jpg")

pix = im.load()



l = []
r=0;
g=0
b=0
l = []
arr = []
for i in range(im.size[1]):
    arr.append(0)
for k in range(0, 1000):
    x = randint(0,im.size[0]-10)
    val =0

    for y in range(0, im.size[1]):
        #for each pixel look at left 5 pixels
        #arr[y] += find_dist(pix[x,y][0],pix[x,y][1], pix[x,y][2], 96, 83, 68)
        arr[y] += find_dist(pix[x,y][0],pix[x,y][1], pix[x,y][2], 93, 91, 82)

for a in range(len(arr)):
    arr[a] = arr[a]/2000

arr = runningMean(arr, 15)
x4 = []
for y in range(0, im.size[1]):
    x4.append(y)

arr2 = []
for a in range(10,len(arr) -10):
    mina = 1000000
    for k in range(0,10):
        mina = min(mina, arr[a+k-5])
    arr2.append(mina)



plt.plot(arr2)
plt.savefig('try-dev.png')

for i in range(0,200):
    l = []
    prev = -1
    for y in range(10,len(arr2)-10):
        if int(round(arr2[y])) != i:
            continue
        if arr2[y] <= arr2[y-1] and arr2[y] >= arr2[y+1] and (prev == -1 or y > prev + 250):
            l.append(y)
            prev = y
    if len(l) == 3:
        break

for a in l:
    print a


# arr3 = []
# left_arr = []
# right_arr = []
# min_arr = []
# for a in range(100, len(arr2)-100):
#     left_sum = np.sum(arr2[a-50:a])/50
#     right_sum = np.sum(arr2[a:(a+10)])/10
#    p if left_sum - right_sum > 5:
#         left_arr.append(a)
#         continue
#     left_sum = np.sum(arr2[a-10:a])/10
#     right_sum = np.sum(arr2[a:(a+50)])/50
#     if right_sum - left_sum > 5:
#         right_arr.append(a)

# print "Dsf"
# prev = 0
# fin_arr = []
# for a in left_arr:
#     if prev != a-1:
#         print a
#         fin_arr.append([arr2[a],a])
#     prev = a

# fin_arr.sort()

# for p in fin_arr:
#     print 




# fin_arr = []
# for a in min_arr:
#     fin_arr.append((arr2[a],a))

# fin_arr.sort()

plt.plot(arr2)
plt.savefig('try-dev-budweizer1.png')



     
    

# for i in range(5 to X_val):
#     for j in range(Y_val):
#             r = 0
#             b = 0
#             g = 0
#             for k in range(0,4):
#                 for l in range(0,4):
#                     if((i*5+k)>=X_val*5 or (j*5+l)>=Y_val*5):
#                         continue
#                     r+=pix[i*5+k,j*5+l][0]
#                     g+=pix[i*5+k,j*5+l][1]
#                     b+=pix[i*5+k,j*5+l][2]
#                     # Set the value to 1 if green is atleast 1.2 times red and blue
  
# for j in range ((max_j)*5-h,(max_j)*5):
#     data[b][a]=pix[i,j]
#     b=b+1
# a=a+1


# img = Image.fromarray(data, 'RGB')
# # save the image of the number palte portion only as my.jpg
# img.save('my.jpg')


