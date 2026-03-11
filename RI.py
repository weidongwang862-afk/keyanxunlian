import numpy as np

# 计算 dp/dt 和 Ringing Intensity (RI)
def calculate_RI(pressure_data, crank_angle, temperature_data, gamma=1.4, R=8.314):
    """
    计算给定压力数据的最大压力变化率 (dp/dt)max 和最大压力 P_max，并计算敲缸倾向 RI
    """
    # 计算 dp/dt（压力变化率）
    dp_dt = np.gradient(pressure_data, crank_angle)  # 使用 np.gradient 计算 dp/dt
    
    # 获取 (dp/dt) 的最大值
    dp_dt_max = np.max(dp_dt)
    
    # 获取最大压力
    P_max = np.max(pressure_data)
    
    # 获取最大温度
    T_max = np.max(temperature_data)  # 从温度数据中获取最大温度
    
    # 计算敲缸倾向（Ringing Intensity, RI）
    RI = (1000 / (2 * gamma)) * (0.05 * dp_dt_max)**2 * (P_max / np.sqrt(gamma * R * T_max))
    
    return dp_dt_max, P_max, T_max, RI

# 读取压力数据文件
def load_pressure_data(filename):
    """
    从 txt 文件中加载压力数据，假设文件格式为 'Crank' 和 'Pressure' 列
    """
    data = np.loadtxt(filename, skiprows=1)  # 跳过第一行标题
    crank_angle = data[:, 0]  # 曲轴角度（°CA）
    pressure_data = data[:, 1]  # 压力数据（MPa）
    return crank_angle, pressure_data

# 读取温度数据文件
def load_temperature_data(filename):
    """
    从温度数据文件加载数据，假设文件格式为 'Crank' 和 'Mean_Temp' 列
    """
    data = np.loadtxt(filename, skiprows=1)  # 跳过第一行标题
    crank_angle = data[:, 0]  # 曲轴角度（°CA）
    temperature_data = data[:, 1]  # 温度数据（K）
    return crank_angle, temperature_data

# 假设你有以下数据文件（这些文件路径需要根据你的具体情况进行修改）
file_names_pressure = {
    'A1': 'A1.txt',
    'A2': 'A2.txt',
    'A3': 'A3.txt',
    'B1': 'B1.txt',
    'B2': 'B2.txt',
    'B3': 'B3.txt'
}

file_names_temperature = {
    'A1': 'A1T.txt',
    'A2': 'A2T.txt',
    'A3': 'A3T.txt',
    'B1': 'B1T.txt',
    'B2': 'B2T.txt',
    'B3': 'B3T.txt'
}


# 计算每个工况的 (dp/dt)max 和 RI
def analyze_all_cases():
    results = {}
    
    # 对每个工况进行分析
    for case_name in file_names_pressure:
        # 加载压力数据
        crank_angle_p, pressure_data = load_pressure_data(file_names_pressure[case_name])
        
        # 加载温度数据
        crank_angle_t, temperature_data = load_temperature_data(file_names_temperature[case_name])
        
        # 确保压力数据和温度数据的曲轴角度相同
        if not np.array_equal(crank_angle_p, crank_angle_t):
            raise ValueError(f"Crank angles for case {case_name} do not match in pressure and temperature data.")
        
        # 计算 dp/dt 和 RI
        dp_dt_max, P_max, T_max, RI = calculate_RI(pressure_data, crank_angle_p, temperature_data)
        
        # 存储结果
        results[case_name] = {'dp/dt_max': dp_dt_max, 'P_max': P_max, 'T_max': T_max, 'RI': RI}
    
    return results

# 获取每个工况的计算结果
results = analyze_all_cases()

# 打印结果
for case_name, result in results.items():
    print(f"Case {case_name}: (dp/dt)max = {result['dp/dt_max']}, P_max = {result['P_max']}, T_max = {result['T_max']}, RI = {result['RI']}")
