import bpy
import random


if __name__ == '__main__':
    X_SPACING = 2.1
    Y_SPACING = 2.1

    for x in range(10):
        for y in range(8):
            if x == 0 and y == 0:
                continue
            panelka = bpy.data.objects['panelka'].copy()
            bpy.context.collection.objects.link(panelka)

            panelka.location.x += x * X_SPACING
            panelka.location.y += y * Y_SPACING
            panelka.location.z += random.random()
            panelka.rotation_euler.z += 3.14 * random.random()
            panelka.rotation_euler.x += 3.14 * random.random()
            panelka.rotation_euler.y += 3.14 * random.random()

