#!/user/bin/env python
#_*_coding:utf-8_*_
import string
import json
from datetime import datetime, timedelta
import fasttext

print string.punctuation

list = ['a,','b!','cj!/n']
item=[]
for i in list:
    i =i.strip(string.punctuation)
    item.append(i)
print item

dict_={'a':2,
      'b':1,'c':3}
t = sorted(dict_.iteritems(),key=lambda x:x[0],reverse=False)
for t1 in t:
    print t1[0] + '\t' + str(t1[1])

for _ in range(5):
    for _ in range(3):
        break
    print 'test'