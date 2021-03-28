import numpy as np
from scipy.ndimage.interpolation import zoom
import math
from PIL import Image


def squared_distance_from_center(x, y):
    x = x % 200
    y = y % 200
    center_x = 120
    center_y = 120
    delta_x = x - center_x
    delta_y = y - center_y
    return delta_x * delta_x + delta_y * delta_y

#########################################################################


def simple_gradient():
    multiplier = 3
    width = 255 * multiplier
    height = 100

    # https://pillow.readthedocs.io/en/latest/reference/Image.html
    im = Image.new("RGB", (width, height), (255, 0, 0))
    pixels = im.load()
    for x in range(0, width):
        for y in range(0, height):
            value = int(255.0 * x / width)
            pixels[x, y] = (value, value, value)
    return im
    # im.save("generated.png")
    # im.show()

#########################################################################


def squared_distance_from_circle_to_value_for_circle_bumps_regular_pattern(squared_distance):
    scaled_distance = math.sqrt(squared_distance) * 3
    scaled = 255 - scaled_distance
    if scaled < 0:
        return 0
    return int(scaled*1.4)


def value_for_location_for_circle_bumps_regular_pattern(x, y):
    squared_distance = squared_distance_from_center(x, y)
    return squared_distance_from_circle_to_value_for_circle_bumps_regular_pattern(squared_distance)


def circle_bumps_regular_pattern():
    size = 1400
    width = size
    height = size

    # https://pillow.readthedocs.io/en/latest/reference/Image.html
    im = Image.new("RGB", (width, height), (255, 0, 0))
    pixels = im.load()
    for x in range(0, width):
        for y in range(0, height):
            value = value_for_location_for_circle_bumps_regular_pattern(x, y)
            pixels[x, y] = (value, value, value)
    return im
    # im.save("generated.png")
    # im.show()

#########################################################################


def irregullar_differently_shaped_islands(random_seed=None):
    generated_noise_areas = 100
    noise_area_size = 10
    value_scaling = 1
    value_scaling = 0.7
    if random_seed != None:
        np.random.seed(random_seed)
    arr = np.random.standard_normal(size=(generated_noise_areas, generated_noise_areas))

    size = generated_noise_areas * noise_area_size
    width = size
    height = size

    arr = zoom(arr, noise_area_size)

    # https://pillow.readthedocs.io/en/latest/reference/Image.html
    im = Image.new("RGB", (width, height), (255, 0, 0))
    pixels = im.load()
    for x in range(0, width):
        for y in range(0, height):
            value = int(255*arr[x, y]*value_scaling)
            pixels[x, y] = (value, value, value)
    return im
    # im.save("generated.png")
    # im.show()

# other considered:
# higher noise_scaling will make noise more gradual, zooming into genrated noise pattern

# lack of proper islands
#arr = np.random.uniform(size=(generated_noise_areas, generated_noise_areas))
#arr = np.random.triangular(0, 0.5, 1, size=(generated_noise_areas, generated_noise_areas))

# lack of proper islands + required divsion by 2
#arr = np.random.weibull(1.5, size=(generated_noise_areas, generated_noise_areas))

# has outliers, as expected
#arr = np.random.wald(0.3, 1, size=(generated_noise_areas, generated_noise_areas))

# has heavy outliers
#arr = np.random.standard_gamma(0.1, size=(generated_noise_areas, generated_noise_areas))

# nice islands but with ouliers, scaling bu 0.5 recommended
# arr = np.random.standard_t(3, size=(generated_noise_areas, generated_noise_areas))

# overexposed, heavy outliers with /3 division
#arr = np.random.standard_exponential(size=(generated_noise_areas, generated_noise_areas))

# overexposed heavily
#arr = np.random.standard_cauchy(size=(generated_noise_areas, generated_noise_areas))

# overexposed
#value_scaling = 0.5
#arr = np.random.chisquare(0.6, size=(generated_noise_areas, generated_noise_areas))

# NOT TOO GOOD
#generated_noise_areas = 100
#noise_area_size = 15
#value_scaling = 0.10
#arr = np.random.noncentral_chisquare(3, .00001, size=(generated_noise_areas, generated_noise_areas))

#generated_noise_areas = 125
#noise_area_size = 25
#value_scaling = 1
#arr = np.random.rayleigh(0.4, size=(generated_noise_areas, generated_noise_areas))

# forms proper islands but sometimes pretty big voids
#arr = np.random.vonmises(0, 4, size=(generated_noise_areas, generated_noise_areas))

# nice islands
