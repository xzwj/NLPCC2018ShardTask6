#coding:utf8
'''
从trian.npz中提取最后的200000条作为验证集
'''

import numpy as np
def main(question_file,outfile):
    '''
    question_file   :   train.npz
    outfile         :   val.npz
    '''
    train = np.load(question_file)
    print len(train['content_word'])
    content_word = train['content_word'][-200000:]
    title_word = train['title_word'][-200000:]
    # title_char = train['title_char'][-200000:]
    # content_char = train['content_char'][-200000:]

    index2qid = train['index2qid']
    np.savez_compressed(outfile,
                            # title_char = title_char,
                            title_word = title_word,
                            # content_char = content_char,
                            content_word = content_word,
                            index2qid = index2qid
                )

if __name__=='__main__':
    import fire
    fire.Fire()
