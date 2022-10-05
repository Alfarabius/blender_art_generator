import bpy
import random
from const import SPACING


class GenerativeArtAPI:
	"""
	A class for create generative art
	"""
	SHAPES_ADD = {
		'CUBE': bpy.ops.mesh.primitive_cube_add,
		'SPHERE': bpy.ops.mesh.primitive_uv_sphere_add,
		'CYLINDER': bpy.ops.mesh.primitive_cylinder_add,
		'CONE': bpy.ops.mesh.primitive_cone_add
	}

	def __init__(self):
		...

	def create_objects_poll(self, shapes: list[str, ...], amount: int) -> list:
		c = len(shapes) if len(shapes) < amount else amount
		poll = [self.create_object(shapes[i]) for i in range(c)]
		return poll

	def create_materials_poll(self, colors: list[tuple, ...], amount: int) -> list:
		c = len(colors) if len(colors) < amount else amount
		poll = [self.create_material(colors[i]) for i in range(c)]
		return poll

	def generate_art(self, magic_number: int):
		bpy.context.scene.render.engine = 'CYCLES'

		world = bpy.data.worlds["World"]
		world.node_tree.nodes["Background"].inputs[0].default_value = (0.787399, 0.176258, 0.0824194, 1)

		magic = magic_number if magic_number > 20 else random.randint(1, 21)

		colors = [tuple(random.random() for _ in range(4)) for _ in range(magic)]
		shapes = [random.choice(list(self.SHAPES_ADD))] * magic

		objects = self.create_objects_poll(shapes, magic)
		materials = self.create_materials_poll(colors, magic)

		for obj in objects:
			obj.data.materials.append(random.choice(materials))

		is_eagle = random.random() > 0.5

		for x in range(30):
			for y in range(30):
				new_obj = random.choice(objects).copy()
				bpy.context.collection.objects.link(new_obj)

				if is_eagle:
					new_obj.modifiers.new('Bevel', 'BEVEL')

				new_obj.location.x += x * SPACING
				new_obj.location.y += y * SPACING
				new_obj.location.z += random.random()

		bpy.ops.object.camera_add(
			enter_editmode=False,
			align='VIEW',
			location=(88.0, 2.5, 24.0),
			rotation=(1.10871, 0.0132652, 1.14827),
			scale=(1, 1, 1)
		)

		bpy.ops.object.light_add(
			type='SUN',
			align='WORLD',
			location=(0, 0, 0.47),
			rotation=(0.65, 0.8, -0.45),
			scale=(1, 1, 1)
		)

	def create_object(self, shape: str) -> 'bpy_types.Object':
		try:
			self.SHAPES_ADD[shape]()
		except KeyError:
			raise SystemExit(f'Wrong shape name! Allowed names: {self.SHAPES_ADD}')

		bpy.context.object.scale.z *= random.randint(1, 5)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		mesh = bpy.context.object.data
		for f in mesh.polygons:
			f.use_smooth = True

		bpy.context.object.data.use_auto_smooth = True

		obj = bpy.context.object.copy()
		bpy.data.objects.remove(bpy.context.object, do_unlink=True)

		return obj

	def create_material(self, color=(0.8, 0.8, 0.8, 1), surface='Principled BSDF') -> list:
		self.SHAPES_ADD['CUBE']()
		bpy.ops.material.new()
		new_material = bpy.data.materials[-1]
		new_material.node_tree.nodes[surface].inputs[0].default_value = color
		bpy.data.objects.remove(bpy.context.object, do_unlink=True)

		return new_material
