import bpy

def moveUVs(context,datasource,move_UV_by, obj):
    for uv_layer in obj.data.uv_layers:
        for loop in obj.data.loops:
            uv_layer.data[loop.index].uv[1] += move_UV_by

def weighted_norm(context,obj):
    obj.data.use_auto_smooth = True
    weighted_normal = obj.modifiers.new(name="Weighted Normal", type='WEIGHTED_NORMAL')
    weighted_normal.mode = 'FACE_AREA_WITH_ANGLE'

def mergebydistance(context,obj):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.object.mode_set(mode='OBJECT')
