import pytesseract
import datetime
import time
import os
from scipy.misc import imsave
import re
from subprocess import call
import numpy as np

import cv2
class Daaru:
	def __init__(name, packs, volume, price):
		self.name = name
		self.packs = packs
		self.volume = volume
		self.price = price

def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

def cleanse_string(str):
	useless_characters = "~!@#$%^&*(){.}`:<.>?,./;'[]|\\"
	char_set = set()
	for c in useless_characters:
		char_set.add(c)

	ret = ""
	for i in range(0,len(str)):
		if str[i] not in char_set:
			ret =  ret + str[i]
    
	return ret

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
	return False


def cleanse_price(str):
	f = str.find("$")
	if f == -1:
		return ("", "")
	str = str[f+1:]
	f = str.find(" ")
	cents= ""
	dollar = ""
	if f == -1:
		cents = str[-2:]
		dollar = str[:2]

	else :
		dollar = str[0:f]
		cents = str[f+1:]

	return (dollar, cents)

def get_daaru_name(str1, str2):
	if len(str1) < 2:
		str1 = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	if len(str2) < 2:
		str2 = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

	daaru_names = ["SIERRA NEVADA TORPEDO",
"BROOKLYN OKTOBERFEST",
"CORONA EXTRA",
"LEFFE BLONDE",
"BROOKLYN PILSNER",
"CORONA LIGHT",
"BECKS",
"SIERRA NEVADA PALE ALE",
"BUD LIGHT",
"BUD LIGHT PLATINUM",
"HOEGAARDEN",
"MAGIC HAT",
"BLUE POINT TOASTED",
"STELLA ARTOIS",
"BUDWEISER",
"COORS LIGHT",
"MILLER LITE",
"BROOKLYN INDIA PALE"]
	min_dist = 1000000
	ans = ""
	for a in daaru_names:
		l_dist = min(edit_distance(a, str1), edit_distance(a,str2))
		#print str(l_dist) +  " <- " + a + " :: " + str1 +" /|\ " +str2 
		if l_dist < min_dist:
			min_dist = l_dist
			ans = a

	return ans

def edit_distance(s1, s2):
	s1 = cleanse_string(s1.lower().strip())
	s2 = cleanse_string(s2.lower().strip())
	m=len(s1)+1
	n=len(s2)+1
	tbl = {}
	for i in range(m): tbl[i,0]=i
	for j in range(n): tbl[0,j]=j
	for i in range(1, m):
		for j in range(1, n):
			cost = 0 if s1[i-1] == s2[j-1] else 1
			tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)
	return tbl[i,j]

def get_list(output_file):
	cnt = 0
	l = []
	with open(output_file) as f:
		for line in f:
			if(len(line.strip()) < 3 ):
				continue
			else:
			 	if cnt == 0 :
			 		cnt = cnt + 1
			 		l.append(line.replace("\n", ""))
			 	elif cnt == 1 :
			 		cnt = cnt + 1
			 		l.append(line.replace("\n", ""))
			 	elif cnt == 2 :
			 		cnt = cnt + 1
			 		l.append(line.replace("\n", ""))
	return l

def get_price(price1, price2):
	price1 = price1.lower().strip()
	price2 = price2.lower().strip()
	dollar1, cents1  = cleanse_price(price1)
	dollar2, cents2 = cleanse_price(price2)
	dollar = dollar1 if is_number(dollar1) else dollar2
	cents = ""
	if cents1[:1] != "9" and cents2[:1] == "9" :
		cents = cents2
	elif cents2[:1] != "9" and cents1[:1] == "9":
		cents = cents1
 	else:
 		cents = cents1 if is_number(cents1) else cents2
 	if cents[-1:] != "9" and len(cents) > 1:
 		cents = cents[0:len(cents)-1] + "9"
 	return "$ " + dollar + "." + cents

def process_packs_volume(str):
	str = str.lower().strip()
	f = str.find("pk")
	if f == -1:
		f = str.find("pm")

	left = str[0:f].strip()
	l_list = re.findall(r'\d+', left)
	if len(l_list) > 0:
		left = l_list[0]
	else :
		left = "6"
	right = str[f+3:].strip()
	cg = ""
	if right.find("ass") == -1:
		cg = "CAN"
	elif right.find("an") == -1:
		cg = "GLASS"
	data = right.split()
	if len(data) > 1 and is_number(data[1]) and data[1][0] != '0':
		return left, data[0]+"."+data[1], cg
	elif len(data) > 0:
		return left, data[0], cg
	else:
		return left, "12", cg



def get_packs_volume(str1, str2):
	packs1,vol1,cg1 = process_packs_volume(str1)
	packs2,vol2,cg2 = process_packs_volume(str2)
	if packs1 == "6" or packs2 == "6":
		packs = "6"
	else :
		packs = packs1 if is_number(packs1)  else packs2
	vol = vol1 if is_number(vol1)  else vol2
	cg = ""
	if len(cg1) == 0 and len(cg2) != 0 :
		cg = cg2
	if len(cg2) == 0 and len(cg1) != 0 :
		cg = cg1
	if len(cg1) !=0 and len(cg2) != 0 and cg1 != cg2:
		cg = "GLASS"
	elif cg1 == cg2:
		cg = cg1
	if len(cg) == 0:
		cg = "GLASS"
	return (packs, vol, cg)

def get_text(image):

	if image[0] == ".":
		return
	img = cv2.imread('a/'+image,0)
	dst = gamma_correction(img, 0.7)
  
	ret_gamma,thr_gamma =cv2.threshold(dst,0,255,cv2.THRESH_OTSU)
	ret,thr =cv2.threshold(img,0,255,cv2.THRESH_OTSU)
	imsave('temp_gamma.jpg', thr_gamma)
	imsave('temp.jpg', thr)  # convert image to monochrome
	call(['tesseract', 'temp.jpg', 'out'])
	call(['tesseract', 'temp_gamma.jpg', 'out_gamma'])
	call(['tesseract', 'temp.jpg', image + 'out'])
	call(['tesseract', 'temp_gamma.jpg', image +'out_gamma'])
	cnt = 0
	name = ""
	packs = ""
	volume = ""
	price = ""
	gamma_list = []
	non_gamma_list = []
	gamma_list = get_list('out_gamma.txt')
	non_gamma_list = get_list('out.txt')
	#print(non_gamma_list)
	#print(gamma_list)
	# Size of array check
	name = get_daaru_name(gamma_list[0], non_gamma_list[0])
	packs,volume,cg = get_packs_volume(gamma_list[1], non_gamma_list[1])
	if is_number(packs) == False:
		packs = "6"
	if packs == "5":
		packs = "6"
	if is_number(volume) == False:
		volume = "12"
	if len(gamma_list) < 3:
		gamma_list.append("")
	if len(non_gamma_list) < 3:
		non_gamma_list.append("")
	price = get_price(gamma_list[2], non_gamma_list[2])
	if volume == "2":
		volume = "12"
	if packs == "2" or packs == "1":
		packs = "12"
	print "------------"
	print name
	print packs + " " + volume + " " + cg
	print price
	print "------------"


if __name__ == "__main__":
    print(edit_distance("!#$!mm CORO NA LGHT","corona light"))
    get_daaru_name("as")
