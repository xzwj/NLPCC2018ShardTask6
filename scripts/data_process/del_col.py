import csv

def del_cvs_col(fname, newfname, idxs, delimiter=','):
    with open(fname) as csvin, open(newfname, 'w') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=delimiter)
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)

del_cvs_col('train_data.csv', 'train_data_deled_col.csv', [0,4])
