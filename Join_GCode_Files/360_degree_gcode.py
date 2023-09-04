"""
Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.
"""

#Combines multiple G Code files into a single output file that rotates the
#rotary axis between input files. This was intended to use the Center_Object
#Fusion360 plugin included in this package to split the model into 4 sides:
#Anterior (front), Posterior (back), Sinister (left), Dexter (right)
#(This terminology is unambiguous with respect to reference point, so I
#use these names across various projects.)

#This script assumes that Z0 and Y0 are calibrated at the
#center of the rotation of the A axis, and X0 is at the
#far left edge of the stock. Additionally, we assume
#that the WCS is set X0 Y0 Z0 and that Z only cuts
#the top half of the stock for each rotation.

#TODO: Support multiple tools
#TODO: Remove file name conventions

name = 'Mew_chess_piece'
tool = '2f_3.175'
rot = 0 # starting rotation

full_rotation_distance = 16 # distance on DRO for your 4th axis to make one full rotation
calibration_mode = False
sides = ['Anterior', 'Posterior'] if calibration_mode == True else ['Anterior', 'Posterior', 'Sinister', 'Dexter']
with open('E:\\NC Files\\{}_{}.nc'.format(name, tool), 'w') as outfile:
    for side in sides:
        print('{}...'.format(side))
        with open('E:\\NC Files\\{}_{}_{}.nc'.format(name, side, tool), 'r') as infile:
            for line in infile.readlines():
                if 'M30' not in line and 'M2' not in line:
                    
                    if side == 'Anterior' or 'G54' not in line: #Only G54 for first file
                        outfile.write(line)
            #rot += 90
            #rot = 0 if rot == 360 else rot
                
            #if rot < 360:
            if side == 'Anterior':
                rot = full_rotation_distance/2 # to Posterior
            elif side == 'Posterior':
                rot = full_rotation_distance/4 # to Sinister
            elif side == 'Sinister':
                rot = 3 * full_rotation_distance/4 # to Dexter
            elif side == 'Dexter':
                rot = 0 # back to Anterior
            outfile.write('\nG0 Z24\nG0 X-10\nG0 Y0\nG0 A{}\n'.format(rot))
    outfile.write('\nM30')
print('done')