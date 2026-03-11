import numpy as np
import matplotlib.pyplot as plt

# 文件列表及标签
pressure_files = ['A1.txt', 'A2.txt', 'A3.txt', 'B1.txt', 'B2.txt', 'B3.txt']
hrr_files = ['A1hrr.txt', 'A2hrr.txt', 'A3hrr.txt', 'B1hrr.txt', 'B2hrr.txt', 'B3hrr.txt']
case_labels = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

# 定义绘图的曲轴角范围（例如从进气门关闭 -131° 到 360°）
lower_threshold = -100
upper_threshold = 50

# 创建图形和两个 y 轴
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.set_xlabel('Crank Angle (°)')
ax1.set_ylabel('Pressure (MPa)', color='blue')
ax1.grid(True)

# 创建第二个 y 轴共享 x 轴
ax2 = ax1.twinx()
ax2.set_ylabel('HRR (J/°CA)', color='red')

# 循环读取并绘制数据
for p_file, h_file, label in zip(pressure_files, hrr_files, case_labels):
    # 读取压力数据：假设文件第一行为注释
    p_data = np.loadtxt(p_file, skiprows=1, comments='#')
    # 筛选出曲轴角在 lower_threshold 到 upper_threshold 范围内的数据
    mask_p = (p_data[:, 0] >= lower_threshold) & (p_data[:, 0] <= upper_threshold)
    p_filtered = p_data[mask_p]
    crank_p = p_filtered[:, 0]
    pressure = p_filtered[:, 1]
    
    # 读取 HRR 数据，同样假设第一行为注释
    h_data = np.loadtxt(h_file, skiprows=1, comments='#')
    mask_h = (h_data[:, 0] >= lower_threshold) & (h_data[:, 0] <= upper_threshold)
    h_filtered = h_data[mask_h]
    crank_h = h_filtered[:, 0]
    hrr = h_filtered[:, 1]
    
    # 绘制压力曲线（实线，蓝色）
    ax1.plot(crank_p, pressure, label=label + ' Pressure', linewidth=1.5)
    # 绘制 HRR 曲线（虚线，红色）
    ax2.plot(crank_h, hrr, label=label + ' HRR', linewidth=1.5, linestyle='--')

# 合并图例：获取两个轴的图例句柄和标签，然后合并显示
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

plt.title('Pressure and HRR Curves for 6 Cases')
plt.show()
