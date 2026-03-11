import pandas as pd
import numpy as np
import re
import io

# =========================
# 1) 基础参数(示例)
# =========================
bore   = 0.215  # m
stroke = 0.320  # m
conrod = 0.520  # m
CR     = 14.0

# 单循环喷油 & 燃料热值
m_M = 1.984e-3    # kg/循环 (甲醇)
m_D = 4.8129e-5   # kg/循环 (柴油)
H_M = 19.58e3     # kJ/kg
H_D = 42.49e3     # kJ/kg

# 死点余隙容积
piston_area = np.pi*(bore**2)/4.0
Vc = piston_area*(stroke/(CR-1.0))

# =========================
# 2) 读文件并清洗
# =========================
def read_and_clean_txt(file_path):
    """
    执行以下步骤:
    1) 以二进制方式读入 -> 移除UTF-8 BOM(若有)
    2) 解码为字符串, 无法解码字符 => '?'
    3) 将各种长横 (–, —, −) 替换成 ASCII 减号 '-'
    4) 对每行做正则过滤, 仅保留 [数字, ., +, -, e, E, 空白,#]
    5) 将能拆成2个可转float的字段视作有效行, 否则跳过
    6) 拼回文本, 用于后续 pd.read_csv
    """
    with open(file_path,"rb") as f:
        raw = f.read()
    
    # 1) 如果有UTF-8 BOM则移除
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    
    # 2) 解码
    text = raw.decode("utf-8","replace")  # 不可解码 => '?'
    
    # 3) 替换“长横”=> '-'
    dash_like = ["–","—","−"]
    for sym in dash_like:
        text = text.replace(sym, "-")
    
    # 4) 对每行做正则清洗 + 判断可否转float
    lines_out = []
    for line in text.splitlines():
        # 如果是以#开头的注释行，直接保留:
        if line.strip().startswith("#"):
            lines_out.append(line)
            continue
        
        # 正则: 仅保留 [0-9 . + - e E 空白 #]
        # 这里顺带保留 #, 以防行内注释. 也可去掉 # 视情况
        cln = re.sub(r"[^0-9\.\-\+\seE#]", "", line)
        
        # 按空白分割
        parts = cln.split()
        if len(parts)==2:
            # 尝试转 float
            try:
                float(parts[0])
                float(parts[1])
                # 成功 => 有效行
                lines_out.append(" ".join(parts))
            except ValueError:
                # 无法转 => 跳过
                pass
        else:
            # 不是2字段 => 跳过
            pass
    
    # 拼装
    cleaned_text = "\n".join(lines_out)
    return cleaned_text

# =========================
# 3) 计算气缸容积
# =========================
def cylinder_volume_deg(crank_deg):
    theta = np.radians(crank_deg)
    r = stroke*0.5
    R = conrod
    
    inside = R**2 - r**2*(np.sin(theta)**2)
    inside_clipped = np.clip(inside, 0, None)   # <0则设成0
    
    n_neg = (inside<0).sum()
    if n_neg>0:
        print(f"[WARN] sqrt里出现负数 {n_neg} 处, 已clip=0!")
    
    sqrtval = np.sqrt(inside_clipped)
    term = (R + r - r*np.cos(theta) - sqrtval)
    
    vol = Vc + piston_area*term
    return vol

# =========================
# 4) 积分 p·dV => 指示功 (kJ)
# =========================
def integrate_pdv(crank_arr, press_arr):
    vol_arr = cylinder_volume_deg(crank_arr)
    if np.isnan(vol_arr).any():
        print("[WARN] vol_arr出现NaN!")
    
    W_i_kJ = 0.0
    for i in range(len(crank_arr)-1):
        p_avg = 0.5*(press_arr[i] + press_arr[i+1])  # MPa
        dV = (vol_arr[i+1] - vol_arr[i])            # m^3
        # 1 MPa*m^3 => 1000 kJ
        W_i_kJ += p_avg * dV * 1000.0
    return W_i_kJ

# =========================
# 5) 核心: 读取 -> 清洗 -> read_csv -> 积分 -> EISFC
# =========================
def calc_eisfc(file_path):
    print(f"\n=== 正在处理: {file_path} ===")
    
    # (a) 读取并清洗
    cleaned_str = read_and_clean_txt(file_path)
    
    # (b) pandas 解析
    df = pd.read_csv(io.StringIO(cleaned_str),
                     sep=r"\s+",
                     comment="#",  # 继续跳过以#开头的行
                     names=["Crank","Press"],
                     engine="python")
    
    # 看前几行
    print(df.head())
    
    # 强制转 float
    df["Crank"] = pd.to_numeric(df["Crank"], errors="coerce")
    df["Press"] = pd.to_numeric(df["Press"], errors="coerce")
    
    # 若全部NaN => 无法继续
    if df["Crank"].isna().all() or df["Press"].isna().all():
        print("[ERR] 全部NaN, 无有效行.")
        return np.nan
    
    # (c) 积分
    crank_arr = df["Crank"].values
    press_arr = df["Press"].values
    
    Wi_kJ = integrate_pdv(crank_arr, press_arr)
    if np.isnan(Wi_kJ) or Wi_kJ==0:
        print(f"[WARN] 积分Wi_kJ={Wi_kJ}, 结果无效!")
        return np.nan
    
    # (d) EISFC
    raw_ratio = (m_M*H_M + m_D*H_D)/( Wi_kJ * H_D )
    eisfc = raw_ratio*(1e3*3600)  # => g/(kW·h)
    return eisfc

# =========================
# 6) main: 批量处理 A1~B3
# =========================
def main():
    files = ["A1.txt","A2.txt","A3.txt","B1.txt","B2.txt","B3.txt"]
    for f in files:
        val = calc_eisfc(f)
        if np.isnan(val):
            print(f"{f}: EISFC= NaN (解析/计算失败)\n")
        else:
            print(f"{f}: EISFC= {val:.2f} g/(kW·h)\n")

if __name__=="__main__":
    main()
