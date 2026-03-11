import numpy as np
import pandas as pd

file_list = ['A1.txt', 'A2.txt', 'A3.txt', 'B1.txt', 'B2.txt', 'B3.txt']
label_list = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

# 1) 读取所有数据到一个 dict
data_dict = {}
for i, file in enumerate(file_list):
    raw = np.loadtxt(file, skiprows=1)
    crank = raw[:,0]
    pressure = raw[:,1]
    # 存到 dict
    data_dict[label_list[i]] = pd.Series(data=pressure, index=crank)

# 2) 合并成一个 DataFrame, 以 crank angle 为统一索引
#   注意: A1, A2 这些文件可能 crank 角步长相同or略有差异
df = pd.DataFrame(data_dict)

# df 的行索引是一串综合了所有工况的 crank angle，会自动对齐
# 如果都一样就完美对齐，如果略有差异，会NaN对齐

# 3) 如果你只想保留某个区间 [theta_min, theta_max], 先切片
theta_min = -150
theta_max = 180

# 先把df索引重命名成 float, 并 sort
df.index = df.index.astype(float)
df = df.sort_index()

# 切片
df_slice = df.loc[theta_min:theta_max]

# 4) 输出到 CSV => 'merged.csv'
df_slice.to_csv('merged_data.csv', index_label='CrankAngle')

# 也可以输出为 Excel XLSX，需要安装 openpyxl:
# df_slice.to_excel('merged_data.xlsx', index_label='CrankAngle')
