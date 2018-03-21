#!/usr/bin/env python
# coding=utf-8
'''
 File Name: intent.py
 Author: guohui
 Mail: guohui1029@foxmail.com
 Created Time: 三 11/22 15:35:39 2017
 每3个短句进行预测，取top3，然后中间短句的预测值如果包含其中则是有效
'''
import sys
import fasttext
import json
reload(sys)
sys.setdefaultencoding("utf8")
'''
def preprocess():
    for line in sys.stdin:
        while "？ ？" in line or "? ?" in line:
            line = line.replace("？ ？", "？").replace("? ?", "?")
        line = line.replace("？\n", "").replace("?\n", "")
        line = line.strip()
        if line.count("？") + line.count("?") < 1:
            print line
preprocess()
'''

def true_data():
    true_value = list()
    for line in open("../data/first_part"):
        line_list = line.strip().split("\t")
        temp = line_list[:-2]
        for it in temp:
            if it == "":
                temp.remove(it)

        true_value.append(temp)
    return true_value
pm_query = list()
def pm_true_data():
    true_value = list()
    for line in open("../data/pm_test"):
        line_list = line.strip().split(" ")
        temp = line_list[:1]
        pm_query.append("".join(line_list[1:]))
        true_value.append(temp)

    return true_value

def generate_check_query(query):
    print "".join(query)
    check_query = list()
    for i, item in enumerate(query):
        if i == 0:
            check_query.append(item + query[i+1])
        elif i == len(query) - 1:
            check_query.append(query[i-1] + item)
        else:
            check_query.append(query[i-1] + item + query[i+1])
    return check_query

def select_proba(clf, query):
    temp = clf.predict_proba(query, 1)
    check_query = generate_check_query(query)
    check_temp = clf.predict_proba(check_query, 3)
    #print json.dumps(temp, ensure_ascii=False)
    #print json.dumps(check_temp, ensure_ascii=False)

    value = list()
    for item in temp:
        value.append(item[0])
    check_value = list()
    for item in check_temp:
        check_value.append(item[0][0] + item[1][0] + item[2][0])

    fp = sorted(value, key=lambda x: x[1], reverse=True)
    result = list()
    for i, item in enumerate(value):

        if item[1] > 0.7 and item[0] in check_value[i]:
            result.append(item[0])
    #防止result为空，候选备份的值
    if not result:
        result.append(fp[0][0])
    return result

def predict_mark():
    clf = fasttext.supervised("../data/mark_data_train", 'model', label_prefix='__label__', epoch=10)
    clf_b = fasttext.supervised("../data/train", 'model2', label_prefix='__label__', epoch=10)
    for line in sys.stdin:
        line_list = line.strip().split(" ")
        query = " ".join(line_list[1:])
        value = clf.predict([query], 1)[0][0]
        result = clf_b.predict([query], 1)[0][0]
        if result == "旅游体验" or result == "旅游方式":
            result = "旅游攻略"
        if result == "游玩项目":
            result = "景点"

        print "%s\t%s\t%s" % ("".join(line_list[1:]), value, result)


def predict():
    clf = fasttext.supervised("../data/mark_data_train", 'model', label_prefix='__label__', epoch=10)
    result = clf.test("../data/pm_test", k=1)

    predict_value = list()

    wf = open("../data/pm_valida", "w+")
    # for line in sys.stdin:
    with open('../data/pm_test', 'rb') as fr:
        for line in fr:
            pp = list()
            line = line.replace("?", "？")
            line_list = line.strip().split(" ")

            temp = " ".join(line_list[1:])
            query = temp.split("？")



            single = clf.predict([temp], 1)[0][0]

            #query.append(query[-2] + query[-1])
            #print json.dumps(query, ensure_ascii=False)
            if "" in query:
                query.remove("")
            key_word = ["什么", "是不是", "吗", "多少", "或", "神马", "呢", "经验", "哪", "那", "如何", "怎么样", "么","怎样", "是否"]

            tmp = query[-1]
            tmp_word = tmp.replace(" ", "")
            query.remove(query[-1])

            for key in key_word:
                if key in tmp_word:
                    query.append(tmp)
                    break
            if len(query) < 2:
                continue
            #if not query:
            #    query.append(tmp)
            #print json.dumps(query, ensure_ascii=False)
            result = select_proba(clf, query)
            item = [it.encode("utf8") for it in result]

            #去重
            item = list(set(item))
            #print json.dumps(pp, ensure_ascii=False)
            predict_value.append(item)
            if len(item) > 1:

                v =  single + "\t" +  json.dumps(item, ensure_ascii=False) + "\t" +"？".join(query)
                wf.write(v+ "\n")
    return predict_value


def calculate_value(true_value, predict_value):
    counter = 0
    i = 0
    for (tv, pv) in zip(true_value, predict_value):
        print json.dumps(tv, ensure_ascii=False) + "\t" + json.dumps(pv, ensure_ascii=False) #+ "\t" + pm_query[i]
        for it in tv:
            if it in pv:
                counter += 1
        i += 1
    tv_sum = sum(len(it) for it in true_value)
    pv_sum = sum(len(it) for it in predict_value)
    print counter, tv_sum, pv_sum
    print float(counter) / tv_sum, float(counter) / pv_sum

if __name__ == "__main__":
    #true_value = true_data()
    predict()
    #predict_value = predict_mark()
    #calculate_value(true_value, predict_value)
