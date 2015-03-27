# 情報 > 「ファイル」メニュー > 「外部データ」メニュー

import bpy
import os

################
# オペレーター #
################

class ReloadAllImage(bpy.types.Operator):
	bl_idname = "image.reload_all_image"
	bl_label = "全ての画像を再読み込み"
	bl_description = "外部ファイルを参照している画像データを全て読み込み直します"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		for img in bpy.data.images:
			if (img.filepath != ""):
				img.reload()
				try:
					img.update()
				except RuntimeError:
					pass
		for area in context.screen.areas:
			area.tag_redraw()
		return {'FINISHED'}

class ResaveAllImage(bpy.types.Operator):
	bl_idname = "image.resave_all_image"
	bl_label = "全ての画像をフォルダに保存し直す"
	bl_description = "外部ファイルを参照している画像データを全て指定フォルダに保存し直します"
	bl_options = {'REGISTER'}
	
	folder_name = bpy.props.StringProperty(name="フォルダ名", default="textures")
	is_relative = bpy.props.BoolProperty(name="相対パス", default=True)
	
	def execute(self, context):
		if (context.blend_data.filepath == ""):
			self.report(type={"ERROR"}, message="blendファイルを保存してから実行して下さい")
			return {'CANCELLED'}
		img_dir = os.path.join( os.path.dirname(context.blend_data.filepath), self.folder_name )
		try:
			os.mkdir(img_dir)
		except FileExistsError:
			self.report(type={"ERROR"}, message="既にそのフォルダが存在します")
			return {'CANCELLED'}
		if (self.is_relative):
			img_dir = '//' + self.folder_name
		for img in context.blend_data.images:
			print(img.filepath, img. filepath_raw)
			if (img.filepath_raw != ""):
				img.filepath_raw = os.path.join( img_dir, bpy.path.basename(img.filepath_raw) )
				img.save()
			print(img.filepath, img. filepath_raw)
		return {'FINISHED'}
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

################
# メニュー追加 #
################

# メニューを登録する関数
def menu(self, context):
	self.layout.separator()
	self.layout.operator(ReloadAllImage.bl_idname, icon="PLUGIN")
	self.layout.operator(ResaveAllImage.bl_idname, icon="PLUGIN")
