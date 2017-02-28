import math
file = open('wiki-en-test.txt')
test = file.readlines()
file2 = open('02_train.txt')
model = file2.readlines()

model_dic = {}
for lines in model:
    lines = lines.rstrip('\n')
    word = lines.split('\t')
    model_dic[word[0]] = float(word[1])

for lines in test:
    beta1 = 0.95
    beta2 = 0.05
    V = 10000000
    H = 0
    W = 0
    lines = lines.rstrip('\n')
    words = lines.split(' ')
    words.insert(0, '<s>')
    words.append('</s>')
    for i in range(1, len(words)):
        n_gram = words[i]+' '+words[i-1]
        if n_gram in model_dic.keys():
            P1 = beta1*model_dic[words[i]] + (1-beta1)/V
            P2 = beta2*model_dic[n_gram] + (1-beta2)*P1
            H += -(math.log2(P2))
            W += 1

print(H/W)
