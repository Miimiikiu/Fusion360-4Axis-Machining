"""
Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.
"""

#Description - Prepares Component for 2-sided 4-Axis CAM

import adsk.core, adsk.fusion, adsk.cam, traceback
import time
import math

# Units are in cm

def center_object(ui, rootComp, occ):
    matrix3D = adsk.core.Matrix3D
    
    #center occurrence
    
    #med = rootComp.occurrences.item(0)
    adjust_z = True
    transform = occ.transform
    transform.translation = adsk.core.Vector3D.create(0, 0, 0)
    occ.transform = transform
    #default_height = .18
    if adjust_z:
        z_offset, cancelled = ui.inputBox('Enter Z offset (default {})'.format(0), 'Z offset (mm)')
        if cancelled:
            exit()
        z_offset = float(z_offset)/10.0
    else:
        #z_offset = default_height
        pass
    #center body
    bodies = adsk.core.ObjectCollection.create()
    body = occ.bRepBodies.item(0)
    body = ui.selectEntity('Body to center', 'SolidBodies').entity
    bodies.add(body)
    body_xmax = body.boundingBox.maxPoint.x.real
    body_ymin = body.boundingBox.minPoint.y.real
    body_ymax = body.boundingBox.maxPoint.y.real
    body_zmin = body.boundingBox.minPoint.z.real
    body_zmax = body.boundingBox.maxPoint.z.real
    translation_x = -body_xmax
    translation_y = -body_ymax + abs(body_ymin - body_ymax)/2 + z_offset
    translation_z = -body_zmax + abs(body_zmin - body_zmax)/2
    vector = adsk.core.Vector3D.create(translation_x, translation_y, translation_z)
    
    transform = matrix3D.create()
    transform.translation = vector
    move = rootComp.features.moveFeatures
    try:
        move_input = move.createInput(bodies, transform)
        move.add(move_input)
    except:
        pass
    
    if (body_zmax - body_zmin) > (body_ymax - body_ymin):
        #ui.messageBox('Vertical')
        transform = matrix3D.create()
        rotX = adsk.core.Matrix3D.create()
        rotX.setToRotation(-math.pi/2, adsk.core.Vector3D.create(1,0,0), adsk.core.Point3D.create(0,0,0))
        transform.transformBy(rotX)
        move_input = move.createInput(bodies, transform)
        move.add(move_input)
    else:
        pass
    '''
    if z_offset != default_height and adjust_z:
        transform = occ.transform
        transform.translation = adsk.core.Vector3D.create(0, 0, 0)
        occ.transform = transform
        bodies = adsk.core.ObjectCollection.create()
        body = occ.bRepBodies.item(0)
        bodies.add(body)
        translation_z = z_offset - default_height
        vector = adsk.core.Vector3D.create(0, 0, translation_z)
        transform = matrix3D.create()
        transform.translation = vector
        move = rootComp.features.moveFeatures
        try:
            move_input = move.createInput(bodies, transform)
            move.add(move_input)
        except:
            pass
    '''
        
def split(ui, rootComp):

    body_to_split = ui.selectEntity('Body to split', 'SolidBodies').entity
    splittingTool = ui.selectEntity('Splitting Tool', 'ConstructionPlanes, PlanarFaces').entity
    split_Input = rootComp.features.splitBodyFeatures.createInput(body_to_split, splittingTool, True)
    rootComp.features.splitBodyFeatures.add(split_Input)

def rotate_bottom(ui, rootComp, occ):
    #med = rootComp.occurrences.item(0)
    #doesn't account for island bodies
    bottom = occ.bRepBodies.item(0)
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(bottom)
    matrix3D = adsk.core.Matrix3D
    transform = matrix3D.create()
    rotX = adsk.core.Matrix3D.create()
    rotX.setToRotation(math.pi, adsk.core.Vector3D.create(1,0,0), adsk.core.Point3D.create(0,0,0))
    transform.transformBy(rotX)
    move = rootComp.features.moveFeatures
    move_input = move.createInput(bodies, transform)
    move.add(move_input)
'''
def prepare_holes(ui, rootComp):
    app = adsk.core.Application.get()
    ui  = app.userInterface
    des = adsk.fusion.Design.cast(app.activeProduct)
    rootComp = des.rootComponent
    edges = adsk.core.ObjectCollection.create()
    amount, cancelled = ui.inputBox('Enter Number of Circular Edges', 'Circular Edges')
    if cancelled:
        return
    
    for x in range(int(amount)):
        edges.add(ui.selectEntity('Edges to Offset', 'CircularEdges').entity)
        
    
    offset = rootComp.features.offsetFeatures
    offset_input = offset.createInput(edges, 0, adsk.fusion.FeatureOperations.NewBodyFeatureOperation, True)
    offset.add(offset_input)
'''

def copypaste(ui, rootComp, occ):
    app = adsk.core.Application.get()
    ui  = app.userInterface
    des = adsk.fusion.Design.cast(app.activeProduct)
    rootComp = des.rootComponent
    #dummy1 = rootComp.occurrences.item(0).component
    #dummy2 = rootComp.occurrences.item(1).bRepBodies
    #dummy2.bRepBodies.item()
    #occ = ui.selectEntity('Component to Center', 'Occurrences').entity
    copypastecomp = occ.component.features.copyPasteBodies.add(occ.bRepBodies.item(0))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = des.rootComponent
        occ = ui.selectEntity('Component to Center', 'Occurrences').entity

        dummy = rootComp.occurrences.item(0)

        center_object(ui, rootComp, occ) #Should be a component
        split(ui, rootComp) #No prompt, just select
        rotate_bottom(ui, rootComp, occ)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
