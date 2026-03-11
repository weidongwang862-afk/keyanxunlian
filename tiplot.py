import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 工况名称
cases = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

# 结果数据
dp_dt_max = [53.79, 54.39, 48.25, 69.04, 52.19, 1.48]  # (dp/dt)max
P_max = [27.57, 27.81, 27.31, 25.70, 25.33, 20.64]  # P_max (MPa)
RI = [417.98, 431.18, 334.98, 668.95, 379.55, 0.26]  # Ringing Intensity (RI)

# 设置柱状图的宽度
barWidth = 0.35

# 创建图形
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制 (dp/dt)max 和 P_max 的柱状图
hold_on = ax1.bar(np.arange(len(cases)) - barWidth/2, dp_dt_max, barWidth, label='(dp/dt)max', color='skyblue')

# 绘制 P_max 的柱状图
bars2 = ax1.bar(np.arange(len(cases)) + barWidth/2, P_max, barWidth, label='P_max', color='orange', alpha=0.7)

# 设置标题和标签
ax1.set_title('Comparison of (dp/dt)max, P_max, and Ringing Intensity (RI)', fontsize=14)
ax1.set_xlabel('Cases', fontsize=12)
ax1.set_ylabel('(dp/dt)max (MPa/°CA) and P_max (MPa)', fontsize=12)
ax1.set_xticks(np.arange(len(cases)))
ax1.set_xticklabels(cases, fontsize=12)

# 设置左侧 y 轴范围，确保所有柱状图都可见
ax1.set_ylim([0, 75])

# 去除网格
ax1.grid(False)

# 绘制 RI 的折线图（右侧 y 轴）
ax2 = ax1.twinx()
ax2.plot(np.arange(len(cases)), RI, '-o', color='red', label='RI', linewidth=2, markersize=6, markerfacecolor='red')

# 设置右侧 y 轴标签和范围
ax2.set_ylabel('Ringing Intensity (RI)', fontsize=12)
ax2.set_ylim([0, 700])

# 添加图例
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

# 优化图形布局
plt.tight_layout()
plt.show()
