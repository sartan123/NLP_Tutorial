import math
train_file = open('wiki-en-train.norm_pos')
train_data = train_file.readlines()

transition = {}
word_dic = {}
context = {}
context['<s>'] = 0
for line in train_data:
    line = line.rstrip('\n')
    words = line.split(' ')
    previous = '<s>'
    words.insert(0, previous)
    context[previous] += 1
    for word in words:
        try:
            words = word.split('_')
            word = words[0]
            tag = words[1]
            word_tag = word + ' ' + tag
            tag_set = previous + ' ' + tag
            if tag_set in transition.keys():
                transition[tag_set] += 1
            else:
                transition[tag_set] = 1
            if tag in context.keys():
                context[tag] += 1
            else:
                context[tag] = 1
            if word_tag in word_dic.keys():
                word_dic[word_tag] += 1
            else:
                word_dic[word_tag] = 1
            previous = tag
        except:
            pass
    if previous + '</s>' in transition.keys():
        transition[previous + '</s>'] += 1
    else:
        transition[previous + '</s>'] = 1

for k, v in transition.items():
    try:
        tag = k.split(' ')
        previous = tag[0]
        word = tag[1]
        transition[k] = v / context[previous]
    except:
        pass

for k, v in word_dic.items():
    try:
        tag = k.split(' ')
        word = tag[0]
        tag = tag[1]
        word_dic[k] = v / context[tag]
    except:
        pass

test_file = open('wiki-en-test.norm')
test_data = test_file.readlines()
best_score = {}
best_edge = {}
for line in test_data:
    words = line.split(' ')
    l = len(words)
    best_score[[0, '<s>']] = 0
    best_edge[[0, '<s>']] = [0, 'NULL']
    prev = '<s>'
    for i in range(l):
        for tag, prov in transition.items():
            tag = tag.split(' ')
            prev = tag[0]
            next = tag[1]
            score = best_score[i][
                prev] + (-math.log2(transition[prev + ' ' + next])) + (-math.log(word_dic[word[i] + ' ' + next]))
            try:
                if best_score[[i + 1, next]] < score:
                    best_score[[i + 1, next]] = score
                    best_edge[[i + 1, next]] = [i, prev]
            except:
                best_score[[i + 1, next]] = score
                best_edge[[i + 1, next]] = [i, prev]

print(best_score)
