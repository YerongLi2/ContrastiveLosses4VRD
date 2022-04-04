import json
filename = './data/vrd/train_fname_mapping.json'
data = json.load(open(filename, 'r'))
print(data)