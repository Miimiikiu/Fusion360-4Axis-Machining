"""
Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.
"""


import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    stock_height = .18
    try:
        real = adsk.core.ValueInput.createByReal
        app = adsk.core.Application.get()
        ui  = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = des.rootComponent
        faces = adsk.core.ObjectCollection.create()
        amount, cancelled = ui.inputBox('Enter Number of Cylindrical Faces', 'Cylindrical Faces')
        z_offset, cancelled = ui.inputBox('Enter Z offset (default {})'.format(0), 'Z offset (mm)')
        z_offset = float(z_offset) / 10.0
        #dummy = rootComp.bRepBodies.item(0).faces.item(0).edges.item(0)
        if cancelled:
            ui.messageBox('Cancelled:\n{}'.format(traceback.format_exc()))
            return
        
        for x in range(int(amount)):
            faces.add(ui.selectEntity('Faces to Offset', 'CylindricalFaces').entity)
            
        
        offset = rootComp.features.offsetFeatures
        offset_input = offset.createInput(faces, real(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation, True)
        offset.add(offset_input)
        faces.item(0).body.parentComponent.isBodiesFolderLightBulbOn = False
        bodies = adsk.core.ObjectCollection.create()
        for x in range(int(amount)):
            bodies.add(ui.selectEntity('Surface Bodies', 'SurfaceBodies').entity)
            
        extend = rootComp.features.extendFeatures
        for x in range(int(amount)):
            edges = adsk.core.ObjectCollection.create()
            
            edges.add(ui.selectEntity('Edges to Extend', 'CircularEdges').entity)

            distance_up = stock_height - edges.item(0).boundingBox.maxPoint.z + z_offset
            extend_input = extend.createInput(edges, real(distance_up), adsk.fusion.SurfaceExtendTypes.NaturalSurfaceExtendType, True)
            extend.add(extend_input)
        for x in range(int(amount)):
            edges = adsk.core.ObjectCollection.create()
            
            edges.add(ui.selectEntity('Edges to Extend', 'CircularEdges').entity)
            min_point = edges.item(0).boundingBox.minPoint.z
            distance_down = stock_height + min_point + .01 - z_offset #ensure a clean breakthrough
            extend_input = extend.createInput(edges, real(distance_down), adsk.fusion.SurfaceExtendTypes.NaturalSurfaceExtendType, True)
            extend.add(extend_input)
        
        faces.item(0).body.parentComponent.isBodiesFolderLightBulbOn = True
            
        
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
