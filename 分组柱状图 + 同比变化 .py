import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# =========================
# 0) 虚拟数据（12个月，单位：万元）
# =========================
months = [f"{i}月" for i in range(1, 13)]

# FY24：给一组看起来合理的月度波动（可改）
fy24 = np.array([419, 606, 538, 585, 869, 508, 560, 620, 590, 640, 710, 780], dtype=float)

# FY25：在FY24基础上做同比波动（可改）
yoy_rate = np.array([-0.09, -0.32, -0.40, -0.09, -0.29, 0.34, 0.08, -0.12, 0.05, 0.18, -0.06, 0.10], dtype=float)
fy25 = np.round(fy24 * (1 + yoy_rate), 1)

yoy = fy25 / fy24 - 1

# =========================
# 1) 样式
# =========================
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(13.5, 5.6), dpi=260)  # 12个月建议加宽

x = np.arange(len(months))
w = 0.26  # 12个月稍微窄一点更舒服

c_fy24 = "#4B4B4B"
c_fy25 = "#4FB3C8"

# 虚线路径颜色：下降偏灰，上升偏蓝（也可统一成灰）
c_path_down = "#9E9E9E"
c_path_up   = "#8CCFE0"

DOT = (0, (1, 2))  # 细密点虚线

# =========================
# 2) 主柱
# =========================
b24 = ax.bar(x - w/2, fy24, width=w, color=c_fy24, zorder=3)
b25 = ax.bar(x + w/2, fy25, width=w, color=c_fy25, zorder=4)

# =========================
# 3) 柱内白字数值
# =========================
def inside_labels(bars):
    for r in bars:
        h = r.get_height()
        y = h - max(18, 0.10*h)
        ax.text(r.get_x()+r.get_width()/2, y, f"{int(round(h))}",
                ha="center", va="top", fontsize=9.5, color="white", zorder=6)

inside_labels(b24)
inside_labels(b25)

# =========================
# 4) 矩形虚线路径（FY24中心 -> 上 -> 横 -> 下 -> FY25中心）+ ↗/↘标注
# =========================
for i, (v24, v25, p) in enumerate(zip(fy24, fy25, yoy)):
    x1 = x[i] - w/2   # FY24柱中心
    x2 = x[i] + w/2   # FY25柱中心

    top = max(v24, v25)
    lift = max(35, top * 0.06)
    y_top = top + lift

    up = p >= 0
    path_color = c_path_up if up else c_path_down

    ax.plot([x1, x1], [v24, y_top], linestyle=DOT, lw=1.6, color=path_color, zorder=5)
    ax.plot([x1, x2], [y_top, y_top], linestyle=DOT, lw=1.6, color=path_color, zorder=5)
    ax.plot([x2, x2], [y_top, v25], linestyle=DOT, lw=1.6, color=path_color, zorder=5)

    # 只加“落地箭头头”
    ax.annotate(
        "", xy=(x2, v25), xytext=(x2, v25 + 1e-6),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color=path_color, mutation_scale=12),
        zorder=6
    )

    sym = "↗" if up else "↘"
    label = f"{sym}{abs(p)*100:.0f}%"
    ax.text((x1+x2)/2, y_top + 8, label,
            ha="center", va="bottom",
            fontsize=10.5, color=("#000000" if not up else c_fy25),
            zorder=7)

# =========================
# 5) 标题 + 单位
# =========================
ax.set_title("FY25各月销售情况与同比分析", fontsize=15, fontweight="bold", pad=14)
ax.text(0.99, 1.02, "单位：万元", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=11, color="#666666")

# =========================
# 6) 坐标轴风格（无网格、y轴不显示）
# =========================
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=10.5, color="#666666")

ymax = max(fy24.max(), fy25.max())
ax.set_ylim(0, ymax * 1.32)

ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color("#9A9A9A")
ax.tick_params(axis="y", length=0)
ax.set_yticklabels([])

handles = [Patch(facecolor=c_fy24, label="FY24"),
           Patch(facecolor=c_fy25, label="FY25")]
ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=11)

plt.tight_layout()
plt.savefig("FY25_月度销售同比_12个月_矩形虚线路径_单位万元.png", dpi=600, bbox_inches="tight")
plt.show()
