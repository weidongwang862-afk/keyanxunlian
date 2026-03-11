import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (6, 4)     # 图像宽 6 英寸、高 4 英寸
plt.rcParams['savefig.dpi']    = 150     # 输出分辨率
plt.rcParams['figure.dpi']     = 150
plt.rcParams['font.sans-serif'] = ['Arial'] # 字体可根据需求修改
plt.rcParams['axes.unicode_minus'] = False  # 使负号正常显示
# 背景色设为白色，不留大空白
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor']   = 'white'

import numpy as np
import matplotlib.pyplot as plt

# 文件列表和对应标签
file_list = ['A1.txt', 'A2.txt', 'A3.txt', 'B1.txt', 'B2.txt', 'B3.txt']
label_list = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

# 定义下限和上限
lower_threshold = -80 # 例如，进气门关闭时刻
upper_threshold = 50# 例如，到整个工作循环结束

plt.figure(figsize=(10,6))
plt.title('Pressure Curves from Intake Valve Closure')
plt.xlabel('Crank Angle (°)')
plt.ylabel('Pressure (MPa)')
plt.grid(True)

# 循环读取每个文件，并根据下限和上限筛选数据
for file, label in zip(file_list, label_list):
    # 读取数据，跳过第一行注释
    data = np.loadtxt(file, skiprows=1, comments='#')
    
    # 筛选出曲轴角在 lower_threshold 与 upper_threshold 之间的数据
    mask = (data[:, 0] >= lower_threshold) & (data[:, 0] <= upper_threshold)
    filtered_data = data[mask]
    
    # 提取曲轴角和压力数据
    crank = filtered_data[:, 0]
    pressure = filtered_data[:, 1]
    
    # 绘制曲线
    plt.plot(crank, pressure, label=label, linewidth=0.5)

plt.legend(loc='best')
plt.show()
