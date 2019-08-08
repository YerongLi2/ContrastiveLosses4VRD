# Included function adapted from Rowan Zellers:
# https://github.com/rowanz/neural-motifs
# Get counts of all of the examples in the dataset. Used for creating the baseline
# dictionary model

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
import json

import utils_rel.boxes_rel as box_utils_rel
from core.config import cfg

from datasets_rel.dataset_catalog_att import ANN_FN2
from datasets_rel.dataset_catalog_att import DATASETS


# This function is adapted from Rowan Zellers:
# https://github.com/rowanz/neural-motifs/blob/master/lib/get_dataset_counts.py
# Modified for this project
def get_att_counts(ds_name):
    """
    Get counts of all of the relations. Used for modeling directly P(rel | o1, o2)
    :param train_data:
    :return: 
    """

#     if ds_name.find('oi') >= 0:
#         with open(DATASETS['oi_att_train'][ANN_FN2]) as f:
#             train_data = json.load(f)
#     elif ds_name.find('gqa') >= 0:
# #         with open(DATASETS['gqa_train'][ANN_FN2]) as f:
#         with open(DATASETS[cfg.TRAIN.DATASETS[0]][ANN_FN2]) as f:
#             train_data = json.load(f)
#     else:
#         raise NotImplementedError
    
    if len(cfg.TRAIN.DATASETS) > 0:
        with open(DATASETS[cfg.TRAIN.DATASETS[0]][ANN_FN2]) as f:
            train_data = json.load(f)
    else:
        ds_keywords = cfg.TEST.DATASETS[0].split('_')
        if ds_keywords[-1] == 'val' or \
            ds_keywords[-1] == 'test'or \
            ds_keywords[-1] == 'all':
            ds_keywords = ds_keywords[:-1]
        ds_name = '_'.join(ds_keywords + ['train'])
        with open(DATASETS[ds_name][ANN_FN2]) as f:
            train_data = json.load(f)

    fg_matrix = np.zeros((
        cfg.MODEL.NUM_CLASSES - 1,  # not include background
        cfg.MODEL.NUM_ATT_CLASSES + 1,  # include background
    ), dtype=np.int64)

    bg_matrix = np.zeros(
        cfg.MODEL.NUM_CLASSES - 1,  # not include background
        dtype=np.int64)
    
    for _, im_rels in train_data.items():
        # get all object boxes
        gt_box_to_label = {}
        for i, rel in enumerate(im_rels):
            obj_box = box_utils_rel.y1y2x1x2_to_x1y1x2y2(rel['object']['bbox'])
            obj_lbl = rel['object']['category']  # not include background
            att_lbl = rel['attribute']  # not include background
            if tuple(obj_box) not in gt_box_to_label:
                gt_box_to_label[tuple(obj_box)] = obj_lbl
            
            fg_matrix[obj_lbl, att_lbl + 1] += 1
        
        for _, l in gt_box_to_label.items():
            bg_matrix[l] += 1

    return fg_matrix, bg_matrix