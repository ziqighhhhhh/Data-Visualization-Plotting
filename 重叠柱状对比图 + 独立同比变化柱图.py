# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


regions = ["华北", "华南", "东北", "西北", "西南", "华东"]

y2025 = np.array([2679, 1501, 3894, 1517, 3509, 3302], dtype=float)
yoy_pct = np.array([14, -21, 18, -18, 21, 27], dtype=float)

y2024 = y2025 / (1 + yoy_pct / 100.0)

y2024_plot = np.rint(y2024).astype(int)
y2025_plot = np.rint(y2025).astype(int)


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

x = np.arange(len(regions))


c_2024     = "#0B6B6B"  
c_2025     = "#8E44AD"  
c_yoy_up   = "#E74C3C"  
c_yoy_down = "#2E86C1"  

fig = plt.figure(figsize=(9, 4))
ax = fig.add_axes([0.06, 0.14, 0.92, 0.68])
ax_yoy = fig.add_axes([0.06, 0.80, 0.92, 0.16], sharex=ax)


bar_w = 0.42

# 2025 虚线框
ax.bar(
    x, y2025_plot, width=bar_w,
    facecolor="none",
    edgecolor=c_2025,
    linewidth=2.2,
    linestyle=(0, (3, 2)),
    zorder=2,
    label="2025 年"
)

# 2024 实心
ax.bar(
    x, y2024_plot, width=bar_w,
    color=c_2024,
    zorder=3,
    label="2024 年"
)

ymax = max(y2024_plot.max(), y2025_plot.max())

for i in range(len(regions)):
    if y2025_plot[i] >= y2024_plot[i]:
        v = y2025_plot[i]
        txt_color = c_2025
    else:
        v = y2024_plot[i]
        txt_color = c_2024

    ax.text(
        x[i], v + ymax * 0.02,
        f"{v}",
        ha="center", va="bottom",
        fontsize=10, color=txt_color,
        zorder=5
    )

# 主轴样式
ax.set_ylim(0, ymax * 1.12)
ax.set_xticks(x)
ax.set_xticklabels(regions, fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.25, zorder=1)

for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_alpha(0.35)
ax.tick_params(axis="y", length=0)
ax.set_yticklabels([])


ax_yoy.set_ylim(-30, 30)
yoy_w = 0.18

yoy_colors = [c_yoy_up if p >= 0 else c_yoy_down for p in yoy_pct]
ax_yoy.bar(x, yoy_pct, width=yoy_w, color=yoy_colors, zorder=3, label="同比")

for i, p in enumerate(yoy_pct):
    ax_yoy.text(
        x[i],
        p + (1.5 if p >= 0 else -1.5),
        f"{int(p)}%",
        ha="center",
        va=("bottom" if p >= 0 else "top"),
        fontsize=10.5,
        color=(c_yoy_up if p >= 0 else c_yoy_down),
        zorder=4
    )

ax_yoy.grid(axis="y", linestyle="--", alpha=0.20, zorder=1)
ax_yoy.set_yticks([])
ax_yoy.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
for s in ["top", "right", "left", "bottom"]:
    ax_yoy.spines[s].set_visible(False)


handles = [
    Patch(facecolor=c_2024, edgecolor="none", label="2024 年"),
    Patch(facecolor="none", edgecolor=c_2025, linewidth=2.2, linestyle=(0, (3, 2)), label="2025 年"),
    Patch(facecolor=c_yoy_up, edgecolor="none", label="上升"),
    Patch(facecolor=c_yoy_down, edgecolor="none", label="下降"),
]
fig.legend(
    handles=handles,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.12),
    ncol=4,
    frameon=False,
    fontsize=10
)

plt.show()


