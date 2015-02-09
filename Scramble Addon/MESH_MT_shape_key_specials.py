# プロパティ > 「オブジェクトデータ」タブ > シェイプキー一覧右の▼

import bpy

################
# オペレーター #
################

class CopyShape(bpy.types.Operator):
	bl_idname = "mesh.copy_shape"
	bl_label = "シェイプキーを複製"
	bl_description = "アクティブなシェイプキーを複製します"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			me = obj.data
			keys = {}
			for key in me.shape_keys.key_blocks:
				keys[key.name] = key.value
				key.value = 0
			obj.active_shape_key.value = 1
			obj.shape_key_add(name=obj.active_shape_key.name, from_mix=True)
			obj.active_shape_key_index = len(me.shape_keys.key_blocks) - 1
			for k, v in keys.items():
				me.shape_keys.key_blocks[k].value = v
		return {'FINISHED'}

class ShowShapeBlockName(bpy.types.Operator):
	bl_idname = "mesh.show_shape_block_name"
	bl_label = "シェイプブロック名を調べる"
	bl_description = "シェイプブロックの名前を表示する為だけに作られたオペレーターです"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if (obj.type == "MESH"):
			shape_keys = obj.data.shape_keys
			if (shape_keys != None):
				self.report(type={"INFO"}, message="シェイプキーブロップ名は「"+shape_keys.name+"」です")
			else:
				self.report(type={"ERROR"}, message="シェイプキーが存在しません")
		else:
			self.report(type={"ERROR"}, message="メッシュオブジェクトではありません")
		return {'FINISHED'}

class RenameShapeBlockName(bpy.types.Operator):
	bl_idname = "mesh.rename_shape_block_name"
	bl_label = "シェイプブロックの名前をオブジェクト名に"
	bl_description = "シェイプブロックの名前をオブジェクト名と同じにします"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		me = obj.data
		me.shape_keys.name = obj.name
		return {'FINISHED'}

class InsertKeyframeAllShapes(bpy.types.Operator):
	bl_idname = "mesh.insert_keyframe_all_shapes"
	bl_label = "全てのシェイプにキーフレームを打つ"
	bl_description = "現在のフレームに、全てのシェイプのキーフレームを挿入します"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		for shape in context.active_object.data.shape_keys.key_blocks:
		    shape.keyframe_insert(data_path="value")
		return {'FINISHED'}

################
# メニュー追加 #
################

# メニューを登録する関数
def menu(self, context):
	self.layout.separator()
	self.layout.operator(CopyShape.bl_idname, icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(InsertKeyframeAllShapes.bl_idname, icon="PLUGIN")
	self.layout.separator()
	self.layout.operator(ShowShapeBlockName.bl_idname, icon="PLUGIN")
	self.layout.operator(RenameShapeBlockName.bl_idname, icon="PLUGIN")
