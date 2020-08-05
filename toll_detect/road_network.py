import pandas as pd 
import folium
from .utils import *
from .road_node import RoadNode
from typing import List, Tuple, Dict, Set, Union

class RoadNetwork(object):

    def __init__(self, rn_path, sep='|', check_node_consistency=False):
        self.df_road_net = pd.read_csv(rn_path, sep=sep, converters={'geom': parse_geom})
        self.nodes = {}
        self.highway_intersection_ids = set()
        self._init_nodes(self.df_road_net, check_node_consistency)

    def _init_nodes(self, df: pd.DataFrame, check_node_consistency: str=False):
        
        for idx, row in df.iterrows():
            start_id, end_id = row['start_id'], row['end_id']
            start_coord, end_coord = row['geom']
            way_type = row['highway']
            self._update_node(start_id, start_coord, way_type, end_id, check_node_consistency)
            self._update_node(end_id, end_coord, way_type, start_id, check_node_consistency)

    def _update_node(self, idx: int, coord: List[float], way_type: str,
            other_idx: int, check_coords: bool):
        if idx not in self.nodes:
            self.nodes[idx] = RoadNode(idx, coord[0], coord[1])
        elif check_coords:
            self.nodes[idx].check_coords_consistency(coord)
        is_highway_intersection = self.nodes[idx].update_connect_road_type(way_type, other_idx)

        if is_highway_intersection:
            self.highway_intersection_ids.add(idx)

    def get_highway_intersections_coords(self, lon_first: bool=False) -> List[List[float]]:
        coords = [self.nodes[idx].get_coord(lon_first) for idx in self.highway_intersection_ids]
        node_ids = [self.nodes[idx].idx for idx in self.highway_intersection_ids]
        return coords, node_ids
    