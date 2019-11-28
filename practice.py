import os
import random
import pandas as pd

hiragana_file = './hiragana.csv'
katakana_file = './katakana.csv'
col_index = [i for i in 'aiueo']
row_index = [''] + [i for i in 'kstnhmyrw']
print(row_index)

wrong_set_file = './wrong_set.txt'

hira = pd.read_csv(hiragana_file, header=None)
kata = pd.read_csv(katakana_file, header=None)
print(hira)

dic = {
    'hira':hira,
    'kata':kata,
}

class WrongSet():
    def __init__(self):
        if not os.path.exists(wrong_set_file):
            print("Wrong set not found")
            self.set = {}
            return
        with open(wrong_set_file, 'r') as f:
            data = f.readlines()
        self.set = {}
        for row in data:
            word, answer, times = row.split()
            times = int(times)
            self.set[word] = [answer, times]

    def save(self):
        global wrong_set_file
        with open(wrong_set_file, 'w') as f:
            for key, val in self.set.items():
                f.write('{} {} {}\n'.format(key, val[0], val[1]))

    def add(self, word, answer):
        if word not in self.set:
            self.set[word] = [answer, 0]
        self.set[word][1] += 1
        self.save()

    def dec(self, word):
        if word not in self.set:
            return
        self.set[word][1] -= 1
        if self.set[word][1] <= 0:
            self.set.pop(word)
        self.save()

    def choose(self, method='weight'):
        keys = sorted(self.set.keys())
        if method == 'weight':
            count = 0
            for key in keys:
                count += self.set[key][1]
            randint = random.randint(0, count-1)
            for key in keys:
                if randint < self.set[key][1]:
                    return key, self.set[key][0]
                else:
                    randint -= self.set[key][1]
            raise Exception("Unexpected Error")
        else:
            return key, self.set[random.choice(keys)][0]

    def size(self):
        return len(self.set)

    def clean(self):
        self.set = {}


def check(word, answer):
    print(word, ": ", end='')
    manswer = input()
    return answer == manswer, manswer

def show(right):
    if right:
        print('⭕️')
    else:
        print('❌')

def search(type_, row, col):
    word = dic[type_][col][row]
    answer = row_index[row] + col_index[col]
    if word == 'xx':
        answer = 'xx'
    return word, answer

def random_choice(type_='all'):
    if type_ == 'all':
        type_ = random.choice(['hira', 'kata'])
    row = random.randint(0, len(row_index)-1)
    col = random.randint(0, len(col_index)-1)
    return search(type_, row, col)


def random_practice(type_='all'):
    global ws
    while True:
        word, answer = random_choice(type_)
        if word == 'xx':
            continue
        right, m = check(word, answer)
        show(right)
        if not right:
            ws.add(word, answer)
            print("It's", answer)

def exam():
    paper = []
    for type_ in ['hira', 'kata']:
        for row in range(len(row_index)):
            for col in range(len(col_index)):
                word, answer = search(type_, row, col)
                if word != 'xx':
                    paper.append((word, answer))
    random.shuffle(paper)
    tot = len(paper)
    count = 0
    wrong_count = []
    for word, answer in paper:
        print("{}/{}  ".format(count, tot), end='')
        right, m = check(word, answer)
        count += 1
        if not right:
            wrong_count.append((word, answer, m))

    if len(wrong_count) == 0:
        print("You get all question right!")
    else:
        print("{} wrong:".format(len(wrong_count)))
        for word, answer, m in wrong_count:
            global ws
            ws.add(word, answer)
            print('{} should be {}, you type {}'.format(word, answer, m))


def review():
    while ws.size() > 0:
        word, answer = ws.choose()
        right, m = check(word, answer)
        ws.dec(word)
    print("You have review all your wrong set")


def clean():
    ws.clean()


if __name__ == '__main__':
    ws = WrongSet()
    try:
        while True:
            mode = input(
                '''
                Choose operation:
                1. random practice, all
                2. random practice, hiragana
                3. random practice, katakana
                4. exam
                5. review wrong set
                6. reset wrong set
                '''
            )
            try:
                print("You can type Ctrl+C to leave")
                if mode == '1':
                    random_practice()
                elif mode == '2':
                    random_practice('hira')
                elif mode == '3':
                    random_practice('kata')
                elif mode == '4':
                    exam()
                elif mode == '5':
                    review()
                elif mode == '6':
                    clean()
            except KeyboardInterrupt:
                print("Back to menu")
    except KeyboardInterrupt:
        print("Byebye")
