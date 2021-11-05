#!/usr/bin/python3
import math
import sys
from matplotlib import pyplot as plt

def small_spiral(searchRadius, pointDistance):
    return spiral(float(pointDistance), float(pointDistance), float(searchRadius))

def big_spiral(searchRadius, pointDistance):
    return spiral(float(pointDistance), float(pointDistance), float(searchRadius))


def polarToCartesian(r,phi):
    return (r*math.cos(phi), r*math.sin(phi))

def spiral(lineSeperation,pointDistance,searchRadius):
    """
    This function creates an archemidean spiral approximately.
    To calculate the distance between two points we simplify the spiral to a circle.

    Parameteris
    ----------
    lineSeperation: int
        Distance between the turnings
    pointDistance: int
        Distance between the (approximately) equidistant points on the spiral
    searchRadius: int
        Radius within the returned points should be in.

    Returns
    -------
    points: list
        Returns an list of tuples representing (x,y) coordinates.
    """

    #points = [(0,0)] does work but we do add a second point to interpolate around 0
    points = [(0,0),(0,-0.7*pointDistance)]
    r = pointDistance
    #Spiral formula r = b*phi
    b = lineSeperation/(2*math.pi)
    # start with first turning
    phi = 2*math.pi

    count = 0
    while( r < searchRadius):
        count+=1
        points.append(polarToCartesian(r,phi))
        # update phi - by assuming the current and next poins are
        # both on a circle with radius r
        phi += pointDistance/r
        # update r with spiral formula
        r = phi*b

    print("Pattern contains " + str(count) + " coordinates.")
    return points


if __name__ == "__main__" :
    '''
    Create spirals and plots them.
    '''
    # set parameters
    big_r,big_precision,small_r,small_precision = 2,0.25,0.7,0.1

    # create spirals
    big_points = big_spiral(big_r, big_precision)
    small_points = small_spiral(small_r, small_precision)
    x_big,y_big,x_small,y_small = [],[],[],[]
    for (px, py) in big_points:
        x_big.append(px)
        y_big.append(py)
    for (px, py) in small_points:
        x_small.append(px)
        y_small.append(py)
    xSmallStart = x_big[-1]
    ySmallStart = y_big[-1]
    #x_small = [i+xSmallStart for i in x_small]
    #y_small = [i+ySmallStart for i in y_small]


    fig,(ax1, ax2) = plt.subplots(1, 2,sharey=True)
    ax1.plot(x_big, y_big, 'o-', color = (0, 89/255, 179/255))
    ax2.plot(x_small, y_small, 'o-', color = (179/255, 71/255, 0))

    ax1.set(xlabel='x',ylabel='y')
    ax2.set(xlabel='x')
    ax1.axis('equal')
    ax2.axis('equal')
    ax1.grid()
    ax2.grid()


    plt.show()

    print("Scan Process with following parameters: BigScan(radius = %s um, prec\
ision = %s um), SmallScan(radius = %s um, precision = %s um)."%(big_r,big_precision,
small_r,small_precision))
