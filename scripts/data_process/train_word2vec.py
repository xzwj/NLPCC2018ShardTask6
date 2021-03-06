# encoding: utf-8

from gensim.models import Word2Vec
import jieba
import os
import time
import numpy as np

def get_stopWords(stopWords_fn):
    with open(stopWords_fn, 'rb') as f:
        stopWords_set = {line.strip('\r\t\n').decode('utf-8') for line in f}
    return stopWords_set


def sentence2words(sentence, stopWords=False, stopWords_set=None):
    """
    split a sentence into words based on jieba
    """
    # seg_words is a generator
    seg_words = jieba.cut(sentence)
    if stopWords:
        words = [word for word in seg_words if word not in stopWords_set and word != ' ' and word != '\n']
        words.extend(['</s>' for _ in range(730000)])
    else:
        words = [word for word in seg_words]
    return words

def sentences(file_csv):
    stopWords_fn = 'all_stopword.txt'
    stopWords_set = get_stopWords(stopWords_fn)

    with open(file_csv, 'r') as f:
        all_text = f.read()
        return [sentence2words(all_text, True, stopWords_set)]


def train_save(file_csv, model_fn):
    num_features = 100
    min_word_count = 3
    num_workers = 48
    context = 6
    epoch = 5
    sample = 1e-5
    model = Word2Vec(
        sentences(file_csv),
        size=num_features,
        min_count=min_word_count,
        # workers=num_workers,
        # sample=sample,
        # window=context,
        iter=epoch,
    )
    model.save(model_fn)
    return model


if __name__ == "__main__":
    start = time.time()
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    text_path = os.path.join(root_path, 'dataset', 'task6data2_new', 'text.csv')
    embeddings_model_path = os.path.join(root_path, 'dataset', 'word2vec_model_0421')
    embeddings_npz_path = os.path.join(root_path, 'dataset', 'word2vec_model_0421.npz')
    embeddings_vec_txt_path = os.path.join(root_path, 'dataset', 'word2vec_0421.txt')
    
    model = train_save(text_path, embeddings_model_path)
    model.wv.save_word2vec_format(embeddings_vec_txt_path, binary=False)
    # weights = model.wv.syn0
    # np.save(open(embeddings_npz_path, 'wb'), weights)
    end = time.time()
    
    print '-------------RUN TIME------------'
    print end-start
    print '---------------------------------'
    # model = train_save('../../dataset/text.csv', '../../dataset/word2vec_model_0417')
    # model = train_save('../task6data2_new/smarty.csv', 'word2vec_model_0925')

    # get the word vector
    for w in model.most_similar(u'互联网'):
        print w[0], w[1]

    print len(model.wv.syn0)
    '''
    KeyedVectors.load_word2vec_format instead of  Word2Vec.load_word2vec_format
    word2vec_model.wv.save_word2vec_format instead of  word2vec_model.save_word2vec_format
    model.wv.syn0norm instead of  model.syn0norm
    model.wv.syn0 instead of  model.syn0
    model.wv.vocab instead of model.vocab
    model.wv.index2word instead of  model.index2word
    '''
    print model.similarity(u'产品', u'航班')

    country_vec = model.wv[u'互联网']
    print type(country_vec)
    print country_vec
