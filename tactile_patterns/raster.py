import numpy as np
from scipy.ndimage.interpolation import zoom
import math
from PIL import Image


def squared_distance_between_points(point_a, point_b):
    delta_x = point_a[0] - point_b[0]
    delta_y = point_a[1] - point_b[1]
    return delta_x * delta_x + delta_y * delta_y

def squared_distance_from_center(x, y):
    x = x % 200
    y = y % 200
    center_x = 120
    center_y = 120
    return squared_distance_between_points((x, y), (center_x, center_y))

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


def pedestrian_crossing_smooth_gradient():
    ####################
    # basic shape
    # X - full white (total_crossing_area)
    # empty space - black (none_crossing_area)
    # . - smooth corner
    # * - smooth gradient
    #
    #         .....****
    #         .....XXXX
    #         .....XXXX
    #         *XXXXXXXX
    #         *XXXXXXXX
    #         *XXXXXXXX
    #         *XXXXXXXX
    #
    # for now x are rescaled to use this repeating pattern, y not
    width = crossing_subpattern_width() * 8
    height = crossing_height() + crossing_margin()*2

    # https://pillow.readthedocs.io/en/latest/reference/Image.html
    white_pixels = []
    for x in range(0, width):
        for y in range(0, height):
            remapped_x = rescale_x_for_crossing(x)
            if remapped_x != x:
                break # started repeating
            if is_in_total_crossing_area(remapped_x, y):
                white_pixels.append((x, y))

    im = Image.new("RGB", (width, height), (255, 0, 0))
    pixels = im.load()
    for x in range(0, width):
        for y in range(0, height):
            remapped_x = rescale_x_for_crossing(x)
            value = 0
            if is_in_total_crossing_area(remapped_x, y):
                value = 255
            elif remapped_x > none_area_subpattern_width():
                distance_from_nearest_white = squared_distance_between_points((remapped_x, y), white_pixels[0])
                for white_point in white_pixels:
                    distance = squared_distance_between_points((remapped_x, y), white_point)
                    if distance_from_nearest_white > distance:
                        distance_from_nearest_white = distance
                value = scaling_distance_from_white_to_value_for_crossings(distance_from_nearest_white)
            pixels[x, y] = (value, value, value)
    return im
    # im.save("generated.png")
    # im.show()

def scaling_distance_from_white_to_value_for_crossings(distance):
    # plan: 
    # (1) smooth lowering on edge
    # (2) vertical cliff
    # (3) smooth at base
    cliff_height_portion = 0.5
    height_portion_for_each_lowering = (1 - cliff_height_portion)/2
    if distance < gradual_ramp_width()/2:
        part_of_lowering = 1.0 * distance / gradual_ramp_width()
        return int(255 * (1 - part_of_lowering * height_portion_for_each_lowering))
    else:
        distance = distance - gradual_ramp_width()/2
        part_of_lowering = 1.0 * distance / gradual_ramp_width()
        return int(255 * (1 - cliff_height_portion - part_of_lowering * height_portion_for_each_lowering))

def rescale_x_for_crossing(x):
    # in examples crossing_subpattern_width() == 4 is used
    # desired pattern in form of
    # 0 1 2 3 2 1 0
    # is wanted

    # input
    # 0 1 2 3 4 5 6 7 8 9

    scaled_x = x % (crossing_subpattern_width()*2)
    # after that:
    # 0 1 2 3 4 5 6 7 0 1

    if scaled_x > crossing_subpattern_width():
        delta = scaled_x - crossing_subpattern_width()
        scaled_x = crossing_subpattern_width() - delta
    # after that:
    # 0 1 2 3 4 3 2 1 0 1
    return scaled_x

def crossing_subpattern_width():
    # basic shape is mirrored - horizontally and vertically
    return 38

def gradual_ramp_width():
    return 14

def none_area_subpattern_width():
    return crossing_subpattern_width() - total_white_crossing_bar_width_in_subpattern() - gradual_ramp_width()

def total_white_crossing_bar_width_in_subpattern():
    return 16

def crossing_height():
    return 150

def crossing_margin():
    return 10

def is_in_total_crossing_area(remapped_x, y):
    if y < crossing_margin() + gradual_ramp_width():
        return False
    if y > crossing_margin() + crossing_height() - gradual_ramp_width():
        return False
    if remapped_x % (crossing_subpattern_width() + 1) > (crossing_subpattern_width() - total_white_crossing_bar_width_in_subpattern()):
        return True
    return False

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
