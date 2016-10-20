#!/usr/bin/env python
import cv2
import numpy as np
import math

####################################################################################################

#Mario Sebasco - Computational Geometry Project

####################################################################################################



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
        #Account for vertical line
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
#this last function finds a point in a polygon given a set of points
def pointInPoly(xmin,xmax,ymin,ymax,image):
    """Function to find a point in a convex polygon"""
    yavg = int(math.floor((ymin + ymax)/2))
    count = 0
    for i in range(xmin,xmax):
        #if you reached a black point
        if image[yavg,i,0] == 0 and image[yavg,i,1] == 0 and image[yavg,i,2] == 0 or count == 1:
            #walk to the nextpoint
            count = 1
            if image[yavg,i,0] == 255 and image[yavg,i,1] == 255 and image[yavg,i,2] == 255:
                xInPoly = i
                yInPoly = yavg
                break

    return xInPoly, yInPoly
    


######################################################################
# Set dimensions of display
width, height = 1000, 1000
unionPoly = create_blank(width,height)
interPoly = create_blank(width,height)


#Ask for user input
print('Please make sure that the format of your text file matches the sample text files provided.\n')


inputFile = raw_input('What is the name of the text file with the polygon vertices (eg. input1.txt)?\n Or type "sample2.txt" to view the sample file\n')


#Quick function used in converting the string file to the needed integers
def str2list(str):
    """convert a string input of a list and convert it to a numerical list"""
    endIndex = str.find(')')
    str = str[1:endIndex]
    str = str.split(',')
    count = 0
    for item in str:
        str[count] = int(item)
        count += 1
    return str
############################################################################################################################################

#set some default values
numLines = 0
numLines2 = 0
count = 0
xinput1 = []
yinput1 = []
xinput2 = []
yinput2 = []
color1 = (255,0,0)
color2 = (0,255,0)

#Read in vertices
with open(inputFile,"r") as input:
    for line in input:
        numLines += 1
        if line[0] == "P":
            count += 1
            numPoly = count
    print('Your file has %d polygon(s)\n' % numPoly)

with open(inputFile,"r") as input:
    if numPoly == 2:
        reachedPoly2 = False
        for line in input:
            if numLines == numLines2+1:
                line = line+'**'
            if line[0:2] == "P2":
                reachedPoly2 = True
            if not reachedPoly2:
                if line[0] == "(":
                    listLine = str2list(line)
                    if len(listLine) == 3:
                        color1 = listLine
                    if len(listLine) == 2:
                        xinput1.append(listLine[0])
                        yinput1.append(listLine[1])

            else:
                if line[0] == "(":
                    listLine = str2list(line)
                    if len(listLine) == 3:
                        color2 = listLine
                    if len(listLine) == 2:
                        xinput2.append(listLine[0])
                        yinput2.append(listLine[1])
            numLines2 += 1
    if numPoly == 1:
        color1 = (0,255,0)
        for line in input:
            if numLines == numLines2+1:
                line = line+'**'
            if line[0] == "(":
                listLine = str2list(line)
                xinput1.append(listLine[0])
                yinput1.append(listLine[1])
            numLines2 += 1

############################################################################################################################################

print('\nPlease wait a few seconds while the images are generated.\n')

######################################################################
#if there are two polygons then this chunk of code is run
#Find polygon in front
if numPoly ==2:
    sorted1 = []
    sorted2 = []
    sorted1y = []
    sorted2y = []

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
        floodImage2, unionPoly,interPoly = floodFill(pointInPoly2y,pointInPoly2x,lineImage2,color2,unionPoly,interPoly)

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
        floodImage1, unionPoly, interPoly = floodFill(pointInPoly1y,pointInPoly1x,lineImage1,color1,unionPoly,interPoly)
 
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
        floodImage1, unionPoly, interPoly = floodFill(pointInPoly1y,pointInPoly1x,lineImage1,color1,unionPoly,interPoly)

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
        floodImage2, unionPoly, interPoly = floodFill(pointInPoly2y,pointInPoly2x,lineImage2,color2,unionPoly,interPoly)

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


######################################################################
#If the number of polygons is 1, then this is prompted
if numPoly == 1:

    sorted1 = []
    sorted1y = []

    for i in xinput1:
        sorted1.append(i)

    for i in yinput1:
        sorted1y.append(i)

    sorted1.sort()
    sorted1y.sort()

    xmin1 = sorted1[0]
    xmax1 = sorted1[-1]
    ymin1 = sorted1y[0]
    ymax1 = sorted1y[-1]

    
    #Polygon 1
    image1 = create_blank(width, height)

    #Draw edges
    lineImage1, unionPoly,interPoly = lineGen(xinput1,yinput1,image1,unionPoly,interPoly)
    
    #Find point in polygon
    pointInPoly1x, pointInPoly1y = pointInPoly(xmin1,xmax1,ymin1,ymax1,lineImage1)
    
    #flood fill the polygon
    floodImage1, unionPoly, interPoly = floodFill(pointInPoly1y,pointInPoly1x,lineImage1,color1,unionPoly,interPoly)


    #image1 = cv2.imwrite('poly_image1.jpg', gray_image)
    #img1 = cv2.imread('poly_image1.jpg',1)
    cv2.imshow("Polygon1",floodImage1)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
