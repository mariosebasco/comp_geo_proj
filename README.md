# Mario Sebasco - Computational Geometry Project 1


## Intro/Description

The program `compGeoProj.py` is a python script which uses python 2.7.6 and the following three libraries:
* math (standard math library)
* cv2 (OpenCV is an open source image processing tool compatible with Python)
* numpy (Extended math library for Python. Enables the use of matrices.)

The program has several different functions that come together to produce the final result. 
* create_blank: This function simply creates a blank image of (height,width) pixels. Please note that the height and width are defaulted to 1000. Changing this needs to be done in the source code.
* lineGen: This function obtains a set of vertices and generates the polygon lines. It follows Bresenham's algorithm in order to generate them.
* floodFill: Flood fill takes in a set of starting points and the image generated from lineGen and colors in the polygon give a specified color (BGR is the default for OpenCV, not RGB). It recursively looks outwards from where it is until it hits all the edges.
* pointInPoly: This function is used in order to find a point inside a polygon (which is later used in floodFill). The function simply walks along the x-axis (at y_avg=(ymax+ymin)/2) until it finds the edge of the polygon, it the continues to walk until it lands inside the polygon and returns the set of points.
*str2list: This small function is used in order to aid in the reading of the input text files. It transforms a list in string format to a numerical list.

The overall program then is just a combination of these functions used to display the polygons, their union, and their intersections.


## Running the code
In order to run the code use the executable file `compGeoProj.py`. The terminal will prompt you to input the name of the text file consisting of the polygonal vertices. If input correctly the program will then generate the images (four if two polygons are involved: polygon1, polygon2, union, intersection). The folder comes with `sample1.txt` and `sample2.txt` as examples of what the user should expect to see.

Please note the following restrictions for the program:
* The text file must mimic that of the two sample text files provided
* The program will only run if there are one or two polygons, it is not developed for more. Although implementation can be applied with relative ease if needed.
* The vertices of the polygons must be integers. Although implementation of polygons with non-integer vertices can be implemented with relative ease if needed.