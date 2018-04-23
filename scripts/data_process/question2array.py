#encoding:utf-8
'''
将问题生成train.npz
'''

import numpy as np
import tqdm
import tensorflow as tf
import jieba
import csv
from gensim.models import Word2Vec

def main(question_file,outfile, c_=40, e_=180):
    with open(question_file ) as f:
        reader = csv.reader(f)
        lines = [row for row in reader]

    results= [0 for _ in range(len(lines))] # 初始化一个长度等于lines行数的list

    model = Word2Vec.load('/home/tianyuan/E/NLPCC2018ShardTask6/NLPCC2018ShardTask6/dataset/word2vec_model_0421')

    def process(line):
        '''
        分词
        '''
        a,c_str,e_str,b,d = [_.decode('utf-8') for _ in line]
        c = [_ for _ in jieba.cut(c_str)]
        e = [_ for _ in jieba.cut(e_str)]
        return c,e,a
        
    for ii,line in tqdm.tqdm(enumerate(lines)):
        results[ii] = process(line) # 每个results[ii]都是list，里面是[c,e,a]，其中c,e也是list，里面是由char或word转成的int

    del lines
    
    qids = [_[2] for _ in results]
    index2qid = {ii:jj for ii,jj in enumerate(qids)}

    pad_sequence = tf.contrib.keras.preprocessing.sequence.pad_sequences


    cs = [[model.wv.vocab[_ if _ in model.wv.vocab else '</s>'].index for _ in line[0]] for line in results] # 对标题的词，如果可以在char_embedding.npz中找到，则取出它的索引，找不到就取出</s>的索引
    c_len = np.array([len(_) for _ in cs])
    cs_packed = pad_sequence(cs,maxlen=c_,padding='pre',truncating='pre',value = 0) # 截断或补齐
    print cs_packed
    print('c')
    del cs

    es = [[model.wv.vocab[_ if _ in model.wv.vocab else '</s>'].index for _ in line[1]] for line in results]
    e_len =  np.array([len(_) for _ in es])
    es_packed = pad_sequence(es,maxlen=e_,padding='pre',truncating='pre',value = 0)
    print('e')
    del es

    #qids = [_[2] for _ in results]
    #index2qid = {ii:jj for ii,jj in enumerate(qids)}

    np.savez_compressed(outfile,
                        title_word = cs_packed,
                        content_word = es_packed,
                        title_word_len = c_len,
                        content_word_len = e_len,
                        index2qid = index2qid
            )

# 标题平均有 22.335409689506584 字 ->50
# 标题平均有 12.90899899898899 词 ->35
# 描述平均有 117.67666210994987 字 ->250
# 描述平均有 58.563685338852 词 ->120

if __name__=='__main__':
    # word2id = np.load('word_embedding.npz')['word2id'].item()
    # print word2id
    # word_keys = set(word2id.keys())
    # print word_keys
    import fire
    fire.Fire()
