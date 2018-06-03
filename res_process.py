import json
import os
import pandas as pd
from collections import OrderedDict

with open('true_locations_names_sorted.json', encoding='utf-8') as f_true_locations_names_sorted:
    true_locations_names_sorted = json.load(f_true_locations_names_sorted, object_pairs_hook=OrderedDict)

with open('res_dists.json', encoding='utf-8') as f_res_dists:
    res_dists = json.load(f_res_dists, object_pairs_hook=OrderedDict)
    
with open('res_times.json', encoding='utf-8') as f_res_times:
    res_times = json.load(f_res_times, object_pairs_hook=OrderedDict)
    
df_dists = pd.DataFrame.from_dict(res_dists)
df_dists.index = true_locations_names_sorted
df_dists.to_excel('res_dists [m].xlsx')

df_times = pd.DataFrame.from_dict(res_times)
df_times.index = true_locations_names_sorted
df_times.to_excel('res_times [s].xlsx')