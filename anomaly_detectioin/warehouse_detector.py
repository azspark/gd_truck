import numpy as np
from sklearn.cluster import DBSCAN 

class WarehouseDetector(object):
    """Detector the warehose in order to calibrate lorry trajectory start and end point
    
    Input points are generated from stay point detection. There are two main senarios which
    Lorry will stay a while: 1. reach the warehouse 2. reach expressway service area.
    This Class will do clustering to detect the warehose and calibrate lorry trajectory start and end point.
    """

    def __init__(self, stay_points, eps, min):
        super().__init__() 

    def draw_clusters(self):
        pass

