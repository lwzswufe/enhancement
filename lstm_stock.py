# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
'''
Build a tweet sentiment analyzer
'''

# -*- coding:utf-8 -*-
import numpy as np
import theano
import theano.tensor as T
import operator
import time


class LSTM_Theano:
   def  __init__(self, word_dim, hidden_dim=128, bptt_truncate=-1):

       #初始化参数
       self.word_dim=word_dim
       self.hidden_dim=hidden_dim
       self.bptt_truncate=bptt_truncate
       E=np.random.uniform(-np.sqrt(1./word_dim), np.sqrt(1./word_dim), (hidden_dim, word_dim))
       U = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (4, hidden_dim, hidden_dim))
       W = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (4, hidden_dim, hidden_dim))
       V = np.random.uniform(-np.sqrt(1./hidden_dim), np.sqrt(1./hidden_dim), (word_dim, hidden_dim))
       b = np.zeros((4, hidden_dim))
       c = np.zeros( word_dim)


       # Theano: 产生 shared variables
       self.E = theano.shared(name='E', value=E.astype(theano.config.floatX))
       self.U = theano.shared(name='U', value=U.astype(theano.config.floatX))
       self.W = theano.shared(name='W', value=W.astype(theano.config.floatX))
       self.V = theano.shared(name='V', value=V.astype(theano.config.floatX))
       self.b = theano.shared(name='b', value=b.astype(theano.config.floatX))
       self.c = theano.shared(name='c', value=c.astype(theano.config.floatX))

        # SGD / 使用rmsprop提供的参数
       self.mE = theano.shared(name='mE', value=np.zeros(E.shape).astype(theano.config.floatX))
       self.mU = theano.shared(name='mU', value=np.zeros(U.shape).astype(theano.config.floatX))
       self.mV = theano.shared(name='mV', value=np.zeros(V.shape).astype(theano.config.floatX))
       self.mW = theano.shared(name='mW', value=np.zeros(W.shape).astype(theano.config.floatX))
       self.mb = theano.shared(name='mb', value=np.zeros(b.shape).astype(theano.config.floatX))
       self.mc = theano.shared(name='mc', value=np.zeros(c.shape).astype(theano.config.floatX))
       self.theano = {}
       self.__theano_build__()


   def __theano_build__(self):
           E, U, W, V , b, c = self.E, self.U, self.W, self.V, self.b, self.c
           x = T.ivector('x')
           y = T.ivector('y')
           #前馈神经网络
           def forward_prop_step(x_t, s_prev,c_prev):
               #word embedding层
               x_e = E[:,x_t]

               #LSTM_layer
               i=T.nnet.hard_sigmoid(U[0].dot(x_e)+W[0].dot(s_prev)+b[0])
               f=T.nnet.hard_sigmoid(U[1].dot(x_e)+W[1].dot(s_prev)+b[1])
               o=T.nnet.hard_sigmoid(U[2].dot(x_e)+W[2].dot(s_prev)+b[2])
               g=T.tanh(U[3].dot(x_e)+W[3].dot(s_prev)+b[3])
               c_t=c_prev*f+g*i
               s_t=T.tanh(c_t)*o

               #计算输出层结果
               o_t = T.nnet.softmax(V.dot(s_t) + c)[0]
               return [o_t,s_t,c_t]

           [o,s,c_o],updates=theano.scan(
               forward_prop_step,
               sequences=x,
               truncate_gradient=self.bptt_truncate,
               outputs_info=[None,
                             dict(initial=T.zeros(self.hidden_dim)),


                             dict(initial=T.zeros(self.hidden_dim))]
           )
           prediction = T.argmax(o, axis=1)
           o_error = T.sum(T.nnet.categorical_crossentropy(o, y))
           #计算总代价（当然可以加上规范化因子）
           cost = o_error

            #计算梯度
           dE = T.grad(cost, E)
           dU = T.grad(cost, U)
           dW = T.grad(cost, W)
           db = T.grad(cost, b)
           dV = T.grad(cost, V)
           dc = T.grad(cost, c)

           self.predict = theano.function([x], o)
           self.predict_class = theano.function([x], prediction)
           self.ce_error = theano.function([x, y], cost)
           self.bptt = theano.function([x, y], [dE, dU, dW, db, dV, dc])


           # 随机梯度下降参数
           learning_rate = T.scalar('learning_rate')
           decay = T.scalar('decay')
           # rmsprop cache 更新
           mE = decay * self.mE + (1 - decay) * dE ** 2
           mU = decay * self.mU + (1 - decay) * dU ** 2
           mW = decay * self.mW + (1 - decay) * dW ** 2
           mV = decay * self.mV + (1 - decay) * dV ** 2
           mb = decay * self.mb + (1 - decay) * db ** 2
           mc = decay * self.mc + (1 - decay) * dc ** 2

            #梯度下降更新参数
           self.sgd_step = theano.function(
            [x, y, learning_rate, theano.Param(decay, default=0.9)],
            [],
            updates=[(E, E - learning_rate * dE / T.sqrt(mE + 1e-6)),
                     (U, U - learning_rate * dU / T.sqrt(mU + 1e-6)),
                     (W, W - learning_rate * dW / T.sqrt(mW + 1e-6)),
                     (V, V - learning_rate * dV / T.sqrt(mV + 1e-6)),
                     (b, b - learning_rate * db / T.sqrt(mb + 1e-6)),
                     (c, c - learning_rate * dc / T.sqrt(mc + 1e-6)),
                     (self.mE, mE),
                     (self.mU, mU),
                     (self.mW, mW),
                     (self.mV, mV),
                     (self.mb, mb),
                     (self.mc, mc)
                    ])

   def calculate_total_loss(self, X, Y):
       return np.sum([self.ce_error(x,y) for x,y in zip(X,Y)])

   def calculate_loss(self, X, Y):
       # Divide calculate_loss by the number of words
       num_words = np.sum([len(y) for y in Y])
       return self.calculate_total_loss(X,Y)/float(num_words)




