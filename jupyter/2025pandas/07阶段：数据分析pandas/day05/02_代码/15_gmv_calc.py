import pandas as pd
import os
data_dir = 'C:/Develop/深圳42/data/report/'
final_df = pd.DataFrame()
for file_name in os.listdir(data_dir):
    df = pd.read_excel(data_dir+file_name,parse_dates=[0])
    # 新建一列, 销售额
    df['销售额'] = df['访客数']*df['转化率']*df['客单价']
    # 筛选2023年的数据
    df['年份'] = df['日期'].dt.year
    df_2023 = df[df['年份']==2023]
    # 统计每个品牌的23年的总销售额
    result_df = df_2023.groupby(['品牌'],as_index=False)['销售额'].sum()
    result_df['类目'] = file_name.replace('.xlsx','')
    final_df = pd.concat([final_df,result_df])

result = final_df.groupby(['品牌'],as_index=False)['销售额'].sum().sort_values('销售额',ascending=False)
result.to_excel('C:/Develop/深圳42/data/2023年总销售额.xlsx',index=False)