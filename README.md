# NTUPS_weighting_program
Weighting program for Taiwanese Meme survey.

## Project 說明：
加權程式及加權後次數分配計算程式。

加權目前僅有「多變數反覆加權法(Raking)」，以109年12月內政部戶政司釋出之性別、年齡、教育、地區資料為底冊。
僅提供一次raking四個變項，自由決定加權變項功能待開發...

次數分配計算程式，可產生次數分配表之dataframe，並可選擇將其輸出為png檔。

## 使用方法：
1. 下載meme_weighting資料夾，與處理資料的主程式置於同一目錄下。
2. 在主程式中輸入下列語法 `from meme_weighting.weighting_racking import *` 、 `from meme_weighting.weight_freq import *`

#### 資料檔變數要求（大小寫均要符合）：
1. 性別變項以SEX命名： 男1女0
2. 年齡變項為5分類以AGE5命名： 20-29:1, 30-39:2, 40-49:3, 50-59:4, 60及以上:5
3. 教育程度變項以EDU命名： 國小及以下:1, 國初中:2, 高中職:3, 大專:4, 研究所及以上:5
4. 地區變項採7大地理區以AREA命名： 北北基:1; 桃竹苗:2; 中彰投:3; 雲嘉南:4; 高屏:5; 宜花東:6; 澎金連:7
5. 遺漏值均變碼為-1

## raking_w function
`raking_w(df, sex_na = [-1], age5_na = [-1], edu_na = [-1], area_na = [-1])`  

Parameters:
1. df: pandas Dataframe 欲加權的資料
2. sex_na: list 性別變項遺漏值與無反應選項 ex. [-1, 97, 98, 99]
3. age5_na: list 教育變項遺漏值與無反應選項
4. edu_na: list 教育變項遺漏值與無反應選項
5. area_na: list 地區變項遺漏值與無反應選項

Return:
在原資料檔Dataframe先增權值欄位weight

## freq_w function
`freq_w(df, var, w='weight')`  

Parameters:
1. df: pandas Dataframe 含權值變數的資料
2. var: str 欲檢視次數分配的變項
3. w: str 權值變數，預設為weight

Return:
加權後次數分配表之Dataframe

## freq_w_fig function
`freq_w_fig(freq_df, title="")`  

Parameter:
1. freq_df: pandas Dataframe 加權後次數分配表
2. title: str 圖表標題

Return:
在當前路徑輸出次數分配表的png檔
`freq_w(df, var, w='weight')`路
`freq_w(df, var, w='weight')`
