from tactile_patterns.data_format import Rescale
from tactile_patterns.data_format import Point
from tactile_patterns.data_format import Polygon
from tactile_patterns.data_format import Collection
from tactile_patterns.data_format import LinearRing
from tactile_patterns.data_format import pretty_geojson_string
from tactile_patterns.data_format import get_recommended_scaling
from tactile_patterns.data_format import projection_code

import copy
import pprint
import time

"""
see project README for usage example
"""
def maze_under_construction_pattern(repetition_x, repetition_y):
    """
                        v
                        2
    l1.l1.l1.l1.        .
                        v
         v              2
         1
         .        l2.l2.l2.l2
         v
         1
    """
    multiplier = 8
    central_point_x = multiplier/2 
    central_point_y = multiplier* 3/2 
    width = multiplier
    height = 1
    l1 = LinearRing([
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
        ])
    central_point_x = multiplier/2 
    central_point_y = multiplier/2 
    width = 1
    height = multiplier
    v1 = LinearRing([
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y - height/2),
            Point(x=central_point_x + width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y + height/2),
            Point(x=central_point_x - width/2, y=central_point_y - height/2),
        ])
    l2 = copy.deepcopy(l1)
    l2.rescale(Rescale(multiply_x=1, multiply_y=1, add_x=multiplier, add_y=-multiplier))
    v2 = copy.deepcopy(v1)
    v2.rescale(Rescale(multiply_x=1, multiply_y=1, add_x=multiplier, add_y=multiplier))
    l1 = Polygon(l1)
    l2 = Polygon(l2)
    v1 = Polygon(v1)
    v2 = Polygon(v2)
    features = [l1, l2, v1, v2]
    collection_group = Collection(features)
    returned = Collection([])
    for x in range(0, repetition_x):
        for y in range(0, repetition_y):
            x_move = (x - repetition_x/2) * multiplier * 2
            y_move = (y - repetition_y/2) * multiplier * 2
            added = copy.deepcopy(collection_group)
            added.rescale(Rescale(multiply_x=1, multiply_y=1, add_x=x_move, add_y=y_move))
            returned.merge_in_list(added.features())
    return returned
