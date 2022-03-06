bl_info = {
    "name": "Blender_UIList",
    "author": "Torrin Leonard",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Example of UIList with Property functionality.",
    "category": "Development",
}

import bpy
from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

# User input Property Group:
class rules_PGT(PropertyGroup):

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

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class CUSTOM_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "rule_list.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.rule_list_index

        try:
            item = scn.rule_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.rule_list) - 1:
                item_next = scn.rule_list[idx + 1].name
                scn.rule_list.move(idx, idx + 1)
                scn.rule_list_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.rule_list_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.rule_list[idx - 1].name
                scn.rule_list.move(idx, idx - 1)
                scn.rule_list_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.rule_list_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.rule_list[idx].name)
                scn.rule_list_index -= 1
                scn.rule_list.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            item = scn.rule_list.add()
            item.name = f"Rule {idx +1}"

            scn.rule_list_index = len(scn.rule_list) - 1
            info = '"%s" added to list' % (item.name)
            self.report({'INFO'}, info)

        return {"FINISHED"}

class CUSTOM_OT_printItems(Operator):
    """Print all items and their properties to the console"""
    bl_idname = "rule_list.print_items"
    bl_label = "Print Items to Console"
    bl_description = "Print all items and their properties to the console"
    bl_options = {'REGISTER', 'UNDO'}

    reverse_order: BoolProperty(
        default=False,
        name="Reverse Order")

    @classmethod
    def poll(cls, context):
        return bool(context.scene.rule_list)

    def execute(self, context):
        scn = context.scene
        if self.reverse_order:
            for i in range(scn.rule_list_index, -1, -1):
                ob = scn.rule_list[i].obj
                print("Object:", ob, "-", ob.name, ob.type)
        else:
            for item in scn.rule_list:
                ob = item.obj
                print("Object:", ob, "-", ob.name, ob.type)
        return {'FINISHED'}

class CUSTOM_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "rule_list.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.rule_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.rule_list):
            context.scene.rule_list.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return {'FINISHED'}

# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------

class RULES_UIList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = context.scene
        mytool = scene.my_tool

        split = layout.split(factor=0.3)
        split.label(text=f'{index}')

        split.prop(mytool, "item1")
        # split.prop(item, data, "item1", text="", emboss=False, translate=False, )


    def invoke(self, context, event):
        pass

class CUSTOM_PT_objectList(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    bl_label = "UIList Test"
    bl_idname = "uilisttest_PT_uilisttest"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blender_UIList'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "logicBool")

        rows = 2
        row = layout.row()
        row.template_list("RULES_UIList", "The_List", scene, "rule_list", scene, "rule_list_index", rows=rows)

        col = row.column(align=True)
        col.operator("rule_list.list_action", icon='ADD', text="").action = 'ADD'
        col.operator("rule_list.list_action", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("rule_list.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("rule_list.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("rule_list.print_items", icon="LINENUMBERS_ON")
        row = col.row(align=True)
        row.operator("rule_list.clear_list", icon="X")

# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_PG_objectCollection(PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)


# Register and Unregister classes from Blender:
classes = (
    CUSTOM_OT_actions,
    CUSTOM_OT_clearList,
    CUSTOM_OT_printItems,
    RULES_UIList,
    rules_PGT,
    CUSTOM_PT_objectList,
    CUSTOM_PG_objectCollection,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=rules_PGT)

    # UIList:
    bpy.types.Scene.rule_list = bpy.props.CollectionProperty(type=rules_PGT)
    bpy.types.Scene.rule_list_index = bpy.props.IntProperty(name="Rule list index.", default=100)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool

    # UIList:
    del bpy.types.Scene.rule_list
    del bpy.types.Scene.rule_list_index


if __name__ == '__main__':
    register()
