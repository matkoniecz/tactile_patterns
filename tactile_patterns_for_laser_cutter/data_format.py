import json
import pprint
import jsbeautifier
from pyproj import Transformer


class Rescale:
    def __init__(self, multiply_lon=None, multiply_lat=None, add_lon=None, add_lat=None, multiply_y=None, multiply_x=None, add_x=None, add_y=None):
        if (multiply_lon != None or multiply_lat != None or add_lon != None or add_lat != None):
            if (multiply_x != None or multiply_y != None or add_x != None or add_y != None):
                raise "unexpectedly specified both lan/lon and x/y"
        if (multiply_lon == None and multiply_lat == None and add_lon == None and add_lat == None):
            multiply_lon = multiply_x
            multiply_lat = multiply_y
            add_lon = add_x
            add_lat = add_y
        if multiply_lon == None:
            raise "unexpected None for multiply lon / x"
        if multiply_lat == None:
            raise "unexpected None for multiply lat / y"
        if add_lon == None:
            raise "unexpected None for add lon / x"
        if add_lat == None:
            raise "unexpected None for add lat / y"
        self.multiply_lon = multiply_lon
        self.multiply_lat = multiply_lat
        self.add_lon = add_lon
        self.add_lat = add_lat


class Point():
    def __init__(self, lat=None, lon=None, x=None, y=None):
        if (lat != None or lon != None) and (x != None or y != None):
            raise "unexpectedly specified both lan/lon and x/y"
        if lat == None and lon == None:
            lat = y
            lon = x
        if lat == None:
            raise "unexpected None for lat / y"
        if lon == None:
            raise "unexpected None for lon / x"
        self.lat = lat
        self.lon = lon

    def to_geojson(self, rescale=None):
        if rescale == None:
            rescale = Rescale(multiply_lon=1, multiply_lat=1, add_lon=0, add_lat=0)
        lon = self.lon * rescale.multiply_lon + rescale.add_lon
        lat = self.lat * rescale.multiply_lat + rescale.add_lat
        return [lon, lat]

class LinearRing:
    def __init__(self, coordinate_list):
        self.coordinate_list = coordinate_list
    
    def to_geojson(self, rescale=None):
        returned = []
        for element in self.coordinate_list:
            returned.append(element.to_geojson(rescale))
        return returned

class Polygon:
    def __init__(self, outer_ring, inner_rings_list=[], properties={}):
        self.outer_ring = outer_ring
        self.inner_rings_list = inner_rings_list
        self.properties = properties
    
    def to_geojson(self, rescale=None):
        coordinates = [self.outer_ring.to_geojson(rescale)]
        for inner in self.inner_rings_list:
            coordinates.append(inner.to_geojson(rescale))
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates,
            },
            "properties": self.properties
        }

class Collection:
    def __init__(self, element_list):
        self.element_list = element_list

    def to_geojson(self, rescale=None):
        features = []
        for element in self.element_list:
            features.append(element.to_geojson(rescale))
        return {
            "type": "FeatureCollection",
            "features": features,
            }

def pretty_geojson_string(geojson):
    return jsbeautifier.beautify(json.dumps(geojson))

def projection_code(meaning):
    meanings = {
        "wgs84": "EPSG:4326",
        "wgs 84": "EPSG:4326",
        "internal": "EPSG:4326", # everything internally is in WGS 84
        "geojson": "EPSG:4326",
        "openstreetmap": "EPSG:4326",
        "osm": "EPSG:4326",
        "web mercator": "EPSG:3857",
        "aaaargh": "EPSG:3857",
    }
    return meanings[meaning.lower()]

"""
returns {'scale_lat': num, 'scale_lon': num} that when applied will
keep shape of a pattern when projected into new projection

useful when you treat geometry as a pattern, rather than as a shape of
something real 
"""
def get_recommended_scaling(lat, lon, projection_to):
    projection_from = projection_code("internal")
    transformer = Transformer.from_crs(projection_from, projection_to)
    point = transformer.transform(lat, lon)
    right = transformer.transform(lat, lon + 0.1)
    up = transformer.transform(lat + 0.1, lon)
    lon_distance = right[0] - point[0]
    lat_distance = up[1] - point[1]

    lat_oversize = lat_distance / lon_distance

    return {'scale_lat': 1.0 / lat_oversize, 'scale_lon': 1.0 }

def main():
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

if __name__ == "__main__":
    main()
