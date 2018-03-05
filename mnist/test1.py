#!/user/bin/env python
#_*_coding:utf-8_*_
import tensorflow as tf
a = tf.constant([1.0,2.0],name='a')
b = tf.constant([2.0,3.0],name='b')
result = a + b

#通过a.graph可以查看张量所属的计算图，因为没有特意指定，所以这个计算图应该是默认的计算图
print(a.graph is tf.get_default_graph())

w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
sess = tf.Session()
sess.run(w1.initializer)
print sess.run(w1)

v = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
with tf.Session() as sess:
    print tf.clip_by_value(v, 2.5, 4.5).eval()
    print tf.log(v).eval()

b = tf.Variable(tf.zeros([10]))
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
print b.eval(session=sess)