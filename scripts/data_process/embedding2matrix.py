#coding:utf8

'''
将word2vec_model 转成numpy矩阵
'''

from gensim.models import Word2Vec
# import word2vec
import numpy as np

def main(em_file, em_result):
    '''
    embedding ->numpy
    '''
    em = Word2Vec.load(em_file)
    vec = (em.wv.vectors)
    word2id = dict(zip(em.wv.index2word, range(len(em.wv.index2word))))
    
    np.savez_compressed(em_result,vector=vec,word2id=word2id)

if __name__ == '__main__':
    import fire
    fire.Fire()
