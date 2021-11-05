import numpy as _np
from pathlib import Path
import webbrowser
import os
import voxelTable
import patterns

#format Header to understand the output of the voxel file
headerString = '#      x,       y,       z, Vdepo, p1, p2, p3, p4\n'
# This message array is used to print errors from.
_messages = _np.array(["X is out of bound. ",
                 "Y is out of bound. ",
                 "Z is out of bound. ",
                 "Deposition Voltage is out of bound. ",
                 "Pressure p1 is out of bound. ",
                 "Pressure p2 is out of bound. ",
                 "Pressure p3 is out of bound. ",
                 "Pressure p4 is out of bound. "])

formater='%8.3f,%8.3f,%8.3f,%1.3f,%3.0f,%3.0f,%3.0f,%3.0f\n'
#formater % tuple(self)


def addPillar(voxels, pillarPosition, useFirst, pillarCharacteristics):
    if (useFirst):
        first = list(voxels[0])[3:]
        print(first)
    else:
        first = list(pillarCharacteristics)

    pillarNeeded = 0
    z = voxels['z']
    pillarIndex = []
    ### Find how many pillar voxels should be added:
    for i in range(1, len(z)):
        if (z[i - 1] < z[i]):
            pillarNeeded += 1
            pillarIndex.append(i)

    splited = _np.split(voxels, pillarIndex)
    new_voxels = _np.empty((0), dtype=voxelTable.dt)

    for arr in splited:
        pillarPos = [pillarPosition[0], pillarPosition[1], arr[-1]['z']]
        v = tuple(pillarPos + first)
        pillarVoxel = _np.array(v,ndmin = 1,dtype=voxelTable.dt)
        new_voxels = _np.concatenate((new_voxels, arr, pillarVoxel))
    return new_voxels


def convertToLabView(voxels):
    '''Converts a 2D numpy array into the typedef defined by voxel array in LabView.'''
    voxelArray = []
    for voxel in voxels:
        voxel = list(voxel)
        position, pressure = list(voxel[:4]), tuple(voxel[4:])
        position.append(pressure)
        voxelArray.append(tuple(position))
    return voxelArray

def convertFromLabview(voxelLabV):
    voxelarray = []
    for voxel in voxelLabV:
        v = list(voxel[:4])
        p = list(voxel[4])
        voxelarray.append(v+p)
    return _np.array(voxelarray)

def OldPatternCsvSave(voxelLabV, path):
    voxelTable.save(convertFromLabview(voxelLabV),path)

def checkBoundaries(voxels, boundaries):
    '''Check if the given voxels have values within the given boundaries'''
    errors = []
    status = True
    line = 0
    for vox in voxels:
        if not(boundaries[0] <= vox['x'] <= boundaries[1]):
            errors.append("At line " + str(line) + ":  " + _messages[0])
            status = status and False

        if not(boundaries[2] <= vox['y'] <= boundaries[3]):
            errors.append("At line " + str(line) + ":  " + _messages[1])
            status = status and False

        if not(boundaries[4] <= vox['z'] <= boundaries[5]):
            errors.append("At line " + str(line) + ":  " + _messages[2])
            status = status and False

        if not(boundaries[6] <= vox['Vdepo'] <= boundaries[7]):
            errors.append("At line " + str(line) + ":  " + _messages[3])
            status = status and False

        if not(boundaries[8] <= vox['p1'] <= boundaries[9]):
            errors.append("At line " + str(line) + ":  " + _messages[4])
            status = status and False

        if not(boundaries[8] <= vox['p2'] <= boundaries[9]):
            errors.append("At line " + str(line) + ":  " + _messages[5])
            status = status and False

        if not(boundaries[8] <= vox['p3'] <= boundaries[9]):
            errors.append("At line " + str(line) + ":  " + _messages[6])
            status = status and False

        if not(boundaries[8] <= vox['p4'] <= boundaries[9]):
            errors.append("At line " + str(line) + ":  " + _messages[7])
            status = status and False
        line += 1
    return (status, errors)

#testit: main()
def main(filename, boundaries, pillarPosition, useFirst, pillarCharacteristics, resultDir, doAddPillar=True, doPillarScan=True):
    assert (useFirst or len(pillarCharacteristics) == 5), 'Specified to not use \
    the Material from the first voxel for the pillar but no pillar material specified.'

    # copy the input file into the result Directory for later reference
    # shutil.copy(filename,os.path.join(resultDir,os.path.split(filename)[1]))
    voxels = voxelTable.load(filename)

    # do not move the whole struture to (xmin,ymin) if a pillar is already included in the csv
    if not(doAddPillar != doPillarScan):
        voxelTable.moveBeyond(voxels,x=boundaries[0], y=boundaries[2])

    (status, errors) = checkBoundaries(voxels, boundaries)

    if status is False:
        # do some html formating of the errors and open an error log in the
        # webbrowser
        name = os.path.join(resultDir,"errors.html")
        header = '<!DOCTYPE html>\n<html>\n<head><title>Errors in %s \
                 </title></head>\n<body>\n'
        footer = '</body>\n</html>'
        html = open(name, "w")
        html.write(header%filename)
        html.write('<ul>\n')
        for line in errors:
            html.write("<li>%s</li>"%line)
        html.write('</ul>\n')
        html.write(footer)
        html.close()
        webbrowser.open(Path(name).as_uri())
        return (convertToLabView([]), status)
    else:
        #Save a plot of the arrays to the desired path
        size = [1,1,0.25]
        voxelTable.plotObject(voxels,size,True, False, None, os.path.join(resultDir,"voxelplot.png"))
        if doAddPillar:
            voxels = addPillar(voxels,pillarPosition,useFirst,pillarCharacteristics)
        #voxel array gets saved in csv as actuallyPrinted.csv
        voxelTable.save(voxels,os.path.join(resultDir,"actuallyPrinted.csv"))
        return (convertToLabView(voxels), status)

if __name__ == '__main__':
    filename = 'C:/Users/david/polybox/multimat/newcode/python/dummy.csv'
    boundaries = (0,100,0,100,0,100,-2,2,-30,30)
    pillarPosition = (5,5)
    pillarCharacteristics = (0,0,0,0,0,0)
    resultdir = 'C:/Users/david/polybox/multimat/newcode/python'
    main(filename, boundaries, pillarPosition, True, pillarCharacteristics, resultdir, True, True)
