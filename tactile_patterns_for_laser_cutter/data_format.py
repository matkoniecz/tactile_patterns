import json
import pprint
import jsbeautifier


class LinearRing:
    def __init__(self, coordinate_list):
        self.coordinate_list = coordinate_list
    
    def to_geojson(self):
        returned = []
        return self.coordinate_list

class Polygon:
    def __init__(self, outer_ring, inner_rings_list=[], properties={}):
        self.outer_ring = outer_ring
        self.inner_rings_list = inner_rings_list
        self.properties = properties
    
    def to_geojson(self):
        coordinates = [self.outer_ring.to_geojson()]
        for inner in self.inner_rings_list:
            coordinates.append(inner.to_geojson())
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

    def to_geojson(self):
        features = []
        for element in self.element_list:
            features.append(element.to_geojson())
        return {
            "type": "FeatureCollection",
            "features": features,
            }

def pretty_geojson_string(geojson):
    return jsbeautifier.beautify(json.dumps(geojson))

def main():
    outer = LinearRing([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    polygon = Polygon(outer)
    collection = Collection([polygon])
    print(pretty_geojson_string(collection.to_geojson()))

if __name__ == "__main__":
    main()
