'''
Contains functions to work with a array - sometimes called table - of voxels. The underlying
data type is a numpy array with custom type `dt`. Facilitates creation, modification and
visualisation of voxel data. See quickStart.ipynp for a tutorial.
'''
# import all modules as privat to preserve a clean the namespace when importing with *
import numpy as _np
from matplotlib import pyplot as _plt
from matplotlib.lines import Line2D as _Line2D
from mpl_toolkits.mplot3d import Axes3D as _Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as _Poly3DColletion
from matplotlib.animation import FuncAnimation as _FuncAnimation
from timeit import default_timer as _default_timer

# custom data type presenting a voxel.
dt = _np.dtype([('x',_np.float),('y',_np.float),('z',_np.float),('Vdepo',_np.float),('p1',_np.float),('p2',_np.float),('p3',_np.float),('p4',_np.float)])
# constants to define the conversion from memory to disk when saving
headerString = '#      x,       y,       z, Vdepo,  p1,  p2,  p3,  p4\n'
formater='%8.3f,%8.3f,%8.3f,%1.3f,%3.1f,%3.1f,%3.1f,%3.1f\n'

def load(filename):
    ''' Given a file returns a corresponding voxel tabel.'''
    return _np.genfromtxt(filename,dtype=dt,delimiter=',')

def save(array,filename):
    ''' Given a voxel table and a filename: saves the voxels to disk.'''
    csv = open(filename,'w')
    csv.write(headerString)
    for vox in array:
        csv.write(formater % tuple(vox))
    csv.close()

def moveBeyond(array,x=None,y=None,z=None):
    ''' Moves the most left bottum voxel to the specified coordinate. Such that the entire object is beyond the specified coordinate.  '''
    if x is not None:
        array['x'] += x - _np.min(array['x'])
    if y is not None:
        array['y'] += y - _np.min(array['y'])
    if z is not None:
        array['z'] += z - _np.min(array['z'])
    return array # return just for consistency

def moveFirstVoxel(array,x=None,y=None,z=None):
    ''' Moves the first voxel, so the base of the object, to the specified posiiton.'''
    if x is not None:
        array['x'] += x - array[0]['x']
    if y is not None:
        array['y'] += y - array[0]['y']
    if z is not None:
        array['z'] += z - array[0]['z']
    return array # for consistency

def add(array,x=None,y=None,z=None,Vdepo=None,p1=None,p2=None,p3=None,p4=None):
    '''
    Adds to every voxel the specified value(s). If a value is not specified leave
    it untouched.
    '''
    if x is not None:
        array['x'] += x
    if y is not None:
        array['y'] += y
    if z is not None:
        array['z'] += z
    if Vdepo is not None:
        array['Vdepo'] += Vdepo
    if p1 is not None:
        array['p1'] += p1
    if p2 is not None:
        array['p2'] += p2
    if p3 is not None:
        array['p3'] += p3
    if p4 is not None:
        array['p4'] += p4
    return array # for consistency

def merge(*objects):
    ''' Given voxel objects merge them all and return'''
    voxels = objects[0]
    for i in objects[1:]:
        voxels = _np.append(voxels,i)
    return voxels

def empty():
    '''
    Returns an empty voxel list. This is usefull if iterativelly creating 
    an object and the merging.
    '''
    return _np.array([],dtype=dt)

def sort(voxels):
    ''' Sort the voxels for printing, sort first in z then in x and last in y direction.'''
    return _np.sort(voxels,order=['z','x','y'])

def _rotate(voxels,xangle=None,yangle=None,zangle=None):
    '''TODO'''
    raise ValueError('This function is not yet implemented.')
    return voxels # for consistency

def _raster(c,siz):
    '''Rasterizes a coordinate.'''
    return round(c/siz)*siz

def rasterize(voxels,size):
    '''Rasterizes the voxel array. Every voxel gets rounded to the nearest point on a grid. The
    grid is ankered at 0,0,0 and has grid-size equal to size. This allows to discretize an arbitrary
    voxel table.'''
    for i in voxels:
        i['x'] = _raster(i['x'],size[0])
        i['y'] = _raster(i['y'],size[1])
        i['z'] = _raster(i['z'],size[2])
    return voxels

def copy(voxels):
    '''Returns a copy from a given voxel array.'''
    return voxels.copy()

def unique(voxels):
    '''Returns a voxel array with all duplicates removed.'''
    return _np.unique(voxels)

def finalize(voxels,size):
    '''Rasterizes, sorts and removes duplicated voxels. After finalize a voxel file should be stable to print.'''
    voxels = rasterize(voxels,size)
    voxels = unique(voxels)
    voxels = sort(voxels)
    return voxels

def _getMaterial(Vdepo=None,p1=None,p2=None,p3=None,p4=None):
    '''
    The material can be defined by setting keyword arguments `Vdepo=18`. Not set values default to 0.
    If Vdepo or all pressure values are undefined a Value error gets raised. This can
    be overriden by manually setting values to 0.
    '''
    if Vdepo is None:
        raise ValueError('The deposition voltage is not set. Not defaulting to zero.\
to override this manually pass: Vdepo=0')
    if p1 == p2 == p3 == p4 == 0:
        return (Vdepo,0,0,0,0)
    if p1 is None:
        p1=0
    if p2 is None:
        p2=0
    if p3 is None:
        p3=0
    if p4 is None:
        p4=0
    if p1 == p2 == p3 == p4 == 0:
        raise ValueError('Every pressure defaults to 0. Explicitly set all values\
                        to force this behavior')
    return (Vdepo,p1,p2,p3,p4)

def voxelizeCurve(curve,size,resolution=1000,precision=5,**kwargs):
    '''
    Given a parameterize Curve returns a correpsonding voxel table. The
    parameterize curve has to be a function that takes one argument t, t element
    [0,1] and returns a list of three poins [x(t),y(t),z(t)]. Note:
    a voxel is defined by its top center coordinate.

    As example one might use a sinus:
    def line(t):
        return([0,0,5t])

    def sinus(t):
        return([t, 0, 10*math.sin(2*math.pi*t) + 10])
    '''
    material = _getMaterial(**kwargs)
    voxels = []
    for i in _np.linspace(0, 1,resolution):
        x,y,z = curve(i)
        x,y,z = _raster(x,size[0]),_raster(y,size[1]),_raster(z,size[2])
        voxels.append((x,y,z,*material))
    voxels = _np.array(voxels, dtype=dt)
    return _np.unique(voxels)

def _floatRange(start,stop,step):
    '''A generator to get C like 'for' behaviour.'''
    f = start
    while(f < stop):
        yield(f)
        f += step

def voxelizeSet(boolSet,size,cuboid,**kwargs):
    '''
    This function goes through the grid defined by size and bound by the cuboid'
    The cuboid argument takes a list of the form[xmin,xmax,ymin,ymax,zmin,zmax].
    While iterating throught the grid the given function boolSet get evaluated.
    boolSet is a funciton that must take three input parameters (x,y and z) and
    return true or false depending on if the given point is element of the set.

    A well known mathematical Set is the sphere. Here it serves as an example
    for a possible boolSet parameter. The chosen radius is hardcoded to 5 and the
    middle of the sphere is [0,0,0].

    def sphere(x,y,z):
        r2 = x**2 + y**2 + z**2
        return r2 <= 5**2

    When choosing a voxel size of [1,1,1] the evaluation cuboid can be: [-6,6,-6,6,-6,6].
    Any bigger cuboid will not change the result. However if providing
    cuboid=[-6,6,-6,6,1,6] a half-sphere results.

    The function can be evaluated with:
    voxels = voxelizeSet(sphere,size=[1,1,1],cuboid=cuboid)
    '''
    material = _getMaterial(**kwargs)
    (xstart,xstop,ystart,ystop,zstart,zstop) = cuboid
    voxels = []
    # start iterating with z then with x to 'avoid' sorting
    for z in _floatRange(zstart,zstop,size[2]):
        for x in _floatRange(xstart,xstop,size[0]):
            for y in _floatRange(ystart,ystop,size[1]):
                if boolSet(x,y,z):
                    voxels.append((x,y,z,*material))
    return _np.array(voxels,dtype=dt)

def cubeFaces(voxel,size):
    ''' Returns a numpy array of faces of a cuboid with its middle point of the top
    surface corresponding to the voxel location. The cuboid has the given size.'''
    # create a list of 6 faces - each face being defined by a list of 4 corners
    faces = [[[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]],
            [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]],
            [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
            [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
            [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    points = _np.array(faces,dtype=float)
    # correct the top middle point to the bottom left corner as the faces
    # are given in respect to 0,0,0
    points -= _np.array([0.5,0.5,1])
    for i in range(3): # scale faces
        points[:,:,i] *= size[i]
    points += _np.array([voxel['x'],voxel['y'],voxel['z']]) # move faces to position
    return points

def plotObject(voxels,size,border=True,info=False,colorDict=None,path=None):
    '''
    Plots the object in 3D space. This only works if the voxels are true voxels,
    meaning they can bee seen as having a constant size.
    `border=False` prevents the drawed voxels to be outlined with black
    `info=True` prints usefull positioning and dimension information
    `colorDict` provide to override the auto coloring. set ``info=True`` for details
    `path` set to a file path to save the plot as .png instead of interactive rendering.
    '''
    if len(voxels)==0:
        raise ValueError('Provide a list of at least one voxel for plotting.')
    startTime =0
    if info:
        startTime = _default_timer()
    if path is None:
        _plt.ioff()
    fig = _plt.figure()
    ax = _Axes3D(fig)
    # voxels to cube
    polyface = None
    polycolor = []
    colorValues = {}
    if colorDict is not None:
        colorValues = colorDict
    for voxel in voxels:
        if polyface is None:
            polyface = _np.array(cubeFaces(voxel,size))
        else:
            polyface = _np.append(polyface,cubeFaces(voxel,size),axis=0)
        material = str(tuple(voxel)[3:])
        # if the material is not yet assigned to a color
        if material not in colorValues:
            mat = hash(material)
            r = round(mat%256/255,3) # round for nicer output
            g = round((mat>>8)%256/255,3)
            b = round((mat>>16)%256/255,3)
            colorValues[material] = [r,g,b]
        # query the color and add it to values list
        polycolor.append(colorValues[material])
    # duplicate colour values 6 times as there are 6 faces per cube
    polycolor = _np.repeat(polycolor,6,axis=0)
    col = _Poly3DColletion(polyface,facecolor=polycolor)
    ax.add_collection3d(col)
    # set axes range - do some math to center object but keep axis range equal
    xmin,ymin,zmin = _np.min(voxels['x'])-0.5*size[0], _np.min(voxels['y'])-0.5*size[1], min(_np.min(voxels['z'])-size[2],0)
    xmax,ymax,zmax = _np.max(voxels['x'])+0.5*size[0], _np.max(voxels['y'])+0.5*size[1], _np.max(voxels['z'])
    xr,yr,zr = xmax-xmin,ymax-ymin,zmax-zmin
    maxr = max(xr,yr,zr) # calculate maximum range of object
    xcenter,ycenter,zcenter = xmin+xr/2,ymin+yr/2,zmin+zr/2
    ax.set_xlim([xcenter-maxr/2,xcenter+maxr/2])
    ax.set_ylim([ycenter-maxr/2,ycenter+maxr/2])
    ax.set_zlim([zmin,zmin+maxr])
    #cosmetics
    if border:
        col.set_edgecolor('k')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    if info:
        print('Voxels printed: %d. Faces printed: %d. Lines drawn: %d.\n' %(len(voxels),len(polyface),12*len(voxels)))
        print('xmax=%s, xmin=%s, ymax=%s, ymin=%s, zmax=%s, zmin=%s'%(xmax,xmin,ymax,ymin,zmax,zmin))
        print('maxRange=%s, xRange=%s, yRange=%s, zRange=%s'%(maxr,xr,yr,zr))
        print('xCenter=%s, yCenter=%s, zCenter=%s\n'%(xcenter,ycenter,zcenter))
        print('colorValues used for this plot:\n%s '%str(colorValues))
    print(path)
    if path is None:
        _plt.show()
    else:
        _plt.savefig(path)
        _plt.cla()
        _plt.close(fig)
    if info:
        print('Plotting used %f seconds.'% (_default_timer()-startTime))

def _update_fig(frame):
    raise NotImplementedError('Planed to be implemented with _animateObject')
    print(frame)

def _animateObject(voxels,size,border=True,info=False,speed='10s'):
    ''' Plot voxels animated, the animation speed can be provided in the format
    '1v/s' voxels per second or absolute time '5s' for the entire object.'''
    raise NotImplementedError()
    global ani # make animation global to keep from dying
    ani = _FuncAnimation(fig,update_fig,frames=_np.arange(0,len(voxels)))
    _plt.show()


# TODO make class and let inherit nupy array
#class voxelTable():
#
#  __new__(cls,input_array,self,x=None,y=None,z=None,m=None):
#        assert len(x) == len(y) == len(z) == len(m),'Provide correct input for your voxel object. X y and m do not have the same lenght. '
#       return Object
#        super().__init__({'x':x,'y':y,'z':z})
#   def __array_finalize__(self,obj):
#       pass
