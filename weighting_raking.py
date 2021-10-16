#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weighting_program
Created on Sat Oct 16 10:38:05 2021

@author: liang-yi
以109.12內政部戶政司釋出之人口資料為底冊
"""

import os
import pandas as pd
import numpy as np
#from instrument.instrument import *
from collections import Counter
from scipy.stats import chisquare
from decimal import Decimal, ROUND_HALF_UP

os.chdir(os.getcwd())

#### 先準備母體底冊
# 性別：女0男1
sexN = pd.Series([0.504, 0.496], index=[0, 1])
# 年齡：20-29: 1; 30-39: 2; 40-49: 3, 50-59: 4; 60以上: 5  
ageN = pd.Series([0.16, 0.18, 0.19, 0.19, 0.28], index=[1, 2, 3, 4, 5])
# 教育程度: 國小及以下: 1; 國、初中: 2; 高中、職: 3, 大專: 4, 研究所及以上: 5
eduN = pd.Series([0.12, 0.12, 0.28, 0.4, 0.08], index=[1, 2, 3, 4, 5])
# 地區: 北北基-1; 桃竹苗-2; 中彰投-3; 雲嘉南-4; 高屏-5; 宜花東-6; 澎金連-7
areaN = pd.Series([0.3, 0.16, 0.19, 0.14, 0.15, 0.04, 0.01], index=[1, 2, 3, 4, 5, 6, 7])

### 新增權值變項'weight'
def add_weight(df):
    '''
    Parameters
    ----------
    df : pandas Dataframe
        欲處理的資料檔.

    Returns
    -------
    df新增權值變項weight(pandas Series).
    '''
    df['weight'] = 1 # 原始權值為1（保護遺漏值）
    print('Build up the weight variable successfuly.')

# def missing_v(df, value = []) -> list:
#     '''
#     Parameters
#     ----------
#     df : pandas Dataframe
#          欲處理的資料檔.
#     value : list, optional
#         遺漏值清單. The default is [].

#     Returns
#     -------
#     list
#         遺漏值清單.

#     '''
    


### 正確四捨五入至整數函式
def roundupN(num:float):
    out = Decimal(str(num)).quantize(0, ROUND_HALF_UP)
    return int(out)


### 加權樣本比例計算
def n_N(df, var:str, value:int, loss=[-1]) -> tuple:
    """
    Parameters
    ----------
    df : pandas Dataframe
        資料檔.
    var : str
        欲計算的變項.
    value : int
        欲計算的值.
    loss : TYPE, optional
        遺漏值. The default is [-1].

    Returns
    -------
    tuple
        （ni樣本佔比, n排除遺漏值後總樣本數).
    """
    # 變項i樣本佔比ni
    ni = roundupN(sum(df[(df[var] == value)]['weight']))
    # drop遺漏值後的樣本總數n
    n = df
    # for i in n.index:
    #     if n[var].loc[i] in loss:
    #         n= n.drop(index=i)
    n = sum(n[(~n[var].isin(loss))]['weight'])
    
    return (ni, n)

### 卡方檢定函式
def chi_test(df, var:str, sex_na = [-1], age5_na = [-1], edu_na = [-1], area_na = [-1]) -> bool:
    if var == 'SEX':
        n = pd.Series([n_N(df, 'SEX', 0, sex_na)[0],
                       n_N(df, 'SEX', 1, sex_na)[0]],
                      index=[0,1])
        N = sexN * roundupN(sum(df[(~df['SEX'].isin(sex_na))]['weight']))
        
        chi2, p = chisquare(n, f_exp= N)
        if p < 0.05:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, sex與母體不一致')
            return False
        else:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, sex與母體一致')
            return True
    
    if var == 'AGE5':
        n = pd.Series([n_N(df, 'AGE5', 1, age5_na)[0],
                       n_N(df, 'AGE5', 2, age5_na)[0],
                       n_N(df, 'AGE5', 3, age5_na)[0],
                       n_N(df, 'AGE5', 4, age5_na)[0],
                       n_N(df, 'AGE5', 5)[0]],
                      index=[1,2,3,4,5])
        N = ageN * roundupN(sum(df[(~df['AGE5'].isin(age5_na))]['weight']))
        
        chi2, p = chisquare(n, f_exp= N)
        if p < 0.05:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, age與母體不一致')
            return False
        else:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, age與母體一致')
            return True
    
    if var == 'EDU':
        n = pd.Series([n_N(df, 'EDU', 1, edu_na)[0],
                       n_N(df, 'EDU', 2, edu_na)[0],
                       n_N(df, 'EDU', 3, edu_na)[0],
                       n_N(df, 'EDU', 4, edu_na)[0],
                       n_N(df, 'EDU', 5, edu_na)[0]],
                      index=[1,2,3,4,5])
        N = eduN * roundupN(sum(df[(~df['EDU'].isin(edu_na))]['weight']))
        
        chi2, p = chisquare(n, f_exp= N)
        if p < 0.05:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, edu與母體不一致')
            return False
        else:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, edu與母體一致')
            return True
    
    if var == 'AREA':
        n = pd.Series([n_N(df, 'AREA', 1, area_na)[0],
                       n_N(df, 'AREA', 2, area_na)[0],
                       n_N(df, 'AREA', 3, area_na)[0],
                       n_N(df, 'AREA', 4, area_na)[0],
                       n_N(df, 'AREA', 5, area_na)[0],
                       n_N(df, 'AREA', 6, area_na)[0],
                       n_N(df, 'AREA', 7, area_na)[0]],
                      index=[1,2,3,4,5,6,7])
        N = areaN * roundupN(sum(df[(~df['AREA'].isin(edu_na))]['weight']))
        
        chi2, p = chisquare(n, f_exp= N)
        if p < 0.05:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, area與母體不一致')
            return False
        else:
            print(f'p = {round(p, 3)}, chi2 = {round(chi2, 1)}, area與母體一致')
            return True


### 正式raking
def raking_w(df, sex_na = [-1], age5_na = [-1], edu_na = [-1], area_na = [-1]):
    add_weight(df)
    c = 1
    while (chi_test(df, 'SEX', sex_na) != True) or (chi_test(df, 'AGE5', age5_na) != True) or (chi_test(df, 'EDU', edu_na) != True) or (chi_test(df, 'AREA', area_na) != True):
            print(f'第 {c} 輪加權')
    
            if chi_test(df, 'SEX', sex_na) != True:
                n0 = n_N(df, 'SEX', 0, sex_na)[0]
                n1 = n_N(df, 'SEX', 1, sex_na)[0]
                n = n_N(df, 'SEX', 0, sex_na)[1]
                
                for i in df.index:
                    if df['SEX'].loc[i] == 0:
                        df['weight'].loc[i] = df['weight'].loc[i] * sexN.loc[0] * n/n0
                    if df['SEX'].loc[i] == 1:
                        df['weight'].loc[i] = df['weight'].loc[i] * sexN.loc[1] * n/n1
                c += 1
                continue
            
            if chi_test(df, 'AGE5') != True:
                n1 = n_N(df, 'AGE5', 1, age5_na)[0]
                n2 = n_N(df, 'AGE5', 2, age5_na)[0]
                n3 = n_N(df, 'AGE5', 3, age5_na)[0]
                n4 = n_N(df, 'AGE5', 4, age5_na)[0]
                n5 = n_N(df, 'AGE5', 5, age5_na)[0]
                n = n_N(df, 'AGE5', 0, age5_na)[1]
                
                for i in df.index:
                    if df['AGE5'].loc[i] == 1:
                        df['weight'].loc[i] = df['weight'].loc[i] * ageN.loc[1] * n/n1
                    if df['AGE5'].loc[i] == 2:
                        df['weight'].loc[i] = df['weight'].loc[i] * ageN.loc[2] * n/n2
                    if df['AGE5'].loc[i] == 3:
                        df['weight'].loc[i] = df['weight'].loc[i] * ageN.loc[3] * n/n3
                    if df['AGE5'].loc[i] == 4:
                        df['weight'].loc[i] = df['weight'].loc[i] * ageN.loc[4] * n/n4
                    if df['AGE5'].loc[i] == 5:
                        df['weight'].loc[i] = df['weight'].loc[i] * ageN.loc[5] * n/n5
                c += 1
                continue
            
            if chi_test(df, 'EDU', edu_na) != True:
                n1 = n_N(df, 'EDU', 1, edu_na)[0]
                n2 = n_N(df, 'EDU', 2, edu_na)[0]
                n3 = n_N(df, 'EDU', 3, edu_na)[0]
                n4 = n_N(df, 'EDU', 4, edu_na)[0]
                n5 = n_N(df, 'EDU', 5, edu_na)[0]
                n = n_N(df, 'EDU', 0, edu_na)[1]
                
                for i in df.index:
                    if df['EDU'].loc[i] == 1:
                        df['weight'].loc[i] = df['weight'].loc[i] * eduN.loc[1] * n/n1
                    if df['EDU'].loc[i] == 2:
                        df['weight'].loc[i] = df['weight'].loc[i] * eduN.loc[2] * n/n2
                    if df['EDU'].loc[i] == 3:
                        df['weight'].loc[i] = df['weight'].loc[i] * eduN.loc[3] * n/n3
                    if df['EDU'].loc[i] == 4:
                        df['weight'].loc[i] = df['weight'].loc[i] * eduN.loc[4] * n/n4
                    if df['EDU'].loc[i] == 5:
                        df['weight'].loc[i] = df['weight'].loc[i] * eduN.loc[5] * n/n5
                c += 1
                continue
            
            if chi_test(df, 'AREA') != True:
                n1 = n_N(df, 'AREA', 1, area_na)[0]
                n2 = n_N(df, 'AREA', 2, area_na)[0]
                n3 = n_N(df, 'AREA', 3, area_na)[0]
                n4 = n_N(df, 'AREA', 4, area_na)[0]
                n5 = n_N(df, 'AREA', 5, area_na)[0]
                n6 = n_N(df, 'AREA', 6, area_na)[0]
                n7 = n_N(df, 'AREA', 7, area_na)[0]
                n = n_N(df, 'AREA', 0, area_na)[1]
                
                for i in df.index:
                    if df['AREA'].loc[i] == 1:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[1] * n/n1
                    if df['AREA'].loc[i] == 2:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[2] * n/n2
                    if df['AREA'].loc[i] == 3:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[3] * n/n3
                    if df['AREA'].loc[i] == 4:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[4] * n/n4
                    if df['AREA'].loc[i] == 5:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[5] * n/n5
                    if df['AREA'].loc[i] == 6:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[6] * n/n6
                    if df['AREA'].loc[i] == 7:
                        df['weight'].loc[i] = df['weight'].loc[i] * areaN.loc[7] * n/n7
                c += 1
                continue
    return df.to_csv('加權後資料檔.csv', encoding='utf_8_sig', index = False)

if __name__ == '__main__':
    df = pd.read_csv('0924_all_weighted.csv')
    raking_w(df)





