import tactile_patterns.vector as vector
import tactile_patterns.raster as raster
from tactile_patterns.data_format import pretty_geojson_string
from tactile_patterns.data_format import get_recommended_scaling
from tactile_patterns.data_format import projection_code
from tactile_patterns.data_format import Rescale
import os
from PIL import Image


def main():
    generate_vector_pattern(vector.lone_squares_pattern(30, 30), "lone_squares")
    generate_vector_pattern(vector.maze_under_construction_pattern(30, 30), "under_construction_maze")

    image_raster = raster.simple_gradient()
    image_raster.save("simple_gradient.png")

    image_raster = raster.circle_bumps_regular_pattern()
    image_raster.save("circle_bumps_regular_pattern.png")

    image_raster = raster.irregullar_differently_shaped_islands(random_seed=784234)
    image_raster.save("irregullar_differently_shaped_islands.png")


def generate_vector_pattern(pattern, name):
    lat = 50.05518
    lon = 19.92757
    base_scaling = 0.000001
    projection_scale = get_recommended_scaling(lat, lon, projection_code("web mercator"))
    scale_lat = projection_scale['scale_lat'] * base_scaling
    scale_lon = projection_scale['scale_lon'] * base_scaling
    pattern.rescale(Rescale(multiply_lat=scale_lat, multiply_lon=scale_lon, add_lon=lon, add_lat=lat))
    filepath = name + ".geojson"
    with open(filepath, "w") as myfile:
        myfile.write(pretty_geojson_string(pattern.to_geojson()))
    os.system("svgis draw '" + filepath + "' --crs " + projection_code("web mercator") +
              " --style '* {stroke: none; fill: #00f}' -o '" + name + ".svg'")


main()
