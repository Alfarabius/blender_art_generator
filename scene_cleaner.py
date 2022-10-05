import bpy


class SceneCleaner:
	"""
	A class to clean up on scene.

	Call SceneCleaner()() or SceneCleaner().clean_scene() to all of the objects,
	collection, materials, particles, textures, images, curves, meshes, actions,
	nodes, and worlds from the scene.

	You can also call clean_<something> methods to remove <something> individually.

	Based on https://github.com/CGArtPython/bpy_building_blocks_examples
	"""
	WORLD_NAME = 'World'
	CANCELLED_STATUS = 'CANCELLED'

	def __init__(self):
		self.objects = bpy.data.objects
		self.collections = bpy.data.collections
		self.worlds = bpy.data.worlds

	def clean_scene(self):
		self.clean_objects()
		self.clean_collections()
		self.clean_worlds()

		self._purge_orphans(self.CANCELLED_STATUS)

	def clean_objects(self):
		if bpy.context.active_object and bpy.context.active_object.mode != "OBJECT":
			bpy.ops.object.mode_set(mode='OBJECT')

		for obj in self.objects:
			obj.hide_set(False)
			obj.hide_select = False
			obj.hide_viewport = False

		bpy.ops.object.select_all(action="SELECT")
		bpy.ops.object.delete()

		self.objects = bpy.data.objects

	def clean_collections(self):
		self._remover(self.collections)
		self.collections = bpy.data.collections

	def clean_worlds(self):
		self._remover(self.worlds)
		self._create_world(self.WORLD_NAME)
		self.worlds = bpy.data.worlds

	def clean_orphans(self):
		self._purge_orphans(self.CANCELLED_STATUS)

	def __call__(self):
		self.clean_scene()

	@staticmethod
	def _create_world(world_name):
		bpy.ops.world.new()
		bpy.context.scene.world = bpy.data.worlds[world_name]

	@staticmethod
	def _remover(container):
		for element in container:
			container.remove(element)

	@staticmethod
	def _purge_orphans(cancelled_status):
		if bpy.app.version >= (3, 0, 0):
			bpy.ops.outliner.orphans_purge(
				do_local_ids=True, do_linked_ids=True, do_recursive=True
			)
			return
		while bpy.ops.outliner.orphans_purge() != cancelled_status:
			pass
