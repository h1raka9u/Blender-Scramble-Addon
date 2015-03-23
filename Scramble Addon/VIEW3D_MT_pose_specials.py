# 3Dビュー > ポーズモード > 「W」キー

import bpy
import re

################
# オペレーター #
################

class CreateCustomShape(bpy.types.Operator):
	bl_idname = "pose.create_custom_shape"
	bl_label = "カスタムシェイプを作成"
	bl_description = "選択中のボーンのカスタムシェイプオブジェクトを作成します"
	bl_options = {'REGISTER', 'UNDO'}
	
	name =  bpy.props.StringProperty(name="オブジェクト名", default="カスタムシェイプ用オブジェクト")
	items = [
		("1", "線", "", 1),
		("2", "ひし形", "", 2),
		]
	shape = bpy.props.EnumProperty(items=items, name="形")
	isObjectMode =  bpy.props.BoolProperty(name="完了後オブジェクトモードに", default=True)
	isHide = bpy.props.BoolProperty(name="完了後アーマチュアを隠す", default=True)
	
	def execute(self, context):
		obj = bpy.context.active_object
		if (obj.type == "ARMATURE"):
			if (obj.mode == "POSE"):
				bpy.ops.object.mode_set(mode="OBJECT")
				for bone in obj.data.bones:
					if(bone.select == True):
						bpy.ops.object.select_all(action="DESELECT")
						
						#context.scene.cursor_location = bone.head_local
						bone.show_wire = True
						
						me = bpy.data.meshes.new(self.name)
						if (self.shape == "1"):
							me.from_pydata([(0,0,0), (0,1,0)], [(0,1)], [])
						elif (self.shape == "2"):
							me.from_pydata([(0,0,0), (0,1,0), (0.1,0.5,0), (0,0.5,0.1), (-0.1,0.5,0), (0,0.5,-0.1)], [(0,1), (0,2), (0,3), (0,4), (0,5), (1,2), (1,3), (1,4), (1,5), (2,3), (3,4), (4,5), (5,2)], [])
						me.update()
						meObj = bpy.data.objects.new(me.name, me)
						meObj.data = me
						context.scene.objects.link(meObj)
						meObj.select = True
						context.scene.objects.active = meObj
						
						meObj.draw_type = "WIRE"
						meObj.show_x_ray = True
						bpy.ops.object.constraint_add(type="COPY_TRANSFORMS")
						meObj.constraints[-1].target = obj
						meObj.constraints[-1].subtarget = bone.name
						bpy.ops.object.visual_transform_apply()
						meObj.constraints.remove(meObj.constraints[-1])
						obj.pose.bones[bone.name].custom_shape = meObj
						len = bone.length
						bpy.ops.transform.resize(value=(len, len, len))
				bpy.ops.object.select_all(action="DESELECT")
				obj.select = True
				context.scene.objects.active = obj
				bpy.ops.object.mode_set(mode="POSE")
				if (self.isObjectMode or self.isHide):
					bpy.ops.object.mode_set(mode="OBJECT")
				if (self.isHide):
					obj.hide = True
			else:
				self.report(type={"ERROR"}, message="ポーズモードで実行してください")
				return {'CANCELLED'}
		else:
			self.report(type={"ERROR"}, message="アクティブオブジェクトがアーマチュアではありません")
			return {'CANCELLED'}
		return {'FINISHED'}

class CreateWeightCopyMesh(bpy.types.Operator):
	bl_idname = "pose.create_weight_copy_mesh"
	bl_label = "ウェイトコピー用メッシュを作成"
	bl_description = "選択中のボーンのウェイトコピーで使用するメッシュを作成します"
	bl_options = {'REGISTER', 'UNDO'}
	
	name =  bpy.props.StringProperty(name="作成するオブジェクト名", default="ウェイトコピー用オブジェクト")
	items = [
		("TAIL", "末尾", "", 1),
		("HEAD", "根本", "", 2),
		]
	mode = bpy.props.EnumProperty(items=items, name="ウェイトの位置")
	
	def execute(self, context):
		obj = bpy.context.active_object
		if (obj.type == "ARMATURE"):
			if (obj.mode == "POSE"):
				bpy.ops.object.mode_set(mode="OBJECT")
				bones = []
				for bone in obj.data.bones:
					if(bone.select and not bone.hide):
						bones.append(bone)
				me = bpy.data.meshes.new(self.name)
				verts = []
				edges = []
				for bone in bones:
					co = bone.tail_local
					if (self.mode == "HEAD"):
						co = bone.head_local
					verts.append(co)
					i = 0
					for b in bones:
						if (bone.parent):
							if (bone.parent.name == b.name):
								edges.append((len(verts)-1, i))
								break
						i += 1
				me.from_pydata(verts, edges, [])
				me.update()
				meObj = bpy.data.objects.new(self.name, me)
				meObj.data = me
				context.scene.objects.link(meObj)
				bpy.ops.object.select_all(action="DESELECT")
				meObj.select = True
				context.scene.objects.active = meObj
				
				i = 0
				for bone in bones:
					meObj.vertex_groups.new(bone.name)
					meObj.vertex_groups[bone.name].add([i], 1.0, "REPLACE")
					i += 1
				
				#bpy.ops.object.mode_set(mode="EDIT")
				#bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.01)})
				#bpy.ops.object.mode_set(mode="OBJECT")
			else:
				self.report(type={"ERROR"}, message="ポーズモードで実行してください")
				return {'CANCELLED'}
		else:
			self.report(type={"ERROR"}, message="アクティブオブジェクトがアーマチュアではありません")
			return {'CANCELLED'}
		return {'FINISHED'}

class CopyBoneName(bpy.types.Operator):
	bl_idname = "pose.copy_bone_name"
	bl_label = "ボーン名をクリップボードにコピー"
	bl_description = "アクティブボーンの名前をクリップボードにコピーします"
	bl_options = {'REGISTER', 'UNDO'}
	
	isObject = bpy.props.BoolProperty(name="オブジェクト名も", default=False)
	
	def execute(self, context):
		if (self.isObject):
			context.window_manager.clipboard = context.active_object.name + ":" + context.active_pose_bone.name
		else:
			context.window_manager.clipboard = context.active_pose_bone.name
		return {'FINISHED'}

class SplineGreasePencil(bpy.types.Operator):
	bl_idname = "pose.spline_grease_pencil"
	bl_label = "チェーン状ボーンをグリースペンシルに沿わせる"
	bl_description = "チェーンの様に繋がった選択ボーンをグリースペンシルに沿わせてポーズを付けます"
	bl_options = {'REGISTER', 'UNDO'}
	
	isRootReset = bpy.props.BoolProperty(name="根本を元の位置に", default=False)
	
	def execute(self, context):
		activeObj = context.active_object
		i = 0
		for bone in context.selected_pose_bones:
			for bone2 in context.selected_pose_bones:
				if (bone.parent):
					if (bone.parent.name == bone2.name):
						i += 1
						break
		if (i+1 < len(context.selected_pose_bones)):
			self.report(type={"ERROR"}, message="チェーン状に繋がったボーン群を選択して実行して下さい")
			return {'CANCELLED'}
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.gpencil.convert(type='CURVE', use_timing_data=True)
		for obj in context.selectable_objects:
			if ("GP_Layer" in obj.name):
				curveObj = obj
		bpy.ops.object.mode_set(mode='POSE')
		tails = []
		for bone in context.selected_pose_bones:
			if (len(bone.children) == 0):
				const = bone.constraints.new("SPLINE_IK")
				const.target = curveObj
				const.use_curve_radius = False
				const.use_y_stretch = False
				const.chain_count = len(context.selected_pose_bones)
				tails.append((bone, const))
			for child in bone.children:
				for bone2 in context.selected_pose_bones:
					if (child.name == bone2.name):
						break
				else:
					const = bone.constraints.new("SPLINE_IK")
					const.target = curveObj
					const.use_curve_radius = False
					const.use_y_stretch = False
					const.chain_count = len(context.selected_pose_bones)
					tails.append((bone, const))
					break
		bpy.ops.pose.visual_transform_apply()
		for bone, const in tails:
			bone.constraints.remove(const)
		bpy.ops.pose.scale_clear()
		context.scene.objects.unlink(curveObj)
		if (self.isRootReset):
			bpy.ops.pose.loc_clear()
		return {'FINISHED'}

class RenameBoneRegularExpression(bpy.types.Operator):
	bl_idname = "pose.rename_bone_regular_expression"
	bl_label = "ボーン名を正規表現で置換"
	bl_description = "(選択中の)ボーン名を正規表現に一致する部分で置換します"
	bl_options = {'REGISTER', 'UNDO'}
	
	isAll = bpy.props.BoolProperty(name="非選択も含め全て", default=False)
	pattern = bpy.props.StringProperty(name="置換前(正規表現)", default="^")
	repl = bpy.props.StringProperty(name="置換後", default="@")
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "ARMATURE"):
			if (obj.mode == "POSE"):
				bones = context.selected_pose_bones
				if (self.isAll):
					bones = obj.pose.bones
				for bone in bones:
					bone.name = re.sub(self.pattern, self.repl, bone.name)
			else:
				self.report(type={"ERROR"}, message="ポーズモードで実行してください")
				return {'CANCELLED'}
		else:
			self.report(type={"ERROR"}, message="アーマチュアオブジェクトではありません")
			return {'CANCELLED'}
		return {'FINISHED'}

class SetSlowParentBone(bpy.types.Operator):
	bl_idname = "pose.set_slow_parent_bone"
	bl_label = "スローペアレントを設定"
	bl_description = "選択中のボーンにスローペアレントを設定します"
	bl_options = {'REGISTER', 'UNDO'}
	
	items = [
		('DAMPED_TRACK', "減衰トラック", "", 1),
		('IK', "IK", "", 2),
		('STRETCH_TO', "ストレッチ", "", 3),
		('COPY_LOCATION', "位置コピー", "", 4),
		]
	constraint = bpy.props.EnumProperty(items=items, name="コンストレイント")
	radius = bpy.props.FloatProperty(name="エンプティの大きさ", default=0.5, min=0.01, max=10, soft_min=0.01, soft_max=10, step=10, precision=3)
	slow_parent_offset = bpy.props.FloatProperty(name="スローペアレントの強度", default=5, min=0, max=100, soft_min=0, soft_max=100, step=50, precision=3)
	is_use_driver = bpy.props.BoolProperty(name="ボーンにドライバを追加", default=True)
	
	def execute(self, context):
		pre_cursor_location = context.space_data.cursor_location[:]
		pre_active_pose_bone = context.active_pose_bone
		obj = context.active_object
		arm = obj.data
		bones = context.selected_pose_bones[:]
		for bone in bones:
			if (not bone.parent):
				self.report(type={'WARNING'}, message="ボーン「"+bone.name+"」には親がありません、スルーします")
				continue
			if (self.constraint == 'COPY_LOCATION'):
				context.space_data.cursor_location = obj.matrix_world * arm.bones[bone.name].head_local
			else:
				context.space_data.cursor_location = obj.matrix_world * arm.bones[bone.name].tail_local
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.empty_add(type='PLAIN_AXES', radius=self.radius)
			empty_obj = context.active_object
			empty_obj.name = bone.name+" slow parent"
			obj.select = True
			context.scene.objects.active = obj
			bpy.ops.object.mode_set(mode='POSE')
			pre_parent_select = arm.bones[bone.parent.name].select
			arm.bones.active = arm.bones[bone.parent.name]
			bpy.ops.object.parent_set(type='BONE')
			arm.bones[bone.parent.name].select = pre_parent_select
			arm.bones.active = arm.bones[bone.name]
			empty_obj.use_slow_parent = True
			empty_obj.slow_parent_offset = self.slow_parent_offset
			const = bone.constraints.new(self.constraint)
			const.target = empty_obj
			if (self.constraint == 'IK'):
				const.chain_count = 1
			empty_obj.select = False
			if (self.is_use_driver):
				bone["SlowParentOffset"] = self.slow_parent_offset
				fcurve = empty_obj.driver_add('slow_parent_offset')
				fcurve.driver.type = 'AVERAGE'
				variable = fcurve.driver.variables.new()
				variable.targets[0].id = obj
				variable.targets[0].data_path = 'pose.bones["'+bone.name+'"]["SlowParentOffset"]'
		arm.bones.active = arm.bones[pre_active_pose_bone.name]
		context.space_data.cursor_location = pre_cursor_location[:]
		return {'FINISHED'}

class RenameBoneNameEnd(bpy.types.Operator):
	bl_idname = "pose.rename_bone_name_end"
	bl_label = "ボーン名の ○.R => ○_R を相互変換"
	bl_description = "ボーン名の ○.R => ○_R を相互変換します"
	bl_options = {'REGISTER', 'UNDO'}
	
	reverse = bpy.props.BoolProperty(name="○.R => ○_R", default=False)
	
	def execute(self, context):
		if (not context.selected_pose_bones):
			self.report(type={"ERROR"}, message="ポーズモードでボーンを選択して実行して下さい")
			return {"CANCELLED"}
		rename_count = 0
		for bone in context.selected_pose_bones:
			pre_name = bone.name
			if (not self.reverse):
				bone.name = re.sub(r'_L$', '.L', bone.name)
				bone.name = re.sub(r'_l$', '.l', bone.name)
				if (pre_name != bone.name):
					continue
				bone.name = re.sub(r'_R$', '.R', bone.name)
				bone.name = re.sub(r'_r$', '.r', bone.name)
			else:
				bone.name = re.sub(r'\.L$', '_L', bone.name)
				bone.name = re.sub(r'\.l$', '_l', bone.name)
				if (pre_name != bone.name):
					continue
				bone.name = re.sub(r'\.R$', '_R', bone.name)
				bone.name = re.sub(r'\.r$', '_r', bone.name)
			if (pre_name != bone.name):
				rename_count += 1
		for area in context.screen.areas:
			area.tag_redraw()
		self.report(type={"INFO"}, message="ボーン名の変換が終了しました、"+str(rename_count)+"個変換しました")
		return {'FINISHED'}

class RenameBoneNameEndJapanese(bpy.types.Operator):
	bl_idname = "pose.rename_bone_name_end_japanese"
	bl_label = "ボーン名の ○.R => 右○ を相互変換"
	bl_description = "ボーン名の ○.R => 右○ を相互変換します"
	bl_options = {'REGISTER', 'UNDO'}
	
	reverse = bpy.props.BoolProperty(name="○.R => 右○", default=False)
	
	def execute(self, context):
		if (not context.selected_pose_bones):
			self.report(type={"ERROR"}, message="ポーズモードでボーンを選択して実行して下さい")
			return {"CANCELLED"}
		rename_count = 0
		for bone in context.selected_pose_bones:
			pre_name = bone.name
			if (not self.reverse):
				if (re.search(r"[\._][rR]$", bone.name)):
					bone.name = "右" + bone.name[:-2]
				if (re.search(r"[\._][lL]$", bone.name)):
					bone.name = "左" + bone.name[:-2]
			else:
				if (re.search(r"^右", bone.name)):
					bone.name = bone.name[1:] + "_R"
				if (re.search(r"^左", bone.name)):
					bone.name = bone.name[1:] + "_L"
			if (pre_name != bone.name):
				rename_count += 1
		for area in context.screen.areas:
			area.tag_redraw()
		self.report(type={"INFO"}, message="ボーン名の変換が終了しました、"+str(rename_count)+"個変換しました")
		return {'FINISHED'}

################
# メニュー追加 #
################

# メニューを登録する関数
def menu(self, context):
	self.layout.separator()
	self.layout.operator(CopyBoneName.bl_idname, icon="PLUGIN")
	self.layout.operator(RenameBoneRegularExpression.bl_idname, icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(RenameBoneNameEnd.bl_idname, text="ボーン名置換「XXX_R => XXX.R」", icon="PLUGIN").reverse = False
	self.layout.operator(RenameBoneNameEnd.bl_idname, text="ボーン名置換「XXX.R => XXX_R」", icon="PLUGIN").reverse = True
	self.layout.separator()
	self.layout.operator(RenameBoneNameEndJapanese.bl_idname, text="ボーン名置換「XXX_R => 右XXX」", icon="PLUGIN").reverse = False
	self.layout.operator(RenameBoneNameEndJapanese.bl_idname, text="ボーン名置換「右XXX => XXX_R」", icon="PLUGIN").reverse = True
	self.layout.separator()
	self.layout.prop_menu_enum(context.object.data, "pose_position", icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(CreateCustomShape.bl_idname, icon="PLUGIN")
	self.layout.operator(CreateWeightCopyMesh.bl_idname, icon="PLUGIN")
	self.layout.operator(SetSlowParentBone.bl_idname, icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(SplineGreasePencil.bl_idname, icon="PLUGIN")
