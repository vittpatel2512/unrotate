import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

draw =True
drawfinal =True
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = 'img/a.jpg'
W = 1600.
oriimg = cv2.imread(filename)
height, width, depth = oriimg.shape
imgScale = W/width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
newimg = cv2.resize(oriimg,(int(newX),int(newY)))

img = newimg
ih = img.shape[0]
iw = img.shape[1]

kernel = np.array([
       [ 1, 1],
       [ 1, 1]],dtype=np.uint8)

vkernel = np.array([
       [0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0]],dtype=np.uint8)

deg = -5
rotdegs = []
avgslopes = []
slopevars = []

while deg < 5:
    img = newimg
    center = (iw / 2, ih / 2)
    M = cv2.getRotationMatrix2D(center,deg , 1) 
    img = cv2.warpAffine(img, M, (iw, ih))
    
    y1 = int(float(ih)/3.0)
    y2 = int(float(ih) - float(ih)/3.0)
    
    x1 = int(float(iw)/3.0)
    x2 = int(float(iw) - float(iw)/3.0)
    
    img = img[y1:y2, x1:x2]

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    cv2.imshow('block filter',opening )
    cv2.waitKey(0) 
    vopening = cv2.morphologyEx(opening,cv2.MORPH_OPEN,vkernel, iterations = 1)
   
    cv2.imshow('h filter',vopening )
    cv2.waitKey(0) 

    edges=cv2.Canny(vopening,100,170,apertureSize=3)
    #theta accuracy of (np.pi / 180) which is 1 degree
    #line threshold is set to 240(number of points on line)
    lines=cv2.HoughLines(edges, 1, (np.pi/180)*.5, 50)
    #we iterate through each line and convert into the format
    #required by cv2.lines(i.e. requiring end points)
    if lines is not None:
        #lineimg = np.zeros((ih,iw,3), np.uint8)
        absvslopes = []
        vslopes = []
        for i in range(0,len(lines)):   
            for rho, theta in lines[i]: 
                a=np.cos(theta)
                b=np.sin(theta)
                x0=a*rho
                y0=b*rho
                if abs(a) > .99:
                    absvslopes.append(abs(a))
                    vslopes.append(a)
                    #print( round(a,4),)
                    if draw:
                        x1=int(x0+iw*(-b))
                        y1=int(y0+iw*(a))
                        x2=int(x0-iw*(-b))
                        y2=int(y0-iw*(a))
                        
                        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
                    
                #cv2.line(lineimg,(x1,y1),(x2,y2),(255,255,255),1)
        print(deg)
        print("\tavg:"+str(np.mean(absvslopes))+' c:'+str(len(absvslopes))+" v:"+str(np.var(absvslopes)))
        rotdegs.append(deg)
        avgslopes.append(np.mean(absvslopes))
        slopevars.append(np.var(absvslopes))
        if draw:
            cv2.imshow('rotated ' +str(deg),img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    deg +=0.2
rotdeg = round(rotdegs[np.argmax(avgslopes)],2)
print(avgslopes)
print(avgslopes)
print(slopevars)

print(rotdeg)

if drawfinal:
    img = newimg
    center = (iw / 2, ih / 2)
    M = cv2.getRotationMatrix2D(center,rotdeg, 1) 
    img = cv2.warpAffine(img, M, (iw, ih))
    cv2.imshow('original',newimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('rotated',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

oheight, owidth, odepth = oriimg.shape
center = (owidth / 2,oheight / 2)
M = cv2.getRotationMatrix2D(center,rotdeg, 1) 
newimg = cv2.warpAffine(oriimg, M, (owidth, oheight))
cv2.imwrite("temp.jpg",newimg)
