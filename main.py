import matplotlib
import matplotlib.pyplot as plt

import numpy as np

import meshio

BW_THRESHOLD = .53

image_path = 'images/smiley.png'

image = plt.imread(image_path)

# Make black and white
image = image.mean(axis=2)
print(image)

# Make image binary
image = np.where(image > BW_THRESHOLD, 1., 0.)

# Show image
plt.imsave('output.png', image, cmap='gray')

light_offset = (image.shape[0], image.shape[0])


points = []

for y in range(image.shape[0]):
    points.append((0., y, 0.))
    i = 0
    while i < image.shape[1]:
        whites = 0
        while i + whites < image.shape[1] and image[y, i + whites] > .5:
            whites += 1

        blacks = 0
        while i + whites + blacks < image.shape[1] and image[y, i + whites + blacks] <= .5:
            blacks += 1

        h = float(light_offset[1] * blacks / (light_offset[0] + whites + blacks + i))

        points.append((float(i + whites), y, h))
        points.append((float(i + whites + blacks), y, 0))
        i += whites + blacks

print(points)


# Generate 3D object

obj_points: list[list[float]] = []
obj_quads: list[list[float]] = []

for p in points:
    obj_points.append([p[0], p[2], p[1]])
    obj_points.append([p[0], p[2], p[1] + 1.])

for i in range(0, len(obj_points) - 2, 2):
    obj_quads.append([i, i+1, i+3, i+2])

print(obj_points)
print(obj_quads)

mesh = meshio.Mesh(
    obj_points,
    [("quad", obj_quads)]
)

mesh.write("output.obj")

