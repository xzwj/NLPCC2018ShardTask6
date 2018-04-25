#coding:utf8

'''
生成每个qid对应的label,保存成json
'''
def main(file):
    max_len=0

    with open(file) as f:
        lines = f.readlines()

    #def process(line):
    for line in lines:
        qid = line.replace('\n','').split(',')[0]
        # labels = line.replace('\n','').replace('\r','').split(',')[-1]
        labels = line.replace('\r\n','').split(',')[-1]
        labels = labels.split('|')
        if len(labels) > max_len:
            max_len = len(labels)
            print labels
        #return qid,labels
    #results = list( map(process, lines))
    print max_len # 18 # 训练数据中单个问题最多被打了18个标签

if __name__=='__main__':
    import fire
    fire.Fire()
