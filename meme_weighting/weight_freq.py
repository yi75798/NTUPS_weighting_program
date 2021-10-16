#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weight_freq
Created on Sat Oct 16 18:00:57 2021
@author: liang-yi
計算加權後次數分配或將其結果輸出為圖檔
"""
import os
os.chdir(os.getcwd())
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### 加權後次數分配表
def freq_w(df, var, w='weight'):
    '''
    Parameters
    ----------
    df : pandas Dataframe
        含權值變項的資料檔.
    var : str
        欲檢視次數分配的變項.
    w : str, optional
        權值變項. The default is 'weight'.

    Returns
    -------
    df_temp : panda Dataframe
        次數分配表之Dataframe.
    '''
    a = pd.Series(df[[var, w]].groupby(var).sum()[w]) / df[w].sum()
    b = a.index
    c = a.values.round(3)
    d = round(df[[var, w]].groupby(var).sum()[w])
    df_temp = pd.DataFrame({'Label': b, 'Num': d, 'Freq': c})
    return df_temp

### 輸出成圖檔
def freq_w_fig(freq_df, title=""):
    '''
    Parameters
    ----------
    freq_df : pandas Dataframe
        加權後次數分配表.
    title : str, optional
        表格標題. The default is "".

    Returns
    -------
    在當前路徑儲存為png檔.

    '''
    plt.figure(dpi = 150)
    ax = plt.axes(frame_on = False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_title(title)
    pd.plotting.table(ax, freq_df, loc='center')
    plt.savefig('fig_'+title)




