import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1) 设置全局字体为 Times New Roman
import matplotlib as mpl
mpl.rcParams["font.family"] = "Times New Roman"

# ----------------------------
# 2) 数据：A组 & B组
# ----------------------------
A_inj = np.array([-250, -225, -200])
A_RI  = np.array([417.98, 431.18, 334.98])
A_EIF = np.array([140.26, 131.68, 137.54])

B_inj = np.array([-30, -20, -10])
B_RI  = np.array([668.95, 379.55, 0.2614])
B_EIF = np.array([114.64, 111.50, 101.05])

# ----------------------------
# 3) 创建Figure: 1行2列子图
# ----------------------------
fig = plt.figure(figsize=(12,6))

ax1 = fig.add_subplot(1,2,1, projection='3d')
ax2 = fig.add_subplot(1,2,2, projection='3d')

# 
# =========== 美化函数 =============
#
def make_axis_clean(ax):
    """
    去除 3D 轴面的网格、边框，使背景透明或无边线
    """
    # 1) pane背景透明
    ax.xaxis.pane.set_facecolor((1,1,1,0))  # facecolor alpha=0 =>透明
    ax.yaxis.pane.set_facecolor((1,1,1,0))
    ax.zaxis.pane.set_facecolor((1,1,1,0))

    # 2) pane边框颜色隐藏
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')


 

# --------------------------------------
# 4) 在 ax1 上画 A 组
# --------------------------------------
ax1.plot3D(
    A_inj, A_RI, A_EIF,
    marker='o',
    markersize=8,
    linewidth=2,
    alpha=0.7,           # 半透明
    color='tab:blue',
    label="Group A"
)
ax1.set_xlabel("Timing (°CA)")
ax1.set_ylabel("RI (MW/m$^2$)")
ax1.set_zlabel("EIFSC (g/(kW·h))")
ax1.set_title("A Group", pad=10)
ax1.legend()

# 美化
make_axis_clean(ax1)

# 手动减少刻度数量 (示例)
ax1.set_xticks(A_inj)  # 让X轴只显示A_inj对应的刻度
# 根据情况你也可以设置Y, Z轴刻度

# --------------------------------------
# 5) 在 ax2 上画 B 组
# --------------------------------------
ax2.plot3D(
    B_inj, B_RI, B_EIF,
    marker='s',
    markersize=8,
    linewidth=2,
    alpha=0.7,           # 半透明
    color='tab:red',
    label="Group B"
)
ax2.set_xlabel("Timing (°CA)")
ax2.set_ylabel("RI (MW/m$^2$)")
ax2.set_zlabel("EIFSC (g/(kW·h))")
ax2.set_title("B Group", pad=10)
ax2.legend()

# 美化
make_axis_clean(ax2)
ax2.set_xticks(B_inj)

# --------------------------------------
# 6) 布局 & 显示
# --------------------------------------
plt.tight_layout()
plt.show()
