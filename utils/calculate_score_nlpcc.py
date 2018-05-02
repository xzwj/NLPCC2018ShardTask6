#coding=utf8


import csv 
import math
import sys

def compute_position_weighted_precision(correct_num, predict_num):
    assert(len(correct_num) == len(predict_num))
    weighted_correct = 0.0
    weighted_predict = 0.0
    for i in xrange(len(correct_num)):
        # print correct_num[i]
        # print '#####################3'
        # print predict_num[i]
        weighted_correct += correct_num[i] / math.log(i + 3.0)
        weighted_predict += predict_num[i] / math.log(i + 3.0)
    return weighted_correct / weighted_predict

def compute_recall(correct_num, ground_truth_num):
    return sum(correct_num) / ground_truth_num

def eval(ground_truth_data, predict_data, max_tag_num=5):
    ground_truth = {}
    ground_truth_num = 0.0
    with open(ground_truth_data, 'rb') as f:
        lines = csv.reader(f)
        for i, items in enumerate(lines):
            if i == 0:
                continue
            id, true_tag_ids = items[0], items[4]
            ground_truth[id] = true_tag_ids.split('|') ###################################################
            ground_truth_num += len(ground_truth[id])

    correct_num = [0.0] * max_tag_num
    predict_num = [0.0] * max_tag_num

    with open(predict_data, 'rb') as f:
        lines = csv.reader(f)
        for i, items in enumerate(lines):#######################3
            if i == 0:
                continue
            assert(len(items) == max_tag_num + 1)
            id = items[0]
            if id not in ground_truth:
                continue
            #assert(id in ground_truth)
            true_tag_ids = ground_truth[id]
            for pos, tag_id in enumerate(items[1:]):
                if tag_id == '-1':
                    continue
                predict_num[pos] += 1
                if tag_id in true_tag_ids:
                    correct_num[pos] += 1
    precision = compute_position_weighted_precision(correct_num, predict_num)
    recall = compute_recall(correct_num, ground_truth_num)
    F1 = 2 * precision * recall / (precision + recall)

    print "precision: {}, recall: {}, F1 {}".format(precision, recall, F1)

    return F1

def get_score(predict_label_and_marked_label_list):
    # print predict_label_and_marked_label_list
    """
    :param predict_label_and_marked_label_list: 一个元组列表。例如
    [ ([1, 2, 3, 4, 5], [4, 5, 6, 7]),
      ([3, 2, 1, 4, 7], [5, 7, 3])
     ]
    需要注意这里 predict_label 是去重复的，例如 [1,2,3,2,4,1,6]，去重后变成[1,2,3,4,6]
    
    marked_label_list 本身没有顺序性，但提交结果有，例如上例的命中情况分别为
    [0，0，0，1，1]   (4，5命中)
    [1，0，0，0，1]   (3，7命中)

    """
    
    ground_truth = {}
    ground_truth_num = 0.0
    max_tag_num=5
    
    for id in range(len(predict_label_and_marked_label_list)):
        predict_labels = predict_label_and_marked_label_list[id][0]
        ground_truth[id] = predict_labels
        ground_truth_num += len(ground_truth[id])
        id = id+1

    correct_num = [0.0] * max_tag_num
    predict_num = [0.0] * max_tag_num
    
    for id in range(len(predict_label_and_marked_label_list)):
        marked_labels = predict_label_and_marked_label_list[id][1]
        
        items = marked_labels
        i = id
        while max_tag_num-len(items):
            items.append('-1')
        assert(len(items) == max_tag_num)
        # print id,ground_truth
        if id not in ground_truth:
            continue
        #assert(id in ground_truth)
        true_tag_ids = ground_truth[id]
        for pos, tag_id in enumerate(items):
            if tag_id == '-1':
                continue
            predict_num[pos] += 1
            if tag_id in true_tag_ids:
                correct_num[pos] += 1
        # print id
        id=id+1
    
    # print correct_num
    # print predict_num
    precision = compute_position_weighted_precision(correct_num, predict_num)
    recall = compute_recall(correct_num, ground_truth_num)
    # F1 = 2 * precision * recall / (precision + recall)
    
    # print '###################### GET SCORE NICE~~~~~ ########################3'

    return 2 * (precision * recall) / (precision + recall +0.0000000000001),precision,recall,correct_num

if __name__=='__main__':
    lst = [ ([1, 2, 3, 4, 5], [4, 5, 6, 7]),([3, 2, 1, 4, 7], [5, 7, 3])]
    print get_score(lst)
    
