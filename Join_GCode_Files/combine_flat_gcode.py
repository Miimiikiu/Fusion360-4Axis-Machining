#Combines multiple G Code files that don't require rotation

#TODO: Remove file name conventions

import os
name = 'Connection1_1Flute'
folder_name = 'Connection1'
tools = ['2f_6.35mm', '2f_6.35mm', '2f_3.175mm']
number_of_operations = 2
operations = [x+1 for x in range(number_of_operations)]
with open('E:\\NC Files\\{}\\{}_{}_combined.nc'.format(folder_name, name, tools), 'w') as outfile:
    for i, op in enumerate(operations):
        print('{}...'.format(op))
        infile_path = 'E:\\NC Files\\{}\\{}_{}_{}.nc'.format(folder_name, name, op, tools[i])
        with open(infile_path, 'r') as infile:
            for line in infile.readlines():
                if 'M30' not in line and 'M2' not in line: # do not end the program unless we say so

                    if op == operations[-1] or 'G54' not in line: # line is valid for the entire last operation (sans M30). Why not 1st?
                        outfile.write(line)
                else: # end of current operation
                    if i < len(tools) - 1: # not on final operation
                        if tools[i+1] != tools[i]:
                            outfile.write('M0') # manual tool change -- resume when ready
                            
        
    outfile.write('\nM30')
print('done')