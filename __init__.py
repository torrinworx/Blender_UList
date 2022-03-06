bl_info = {
    "name": "Blender_UIList",
    "author": "Torrin Leonard",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Example of UIList with Property functionality.",
    "category": "Development",
}

# Import handling:

import bpy
from bpy.app.handlers import persistent

import os
import importlib

# Import files from main directory:

if bpy in locals():
        importlib.reload(UIList)
else:
    from . import UIList

# User input Property Group:
class BMNFTS_PGT_MyProperties(bpy.types.PropertyGroup):

    # Rules for Logic:
    logicBool: bpy.props.BoolProperty(name="Logic")
    item1: bpy.props.StringProperty(name="item1")
    ruleEnum: bpy.props.EnumProperty(
        name="",
        description="Select DNA Rule",
        items=[
            ('Only with', "Only with", "Only with Rule"),
            ('Never with', "Never with", "Never with Rule")
        ]
    )
    item2: bpy.props.StringProperty(name="item2")


# Register and Unregister classes from Blender:
classes = (
    UIList.CUSTOM_OT_actions,
    UIList.CUSTOM_OT_clearList,
    UIList.CUSTOM_OT_printItems,
    UIList.CUSTOM_UL_items,
    UIList.CUSTOM_PT_objectList,
    UIList.CUSTOM_PG_objectCollection,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=BMNFTS_PGT_MyProperties)

    # UIList:
    bpy.types.Scene.custom = bpy.props.CollectionProperty(type=UIList.CUSTOM_PG_objectCollection)
    bpy.types.Scene.custom_index = bpy.props.IntProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool

    # UIList:
    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index


if __name__ == '__main__':
    register()
