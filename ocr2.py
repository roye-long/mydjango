# !/bin/python env
# -*- coding:gbk -*-
import numpy as np
from sklearn.externals import joblib
from vc import *
import os
#计算位置附近的黑点数
class OCR(object):
    tableDict = {}
    threshold=140    #灰度处理 如 150
    noiseSize=2    #噪点间隔 如 2
    rangeSize=1    #随机 如 1
    splitThreshold=5 # 图片切割，像素分隔值
    targetNum=4 # 图片强制分割 ，分割成几部分的值
    wdith=30 #标准化图片宽
    high=30 #标准化图片高
    model=None
    def __new__(cls,modelFile):
        cls.model = joblib.load(modelFile)
        return super(OCR, cls).__new__(cls)
    def __del__(self):
        return None
 
    def getFeature(self,imgs):
        feature=[]
        for img in imgs:
            fe=img.getdata()
            feature.append(fe)
        return feature
    def predict(self,features):
        lablist=[]
        result=''
        for xt in features:
            data=np.array(xt).reshape((1,-1))
            p_label=self.__class__.model.predict(data)
            if int(p_label[0])<=9:
                lab=int(p_label[0])
            else :
                 lab=chr(int(p_label[0]))
            lablist.append(lab)
        for label in lablist:
            result+=str(label)
        return result
    
    def run(self, img):
        standar = standard(zoom(binarization(zoom(split(img), self.__class__.wdith), self.__class__.threshold), self.__class__.wdith), self.__class__.wdith)
        feature = self.getFeature(standar)
        return self.predict(feature)
