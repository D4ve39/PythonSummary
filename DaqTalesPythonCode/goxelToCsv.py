#!/usr/bin/python3
import numpy as np
import csv
import sys
import re
from modifyCSV import writeCSV
from modifyCSV import plotObject


def colored(string,color):
    '''
    returns an ansi escaped text collored with the color tuple: color=(r,g,b)
    Note that the terminal must support 24bit ANSI escape sequences.
    see: <https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit>
    The forgrownd is reversed for easier reading.
    '''
    return '\33[48;2;{};{};{}m{}\33[0m'.format(color[0],color[1],color[2],string)

def hexToRgb(hexString):
    r = int(hexString[0:2],base=16)
    g = int(hexString[2:4],base=16)
    b = int(hexString[4:6],base=16)
    return (r,g,b)

def promptMaterial(hexString):
    '''
    Promts the user to provide the material corresponding to a function.
    '''
    prompt = "for color "+colored('0x'+hexString,hexToRgb(hexString))+" provide "
    values = ["Pset","Vdepo","p1","p2","p3","p4"]
    material = []
    for i in values:
        while True:
            try:
                mat = float(input(prompt+i+" :  "))
                material.append(mat)
                break
            except(ValueError):
                print("Please enter a float.")
    return material

def fromGoxel(fname):
    '''
    Converts the .txt output format of open source voxel editor Goxel into a
    .csv - colors are mapped to materials with the help of the user
    '''
    material = {} # dictionary to convert color to material (Vdepo,Pset,p1,p2,p3,p4)
    voxels = []

    csvfile = open(fname)
    r = csv.reader(csvfile,delimiter=' ')
    for row in r:
        # First read all the values
        if(row[0] == '#'):
            continue # break as this is a comment
        x,y,z = float(row[0]), float(row[1]), float(row[2])
        if len(row[3])==6:
            color = row[3]
        else:
            #hex value can contain whitespace (seems to be a bug in goxel)
            color=''
            for i in row[3:]:
                color+=i
                if len(color) != 6:
                    color+='0'
                    # zero Pad hex values smaller than 0x10
                    # so make 0x75 f3f equal to 0x750f3f
                    # if confused open some dark colored txt files
        assert len(color) == 6, "Could not read hex value from input file."

        # Second check for color and if not in dictionary prompt user
        if color not in material:
            material[color] = promptMaterial(color)
        Vdepo,Pset,p1,p2,p3,p4 = material[color]
        voxels.append([x,y,z,Vdepo,Pset,p1,p2,p3,p4])
    return voxels

def scaleVoxels(voxels,size):
    '''
    scales all voxel in voxels with a factor size = (sizeX,sizeY,sizeZ)
    '''
    for voxel in voxels:
        for i in (0,1,2):
            voxel[i]*=size[i]

# handle user commandline input
if len(sys.argv) == 2:
    print("Not provided default voxel size: assuming (0.25,0.25,0.25)")
    size = (0.25,0.25,0.25)
elif len(sys.argv) == 5:
    size = (float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]))
else:
    print("Ussage: "+sys.argv[0]+" filename xSize ySize zSize")
    sys.exit(1) # exit with error state

# process voxels
filename = sys.argv[1]
voxels = fromGoxel(filename)
scaleVoxels(voxels,size) #goxel returns all voxels in integer size
csvname = re.sub(r'.txt$','.csv',filename)
writeCSV(csvname,voxels)
plotObject(np.array(voxels),"/tmp/test.txt",interactive=True)
