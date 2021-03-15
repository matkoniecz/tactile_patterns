# Disclaimer

Pattern here are of pre-alpha quality - not tested, never used on actual laser cutter, not validated in actual use, examples are missing, usage instruction is missing, tested only in LightBurn etc etc.

All of that will change.

# Tactile patterns for laser cutter

Generates patterns recognisable by touch, for use in laser-cut materials.

Used for example on maps for blind people.

Available as tactile_patterns pip package.

If you would use it but "pip package" is too scary - please open an issue to let me know how it can be also published in way that makes it useful.

# Examples

## Square

```
from tactile_patterns_for_laser_cutter.data_format import Rescale
from tactile_patterns_for_laser_cutter.data_format import Point
from tactile_patterns_for_laser_cutter.data_format import Polygon
from tactile_patterns_for_laser_cutter.data_format import Collection
from tactile_patterns_for_laser_cutter.data_format import LinearRing
from tactile_patterns_for_laser_cutter.data_format import pretty_geojson_string


outer = LinearRing([
            Point(x=0, y=0),
            Point(x=1, y=0),
            Point(x=1, y=1),
            Point(x=0, y=1),
            Point(x=0, y=0),
        ])
polygon = Polygon(outer)
collection = Collection([polygon])
print(pretty_geojson_string(collection.to_geojson()))
```

# Sponsors

<a href="https://osmfoundation.org/"><img src="logo_osmf.png" height="100"/></a><br/>

The [OpenStreetMap foundation](https://wiki.osmfoundation.org/wiki/Main_Page) was funding the development of this project in their first round of the [microgrant program](https://wiki.osmfoundation.org/wiki/Microgrants) in 2020. It was done as part of making [tactile maps based on OpenStreetMap data, for blind or visually impaired children](https://wiki.openstreetmap.org/wiki/Microgrants/Microgrants_2020/Proposal/Tactile_maps_for_blind_or_visually_impaired_children).

If anyone else is also interested in supporting this project via funding - [let me know](mailto:osm-messages@etutanota.com) (opening a new issue is also OK) :)
