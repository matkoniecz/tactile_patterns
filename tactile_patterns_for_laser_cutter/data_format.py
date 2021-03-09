import json
import pprint
import jsbeautifier


class Rescale:
    def __init__(self, multiply_lon, multiply_lat, add_lon, add_lat):
        self.multiply_lon = multiply_lon
        self.multiply_lat = multiply_lat
        self.add_lon = add_lon
        self.add_lat = add_lat


class Point():
    def __init__(self, lat=None, lon=None, x=None, y=None):
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
