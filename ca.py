import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ============= 设置全局字体为 Times New Roman =============
mpl.rcParams['font.family'] = 'Times New Roman'

# ============= 文件列表及标签，便于后续在循环中读取 =============
file_list = [
    "A1hrr.txt",
    "A2hrr.txt",
    "A3hrr.txt",
    "B1hrr.txt",
    "B2hrr.txt",
    "B3hrr.txt"
]
labels = [
    "A1",
    "A2",
    "A3",
    "B1",
    "B2",
    "B3"
]

def read_hrr_file(filename):
    """
    从指定文件中读取 (Crank, HR_Rate) 数据。
    跳过空行和以 '#' 开头的注释行。返回两个 numpy array：angle, hrr
    """
    angle_vals = []
    hrr_vals = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # 跳过空行或注释行
            if (not line) or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 2:
                # 解析浮点数
                ca = float(parts[0])
                hrr = float(parts[1])
                angle_vals.append(ca)
                hrr_vals.append(hrr)

    angle_vals = np.array(angle_vals)
    hrr_vals = np.array(hrr_vals)
    return angle_vals, hrr_vals


def trapezoidal_integration(angle, hrr):
    """
    采用梯形法对 hrr 进行数值积分，得到累计放热量 cumHR。
    假设 angle 单调递增。返回：cumHR (与 angle 同长度的数组)
    """
    cumHR = np.zeros_like(hrr)
    for i in range(1, len(angle)):
        dx = angle[i] - angle[i - 1]
        avg_val = 0.5 * (hrr[i] + hrr[i - 1])
        cumHR[i] = cumHR[i - 1] + avg_val * dx
    return cumHR


def find_CA_for_fraction(angle, cumHR, fraction):
    """
    在累计放热量曲线(cumHR)中查找达到 fraction (0~1) * totalHR 时的曲轴角。
    采用线性插值方式精细定位。
    """
    totalHR = cumHR[-1]
    target = fraction * totalHR

    if abs(totalHR) < 1e-12:
        # 几乎无热释放
        return angle[-1]

    idx = np.searchsorted(cumHR, target)
    if idx == 0:
        return angle[0]
    elif idx >= len(angle):
        return angle[-1]
    else:
        hr_low = cumHR[idx - 1]
        hr_high = cumHR[idx]
        angle_low = angle[idx - 1]
        angle_high = angle[idx]
        ratio = (target - hr_low) / (hr_high - hr_low) if (hr_high != hr_low) else 0.0
        return angle_low + ratio * (angle_high - angle_low)


def main():
    # 保存各工况的结果 (label, CA10, CA50, CA90)
    results = []

    # 创建画布
    plt.figure(figsize=(8, 6))

    for fname, label in zip(file_list, labels):
        # 1. 读取文件
        angle, hrr = read_hrr_file(fname)

        # 2. 积分得到累计放热量
        cumHR = trapezoidal_integration(angle, hrr)

        # 3. 计算 CA10, CA50, CA90（可根据需求改成 CA3, CA50, CA97）
        CA10 = find_CA_for_fraction(angle, cumHR, 0.10)
        CA50 = find_CA_for_fraction(angle, cumHR, 0.50)
        CA90 = find_CA_for_fraction(angle, cumHR, 0.90)

        totalHR = cumHR[-1]
        results.append((label, CA10, CA50, CA90, totalHR))

        # 4. 画出累计放热量曲线 (只显示 -80 到 60 范围内的数据)
        #   先做一个掩码筛选
        mask = (angle >= -80) & (angle <= 60)
        angle_masked = angle[mask]
        cumHR_masked = cumHR[mask]

        plt.plot(angle_masked, cumHR_masked, label=f"{label}")

    # 设置坐标轴范围：-80 ~ 60
    plt.xlim(-60, 40)

    plt.xlabel("Crank Angle (deg)", fontsize=12)
    plt.ylabel("Cumulative Heat Release", fontsize=12)
    plt.title("Cumulative HR Curves (-80 to 60 CA)", fontsize=14)

    # 去除网格
    # plt.grid(False)  # 默认就没有网格，也可以使用此行显式关闭

    plt.legend()
    plt.tight_layout()
    plt.show()

    # 输出数值结果
    print("==== CA10, CA50, CA90 统计结果 ====")
    print("工况  |   CA10     CA50     CA90     TotalHR")
    for (lb, c10, c50, c90, th) in results:
        print(f"{lb:<4s} | {c10:8.2f} {c50:8.2f} {c90:8.2f}  {th:10.4e}")


if __name__ == "__main__":
    main()
