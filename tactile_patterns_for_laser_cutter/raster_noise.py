import numpy as np
from scipy.ndimage.interpolation import zoom
from PIL import Image


generated_noise_areas = 100
noise_scaling = 10
size = generated_noise_areas * noise_scaling
# higher noise_scaling will make noise more gradual, zooming into genrated noise pattern
arr = np.random.uniform(size=(generated_noise_areas, generated_noise_areas))
arr = zoom(arr, noise_scaling)

width = size
height = size
# https://pillow.readthedocs.io/en/latest/reference/Image.html
im = Image.new("RGB", (width, height), (255, 0, 0))
pixels = im.load()
for x in range(0, width):
    for y in range(0, height):
        value = int(255*arr[x, y])
        pixels[x, y] = (value, value, value)
im.save("generated.png")
im.show()
