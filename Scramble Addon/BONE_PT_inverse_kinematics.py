# 「プロパティ」エリア > 「ボーン」タブ > 「インバースキネマティクス (IK)」パネル

import bpy

################
# オペレーター #
################

class CopyIKSettings(bpy.types.Operator):
	bl_idname = "pose.copy_ik_settings"
	bl_label = "Copy the IK set"
	bl_description = "Copies of other selected bone IK settings Active"
	bl_options = {'REGISTER', 'UNDO'}
	
	lock_ik_x = bpy.props.BoolProperty(name="Lock", default=True)
	ik_stiffness_x = bpy.props.BoolProperty(name="Rigid", default=True)
	use_ik_limit_x = bpy.props.BoolProperty(name="Limit", default=True)
	ik_min_x = bpy.props.BoolProperty(name="Smallest", default=True)
	ik_max_x = bpy.props.BoolProperty(name="Biggest", default=True)
	
	lock_ik_y = bpy.props.BoolProperty(name="Lock", default=True)
	ik_stiffness_y = bpy.props.BoolProperty(name="Rigid", default=True)
	use_ik_limit_y = bpy.props.BoolProperty(name="Limit", default=True)
	ik_min_y = bpy.props.BoolProperty(name="Smallest", default=True)
	ik_max_y = bpy.props.BoolProperty(name="Biggest", default=True)
	
	lock_ik_z = bpy.props.BoolProperty(name="Lock", default=True)
	ik_stiffness_z = bpy.props.BoolProperty(name="Rigid", default=True)
	use_ik_limit_z = bpy.props.BoolProperty(name="Limit", default=True)
	ik_min_z = bpy.props.BoolProperty(name="Smallest", default=True)
	ik_max_z = bpy.props.BoolProperty(name="Biggest", default=True)
	
	ik_stretch = bpy.props.BoolProperty(name="Stretch", default=True)
	
	@classmethod
	def poll(cls, context):
		if (2 <= len(context.selected_pose_bones)):
			return True
		return False
	
	def draw(self, context):
		for axis in ['x', 'y', 'z']:
			self.layout.label(axis.upper())
			row = self.layout.row()
			row.prop(self, 'lock_ik_'+axis)
			row.prop(self, 'ik_stiffness_'+axis)
			row = self.layout.row()
			row.prop(self, 'use_ik_limit_'+axis)
			row.prop(self, 'ik_min_'+axis)
			row.prop(self, 'ik_max_'+axis)
		self.layout.label("")
		self.layout.prop(self, 'ik_stretch')
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
	def execute(self, context):
		source = context.active_pose_bone
		for target in context.selected_pose_bones[:]:
			if (source.name != target.name):
				for axis in ['x', 'y', 'z']:
					if (self.__getattribute__('lock_ik_'+axis)):
						target.__setattr__('lock_ik_'+axis, source.__getattribute__('lock_ik_'+axis))
					if (self.__getattribute__('ik_stiffness_'+axis)):
						target.__setattr__('ik_stiffness_'+axis, source.__getattribute__('ik_stiffness_'+axis))
					if (self.__getattribute__('use_ik_limit_'+axis)):
						target.__setattr__('use_ik_limit_'+axis, source.__getattribute__('use_ik_limit_'+axis))
					if (self.__getattribute__('ik_min_'+axis)):
						target.__setattr__('ik_min_'+axis, source.__getattribute__('ik_min_'+axis))
					if (self.__getattribute__('ik_max_'+axis)):
						target.__setattr__('ik_max_'+axis, source.__getattribute__('ik_max_'+axis))
				if (self.ik_stretch):
					target.ik_stretch = source.ik_stretch
		return {'FINISHED'}

################
# メニュー追加 #
################

# メニューのオン/オフの判定
def IsMenuEnable(self_id):
	for id in bpy.context.user_preferences.addons["Scramble Addon"].preferences.disabled_menu.split(','):
		if (id == self_id):
			return False
	else:
		return True

# メニューを登録する関数
def menu(self, context):
	if (IsMenuEnable(__name__.split('.')[-1])):
		self.layout.operator(CopyIKSettings.bl_idname, icon='COPY_ID')
	if (context.user_preferences.addons["Scramble Addon"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]