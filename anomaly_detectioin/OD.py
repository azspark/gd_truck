from .detect_toll_of_traj import TrajTollDetector
import numpy as np
import pandas as pd
import folium

class OD(object):
    def __init__(self, df):
        self.df = df
        self.df.set_index(np.arange(len(df)), inplace=True)

    def init_detector(self, tolls):
        self.tolls = tolls
        self.detector = TrajTollDetector(tolls)

    def detect_toll(self):
        assert self.detector is not None, "You should first init the detector to use this."
        uptoll_class_list, downtoll_class_list, uptoll_dis, downtoll_dis = [], [], [], []

        for idx, row in self.df.iterrows():
            coords, speeds = row['coords'], row['speeds']
            toll_class1, toll_coord1, toll_class2, toll_coord2, dis1, dis2 \
                = self.detector.detect_passed_toll_of_traj(coords, speeds, count_distance=True)
            uptoll_class_list.append(toll_class1)
            downtoll_class_list.append(toll_class2)
            uptoll_dis.append(dis1)
            downtoll_dis.append(dis2)
        self.df['uptoll_class'] = uptoll_class_list
        self.df['downtoll_class'] = downtoll_class_list
        self.df['uptoll_dis'] = uptoll_dis
        self.df['downtoll_dis'] = downtoll_dis

    def toll_distribution(self):
        pass

    def vis_trajs(self):
        pass

    def vis_uptoll_ratio(self, warehoue):
        assert self.tolls is not None, "You should first init the detector to use this."
        df_warehouse = self.df[self.df['start_warehoue'] == warehoue]
        series_size = df_warehouse.groupby('uptoll_class').size()
        total_num = series_size.sum()
        m = None
        for toll_class, toll_num in series_size.to_dict().items():
            toll_coord = np.array(self.tolls.get_coords_of_class(toll_class)).mean(axis=0)
            if m is None:
                m = folium.Map(toll_coord, zoom_start=12)
            folium.Circle(
                radius=int(toll_num / total_num * 1000),
                location=toll_coord,
                popup=str(toll_class),
                color='#3186cc',
                fill=True,
                fill_color='#3186cc'
            ).add_to(m)
        return m