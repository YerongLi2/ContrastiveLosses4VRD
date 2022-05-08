import json
import os
filename = os.getenv('HOME')+'/data/vg/rel_annotations_val.json'
data = json.load(open(filename, 'r'))
print(data['2315355.jpg'])
# print(len(set(data.values())))
# print(data)