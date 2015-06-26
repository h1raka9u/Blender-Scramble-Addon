# 「3Dビュー」エリア > プロパティ > レイヤーボタンがあるパネル

import bpy

################
# オペレーター #
################

class GroupLayers(bpy.types.Operator):
	bl_idname = "object.group_layers"
	bl_label = "グループで表示/非表示を切り替え"
	bl_description = "所属しているグループで表示/非表示を切り替えます"
	bl_options = {'REGISTER', 'UNDO'}
	
	group = bpy.props.StringProperty(name="グループ名")
	
	def execute(self, context):
		for obj in bpy.data.objects:
			for l1 in obj.layers:
				for l2 in context.scene.layers:
					if (l1 and l2):
						if (self.group != ""):
							for group in obj.users_group:
								if (group.name == self.group):
									obj.hide = False
									break
							else:
								obj.hide = True
						else:
							if (len(obj.users_group) == 0):
								obj.hide = False
							else:
								obj.hide = True
		return {'FINISHED'}

##########
# パネル #
##########

class ObjectSelectPanel(bpy.types.Panel):
	bl_idname = "VIEW3D_PT_layers"
	bl_label = " "
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_options = {'DEFAULT_CLOSED'}
	
	@classmethod
	def poll(cls, context):
		return (context.object is not None)
	
	def draw_header(self, context):
		row = self.layout.row()
		row.scale_x=0.7
		row.scale_y=0.7
		row.prop(context.scene, 'layers', text="")
	
	def draw(self, context):
		self.layout.label(text="グループでレイヤー")
		objs = []
		for obj in bpy.data.objects:
			for i in range(len(obj.layers)):
				if (obj.layers[i] and context.scene.layers[i]):
					objs.append(obj)
		groups = []
		for obj in objs:
			for group in obj.users_group:
				if (not group in groups):
					groups.append(group)
		col = self.layout.column(align=True)
		col.operator('object.hide_view_clear', text="全て表示", icon='PLUGIN')
		col.operator(GroupLayers.bl_idname, text="無所属を表示", icon='PLUGIN').group = ''
		self.layout.separator()
		col = self.layout.column(align=True)
		for group in groups:
			col.operator(GroupLayers.bl_idname, text=group.name, icon='PLUGIN').group = group.name

################
# メニュー追加 #
################

# メニューを登録する関数
def menu(self, context):
	pass