import pickle
from r2d2_hw3 import generate_map, generate_random
from r2d2_hw3 import FlagCaptureGraph as Graph
import os

######generate any map you want and save it as pickle####
base_dir = os.path.abspath(os.path.dirname(__file__))
robots_pos = {'D2_1': None, 'D2_2': None, 'Q5_1': None, 'Q5_2': None}
flags_pos = {'flag_D2': None, 'flag_Q5': None}
vertics, edges = generate_map(5, 5, [((0, 2), (0, 3)), ((1, 2), (1, 3)), ((3, 1), (3, 2)), ((4, 1), (4, 2))])
graph = Graph(V=vertics, E=edges, robots_pos=robots_pos, flags_pos=flags_pos)
fp = os.path.join(base_dir, 'scenes', 'scene_5x5_2.sc')
with open(fp, 'wb') as f:
    pickle.dump(graph, f)

