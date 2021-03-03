# Tactile patterns for laser cutter

Generates patterns recognisable by touch, for use in laser-cut materials.

Used for exaples on maps for blind people.

Available as tactile_patterns_for_laser_cutter pip package.

If you would use it but "pip package" is too scary - please open an issue to let me know how it can be also published in way that makes it useful.

# Example

```
from tactile_patterns_for_laser_cutter.data_format import Polygon
from tactile_patterns_for_laser_cutter.data_format import Collection
from tactile_patterns_for_laser_cutter.data_format import LinearRing
from tactile_patterns_for_laser_cutter.data_format import pretty_geojson_string


triangle = Polygon(LinearRing([[0, 0], [1, 1], [0, 1], [0, 0]]))
collection = Collection([triangle])
print(pretty_geojson_string(collection.to_geojson()))
```
