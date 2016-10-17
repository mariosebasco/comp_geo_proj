#!/usr/bin/env python
import cv2
import numpy as np
import math


######################################################################
#First we create an empty image, which is just white
def create_blank(width, height):
    """Create empty grid"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    #Switch color to white
    image[:] = (255,255,255)
    return image

######################################################################
#Next we will draw lines from veritices by creating the lineGen function
def lineGen(x,y,blank,unionPoly,interPoly):
    """Create edges from vertices"""
    x.append(x[0])
    y.append(y[0])
    for i in range(len(x) - 1):
        #first account for vertial line
        if x[i] == x[i+1]:
            x[i+1] += 1
        #Account for horizontal lines
        if y[i] == y[i+1]:
            y[i+1] += 1
        slope = (y[i+1] - y[i])/float((x[i+1] - x[i]))
        yint = y[i] - slope*x[i]
        xcurr = x[i]
        ycurr = y[i]
        xend = x[i+1]
        yend = y[i+1]
        #if you are in the starting point then mark it in the blank image
        blank[y[i],x[i]] = (0,0,0)
        blank[y[i+1],x[i+1]] = (0,0,0)
        unionPoly[y[i],x[i]] = (0,0,255)
        unionPoly[y[i+1],x[i+1]] = (0,0,255)
        interPoly[y[i],x[i]] = (0,0,0)
        interPoly[y[i+1],x[i+1]] = (0,0,0)
#1)forward, positive slope, steep line
        if x[i+1] > x[i]:
            if slope > 0:
                if abs(slope) > 1:
                    while ycurr != yend:
                        xactual = (ycurr - yint)/slope
                        if xactual - (xcurr + 0.5) >= 0:
                            xcurr += 1
                            ycurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            ycurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#2)forward, positive slope, short line
                else:
                    while xcurr != xend:
                        yactual = slope*xcurr + yint
                        if yactual - (ycurr + 0.5) >= 0:
                            xcurr += 1
                            ycurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            xcurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#3)backward,positive slope, steep line
        if x[i+1] < x[i]:
            if slope > 0:
                if abs(slope) > 1:
                    while ycurr != yend:
                        xactual = (ycurr - yint)/slope
                        if xactual - (xcurr - 0.5) <= 0: 
                            xcurr -= 1
                            ycurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            ycurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#4)backward, positive slope, short line
                else:
                    while xcurr != xend:
                        yactual = slope*xcurr + yint
                        if yactual - (ycurr - 0.5) <= 0:
                            xcurr -= 1
                            ycurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            xcurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#5)forward, negative slope, steep line
        if x[i+1] > x[i]:
            if slope < 0:
                if abs(slope) > 1:
                    while ycurr != yend:
                        xactual = (ycurr - yint)/slope
                        if xactual - (xcurr + 0.5) >= 0:
                            xcurr += 1
                            ycurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            ycurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#6)forward, negative slope, short line
                else:
                    while xcurr != xend:
                        yactual = slope*xcurr + yint
                        if yactual - (ycurr - 0.5) <= 0:
                            xcurr += 1
                            ycurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            xcurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#7)backward, negative slope, steep line
        if x[i+1] < x[i]:
            if slope < 0:
                if abs(slope) > 1:
                    while ycurr != yend:
                        xactual = (ycurr - yint)/slope
                        if xactual - (xcurr - 0.5) <= 0:
                            xcurr -= 1
                            ycurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            ycurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
#8)backward, negative slope, short line
                else:
                    while xcurr != xend:
                        yactual = slope*xcurr + yint
                        if yactual - (ycurr + 0.5) >= 0:
                            xcurr -= 1
                            ycurr += 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
                        else:
                            xcurr -= 1
                            blank[ycurr,xcurr] = (0,0,0)
                            unionPoly[ycurr,xcurr] = (0,0,255)
                            interPoly[ycurr,xcurr] = (0,0,0)
    
    return blank, unionPoly, interPoly
                


##################################################
#Next we color the inside of the polygon
def floodFill(xstart,ystart,image,color,unionPoly,interPoly):
    """Color in a set of closed vertices (polygon)"""
    image[xstart,ystart] = color
    unionPoly[xstart,ystart] = (0,0,255)
    interPoly[xstart,ystart] = color
    oldList = []
    newList = []
    oldList.append((xstart,ystart))
    shouldContinue = True
    #failsafe
    i = 0
    while shouldContinue == True:
        for point in oldList:
            currx = point[0]
            curry = point[1]
            if image[(currx + 1),curry,0] == 255 and image[(currx + 1),curry,1] == 255 and image[(currx + 1),curry,2] == 255:
                image[currx+1,curry] = color
                unionPoly[currx+1,curry] = (0,0,255)
                interPoly[currx+1,curry] = color
                newList.append((currx+1,curry))
            if image[(currx - 1),curry,0] == 255 and image[(currx - 1),curry,1] == 255 and image[(currx - 1),curry,2] == 255:                
                image[currx-1,curry] = color
                unionPoly[currx-1,curry] = (0,0,255)
                interPoly[currx-1,curry] = color
                newList.append((currx-1,curry))
            if image[currx,curry + 1,0] == 255 and image[currx,curry + 1,1] == 255 and image[currx,curry + 1,2] == 255:
                image[currx,curry+1] = color
                unionPoly[currx,curry+1] = (0,0,255)
                interPoly[currx,curry+1] = color
                newList.append((currx,curry+1))
            if image[currx,curry - 1,0] == 255 and image[currx,curry - 1,1] == 255 and image[currx,curry - 1,2] == 255:
                image[currx,curry-1] = color
                unionPoly[currx,curry-1] = (0,0,255)
                interPoly[currx,curry-1] = color
                newList.append((currx,curry-1))
        i += 1
        if len(newList) == 0 or i > 2000:
            shouldContinue = False
        oldList = newList
        newList = []

    return image, unionPoly, interPoly
    

######################################################################
def pointInPoly(xmin,xmax,ymin,ymax,image):
    """Function to find a point in a convex polygon"""
    yavg = int(math.floor((ymin + ymax)/2))
    for i in range(xmin,xmax):
        if image[yavg,i,0] == 0 and image[yavg,i,1] == 0 and image[yavg,i,2] == 0:
            xInPoly = i + 1
            yInPoly = yavg
            break
        else:
            i += 1
    return xInPoly, yInPoly
    


######################################################################
# Set dimensions of display
width, height = 1000, 1000
unionPoly = create_blank(width,height)
interPoly = create_blank(width,height)

#Obtain Input
xinput1 = [150,450,570,653,495,350,100]
yinput1 = [300,300,525,780,845,790,345]

xinput2 = [285,500,831,625,444,285]
yinput2 = [420,225,543,695,710,555]

sorted1 = []
sorted2 = []
sorted1y = []
sorted2y = []

#Find polygon in front
for i in xinput1:
    sorted1.append(i)
    
for i in yinput1:
    sorted1y.append(i)

for i in xinput2:
    sorted2.append(i)

for i in yinput2:
    sorted2y.append(i)
    
sorted1.sort()
sorted2.sort()
sorted1y.sort()
sorted2y.sort()

xmin1 = sorted1[0]
xmax1 = sorted1[-1]
ymin1 = sorted1y[0]
ymax1 = sorted1y[-1]

xmin2 = sorted2[0]
xmax2 = sorted2[-1]
ymin2 = sorted2y[0]
ymax2 = sorted2y[-1]

if sorted1[0] <= sorted2[0]:
    poly1IsFirst = True
else:
    poly1IsFirst = False

if poly1IsFirst:
    #draw polygon 2 then draw polygon 1 (in the intersection image)
    ####################################################################
    #Polygon 2
    image2 = create_blank(width,height)

    #Draw edges
    lineImage2, unionPoly, interPoly = lineGen(xinput2,yinput2,image2,unionPoly,interPoly)

    #Find point inside polygon
    pointInPoly2x, pointInPoly2y = pointInPoly(xmin2,xmax2,ymin2,ymax2,lineImage2)

    #flood fill the polygon
    color2 = (0,255,0)
    floodImage2, unionPoly,interPoly = floodFill(pointInPoly2y,pointInPoly2x,lineImage2,color2,unionPoly,interPoly)
    #grayImage2 = cv2.cvtColor(floodImage2,cv2.COLOR_BGR2GRAY)
    #(thresh, bwImage2) = cv2.threshold(grayImage2, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #image2 = cv2.imwrite('poly_image2.jpg', floodImage2)
    #img2 = cv2.imread('poly_image2.jpg',1)
    cv2.imshow("Polygon2",floodImage2)

    ######################################################################
    #Polygon 1
    image1 = create_blank(width, height)

    #Draw edges
    lineImage1, unionPoly,interPoly = lineGen(xinput1,yinput1,image1,unionPoly,interPoly)
    
    #Find point in polygon
    pointInPoly1x, pointInPoly1y = pointInPoly(xmin1,xmax1,ymin1,ymax1,lineImage1)
    
    #flood fill the polygon
    color1 = (255,0,0)
    floodImage1, unionPoly, interPoly = floodFill(pointInPoly1y,pointInPoly1x,lineImage1,color1,unionPoly,interPoly)
    #grayImage1 = cv2.cvtColor(floodImage1,cv2.COLOR_BGR2GRAY)
    #(thresh, bwImage1) = cv2.threshold(grayImage1, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #image1 = cv2.imwrite('poly_image1.jpg', gray_image)
    #img1 = cv2.imread('poly_image1.jpg',1)
    cv2.imshow("Polygon1",floodImage1)
    

    ######################################################################
    #Find the Union
    cv2.imshow("Polygon_Union",unionPoly)

    ######################################################################
    #find the intersection
    cv2.imshow("Polygon_Intersection",interPoly)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    #draw polygon 1 then draw polygon 2
    ######################################################################
    #Polygon 1
    image1 = create_blank(width, height)

    #Draw edges
    lineImage1, unionPoly, interPoly = lineGen(xinput1,yinput1,image1,unionPoly,interPoly)

    #Find point inside polygon
    pointInPoly1x, pointInPoly1y = pointInPoly(xmin1,xmax1,ymin1,ymax1,lineImage1)

    #flood fill the polygon
    color1 = (255,0,0)
    floodImage1, unionPoly, interPoly = floodFill(pointInPoly1y,pointInPoly1x,lineImage1,color1,unionPoly,interPoly)
    #grayImage1 = cv2.cvtColor(floodImage1,cv2.COLOR_BGR2GRAY)
    #(thresh, bwImage1) = cv2.threshold(grayImage1, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #image1 = cv2.imwrite('poly_image1.jpg', gray_image)
    #img1 = cv2.imread('poly_image1.jpg',1)
    cv2.imshow("Polygon1",floodImage1)


    ####################################################################
    #Polygon 2
    image2 = create_blank(width,height)

    #Draw edges
    lineImage2, unionPoly, interPoly = lineGen(xinput2,yinput2,image2,unionPoly, interPoly)

    #Find point inside polygon
    pointInPoly2x, pointInPoly2y = pointInPoly(xmin2,xmax2,ymin2,ymax2,lineImage2)

    #flood fill the polygon
    color2 = (0,255,0)
    floodImage2, unionPoly, interPoly = floodFill(pointInPoly2y,pointInPoly2x,lineImage2,color2,unionPoly,interPoly)
    #grayImage2 = cv2.cvtColor(floodImage2,cv2.COLOR_BGR2GRAY)
    #(thresh, bwImage2) = cv2.threshold(grayImage2, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #image2 = cv2.imwrite('poly_image2.jpg', floodImage2)
    #img2 = cv2.imread('poly_image2.jpg',1)
    cv2.imshow("Polygon2",floodImage2)

    ######################################################################
    #Find the Union
    cv2.imshow("Polygon_Union",unionPoly)

    ######################################################################
    #find the intersection
    cv2.imshow("Polygon_Intersection",interPoly)


    
    cv2.waitKey(0)
    cv2.destroyAllWindows()




