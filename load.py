import json
import os
filename = os.getenv('HOME')+'/data/vrd/train_fname_mapping.json'
data = json.load(open(filename, 'r'))
print(len(data.keys()))
print(len(set(data.values())))
# print(data)