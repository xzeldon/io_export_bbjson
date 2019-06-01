bl_info = {
    "name": "Blockbuster JSON export",
    "author": "McHorse",
    "version": (0, 1, 0),
    "blender": (2, 77, 0),
    "location": "File > Export",
    "description": "Exports JSON model out of Blender document for Blockbuster mod. Its main task is to create limbs and poses configuration to avoid doing it by hand.",
    "warning": "",
    "category": "Export"
}

import bpy
from bpy.props import (BoolProperty, FloatProperty, StringProperty, EnumProperty)
from bpy_extras.io_utils import (ExportHelper, orientation_helper_factory, path_reference_mode, axis_conversion)

# Export panel
class ExportOBJ(bpy.types.Operator, ExportHelper):
    # Panel's information
    bl_idname = "export_scene.bbjson"
    bl_label = 'Export Blockbuster JSON'
    bl_options = {'PRESET'}

    # Panel's properties
    filename_ext = ".json"
    filter_glob = StringProperty(default="*.json", options={'HIDDEN'})
    use_selection = BoolProperty(name="Selection Only", description="Export selected objects only", default=False)
    path_mode = path_reference_mode
    check_extension = True

    def execute(self, context):
        from . import export
        
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "check_existing", "filter_glob", "path_mode"))
        
        return export.save(context, **keywords)

# Register and stuff
def menu_func_export(self, context):
    self.layout.operator(ExportOBJ.bl_idname, text="Blockbuster JSON (.json)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if "bpy" in locals():
    import importlib
    
    if "export_bobj" in locals():
        importlib.reload(export_bobj)

if __name__ == "__main__":
    register()