# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "OST-OpenCam",
    "author" : "pixelflattop", 
    "description" : "Custome Camera from the OpenShort Tools series",
    "blender" : (4, 2, 0),
    "version" : (0, 0, 1),
    "location" : "N-Panel",
    "warning" : "",
    "doc_url": "https://github.com/PixelFlatTop/OST-OpenCam", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
from bpy.app.handlers import persistent
import os


addon_keymaps = {}
_icons = None


def sna_update_sna_active_index_fstop_BE99A(self, context):
    sna_updated_prop = self.sna_active_index_fstop
    bpy.context.scene.camera.data.dof.aperture_fstop = bpy.context.scene.sna_fstop[sna_updated_prop].fstop


def sna_update_sna_active_index_lens_280CE(self, context):
    sna_updated_prop = self.sna_active_index_lens
    bpy.context.scene.camera.data.lens = bpy.context.scene.sna_lens[sna_updated_prop].lens


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def sna_update_sna_aspect_ration_presets_9D9AC(self, context):
    sna_updated_prop = self.sna_aspect_ration_presets
    if sna_updated_prop == "16:9":
        sna_set_resolution_9F8D5(1920, 1080)
    elif sna_updated_prop == "1.35:1":
        sna_set_resolution_9F8D5(1920, 1443)
    elif sna_updated_prop == "2.35:1":
        sna_set_resolution_9F8D5(1920, 817)
    else:
        pass


class SNA_UL_display_collection_list_065DB(bpy.types.UIList):

    def draw_item(self, context, layout, data, item_065DB, icon, active_data, active_propname, index_065DB):
        row = layout
        layout.prop(item_065DB, 'name', text='', icon_value=0, emboss=False)
        if bpy.context.scene.sna_show_lens_value:
            layout.prop(item_065DB, 'lens', text='', icon_value=0, emboss=False)

    def filter_items(self, context, data, propname):
        flt_flags = []
        for item in getattr(data, propname):
            if not self.filter_name or self.filter_name.lower() in item.name.lower():
                if True:
                    flt_flags.append(self.bitflag_filter_item)
                else:
                    flt_flags.append(0)
            else:
                flt_flags.append(0)
        return flt_flags, []


def display_collection_id(uid, vars):
    id = f"coll_{uid}"
    for var in vars.keys():
        if var.startswith("i_"):
            id += f"_{var}_{vars[var]}"
    return id


class SNA_UL_display_collection_list001_23080(bpy.types.UIList):

    def draw_item(self, context, layout, data, item_23080, icon, active_data, active_propname, index_23080):
        row = layout
        layout.prop(item_23080, 'name', text='', icon_value=0, emboss=False)
        if bpy.context.scene.sna_show_fstop_value:
            layout.prop(item_23080, 'fstop', text='', icon_value=0, emboss=False)

    def filter_items(self, context, data, propname):
        flt_flags = []
        for item in getattr(data, propname):
            if not self.filter_name or self.filter_name.lower() in item.name.lower():
                if True:
                    flt_flags.append(self.bitflag_filter_item)
                else:
                    flt_flags.append(0)
            else:
                flt_flags.append(0)
        return flt_flags, []


class SNA_OT_Fstop_Add_Item_652Ef(bpy.types.Operator):
    bl_idname = "sna.fstop_add_item_652ef"
    bl_label = "fstop Add Item"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        item_9B50B = bpy.context.scene.sna_fstop.add()
        item_9B50B.name = 'F/' + str(round(bpy.context.scene.camera.data.dof.aperture_fstop, abs(1)))
        item_9B50B.fstop = bpy.context.scene.camera.data.dof.aperture_fstop
        bpy.context.scene.sna_active_index_fstop = int(len(bpy.context.scene.sna_fstop) - 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Fstop_Remove_Item_B302E(bpy.types.Operator):
    bl_idname = "sna.fstop_remove_item_b302e"
    bl_label = "fstop Remove Item"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (int(len(bpy.context.scene.sna_fstop) - 1.0) == bpy.context.scene.sna_active_index_fstop):
            if len(bpy.context.scene.sna_fstop) > bpy.context.scene.sna_active_index_fstop:
                bpy.context.scene.sna_fstop.remove(bpy.context.scene.sna_active_index_fstop)
            bpy.context.scene.sna_active_index_fstop = int(len(bpy.context.scene.sna_fstop) - 1.0)
        else:
            if len(bpy.context.scene.sna_fstop) > bpy.context.scene.sna_active_index_fstop:
                bpy.context.scene.sna_fstop.remove(bpy.context.scene.sna_active_index_fstop)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Fstop_Move_Up_93F62(bpy.types.Operator):
    bl_idname = "sna.fstop_move_up_93f62"
    bl_label = "fstop Move Up"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_active_index_fstop == 0):
            pass
        else:
            bpy.context.scene.sna_fstop.move(bpy.context.scene.sna_active_index_fstop, int(bpy.context.scene.sna_active_index_fstop - 1.0))
            item_6DEE2 = bpy.context.scene.sna_fstop[int(bpy.context.scene.sna_active_index_fstop - 1.0)]
            bpy.context.scene.sna_active_index_fstop = int(bpy.context.scene.sna_active_index_fstop - 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Fstop_Move_Down_71820(bpy.types.Operator):
    bl_idname = "sna.fstop_move_down_71820"
    bl_label = "fstop Move Down"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_active_index_fstop == int(len(bpy.context.scene.sna_fstop) - 1.0)):
            pass
        else:
            bpy.context.scene.sna_fstop.move(bpy.context.scene.sna_active_index_fstop, int(bpy.context.scene.sna_active_index_fstop + 1.0))
            item_425F5 = bpy.context.scene.sna_fstop[int(bpy.context.scene.sna_active_index_fstop + 1.0)]
            bpy.context.scene.sna_active_index_fstop = int(bpy.context.scene.sna_active_index_fstop + 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Lens_Remove_Item_7256D(bpy.types.Operator):
    bl_idname = "sna.lens_remove_item_7256d"
    bl_label = "Lens Remove Item"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (int(len(bpy.context.scene.sna_lens) - 1.0) == bpy.context.scene.sna_active_index_lens):
            if len(bpy.context.scene.sna_lens) > bpy.context.scene.sna_active_index_lens:
                bpy.context.scene.sna_lens.remove(bpy.context.scene.sna_active_index_lens)
            bpy.context.scene.sna_active_index_lens = int(len(bpy.context.scene.sna_lens) - 1.0)
        else:
            if len(bpy.context.scene.sna_lens) > bpy.context.scene.sna_active_index_lens:
                bpy.context.scene.sna_lens.remove(bpy.context.scene.sna_active_index_lens)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Lens_Add_Item_E1Ec1(bpy.types.Operator):
    bl_idname = "sna.lens_add_item_e1ec1"
    bl_label = "Lens Add item"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        item_7AEDC = bpy.context.scene.sna_lens.add()
        item_7AEDC.name = str(bpy.context.scene.camera.data.lens) + ' mm'
        item_7AEDC.lens = bpy.context.scene.camera.data.lens
        bpy.context.scene.sna_active_index_lens = int(len(bpy.context.scene.sna_lens) - 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Lens_Move_Up_Fef16(bpy.types.Operator):
    bl_idname = "sna.lens_move_up_fef16"
    bl_label = "Lens Move Up"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_active_index_lens == 0):
            pass
        else:
            bpy.context.scene.sna_lens.move(bpy.context.scene.sna_active_index_lens, int(bpy.context.scene.sna_active_index_lens - 1.0))
            item_86400 = bpy.context.scene.sna_lens[int(bpy.context.scene.sna_active_index_lens - 1.0)]
            bpy.context.scene.sna_active_index_lens = int(bpy.context.scene.sna_active_index_lens - 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Lens_Move_Down_0Cbaa(bpy.types.Operator):
    bl_idname = "sna.lens_move_down_0cbaa"
    bl_label = "Lens Move Down"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_active_index_lens == int(len(bpy.context.scene.sna_lens) - 1.0)):
            pass
        else:
            bpy.context.scene.sna_lens.move(bpy.context.scene.sna_active_index_lens, int(bpy.context.scene.sna_active_index_lens + 1.0))
            item_D285A = bpy.context.scene.sna_lens[int(bpy.context.scene.sna_active_index_lens + 1.0)]
            bpy.context.scene.sna_active_index_lens = int(bpy.context.scene.sna_active_index_lens + 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


@persistent
def load_pre_handler_B4CAD(dummy):
    pass


def sna_export__render_F6F8C(layout_function, ):
    col_14EC3 = layout_function.column(heading='', align=False)
    col_14EC3.alert = False
    col_14EC3.enabled = True
    col_14EC3.active = True
    col_14EC3.use_property_split = False
    col_14EC3.use_property_decorate = False
    col_14EC3.scale_x = 1.0
    col_14EC3.scale_y = 1.090000033378601
    col_14EC3.alignment = 'Expand'.upper()
    col_14EC3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_AED00 = col_14EC3.row(heading='', align=True)
    row_AED00.alert = False
    row_AED00.enabled = True
    row_AED00.active = True
    row_AED00.use_property_split = False
    row_AED00.use_property_decorate = False
    row_AED00.scale_x = 1.4800000190734863
    row_AED00.scale_y = 1.4800000190734863
    row_AED00.alignment = 'Expand'.upper()
    row_AED00.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = row_AED00.operator('render.render', text='RENDER STILL', icon_value=189, emboss=True, depress=False)
    op.write_still = True
    op = row_AED00.operator('render.render', text='RENDER ANIMATION', icon_value=214, emboss=True, depress=False)
    op.animation = True
    op.write_still = True
    op.use_viewport = True
    col_14EC3.prop(bpy.context.scene.render, 'film_transparent', text='Transparent', icon_value=0, emboss=True, toggle=True)
    col_14EC3.separator(factor=1.3899999856948853)
    col_14EC3.prop(bpy.context.scene.render, 'filepath', text='File Path', icon_value=0, emboss=True)
    row_D254D = col_14EC3.row(heading='', align=True)
    row_D254D.alert = False
    row_D254D.enabled = True
    row_D254D.active = True
    row_D254D.use_property_split = False
    row_D254D.use_property_decorate = False
    row_D254D.scale_x = 1.3600000143051147
    row_D254D.scale_y = 1.0
    row_D254D.alignment = 'Expand'.upper()
    row_D254D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_D254D.prop(bpy.data.scenes[0].render.image_settings, 'file_format', text='', icon_value=0, emboss=True)
    row_D254D.prop(bpy.context.scene, 'sna_show_ffmpeg_video', text='', icon_value=142, emboss=True)
    if bpy.context.scene.sna_show_ffmpeg_video:
        grid_2770E = col_14EC3.grid_flow(columns=1, row_major=True, even_columns=False, even_rows=False, align=True)
        grid_2770E.enabled = True
        grid_2770E.active = True
        grid_2770E.use_property_split = True
        grid_2770E.use_property_decorate = False
        grid_2770E.alignment = 'Expand'.upper()
        grid_2770E.scale_x = 0.3700000047683716
        grid_2770E.scale_y = 1.2699999809265137
        if not True: grid_2770E.operator_context = "EXEC_DEFAULT"
        grid_2770E.separator(factor=0.5139999985694885)
        grid_2770E.prop(bpy.context.scene.render.ffmpeg, 'format', text='', icon_value=0, emboss=True)
        grid_2770E.separator(factor=0.009999990463256836)
        grid_2770E.prop(bpy.context.scene.render.ffmpeg, 'codec', text='', icon_value=0, emboss=True)
        grid_2770E.separator(factor=0.3190000057220459)
        grid_2770E.prop(bpy.context.scene.render.ffmpeg, 'constant_rate_factor', text='', icon_value=0, emboss=True)


def sna_add_to_view3d_mt_camera_add_E77EE(self, context):
    if not (False):
        layout = self.layout
        op = layout.operator('sna.importcam_b7bd8', text='Open Cam Rig', icon_value=616, emboss=True, depress=False)


class SNA_OT_Importcam_B7Bd8(bpy.types.Operator):
    bl_idname = "sna.importcam_b7bd8"
    bl_label = "ImportCam"
    bl_description = "Import Open Cam Rig into the scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if property_exists("bpy.data.collections['CA-OpenCam'].name", globals(), locals()):
            self.report({'WARNING'}, message='OpenCam Rig already exist. only one instance of OpenCam Rig at the moment')
        else:
            before_data = list(bpy.data.collections)
            bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'OpenCAM_v004.blend') + r'\Collection', filename='CA-OpenCam', link=False)
            new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
            appended_B5286 = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Make_Active_Camera_Cffa3(bpy.types.Operator):
    bl_idname = "sna.make_active_camera_cffa3"
    bl_label = "Make Active Camera"
    bl_description = "Make selected camera the active camera in the blender scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.view_layer.objects.active.type == 'CAMERA':
            prev_context = bpy.context.area.type
            bpy.context.area.type = 'VIEW_3D'
            bpy.ops.view3d.object_as_camera('INVOKE_DEFAULT', )
            bpy.context.area.type = prev_context
        else:
            self.report({'WARNING'}, message='Is not a Camera object')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2(bpy.types.Panel):
    bl_label = 'OpenCam - Control  Panel'
    bl_idname = 'SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Item'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=258, scale=1.0)

    def draw(self, context):
        layout = self.layout
        col_35CAD = layout.column(heading='', align=True)
        col_35CAD.alert = False
        col_35CAD.enabled = True
        col_35CAD.active = True
        col_35CAD.use_property_split = True
        col_35CAD.use_property_decorate = True
        col_35CAD.scale_x = 1.0
        col_35CAD.scale_y = 1.0
        col_35CAD.alignment = 'Expand'.upper()
        col_35CAD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_48FEB = col_35CAD.column(heading='', align=True)
        col_48FEB.alert = False
        col_48FEB.enabled = True
        col_48FEB.active = True
        col_48FEB.use_property_split = True
        col_48FEB.use_property_decorate = True
        col_48FEB.scale_x = 1.0
        col_48FEB.scale_y = 1.0
        col_48FEB.alignment = 'Expand'.upper()
        col_48FEB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_48FEB.prop(bpy.context.scene.camera.data, 'lens', text='Focal Length', icon_value=0, emboss=True)
        col_48FEB.prop(bpy.context.scene.camera.data.dof, 'aperture_fstop', text='F-Stop', icon_value=0, emboss=True)
        col_35CAD.separator(factor=1.0)
        row_0192F = col_35CAD.row(heading='', align=False)
        row_0192F.alert = False
        row_0192F.enabled = True
        row_0192F.active = True
        row_0192F.use_property_split = True
        row_0192F.use_property_decorate = True
        row_0192F.scale_x = 1.0
        row_0192F.scale_y = 1.0
        row_0192F.alignment = 'Expand'.upper()
        row_0192F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_0192F.prop(bpy.context.scene.camera.data, 'sensor_width', text='Sensor Size', icon_value=0, emboss=True)
        col_35CAD.separator(factor=1.0)
        col_35CAD.prop(bpy.context.scene.camera.data, 'clip_start', text='Near Clip', icon_value=0, emboss=True)
        col_35CAD.prop(bpy.context.scene.camera.data, 'clip_end', text='Far Clip', icon_value=0, emboss=True)


class SNA_OT_Lenses_4Add7(bpy.types.Operator):
    bl_idname = "sna.lenses_4add7"
    bl_label = "Lenses"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    sna_lens_value: bpy.props.FloatProperty(name='lens_value', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        self.report({'INFO'}, message='Lens Change')
        sna_lens_96A6F(self.sna_lens_value)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_lens_96A6F(lens_value):
    bpy.context.scene.camera.data.lens = lens_value


def sna_fstop_7261F(fstop_value):
    bpy.context.scene.camera.data.dof.aperture_fstop = fstop_value


class SNA_OT_Fstops_C7002(bpy.types.Operator):
    bl_idname = "sna.fstops_c7002"
    bl_label = "Fstops"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    sna_fstop_value: bpy.props.FloatProperty(name='fstop_value', description='', default=0.0, subtype='NONE', unit='NONE', step=1, precision=6)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        self.report({'INFO'}, message='F-stop Change')
        sna_fstop_7261F(self.sna_fstop_value)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_OPEN_CAM_OUTPUT_132BF(bpy.types.Panel):
    bl_label = 'Open Cam Output'
    bl_idname = 'SNA_PT_OPEN_CAM_OUTPUT_132BF'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Item'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=213, scale=1.0)

    def draw(self, context):
        layout = self.layout
        row_A30BD = layout.row(heading='', align=False)
        row_A30BD.alert = False
        row_A30BD.enabled = True
        row_A30BD.active = True
        row_A30BD.use_property_split = False
        row_A30BD.use_property_decorate = False
        row_A30BD.scale_x = 9.25
        row_A30BD.scale_y = 1.0
        row_A30BD.alignment = 'Right'.upper()
        row_A30BD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A30BD.label(text='Aspect Ratio Presets', icon_value=0)
        row_A30BD.prop(bpy.context.scene, 'sna_aspect_ration_presets', text='', icon_value=0, emboss=True)
        layout_function = layout
        sna_export__render_F6F8C(layout_function, )


def sna_set_resolution_9F8D5(X, Y):
    bpy.context.scene.render.resolution_x = X
    bpy.context.scene.render.resolution_y = Y


class SNA_OT_My_Generic_Operator_0Ad3C(bpy.types.Operator):
    bl_idname = "sna.my_generic_operator_0ad3c"
    bl_label = "1.35:1"
    bl_description = "1920 x 1443 HD "
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1443
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_My_Generic_Operator_E6008(bpy.types.Operator):
    bl_idname = "sna.my_generic_operator_e6008"
    bl_label = "16:9"
    bl_description = "1920 x 1080 HD "
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.render.resolution_x = 'res_x'
        bpy.context.scene.render.resolution_y = 1080
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_My_Generic_Operator_7F6D6(bpy.types.Operator):
    bl_idname = "sna.my_generic_operator_7f6d6"
    bl_label = "2.35:1"
    bl_description = "1920 x 817 HD "
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        Variable = None
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 817
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_IMPORT_CAMERA_DF348(bpy.types.Panel):
    bl_label = 'Import Camera'
    bl_idname = 'SNA_PT_IMPORT_CAMERA_DF348'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        row_FC917 = layout.row(heading='', align=False)
        row_FC917.alert = False
        row_FC917.enabled = True
        row_FC917.active = True
        row_FC917.use_property_split = False
        row_FC917.use_property_decorate = False
        row_FC917.scale_x = 1.0
        row_FC917.scale_y = 1.0
        row_FC917.alignment = 'Expand'.upper()
        row_FC917.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_FC917.operator('sna.importcam_b7bd8', text='Import OpenCamRig', icon_value=0, emboss=True, depress=False)
        op = row_FC917.operator('sna.make_active_camera_cffa3', text='', icon_value=615, emboss=False, depress=False)


class SNA_PT_DOF_A3DB9(bpy.types.Panel):
    bl_label = 'DOF'
    bl_idname = 'SNA_PT_DOF_A3DB9'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene.camera.data.dof, 'use_dof', text='', icon_value=0, emboss=True)

    def draw(self, context):
        layout = self.layout
        col_8F4C7 = layout.column(heading='', align=True)
        col_8F4C7.alert = False
        col_8F4C7.enabled = bpy.context.scene.camera.data.dof.use_dof
        col_8F4C7.active = True
        col_8F4C7.use_property_split = True
        col_8F4C7.use_property_decorate = False
        col_8F4C7.scale_x = 1.0
        col_8F4C7.scale_y = 1.0
        col_8F4C7.alignment = 'Expand'.upper()
        col_8F4C7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_8F4C7.prop(bpy.context.scene.camera.data.dof, 'focus_object', text='Focus on Object', icon_value=0, emboss=True)
        row_3E06F = col_8F4C7.row(heading='', align=False)
        row_3E06F.alert = False
        row_3E06F.enabled = True
        row_3E06F.active = True
        row_3E06F.use_property_split = True
        row_3E06F.use_property_decorate = True
        row_3E06F.scale_x = 1.0
        row_3E06F.scale_y = 1.0
        row_3E06F.alignment = 'Expand'.upper()
        row_3E06F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_3E06F.prop(bpy.context.scene.camera.data.dof, 'focus_distance', text='Focus Distance', icon_value=0, emboss=True)


class SNA_PT_CAM_DISPLAYS_A02D5(bpy.types.Panel):
    bl_label = 'Cam Displays'
    bl_idname = 'SNA_PT_CAM_DISPLAYS_A02D5'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        row_123BD = layout.row(heading='', align=False)
        row_123BD.alert = False
        row_123BD.enabled = True
        row_123BD.active = True
        row_123BD.use_property_split = True
        row_123BD.use_property_decorate = False
        row_123BD.scale_x = 1.0
        row_123BD.scale_y = 1.0
        row_123BD.alignment = 'Expand'.upper()
        row_123BD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_123BD.label(text='Depth Plane', icon_value=620)
        attr_CF2D0 = '["' + str('Socket_7' + '"]') 
        row_123BD.prop(bpy.data.objects['GN-Depth Plane'].modifiers['GN-Depth Plane'], attr_CF2D0, text='', icon_value=0, emboss=True)
        row_9B43C = layout.row(heading='', align=False)
        row_9B43C.alert = False
        row_9B43C.enabled = True
        row_9B43C.active = True
        row_9B43C.use_property_split = True
        row_9B43C.use_property_decorate = False
        row_9B43C.scale_x = 1.0
        row_9B43C.scale_y = 1.0
        row_9B43C.alignment = 'Expand'.upper()
        row_9B43C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_9B43C.label(text='Grid Plane', icon_value=618)
        attr_845FB = '["' + str('Socket_6' + '"]') 
        row_9B43C.prop(bpy.data.objects['GN-Focal Length Plane'].modifiers['GN-Focal Length Plane'], attr_845FB, text='', icon_value=0, emboss=True, expand=False, toggle=False)
        row_7985D = layout.row(heading='', align=False)
        row_7985D.alert = False
        row_7985D.enabled = True
        row_7985D.active = True
        row_7985D.use_property_split = True
        row_7985D.use_property_decorate = False
        row_7985D.scale_x = 1.0
        row_7985D.scale_y = 1.0
        row_7985D.alignment = 'Expand'.upper()
        row_7985D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7985D.template_icon(icon_value=282, scale=1.25)
        row_7985D.prop(bpy.data.cameras['Camera'], 'passepartout_alpha', text='Passespartout', icon_value=0, emboss=True)


class SNA_PT_CAM_PRESETS_29E02(bpy.types.Panel):
    bl_label = 'Cam Presets'
    bl_idname = 'SNA_PT_CAM_PRESETS_29E02'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 3
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.label(text='Lens Presets', icon_value=0)
        row_2E9E1 = layout.row(heading='', align=True)
        row_2E9E1.alert = False
        row_2E9E1.enabled = True
        row_2E9E1.active = True
        row_2E9E1.use_property_split = False
        row_2E9E1.use_property_decorate = False
        row_2E9E1.scale_x = 1.0
        row_2E9E1.scale_y = 1.0
        row_2E9E1.alignment = 'Expand'.upper()
        row_2E9E1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        coll_id = display_collection_id('065DB', locals())
        row_2E9E1.template_list('SNA_UL_display_collection_list_065DB', coll_id, bpy.context.scene, 'sna_lens', bpy.context.scene, 'sna_active_index_lens', rows=0)
        col_10FB0 = row_2E9E1.column(heading='', align=True)
        col_10FB0.alert = False
        col_10FB0.enabled = True
        col_10FB0.active = True
        col_10FB0.use_property_split = False
        col_10FB0.use_property_decorate = False
        col_10FB0.scale_x = 1.0
        col_10FB0.scale_y = 1.0
        col_10FB0.alignment = 'Expand'.upper()
        col_10FB0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_10FB0.operator('sna.lens_add_item_e1ec1', text='', icon_value=45, emboss=False, depress=False)
        op = col_10FB0.operator('sna.lens_remove_item_7256d', text='', icon_value=87, emboss=False, depress=False)
        col_10FB0.separator(factor=1.0)
        op = col_10FB0.operator('sna.lens_move_up_fef16', text='', icon_value=98, emboss=False, depress=False)
        op = col_10FB0.operator('sna.lens_move_down_0cbaa', text='', icon_value=95, emboss=False, depress=False)
        col_10FB0.prop(bpy.context.scene, 'sna_show_lens_value', text='', icon_value=424, emboss=True)
        layout.label(text='Lens Presets', icon_value=0)
        row_6F513 = layout.row(heading='', align=True)
        row_6F513.alert = False
        row_6F513.enabled = True
        row_6F513.active = True
        row_6F513.use_property_split = False
        row_6F513.use_property_decorate = False
        row_6F513.scale_x = 1.0
        row_6F513.scale_y = 1.0
        row_6F513.alignment = 'Expand'.upper()
        row_6F513.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        coll_id = display_collection_id('23080', locals())
        row_6F513.template_list('SNA_UL_display_collection_list001_23080', coll_id, bpy.context.scene, 'sna_fstop', bpy.context.scene, 'sna_active_index_fstop', rows=0)
        col_85141 = row_6F513.column(heading='', align=True)
        col_85141.alert = False
        col_85141.enabled = True
        col_85141.active = True
        col_85141.use_property_split = False
        col_85141.use_property_decorate = False
        col_85141.scale_x = 1.0
        col_85141.scale_y = 1.0
        col_85141.alignment = 'Expand'.upper()
        col_85141.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_85141.operator('sna.fstop_add_item_652ef', text='', icon_value=45, emboss=False, depress=False)
        op = col_85141.operator('sna.fstop_remove_item_b302e', text='', icon_value=87, emboss=False, depress=False)
        col_85141.separator(factor=1.0)
        op = col_85141.operator('sna.fstop_move_up_93f62', text='', icon_value=98, emboss=False, depress=False)
        op = col_85141.operator('sna.fstop_move_down_71820', text='', icon_value=95, emboss=False, depress=False)
        col_85141.prop(bpy.context.scene, 'sna_show_fstop_value', text='', icon_value=424, emboss=True)


class SNA_PT_COLOR_MANAGEMENT_96372(bpy.types.Panel):
    bl_label = 'Color Management'
    bl_idname = 'SNA_PT_COLOR_MANAGEMENT_96372'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_OPEN_CAM_OUTPUT_132BF'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.separator(factor=0.9699999690055847)
        col_5472D = layout.column(heading='', align=False)
        col_5472D.alert = False
        col_5472D.enabled = True
        col_5472D.active = True
        col_5472D.use_property_split = True
        col_5472D.use_property_decorate = False
        col_5472D.scale_x = 0.01000058650970459
        col_5472D.scale_y = 1.0
        col_5472D.alignment = 'Center'.upper()
        col_5472D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_5472D.prop(bpy.context.scene.display_settings, 'display_device', text='Color Transform', icon_value=0, emboss=True)
        col_5472D.prop(bpy.data.scenes[0].view_settings, 'view_transform', text='View Transform', icon_value=0, emboss=True)
        col_5472D.prop(bpy.data.scenes[0].view_settings, 'look', text='Look', icon_value=0, emboss=True)
        layout.separator(factor=0.9699999690055847)
        col_70733 = layout.column(heading='', align=False)
        col_70733.alert = False
        col_70733.enabled = True
        col_70733.active = True
        col_70733.use_property_split = False
        col_70733.use_property_decorate = False
        col_70733.scale_x = 1.0
        col_70733.scale_y = 1.0
        col_70733.alignment = 'Expand'.upper()
        col_70733.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_70733.prop(bpy.data.scenes[0].view_settings, 'exposure', text='Exposure', icon_value=0, emboss=True)
        col_70733.prop(bpy.data.scenes[0].view_settings, 'gamma', text='Gamma', icon_value=0, emboss=True)


class SNA_GROUP_sna_lens_data(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', description='', default='', subtype='NONE', maxlen=0)
    lens: bpy.props.FloatProperty(name='Lens', description='', default=0.0, subtype='DISTANCE_CAMERA', unit='NONE', step=3, precision=6)


class SNA_GROUP_sna_fstop_data(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', description='', default='', subtype='NONE', maxlen=0)
    fstop: bpy.props.FloatProperty(name='F-stop', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_lens_data)
    bpy.utils.register_class(SNA_GROUP_sna_fstop_data)
    bpy.types.Scene.sna_active_index_lens = bpy.props.IntProperty(name='Active Index lens', description='', default=0, subtype='NONE', update=sna_update_sna_active_index_lens_280CE)
    bpy.types.Scene.sna_active_index_fstop = bpy.props.IntProperty(name='Active Index fstop', description='', default=0, subtype='NONE', update=sna_update_sna_active_index_fstop_BE99A)
    bpy.types.Scene.sna_lens = bpy.props.CollectionProperty(name='Lens', description='', type=SNA_GROUP_sna_lens_data)
    bpy.types.Scene.sna_fstop = bpy.props.CollectionProperty(name='F-stop', description='', type=SNA_GROUP_sna_fstop_data)
    bpy.types.Scene.sna_show_lens_value = bpy.props.BoolProperty(name='Show Lens value', description='', default=False)
    bpy.types.Scene.sna_show_fstop_value = bpy.props.BoolProperty(name='Show fstop value', description='', default=False)
    bpy.types.Scene.sna_show_ffmpeg_video = bpy.props.BoolProperty(name='Show FFmpeg Video', description='', default=False)
    bpy.types.Scene.sna_aspect_ration_presets = bpy.props.EnumProperty(name='Aspect Ration Presets', description='', items=[('16:9', '16:9', '', 0, 0), ('1.35:1', '1.35:1', '', 0, 1), ('2.35:1', '2.35:1', '', 0, 2)], update=sna_update_sna_aspect_ration_presets_9D9AC)
    bpy.utils.register_class(SNA_OT_Fstop_Add_Item_652Ef)
    bpy.utils.register_class(SNA_OT_Fstop_Remove_Item_B302E)
    bpy.utils.register_class(SNA_OT_Fstop_Move_Up_93F62)
    bpy.utils.register_class(SNA_OT_Fstop_Move_Down_71820)
    bpy.utils.register_class(SNA_OT_Lens_Remove_Item_7256D)
    bpy.utils.register_class(SNA_OT_Lens_Add_Item_E1Ec1)
    bpy.utils.register_class(SNA_OT_Lens_Move_Up_Fef16)
    bpy.utils.register_class(SNA_OT_Lens_Move_Down_0Cbaa)
    bpy.app.handlers.load_pre.append(load_pre_handler_B4CAD)
    bpy.types.VIEW3D_MT_camera_add.prepend(sna_add_to_view3d_mt_camera_add_E77EE)
    bpy.utils.register_class(SNA_OT_Importcam_B7Bd8)
    bpy.utils.register_class(SNA_OT_Make_Active_Camera_Cffa3)
    bpy.utils.register_class(SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2)
    bpy.utils.register_class(SNA_OT_Lenses_4Add7)
    bpy.utils.register_class(SNA_OT_Fstops_C7002)
    bpy.utils.register_class(SNA_PT_OPEN_CAM_OUTPUT_132BF)
    bpy.utils.register_class(SNA_OT_My_Generic_Operator_0Ad3C)
    bpy.utils.register_class(SNA_OT_My_Generic_Operator_E6008)
    bpy.utils.register_class(SNA_OT_My_Generic_Operator_7F6D6)
    bpy.utils.register_class(SNA_PT_IMPORT_CAMERA_DF348)
    bpy.utils.register_class(SNA_PT_DOF_A3DB9)
    bpy.utils.register_class(SNA_PT_CAM_DISPLAYS_A02D5)
    bpy.utils.register_class(SNA_PT_CAM_PRESETS_29E02)
    bpy.utils.register_class(SNA_UL_display_collection_list_065DB)
    bpy.utils.register_class(SNA_UL_display_collection_list001_23080)
    bpy.utils.register_class(SNA_PT_COLOR_MANAGEMENT_96372)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_aspect_ration_presets
    del bpy.types.Scene.sna_show_ffmpeg_video
    del bpy.types.Scene.sna_show_fstop_value
    del bpy.types.Scene.sna_show_lens_value
    del bpy.types.Scene.sna_fstop
    del bpy.types.Scene.sna_lens
    del bpy.types.Scene.sna_active_index_fstop
    del bpy.types.Scene.sna_active_index_lens
    bpy.utils.unregister_class(SNA_GROUP_sna_fstop_data)
    bpy.utils.unregister_class(SNA_GROUP_sna_lens_data)
    bpy.utils.unregister_class(SNA_OT_Fstop_Add_Item_652Ef)
    bpy.utils.unregister_class(SNA_OT_Fstop_Remove_Item_B302E)
    bpy.utils.unregister_class(SNA_OT_Fstop_Move_Up_93F62)
    bpy.utils.unregister_class(SNA_OT_Fstop_Move_Down_71820)
    bpy.utils.unregister_class(SNA_OT_Lens_Remove_Item_7256D)
    bpy.utils.unregister_class(SNA_OT_Lens_Add_Item_E1Ec1)
    bpy.utils.unregister_class(SNA_OT_Lens_Move_Up_Fef16)
    bpy.utils.unregister_class(SNA_OT_Lens_Move_Down_0Cbaa)
    bpy.app.handlers.load_pre.remove(load_pre_handler_B4CAD)
    bpy.types.VIEW3D_MT_camera_add.remove(sna_add_to_view3d_mt_camera_add_E77EE)
    bpy.utils.unregister_class(SNA_OT_Importcam_B7Bd8)
    bpy.utils.unregister_class(SNA_OT_Make_Active_Camera_Cffa3)
    bpy.utils.unregister_class(SNA_PT_OPENCAM__CONTROL__PANEL_DB4A2)
    bpy.utils.unregister_class(SNA_OT_Lenses_4Add7)
    bpy.utils.unregister_class(SNA_OT_Fstops_C7002)
    bpy.utils.unregister_class(SNA_PT_OPEN_CAM_OUTPUT_132BF)
    bpy.utils.unregister_class(SNA_OT_My_Generic_Operator_0Ad3C)
    bpy.utils.unregister_class(SNA_OT_My_Generic_Operator_E6008)
    bpy.utils.unregister_class(SNA_OT_My_Generic_Operator_7F6D6)
    bpy.utils.unregister_class(SNA_PT_IMPORT_CAMERA_DF348)
    bpy.utils.unregister_class(SNA_PT_DOF_A3DB9)
    bpy.utils.unregister_class(SNA_PT_CAM_DISPLAYS_A02D5)
    bpy.utils.unregister_class(SNA_PT_CAM_PRESETS_29E02)
    bpy.utils.unregister_class(SNA_UL_display_collection_list_065DB)
    bpy.utils.unregister_class(SNA_UL_display_collection_list001_23080)
    bpy.utils.unregister_class(SNA_PT_COLOR_MANAGEMENT_96372)
