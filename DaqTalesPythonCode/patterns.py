'''
helper library defining functions and tools to create specific shapes and patterns
'''
import voxelTable

def line(x0,y0,z0,x1,y1,z1):
   '''
   Returns a parameterization of a line with start [x0,y0,z0] and end [x1,y1,z1] point.
   '''
   def f(t): #0<=t<=1
       x = x0 + t*(x1-x0)
       y = y0 + t*(y1-y0)
       z = z0 + t*(z1-z0)
       return [x,y,z]
   return f


def plane(x0,y0,z0,x1,y1,z1,x2,y2,z2,invert=False):
    '''
    Returns a boolean set
    '''
    def f(x,y,z):
        val = 0 < -(y0*(z1-z2)-y1*(z0-z2)+y2*(z0-z1))*x\
                +(x0*(z1-z2)-x1*(z0-z2)+x2*(z0-z1))*y\
                +x0*(y1*z2-y2*z1)\
                +x1*(y0*z2-y2*z0)-\
                x2*(y0*z1-y1*z0)\
                +z*(x0*(y1-y2)-x1*(y0-y2)+x2*(y0-y1))
        if invert:
            return not val
        return val
    return f


def helix(x,y,z, radius, pitch):
    """
    Returns a parametrization of a helix with height z, centered around x,y with a given pitch and 
    """
    raise NotImplementedError()


def circle(x,y,z,radius):
    #TODO: define 
    cuboid = [-15,15,0,1,-15,15]
    circle = voxelizeSet(pipe,size,cuboid,**mat)
    raise NotImplementedError()

def pipe(x,y,z):
    radius = 10
    thick = 2
    r2 = x**2 + z**2 # circle equation
    return (radius-thick/2)**2 <= r2 and r2 <= (radius+thick/2)**2

def overhang(x0,y0,z0,height,extend):
    '''
    This function returns a parameterization pf a pillar with an overhang in x direction.
    '''
    def f(t): # an overhang is just two lines parameterized subseq.
        if t<0.5:
            return line(x0,y0,z0,  x0,y0,z0+height)(2*t)
        else:
            return line(x0,y0,z0+height, x0+extend,y0,z0+height)(2*(t-0.5))
    return f


def pillar(x0,y0,z0,height):
    '''
    Creates a pillar starting at position x0,y0,z0 with height height.
    '''
    return line(x0,y0,z0,  x0,y0,z0+height)


def wall(xStart,yStart,xEnd,yEnd,**args):
    raise NotImplementedError()

