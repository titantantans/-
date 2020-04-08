# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 00:39:09 2020

@author: user
"""
#忽略语句
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
df=pd.read_excel('D:/ciwei/项目练习5_奥运健儿数据分析/奥运运动员数据.xlsx')

#设置风格
import matplotlib.style as pst


#选出'age','height','weight','arm','leg'这些需要用到的字段
dff=df[['name','age','height','weight','arm','leg','gender']]
#选出的dff任一字段有缺失值都影响指标的判定,因此是对整个dff对象进行drona
dff.dropna(inplace=True)

#选出男女运动员
dffemale=dff[dff['gender']=='女']
dfmale=dff[dff['gender']=='男']

#分别制作男女运动员的各指标字段直方图
import matplotlib.pyplot as plt
dffemale[['age','height','weight','arm','leg']].hist(figsize=(12,10),bins=30,alpha=0.8,color='green')
plt.savefig('D:\\ciwei\\项目练习5_奥运健儿数据分析\\项目5\\female.jpg',dpi=400)

dfmale[['age','height','weight','arm','leg']].hist(figsize=(12,10),bins=30,alpha=0.8,color='green')
plt.savefig('D:\\ciwei\\项目练习5_奥运健儿数据分析\\项目5\\male.jpg',dpi=400)

#基本指数
dff['w/h**2']=dff['weight']/(dff['height']/100)**2
dff['l/h']=dff['leg']/dff['height']
dff['a/h']=dff['arm']/dff['height']
dff=dff[dff['l/h']<0.7]
dff=dff[dff['a/h']>0.7]
#指数计算方式
dff['BMI']=abs(dff['w/h**2']-22)#BMI指数越接近22越优秀
dff['LEG']=dff['l/h']#腿长身高比越大越优秀
dff['ARM']=abs(dff['a/h']-1)#臂长身高比越接近1越优秀
dff['AGE']=dff['age']#年龄越小越优秀
#指数标准化(Min-Max)
dff['BMI_NOR']=(dff['BMI'].max()-dff['BMI'])/(dff['BMI'].max()-dff['BMI'].min())
dff['ARM_NOR']=(dff['ARM'].max()-dff['ARM'])/(dff['ARM'].max()-dff['ARM'].min())
dff['AGE_NOR']=(dff['AGE'].max()-dff['AGE'])/(dff['AGE'].max()-dff['AGE'].min())
dff['LEG_NOR']=(dff['LEG']-dff['LEG'].min())/(dff['LEG'].max()-dff['LEG'].min())
#总分计算方式
dff['score']=(dff['BMI_NOR']+dff['AGE_NOR']+dff['ARM_NOR']+dff['LEG_NOR'])/4
#将DF按照总分进行降序排列
dff.sort_values(by='score',ascending=False,inplace=True)
#将index设为名字字段(作为堆叠面积图的X轴参数)
dff.index=dff['name']
#使用风格
pst.use('ggplot')
#绘制堆叠面积图
dff[['BMI_NOR','ARM_NOR','LEG_NOR','AGE_NOR']].plot.area(colormap='GnBu_r',alpha = 0.5,figsize=(10,6),title='运动员的身材综合指标判断')
plt.ylim([0,4])
plt.savefig('D:\\ciwei\\项目练习5_奥运健儿数据分析\\项目5\\运动员的身材综合指标判断.jpg',dpi=500)
#将Top8的运动员身材数据导出
dfff=dff[['ARM_NOR','AGE_NOR','LEG_NOR','BMI_NOR']][:8]
dfff.to_excel('D:\\ciwei\\项目练习5_奥运健儿数据分析\\项目5\\8个运动员数据.xlsx')






