# Fusion 360 4Axis Machining

Basic 4Axis tools that don't require a paid subscription

## Description

This collection is intended to take a CAD model, split it into 4 parts (front, back, left, right), and machine one part then rotate to the next. While it's not as smooth as the Fusion360 paid subscription 4Axis tools, this is a great start for anyone with a lower budget and a rotary axis.

Center_Object easily splits a body into multiple bodies and centers them near the origin to prepare for machining. It then flips the bottom part upside-down.

If holes are present, use the PrepareHoles script to extend the holes to the top of the stock. Then use PrepareHolesBottom to extend them to the bottom of the stock.

Then both the top and the bottom can be prepared as usual using the manufacturing tab.

360_degree_gcode.py combines multiple G Code files (one for each part the model was split into) into one, rotating between each side. combine_flat_gcode.py does the same but without rotation. 360_aluminum_freeform.py is for rotating stock that isn't even, such as an extruded metal bar, but is a little more specific to my particular use case.



## Usage

On Windows, these 3 folders should be placed under [Username] > AppData > Roaming > Autodesk > Autodesk Fusion 360 > API > Scripts. You can place the Join_GCode_Files folder wherever you'd like, since it won't be used in Fusion 360.

After using these scripts, users with 3Axis machines will have to physically flip the part manually. Users with a 4th axis can use 360_degree_gcode.py or 360_aluminum_freeform.py outside of Fusion 360 to consolidate the post-processed files into a single file that automatically rotates after each side is finished. 360_aluminum_freeform.py also accounts for horizontal offsets for maximizing stock space and vertical offsets for stock that isn't properly centered (such as flat aluminum extrusions), but was intended strictly for my own purposes on my previous (much smaller) specific setup so I'll work on generalizing this in the future.

This package splits and utilizes the model as 4 sides: Anterior (front), Posterior (back), Sinister (left), Dexter (right). (This terminology is unambiguous with respect to reference point, so I use these names across various projects.)

#### Before using, please look through the code carefully to confirm that nothing will be damaged using your setup, especially when using anything under Join_GCode_Files. Some files in this repo are intended to modify G Code files generated by Fusion 360, so any collision checking performed in Fusion 360 may be inaccurate. This was tested on a 3018 CNC router using a 4-chuck 4th axis. I am not responsible for any damage, injury, or loss of data, etc when using this repository. Know what you're doing and use it at your own risk.


