"""#本图为 Hanging Rootogram（图基悬挂根图），用于比较
“当前周期销售分布”与“历史基准销售分布”的结构差异。

绘制该图需要以下三类数据与设定：

1. 历史基准销售数据（Baseline）
   - 数据形式：一维数值序列
   - 含义：历史正常时期的销售观测值
   - 示例：过去 6–12 个月的每日销售额 / 每笔订单金额
   - 用途：用于估计在各销售额区间内的期望出现频数（Expected）

2. 当前周期销售数据（Observed）
   - 数据形式：一维数值序列
   - 含义：需要评估的当前销售观测值
   - 示例：本月每日销售额 / 本次促销期的订单金额
   - 用途：计算各销售额区间内的实际出现频数（Observed）

3. 统一的销售额分箱区间（Bins）
   - 数据形式：数值区间（如 70–72, 72–74, …）
   - 要求：Observed 与 Baseline 必须使用完全一致的分箱方式
   - 用途：确保不同分布在同一销售额区间内可直接比较

基于上述数据：
- 先分别统计 Observed 与 Baseline 在每个区间内的频数
- 再将 Baseline 频数按样本量比例缩放为期望频数（Expected）
- 最终在平方根尺度下计算差异：
  √Observed − √Expected
并将该差异“悬挂”在 y=0 的历史基准线上进行展示。
 """
import numpy as np
import matplotlib.pyplot as plt
import math


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


np.random.seed(42)


baseline_sales = np.random.normal(loc=80, scale=4.5, size=4000)
baseline_sales = baseline_sales[(baseline_sales >= 70) & (baseline_sales <= 90)]

current_sales = np.concatenate([
    np.random.normal(80, 4.2, 900),
    np.random.normal(87, 1.5, 120)   
])
current_sales = current_sales[(current_sales >= 70) & (current_sales <= 90)]


bins = np.arange(70, 91, 2)  
bin_centers = (bins[:-1] + bins[1:]) / 2
bin_width = np.diff(bins)


obs_counts, _ = np.histogram(current_sales, bins=bins)

base_counts, _ = np.histogram(baseline_sales, bins=bins)
expected_counts = base_counts / base_counts.sum() * obs_counts.sum()

expected_counts = np.clip(expected_counts, 1e-6, None)


root_diff = np.sqrt(obs_counts) - np.sqrt(expected_counts)


fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=160)

# --- 红色悬挂柱 ---
ax.bar(
    bin_centers,
    root_diff,
    width=bin_width * 0.75,
    color="#FF3B30",
    edgecolor="white",
    linewidth=1.2,
    zorder=3
)

ax.plot(
    bin_centers,
    np.sqrt(expected_counts) - np.sqrt(expected_counts.mean()),
    color="#1F2A44",
    linewidth=2.0,
    marker="o",
    markersize=6,
    markerfacecolor="#1F2A44",
    markeredgecolor="white",
    zorder=4
)

ax.axhline(0, color="#1F2A44", linewidth=1.4, zorder=2)


ax.set_xlabel("销售额区间（万元）", labelpad=8)
ax.set_ylabel(r"$\sqrt{Observed}-\sqrt{Expected}$（√频数）")

ax.set_xlim(69, 91)
ax.set_xticks(bins)
ax.tick_params(axis="x", length=6)
ax.tick_params(axis="y", length=6)

ax.yaxis.grid(True, linestyle="--", alpha=0.35)
ax.xaxis.grid(False)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ax.set_title("当前销售 vs 历史基准分布", pad=12)

plt.tight_layout()
plt.show()
