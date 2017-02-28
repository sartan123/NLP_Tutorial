from collections import defaultdict
import numpy as np


def predict_all(model, input_test, ids):
    predict_count = 0
    count = 0
    for line in input_test:
        count += 1
        line = line.split('\t')
        y = line[0]
        x = line[1]
        phi = create_features(x, ids)
        y2 = predict_one(w, phi)
        if int(y) == int(y2):
            predict_count += 1
    print(predict_count / count)


def predict_one(w, phi):
    phi = np.array(phi)
    score = np.dot(w, phi)
    return 1 if score >= 0 else -1


def create_features(x, ids):
    phi = [0]*(len(ids)+1)
    words = x.split(' ')
    for word in words:
        try:
            phi[ids[word]] += 1
        except:
            pass
    return phi


def create_wordlist(data):
    ids = {}
    count = 0
    for line in data:
        line = line.rstrip('\n')
        line = line.split('\t')
        words = line[1].split(' ')
        for word in words:
            if word not in ids:
                ids[word] = 1
                count += 1
            else:
                ids[word] += 1
    return ids


def init_ids(word_list):
    ids = {}
    count = 0
    for k in word_list.keys():
        if k not in ids.keys():
            ids[k] = count
            count += 1
    return ids


def update_weights(w, phi, y):
    w += 0.1*np.array(phi)*int(y)
    return w

file = open('titles-en-train.labeled')
data = file.readlines()
word_list = create_wordlist(data)
ids = init_ids(word_list)
w = np.zeros(len(ids)+1)

for line in data:
    line = line.rstrip('\n')
    line = line.split('\t')
    y = line[0]
    x = line[1]
    phi = create_features(x, ids)
    y1 = predict_one(w, phi)
    if int(y1) != int(y):
        w = update_weights(w, phi, y)

test_file = open('titles-en-test.word')
test_data = test_file.readlines()
predict_all(w, test_data, ids)
print('Finish')
