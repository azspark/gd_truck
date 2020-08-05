import numpy as np
from typing import List, Tuple, Dict, Set, Union
from geopy.distance import distance


class RoadNode(object):

    def __init__(self, idx, lon, lat):
        assert lon >= -180.0 and lon < 180.0, "Node longitude is not set properly"
        assert lat >= -90.0 and lat <= 90.0, "Node latitude is not set properly"        
        self.idx = idx
        self.lon = lon 
        self.lat = lat
        self.node_connected_type = {}
        self.connect_to_highway = False
        self.connect_to_normalway = False

    def update_connect_road_type(self, way_type: str, idx: int) -> bool:
        if idx not in self.node_connected_type:
            self.node_connected_type[idx] = way_type
            if way_type == 'motorway' or way_type == 'trunk':
                self.connect_to_highway = True
            else:
                self.connect_to_normalway = True
        return self.connect_to_highway and self.connect_to_normalway
        
    def get_coord(self, lon_first):
        if lon_first:
            return [self.lon, self.lat]
        else:
            return [self.lat, self.lon]

    def check_coords_consistency(self, coords: List[float]):
        new_lon, new_lat = coords
        assert np.abs(new_lon - self.lon) < 1e-6
        assert np.abs(new_lat - self.lat) < 1e-6

    @property
    def connected_road_num(self):
        return len(self.node_connected_type)

    @property
    def connection_type(self):
        pass

    def __repr__(self):
        return super().__repr__()

    def distance_to(self, node) -> float:
        return distance(self.get_coord(False), node.get_coord(False)).meters