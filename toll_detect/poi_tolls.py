import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
from geopy.distance import distance
from .cluster_set import ClusterSet
from .node_set import NodeSet
from .utils import parse_position
import folium


def plot_toll_with_neareast_intersection_node(node_set, toll_set, 
    irange=None, show_distances=False, show_connect_line=False):
    m = folium.Map(location=node_set[0].get_coord(False), zoom_start=12)
    if irange is None:
        irange = np.arange(len(node_set))
    
    for idx in irange:
        nodes = node_set[idx]
        toll_coord, toll_name = toll_set[idx]
        folium.Marker(toll_coord, icon=folium.map.Icon(color='orange'), popup=toll_name).add_to(m)
        if not isinstance(nodes, list):  # Support k >= 1
            nodes = [nodes]
        for node in nodes:
            node_coord = node.get_coord(False)
            node_info = node.connection_type + ':%d intersections. ' % node.connected_road_num
            if show_distances:
                node_info += ('distance to toll %.2f' % node.distance_to_coord(toll_coord))
            folium.Marker(node_coord, icon=folium.map.Icon(color='blue'), popup=node_info).add_to(m)
        if show_connect_line:
            folium.PolyLine(locations=[toll_coord, node_coord]).add_to(m)

    return m


class POITolls(ClusterSet):

    def __init__(self, poi_toll_path):
        self.df_toll = pd.read_csv(poi_toll_path, sep='|', converters={'position': parse_position})

    def nearest_nodes(self, node_set, k, return_distance=False):
        """Find the neareast nodes of each given POI_Toll

        Args:
            node_set: NodeSet object
            k: k neareast nodes  # TODO: doesn't support k > 1 for now
            with_distance: whether return the distacne between Toll and it's neareast node.
        Returns:
            neareaset_node_set: NodeSet, in order to analyse neareast node attributes
            distances_to_neareast_node: if return_distance == True, return the distances 
        """
        assert k >= 1, 'k is not set properly'
        toll_coords = np.array(self.get_coords())  # lat, lon
        node_coords = np.array(node_set.coords(lon_first=False))
        ball_tree = BallTree(node_coords, leaf_size=20, metric='haversine')
        indexs = ball_tree.query(toll_coords, k, return_distance=False)

        neareaset_node_list = [[node_set[i] for i in row] for row in indexs] 
        if k == 1:
            neareaset_node_list = [n for row in neareaset_node_list for n in row]  # k == 1 then flatten
        neareaset_node_set = NodeSet(neareaset_node_list)
        
        if return_distance:
            if k == 1:
                distances_to_neareast_node = [n.distance_to_coord(tc) for n, tc in zip(neareaset_node_list, toll_coords)]
            else:
                distances_to_neareast_node = None
            return neareaset_node_set, distances_to_neareast_node
        else:
            return neareaset_node_set
    
    def get_coords(self):
        """coords of each toll"""
        return [coord for coord in self.df_toll['position'].values]

    def __getitem__(self, idx):
        return self.df_toll.loc[idx, 'position'], self.df_toll.loc[idx, 'poi_name']