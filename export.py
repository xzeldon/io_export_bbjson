import os
import json
import ntpath

import bpy

from progress_report import ProgressReport, ProgressReportSubstep

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# Remove spaces from given string (so it would be spaceless)
def name_compat(name):
    return 'None' if name is None else name.replace(' ', '_')

def save(context, filepath, use_selection=True):
    with ProgressReport(context.window_manager) as progress:
        scene = context.scene

        # Exit edit mode before exporting, so current object states are exported properly.
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        objects = context.selected_objects if use_selection else scene.objects

        progress.enter_substeps(1)
        write_file(context, filepath, objects, scene, progress)
        progress.leave_substeps()

    return {'FINISHED'}

def write_file(context, filepath, objects, scene, progress=ProgressReport()):
    with ProgressReportSubstep(progress, 2, "JSON export path: %r" % filepath, "JSON export finished") as subprogress1:
        with open(filepath, "w", encoding="utf8", newline="\n") as f:
            limbs = {}
            pose = {}

            for obj in objects:
                if obj.type != "MESH":
                    print("here")
                    continue
                
                print("over here")
                name = name_compat(obj.name)
                x = obj.location[0]
                y = obj.location[2]
                z = obj.location[1]
                
                limb = { 'origin': [x, y, z] }
                transform = {
                    'translate': [x * 16, y * 16, z * 16]
                }
                
                limbs[name] = limb
                pose[name] = transform
            
            # Write JSON to the file
            pose = {
                'size': [0.6, 1.8, 0.6],
                'limbs': pose
            }
            
            data = {
                'scheme': "1.3",
                'providesObj': True,
                'name': path_leaf(filepath),
                'limbs': limbs,
                'poses': {
                    'standing': pose,
                    'sneaking': pose,
                    'sleeping': pose,
                    'flying': pose
                }
            }
            
            f.write(json.dumps(data, indent=4, sort_keys=True))
        subprogress1.step("Finished exporting JSON")