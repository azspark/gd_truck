import numpy as np
from typing import List, Tuple, Dict, Set, Union

def parse_geom(geom: str) -> List:
    def get_coords(coord_str):
        coord_str = coord_str.strip().split(' ')
        return [float(coord_str[0]), float(coord_str[1])]
    geom = geom[12: -1]  # remove 'LINESTRING (' and ')'
    coords = geom.split(',')
    return [get_coords(coords[0]), get_coords(coords[-1])]

if __name__ == "__main__":
    test_string = 'LINESTRING (110.8598708 21.4391107, 110.8893308 21.4508543, 110.8887354 21.45037, 110.8601886 21.4392018)'
    print(parse_geom(test_string))