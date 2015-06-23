# 3Dビュー > オブジェクトモード > 「Ctrl+L」キー

import bpy, bmesh

################
# オペレーター #
################

class MakeLinkObjectName(bpy.types.Operator):
	bl_idname = "object.make_link_object_name"
	bl_label = "オブジェクト名を同じに"
	bl_description = "他の選択オブジェクトにアクティブオブジェクトの名前をリンクします"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		name = context.active_object.name
		for obj in context.selected_objects:
			if (obj.name != name):
				obj.name = "temp"
				obj.name = name
		bpy.context.active_object.name = name
		return {'FINISHED'}

class MakeLinkLayer(bpy.types.Operator):
	bl_idname = "object.make_link_layer"
	bl_label = "レイヤーを同じに"
	bl_description = "他の選択オブジェクトにアクティブオブジェクトのレイヤーをリンクします"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		for obj in context.selected_objects:
			if (obj.name != context.active_object.name):
				obj.layers = context.active_object.layers
		return {'FINISHED'}

class MakeLinkDisplaySetting(bpy.types.Operator):
	bl_idname = "object.make_link_display_setting"
	bl_label = "オブジェクトの表示設定を同じに"
	bl_description = "他の選択オブジェクトにアクティブオブジェクトの表示パネルの設定をコピーします"
	bl_options = {'REGISTER', 'UNDO'}
	
	isSameType = bpy.props.BoolProperty(name="同タイプのオブジェクトのみ", default=True)
	show_name = bpy.props.BoolProperty(name="名前", default=True)
	show_axis = bpy.props.BoolProperty(name="座標軸", default=True)
	show_wire = bpy.props.BoolProperty(name="ワイヤーフレーム", default=True)
	show_all_edges = bpy.props.BoolProperty(name="すべての辺を表示", default=True)
	show_bounds = bpy.props.BoolProperty(name="バウンド", default=True)
	show_texture_space = bpy.props.BoolProperty(name="テクスチャ スペース", default=True)
	show_x_ray = bpy.props.BoolProperty(name="レントゲン", default=True)
	show_transparent = bpy.props.BoolProperty(name="透過", default=True)
	draw_bounds_type = bpy.props.BoolProperty(name="バウンドのタイプ", default=True)
	draw_type = bpy.props.BoolProperty(name="最高描画タイプ", default=True)
	color = bpy.props.BoolProperty(name="オブジェクトカラー", default=True)
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		activeObj = context.active_object
		for obj in context.selected_objects:
			if (not self.isSameType or activeObj.type == obj.type):
				if (obj.name != activeObj.name):
					if (self.show_name):
						obj.show_name = activeObj.show_name
					if (self.show_axis):
						obj.show_axis = activeObj.show_axis
					if (self.show_wire):
						obj.show_wire = activeObj.show_wire
					if (self.show_all_edges):
						obj.show_all_edges = activeObj.show_all_edges
					if (self.show_bounds):
						obj.show_bounds = activeObj.show_bounds
					if (self.show_texture_space):
						obj.show_texture_space = activeObj.show_texture_space
					if (self.show_x_ray):
						obj.show_x_ray = activeObj.show_x_ray
					if (self.show_transparent):
						obj.show_transparent = activeObj.show_transparent
					if (self.draw_bounds_type):
						obj.draw_bounds_type = activeObj.draw_bounds_type
					if (self.draw_type):
						obj.draw_type = activeObj.draw_type
					if (self.color):
						obj.color = activeObj.color
		return {'FINISHED'}

class MakeLinkUVNames(bpy.types.Operator):
	bl_idname = "object.make_link_uv_names"
	bl_label = "空のUVマップをリンク"
	bl_description = "他の選択オブジェクトにアクティブオブジェクトのUVを空にして追加します"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		if (context.object.type != 'MESH'):
			return False
		if (len(context.object.data.uv_layers) <= 0):
			return False
		for obj in context.selected_objects:
			if (obj.name != context.object.name):
				if (obj.type == 'MESH'):
					return True
		return False
	def execute(self, context):
		active_obj = context.active_object
		target_objs = []
		for obj in context.selected_objects:
			if (obj.type == 'MESH' and active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			for uv in active_obj.data.uv_layers:
				obj.data.uv_textures.new(uv.name)
		return {'FINISHED'}

class MakeLinkArmaturePose(bpy.types.Operator):
	bl_idname = "object.make_link_armature_pose"
	bl_label = "アーマチュアの動きをリンク"
	bl_description = "コンストレイントによって、他の選択アーマチュアにアクティブアーマチュアの動きを真似させます"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		if (context.object.type != 'ARMATURE'):
			return False
		for obj in context.selected_objects:
			if (obj.name != context.object.name):
				if (obj.type == 'ARMATURE'):
					return True
		return False
	def execute(self, context):
		active_obj = context.active_object
		target_objs = []
		for obj in context.selected_objects:
			if (obj.type == 'ARMATURE' and active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			for bone in active_obj.pose.bones:
				try:
					target_bone = obj.pose.bones[bone.name]
				except KeyError:
					continue
				consts = target_bone.constraints
				for const in consts[:]:
					consts.remove(const)
				const = consts.new('COPY_TRANSFORMS')
				const.target = active_obj
				const.subtarget = bone.name
		return {'FINISHED'}

class MakeLinkSoftbodySettings(bpy.types.Operator):
	bl_idname = "object.make_link_softbody_settings"
	bl_label = "ソフトボディの設定をリンク"
	bl_description = "アクティブオブジェクトのソフトボディの設定を、他の選択オブジェクトにコピーします"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		for mod in context.object.modifiers:
			if (mod.type == 'SOFT_BODY'):
				break
		else:
			return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		active_softbody = None
		for mod in active_obj.modifiers:
			if (mod.type == 'SOFT_BODY'):
				active_softbody = mod
				break
		target_objs = []
		for obj in context.selected_objects:
			if (active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			target_softbody = None
			for mod in obj.modifiers:
				if (mod.type == 'SOFT_BODY'):
					target_softbody = mod
					break
			else:
				target_softbody = obj.modifiers.new("Softbody", 'SOFT_BODY')
			for name in dir(active_softbody.settings):
				if (name[0] != '_'):
					try:
						value = active_softbody.settings.__getattribute__(name)
						target_softbody.settings.__setattr__(name, value)
					except AttributeError:
						pass
			for name in dir(active_softbody.point_cache):
				if (name[0] != '_'):
					try:
						value = active_softbody.point_cache.__getattribute__(name)
						target_softbody.point_cache.__setattr__(name, value)
					except AttributeError:
						pass
		return {'FINISHED'}

class MakeLinkClothSettings(bpy.types.Operator):
	bl_idname = "object.make_link_cloth_settings"
	bl_label = "クロスの設定をリンク"
	bl_description = "アクティブオブジェクトのクロスシミュレーション設定を、他の選択オブジェクトにコピーします"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		for mod in context.object.modifiers:
			if (mod.type == 'CLOTH'):
				break
		else:
			return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		active_cloth = None
		for mod in active_obj.modifiers:
			if (mod.type == 'CLOTH'):
				active_cloth = mod
				break
		target_objs = []
		for obj in context.selected_objects:
			if (active_obj.name != obj.name):
				target_objs.append(obj)
		for obj in target_objs:
			target_cloth = None
			for mod in obj.modifiers:
				if (mod.type == 'CLOTH'):
					target_cloth = mod
					break
			else:
				target_cloth = obj.modifiers.new("Cloth", 'CLOTH')
			for name in dir(active_cloth.settings):
				if (name[0] != '_'):
					try:
						value = active_cloth.settings.__getattribute__(name)
						target_cloth.settings.__setattr__(name, value)
					except AttributeError:
						pass
			for name in dir(active_cloth.point_cache):
				if (name[0] != '_'):
					try:
						value = active_cloth.point_cache.__getattribute__(name)
						target_cloth.point_cache.__setattr__(name, value)
					except AttributeError:
						pass
		return {'FINISHED'}

######################
# オペレーター(変形) #
######################

class MakeLinkTransform(bpy.types.Operator):
	bl_idname = "object.make_link_transform"
	bl_label = "変形をリンク"
	bl_description = "アクティブオブジェクトの変形情報を、他の選択オブジェクトにコピーします"
	bl_options = {'REGISTER', 'UNDO'}
	
	copy_location = bpy.props.BoolProperty(name="位置", default=True)
	copy_rotation = bpy.props.BoolProperty(name="回転", default=True)
	copy_scale = bpy.props.BoolProperty(name="拡大/縮小", default=True)
	
	@classmethod
	def poll(cls, context):
		if (len(context.selected_objects) < 2):
			return False
		return True
	def execute(self, context):
		active_obj = context.active_object
		for obj in context.selected_objects:
			if (obj.name != active_obj.name):
				if (self.copy_location):
					obj.location = active_obj.location[:]
				if (self.copy_rotation):
					obj.rotation_mode = active_obj.rotation_mode
					if (obj.rotation_mode == 'QUATERNION'):
						obj.rotation_quaternion = active_obj.rotation_quaternion[:]
					elif (obj.rotation_mode == 'AXIS_ANGLE'):
						obj.rotation_axis_angle = active_obj.rotation_axis_angle[:]
					else:
						obj.rotation_euler = active_obj.rotation_euler[:]
				if (self.copy_scale):
					obj.scale = active_obj.scale[:]
		return {'FINISHED'}

################
# サブメニュー #
################

class TransformMenu(bpy.types.Menu):
	bl_idname = "VIEW3D_MT_make_links_transform"
	bl_label = "変形"
	bl_description = "オブジェクトの変形情報をリンクします"
	
	def draw(self, context):
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="トランスフォーム", icon='PLUGIN')
		op.copy_location, op.copy_rotation, op.copy_scale = True, True, True
		self.layout.separator()
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="位置", icon='PLUGIN')
		op.copy_location, op.copy_rotation, op.copy_scale = True, False, False
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="回転", icon='PLUGIN')
		op.copy_location, op.copy_rotation, op.copy_scale = False, True, False
		op = self.layout.operator(MakeLinkTransform.bl_idname, text="拡大/縮小", icon='PLUGIN')
		op.copy_location, op.copy_rotation, op.copy_scale = False, False, True

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
		self.layout.separator()
		self.layout.menu(TransformMenu.bl_idname, icon='PLUGIN')
		self.layout.separator()
		self.layout.operator(MakeLinkObjectName.bl_idname, text="オブジェクト名", icon="PLUGIN")
		self.layout.operator(MakeLinkLayer.bl_idname, text="レイヤー", icon="PLUGIN")
		self.layout.operator(MakeLinkDisplaySetting.bl_idname, text="表示設定", icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(MakeLinkSoftbodySettings.bl_idname, text="ソフトボディ設定", icon="PLUGIN")
		self.layout.operator(MakeLinkClothSettings.bl_idname, text="クロス設定", icon="PLUGIN")
		self.layout.separator()
		self.layout.operator(MakeLinkUVNames.bl_idname, text="空UV", icon="PLUGIN")
		self.layout.operator(MakeLinkArmaturePose.bl_idname, text="アーマチュアの動き", icon="PLUGIN")
	if (context.user_preferences.addons["Scramble Addon"].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]
