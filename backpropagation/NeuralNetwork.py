# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

class NeuralNetwork:#神经网络大类
    def __init__(self):
        self._layers = []#获取网络层列表
    def add_layer(self ,layer):
        self._layers.append(layer)#追加网络层
    def feed_forword(self, r):#前向传播循环调用网络层对象前向计算函数
        for i in range(len(self._layers)):
            if i > 0 :
                r = self._layers[i-1].last_activation
                #r = np.mat(r)
            X = self._layers[i].activate(r)
        return X
    def backpropagation(self, X , y, learning_rate):#反向传播算法
        output = self.feed_forword(X)#获取前向计算的输出值
        for i in reversed(range(len(self._layers))):#反向循环
            layer = self._layers[i]#获取反向循环当前网络层对象
            #如果是输出层
            if layer == self._layers[-1]:
                layer.error = y -output#2分类任务均方差导数
                #关键：计算最后一层的delta
                layer.delta = layer.error * layer.apply_activation_derivative(output)
            #如果是隐藏层
            else:
                next_layer = self._layers[ i+1 ]
                layer.error = np.dot(next_layer.delta ,next_layer.weights.T)
                layer.delta = layer.error * layer.apply_activation_derivative(layer.last_activation)
        for i in range(len(self._layers)):
            layer = self._layers[i]
            # o_i 为上一网络层的输出
            o_i = np.atleast_2d(X if i == 0 else self._layers[i - 1].last_activation)
            # 梯度下降算法，delta 是公式中的负数，故这里用加号
            layer.weights += np.dot(o_i.T , layer.delta)* learning_rate
    def predict(self,X,y):#获取前向计算的输出值
        output = self.feed_forword(X)
        indexs = np.array(np.argmax(output,axis=1)).reshape(y.shape)
        result = indexs == y
        acc = np.sum(result != 0) / len(result)
        indexs = indexs.reshape(len(indexs),)
        return indexs,acc
    def one_hot(self,y):# one-hot 编码
        y_onehot = np.zeros((y.shape[0], 2))
        for i, j in zip(range(len(y)), y):
            y_onehot[i][j] = 1
        return y_onehot
    def decisionboundary(self ,X, y, y_, axes):#画出边界
        plt.plot(X[y_ == 0][:, 0], X[y_ == 0][:, 1], 'r.')
        plt.plot(X[y_ == 1][:, 0], X[y_ == 1][:, 1], 'b.')
        plt.grid()
        plt.axis(axes)
        svc = SVC(C=10)
        svc.fit(X, y)
        x0s = np.linspace(axes[0], axes[1], 200)
        x1s = np.linspace(axes[2], axes[3], 200)
        x0, x1 = np.meshgrid(x0s, x1s)
        X = np.c_[x0.ravel(), x1.ravel()]
        y_pred = svc.predict(X)
        y_pred = y_pred.reshape(x0.shape)
        plt.contourf(x0, x1, y_pred, cmap=plt.cm.brg, alpha=0.2)
        plt.show()
    def train(self, X_train, X_test, y_train, y_test, learning_rate, max_epochs):# 网络训练函数
        y_onehot = self.one_hot(y_train)
        Loss = []
        Accuracy = []
        output_lable = None
        for i in range(max_epochs+1):  # 训练 1000 个 epoch
            self.backpropagation(X_train, y_onehot, learning_rate)
            if i % 10 == 0:
            # 打印出 MSE Loss
                #mse = np.mean(np.square(y_onehot - self.feed_forword(X_train)))
                mse = np.mean(np.square(y_onehot - self._layers[-1].last_activation))
                Loss.append(mse)
                output_lable,accuracy = self.predict(X_test,y_test)# 统计并打印准确率
                print('Epoch: %s, Loss: %f Acc : %f' % (i, float(mse) , float(accuracy)))
                Accuracy.append(accuracy)
        plt.plot(np.arange(1, len(Loss) + 1), Loss)#展示MSE Loss
        plt.plot(np.arange(1, len(Accuracy) + 1), Accuracy)
        plt.show()
        return output_lable,Loss,Accuracy














