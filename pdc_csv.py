#coding:utf8
'''
根据.pth文件生成.csv文件，即最终结果
'''

import torch as t
import sys
sys.path.append('../')
from utils import get_score
import glob
import torch as t 
import numpy as np
import json
import time
import csv

def main(pth_fn,csv_fn):
    label_path =   './dataset/lables_0422.json'
    # test_data_path='./dataset/tasktestdata06/dev_data.npz' 
    test_data_path='./dataset/val_with_300w.npz'
    index2qid = np.load(test_data_path)['index2qid'].item()
    with open(label_path) as f: 
          labels_info = json.load(f)
    qid2label = labels_info['d']
    label2qid = labels_info['id2label']

    files = glob.glob(pth_fn)
    tmp = t.load(files[0])
    result=(tmp).topk(5,1)[1]

    ## 写csv 提交结果
    rows = range(result.size(0))
    for ii,item in enumerate(result):
        # print result
        rows[ii] = [index2qid[ii]] + [label2qid[str(_)] for _ in item ]

    with open(csv_fn,'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    

if __name__=='__main__':
    import fire
    fire.Fire()
