# 3Dビュー > 「ビュー」メニュー > 「視点を揃える」メニュー

import bpy

################
# オペレーター #
################

class ViewSelectedEX(bpy.types.Operator):
	bl_idname = "view3d.view_selected_ex"
	bl_label = "選択部分を表示 (非ズーム)"
	bl_description = "選択中の物に3D視点の中心を合わせます(ズームはしません)"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		smooth_view = context.user_preferences.view.smooth_view
		context.user_preferences.view.smooth_view = 0
		view_distance = context.region_data.view_distance
		bpy.ops.view3d.view_selected()
		context.region_data.view_distance = view_distance
		context.user_preferences.view.smooth_view = smooth_view
		return {'FINISHED'}

class ResetCursor(bpy.types.Operator):
	bl_idname = "view3d.reset_cursor"
	bl_label = "カーソルの位置をリセット"
	bl_description = "カーソルのXYZを0.0にします(他の位置も可)"
	bl_options = {'REGISTER', 'UNDO'}
	
	co = bpy.props.FloatVectorProperty(name="カーソル位置", default=(0.0, 0.0, 0.0), step=10, precision=3)
	isLookCenter = bpy.props.BoolProperty(name="視点を3Dカーソルに", default=False)
	
	def execute(self, context):
		context.space_data.cursor_location = self.co
		if (self.isLookCenter):
			bpy.ops.view3d.view_center_cursor()
		return {'FINISHED'}

class ResetView(bpy.types.Operator):
	bl_idname = "view3d.reset_view"
	bl_label = "視点を中心に"
	bl_description = "3Dビューの視点を座標の中心に移動します"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		context.region_data.view_location = (0.0, 0.0, 0.0)
		context.region_data.update()
		return {'FINISHED'}

class SelectAndView(bpy.types.Operator):
	bl_idname = "view3d.select_and_view"
	bl_label = "選択+視点の中心に"
	bl_description = "マウス下の物を選択し視点の中心にします (Shiftを押しながらで追加選択)"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		("view_selected_ex", "ズームしない", "", 1),
		("view_selected", "ズームする", "", 2),
		]
	mode = bpy.props.EnumProperty(items=items, name="視点変更方法")
	mouse_loc = bpy.props.IntVectorProperty(name="マウス位置", size=2)
	isExtend = bpy.props.BoolProperty(name="追加選択", default=False)
	
	def execute(self, context):
		bpy.ops.view3d.select(location=self.mouse_loc, extend=self.isExtend)
		if (self.mode == "view_selected_ex"):
			bpy.ops.view3d.view_selected_ex()
		else:
			bpy.ops.view3d.view_selected()
		return {'FINISHED'}
	def invoke(self, context, event):
		self.mouse_loc[0] = event.mouse_region_x
		self.mouse_loc[1] = event.mouse_region_y
		self.isExtend = event.shift
		return self.execute(context)

################
# メニュー追加 #
################

# メニューを登録する関数
def menu(self, context):
	self.layout.separator()
	self.layout.operator(ResetCursor.bl_idname, icon="PLUGIN")
	self.layout.operator(ResetView.bl_idname, icon="PLUGIN")
	self.layout.operator(ViewSelectedEX.bl_idname, icon="PLUGIN")
	self.layout.operator(SelectAndView.bl_idname, icon="PLUGIN")
