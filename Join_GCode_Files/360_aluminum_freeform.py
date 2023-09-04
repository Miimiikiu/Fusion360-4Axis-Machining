"""

Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.

"""
import os
import ast

def offset_x_y_z(x_offset, y_offset, z_offset, z_toolchange_adjustment, z_raise_bottom, line, rot, max_x, min_x, max_y, min_y, max_z, min_z):
    #print(line)
    commands = line.split(' ')
    for i, command in enumerate(commands):
        if 'Y' in command:
            y_coord = float(command[1:])
            if rot == 0:
                y_coord += y_offset
            elif rot == 180:
                y_coord -= y_offset
                if y_coord >= max_y or y_coord <= min_y:
                    raise RuntimeError('ERROR: max_y:{} min_y:{} requested_y:{}'.format(max_y, min_y, y_coord))
            else:
                raise RuntimeError('ERROR: Invalid rotation')

            command = 'Y' + str(round(y_coord, 3))
        
        elif 'Z' in command:
            z_coord = float(command[1:])
            z_coord += z_toolchange_adjustment# + z_offset  #maybe F360 already accounts for this...
            if rot == 0:
                z_coord -= z_offset
            if rot == 180:
                z_coord += z_raise_bottom 
                z_coord += z_offset
            if z_coord >= max_z or z_coord <= min_z:
                raise RuntimeError('ERROR: max_z:{} min_z:{} requested_z:{}'.format(max_z, min_z, z_coord))
            command = 'Z' + str(round(z_coord, 3))
            
        elif 'X' in command:
            x_coord = float(command[1:])
            x_coord += x_offset
            if x_coord >= max_x or x_coord <= min_x:
                raise RuntimeError('ERROR: max_x:{} min_x:{} requested_x:{}'.format(max_x, min_x, x_coord))
            command = 'X' + str(round(x_coord, 3))
        
        commands[i] = command + ' '
    line = ''.join(commands) + '\n'
    return(line)
            
class Job():
    def __init__(self):
        self.folder = None
        self.filenames = None
        self.rotations = None
        self.end_mills_in_use = None
        self.y_offset = None
        self.z_offset = None





read_dat = False
#first_tool = 1.5
#hole_tool = 1.5 #if no hole then ignore
tool_change = True #True to include tool changes into main file; False for separate files
'''
if read_dat == True:    
    with open('E:\\NC Files\\{}\\{}.dat'.format(job0.folder_name, job0.output_name), 'r') as datfile:
        for i, line in enumerate(datfile.readlines()):
            if i == 0:
                job0.filenames = ast.literal_eval(line.split('=')[1])
            elif i == 1:
                job0.rotations = ast.literal_eval(line.split('=')[1])
            elif i == 2:
                job0.y_offset = ast.literal_eval(line.split('=')[1])
    #print(filenames, type(filenames))
    #print(filenames[0], type(filenames[0]))
    #print(rotations, type(rotations))
    #print(rotations[0], type(rotations[0]))
    #print(y_offset, type(y_offset))
'''
job0 = Job()
job1 = Job()
jobs = [job0]
if read_dat == True:
    pass
else:
    job0.folder = 'Prox Back'
    job0.filenames = ['Prox Back Top Holes', 'Prox back bottom contours', 'Prox back top', 'Prox back bottom']
    job0.rotations = [0, 180, 0, 180] 
    job0.end_mills_in_use = ['1F1.5', '1F1.5', '1F3.0', '1F3.0']
    job0.x_offset = 0 # When cutting 3 or more pieces
    job0.y_offset = -10  #negative is piece toward user, positive is away (when rotation = 0)
    job0.z_offset = 0.5 #For when we shifted it up or down in F360 -- refer to z_offset from Center_Object.py
    job0.i = 0
    #TODO: Add x_offset for more than 2 jobs
    '''
    job1.folder = 'Dist Back'
    job1.filenames = ['Dist Back Top Holes Contour', 'Dist Back Bottom Holes', 'Dist Back Top', 'Dist Back Bottom'] 
    job1.rotations = [0, 180, 0, 180] 
    job1.end_mills_in_use = ['1F1.5', '1F1.5', '1F3.0', '1F3.0']
    job1.x_offset = 0
    job1.y_offset = -13  #negative is tray toward user, positive is away (when rotation = 0)
    job1.z_offset = 1.0
    job1.i = 0
    '''

min_x = -75
max_x = 75    
max_y = 50
min_y = -25
max_z = 10
min_z = -4
first_tool = job0.end_mills_in_use[0]
end_mills = {'1F1.5':0.000, '1F3.0':3.603, 'ThreadGen':8.476} # error +- .05
z_raise_bottom = -.1 #raise the height of the stock when rot = 180 (cont...)
# updated 1/18/2022, likely from sanding down support beam (cont...)
# Furthermore, this value is constant regardless of x position
delete_files = False
calibration_mode = False
rot = job0.rotations[0]
k = {}
override = True
#reset_j = False
#TODO: Copy the first file to include the new y values
if len(jobs) > 1:
    output_folder = 'Prox Back' # only need if you have multiple jobs running
    output_name = '{}_{}'.format(output_folder, first_tool)
else:
    output_folder = job0.folder
    output_name = '{}_{}'.format(job0.folder, first_tool)

path = 'E:\\NC Files\\{}\\output'.format(output_folder)
if not os.path.exists(path):
    print('Path not found. Creating directory.')
    os.makedirs(path)

with open('E:\\NC Files\\{}\\output\\{}.nc'.format(output_folder, output_name), 'w') as outfile: # all in one big file
    j = 0
    while j < len(jobs):
        #print('new job:{}'.format(j))
        job = jobs[j]
        i = job.i

        while i < len(job.filenames):
            f = job.filenames[i]
            print('{}, {}, {}...'.format(f, job.end_mills_in_use[i], rot))
            z_toolchange_adjustment = end_mills[job.end_mills_in_use[i]] - end_mills['1F1.5'] # ALWAYS use 1F1.5 as a starting point
            with open('E:\\NC Files\\{}\\{}.nc'.format(job.folder, f), 'r') as infile:
                for line in infile.readlines():
                    if 'M30' not in line and 'G91' not in line:
                        if f == job.filenames[0] or 'G54' not in line: #only enters WCS for first file
                            if 'Y' in line or 'Z' in line or 'X' in line:
                                if line[0] != '(':
                                    line = offset_x_y_z(job.x_offset, job.y_offset, job.z_offset, z_toolchange_adjustment, z_raise_bottom, line, rot, max_x, min_x, max_y, min_y, max_z, min_z)
                            outfile.write(line)
                rot = job.rotations[(i+1) % len(job.rotations)] #TODO: Should be for the next job.
                outfile.write('\nG0 Z{}\nG0 X-10\nG0 Y59\nG0 A{}\n'.format(5 + z_toolchange_adjustment, rot))
                if i < len(job.end_mills_in_use) - 1: # Prevents "index out of range" error
                    #next_job = jobs[(j + 1) % len(jobs)]
                    if job.end_mills_in_use[i] != job.end_mills_in_use[i+1] and tool_change == True: # Check if the next end mill is the same as this one. #TODO: i+1 Should be i+1 for next job. Not out of the woods yet.
                        # decide whether to change tools or move to next job. Remember current i value and we'll continue with this later.
                        if j == len(jobs)-1:
                            print('tool change')
                            prompt = '(Previous End Mill: {} New End Mill: {})'.format(job.end_mills_in_use[i], job.end_mills_in_use[i+1])
                            z_toolchange_adjustment_temp = end_mills[job0.end_mills_in_use[i+1]] - end_mills['1F1.5']
                            outfile.write('\n G0 Z{}\n {}\n M00\n'.format(5 + z_toolchange_adjustment_temp, prompt)) #pause for tool change, raise height for safe travel
                            j = -1 #j+1 later
                            job.i = i + 1
                            break
                        else:
                            print('next job')
                            j += 0 # j+1 later
                            job.i = i + 1
                            break
                    #elif job.end_mills_in_use[i] != next_job.end_mills_in_use[next_job.i]:
                        #pass
                        
                i += 1
        j += 1
        
    outfile.write('\nM30') # end program

print('done')
                

#if delete_files:
#    print('removing originals')
#    for f in filenames:
#        os.remove('E:\\NC Files\\{}\\{}.nc'.format(folder_name, f))
