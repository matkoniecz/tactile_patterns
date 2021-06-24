# Archived, replaced, deprecated!

Please see [https://github.com/matkoniecz/lunar_assembler](https://github.com/matkoniecz/lunar_assembler) for a replacement.

I switched to JS based solution, as using browser as an operating systems allows to skip installation.

Still, maybe patterns here will be useful for someone.

Right now I am not using it as turned out that the simplest patterns were better (though, testing more complex solutions was worth doing).

# current blocker:

https://forum.lightburnsoftware.com/t/bugs-on-importing-svg-with-small-elements/37173

# Disclaimer

Pattern here are of alpha quality - not validated in actual use, examples are missing, usage instruction is missing, tested only in LightBurn etc etc.

All of that will change.

Part of designs were prototyped already, so initial testing is done.

# Pregenerated patterns

[/patterns](/patterns) folder contains pregenerated patterns, so you can use them without running any code.

# Usage

## Laser cut wood

Plywood is commonly used for laser cutters.

There are two major problems with using wood (plywood) engraved with laser cutter.

First is charring, this can be avoided by engraving in multiple passes with reduced power rather than one pass with high power.

Second is that inherent wood texture is often masking shapes created by laser engraving. This is more problematic with laser engraving compared to other potential production methods.

Note that raster engraving are often optimalized for how generated works looks like. Requirements for tactile materials may differ. For example in LightBurn typically recommended Jarvis is the best for something that will be looked at, not touched. For tactile patterns grayscale setting is superior. Jarvis may look well, but produces rough texture, with fine elements that are crushed on touch, with very poor recognizability of overall shape.

TODO: include example settings in LightBurn

TODO: include photo with both charring and succesful burns

## Laser cut plexiglass

Plexiglass is also usable on laser cutters and texture cut into it is much more recognisable by touch, as it has no grain or large scale internal structure.

Note that cutting through plexiglass is more tricky, one (untested) recomendation is to use two passes with lower power, as settings typical to wood will leave unclean cut with stringy parts or jagged edge.

Combining plywood and plexiglass in one design is a good idea, as difference in materials is clear by touch. Plywood without pattern and plexiglass without pattern are clearly recognisable.

## Cloth, felt

Problematic due to hygienic issues. It would become dirty quickly and is basically impossible to clean it.

## Cork

??? should be interesting and useful

## Leather

??? should be interesting and useful

# Tactile patterns for laser cutter

Generates patterns recognisable by touch, for use in laser-cut materials.

Used for example on maps for blind people.

Available as tactile_patterns pip package.

If you would use it but "pip package" is too scary - please open an issue to let me know how it can be also published in way that makes it useful.

# Examples

## Square

```
from tactile_patterns.data_format import Rescale
from tactile_patterns.data_format import Point
from tactile_patterns.data_format import Polygon
from tactile_patterns.data_format import Collection
from tactile_patterns.data_format import LinearRing
from tactile_patterns.data_format import pretty_geojson_string


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

## Use one of vector generators

```
from tactile_patterns.vector import maze_under_construction_pattern
from tactile_patterns.data_format import pretty_geojson_string
from tactile_patterns.data_format import get_recommended_scaling
from tactile_patterns.data_format import projection_code


pattern = maze_under_construction_pattern(30, 30)
lat = 50.05518
lon = 19.92757
base_scaling = 0.000001
projection_scale = get_recommended_scaling(lat, lon, projection_code("web mercator"))
scale_lat = projection_scale['scale_lat'] * base_scaling
scale_lon = projection_scale['scale_lon'] * base_scaling
pattern.rescale(Rescale(multiply_lat=scale_lat, multiply_lon=scale_lon, add_lon=lon, add_lat=lat))
print(pretty_geojson_string(pattern.to_geojson()))
```

If you want SVG file rather than geojson file, you can run

`svgis draw test.geojson --style '* {stroke: none; fill: #00f}' -o out.svg`

## Use one of raster generators


# Sponsors

<a href="https://osmfoundation.org/"><img src="logo_osmf.png" height="100"/></a><br/>

The [OpenStreetMap foundation](https://wiki.osmfoundation.org/wiki/Main_Page) was funding the development of this project in their first round of the [microgrant program](https://wiki.osmfoundation.org/wiki/Microgrants) in 2020. It was done as part of making [tactile maps based on OpenStreetMap data, for blind or visually impaired children](https://wiki.openstreetmap.org/wiki/Microgrants/Microgrants_2020/Proposal/Tactile_maps_for_blind_or_visually_impaired_children).

If anyone else is also interested in supporting this project via funding - [let me know](mailto:osm-messages@tutanota.com) (opening a new issue is also OK) :)
