

import numpy as np
import matplotlib.pyplot as plt


plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


models = [
    ("型号A", 73.0, 520,  "good"),
    ("型号B", 75.5, 1260, "bad"),
    ("型号C", 74.0, 980,  "bad"),
    ("型号D", 78.0, 1020, "bad"),
    ("型号E", 85.5, 760,  "good"),
    ("型号F", 79.0, 960,  "bad"),
    ("型号G", 76.0, 820,  "good"),
]

avg_x = 72.0
avg_y = 900

x_min, x_max = 60, 90
y_min, y_max = 0, 1400

good_color = "#9aa0a6"
bad_color  = "#d34a4a"
avg_color  = "#222222"


FS_TITLE   = 20
FS_AXIS    = 18
FS_TICK    = 12
FS_SIDE    = 14
FS_TOPCOR  = 14
FS_QUAD    = 28
FS_POINT   = 15.5
FS_AVG     = 12.5


fig, ax = plt.subplots(figsize=(11.5, 6.5))

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_max, y_min)  

ax.axvline(avg_x, color=avg_color, linewidth=1.2)
ax.axhline(avg_y, color=avg_color, linewidth=1.2)

ax.scatter([avg_x], [avg_y], s=105, color=avg_color, zorder=6)
ax.annotate(
    "上一年平均\n（所有型号）",
    xy=(avg_x, avg_y),
    xytext=(-5, 5),  
    textcoords="offset points",
    ha="right", va="bottom",
    fontsize=FS_AVG, color=avg_color
)


label_offsets = {
    "型号A": (14,  8),
    "型号B": (14,  2),
    "型号C": (14, -12),
    "型号D": (14, -12),
    "型号E": (14,  8),
    "型号F": (14, -2),
    "型号G": (14,  8),
}

for name, x, y, grp in models:
    color = good_color if grp == "good" else bad_color
    ax.scatter([x], [y], s=125, color=color, edgecolor="white", linewidth=1.2, zorder=5)

    dx, dy = label_offsets.get(name, (14, 8))
    ax.annotate(
        name, xy=(x, y),
        xytext=(dx, dy), textcoords="offset points",
        ha="left", va="center",
        fontsize=FS_POINT, color=color
    )


# 顶部三层：标题(最高) -> 角标(中) -> x轴标题(低)
title_y      = 1.22
top_corner_y = 1.07
top_label_y  = 1.14

x0 = -0.12
col_norm = "#6b7280"
col_bold = "#374151"
fs_norm = FS_TITLE
fs_bold = FS_TITLE + 4
w_bold = "heavy"
w_norm = "normal"

t1 = ax.text(x0, title_y, "问题数", transform=ax.transAxes,
             ha="left", va="bottom", fontsize=fs_bold, color=col_bold, fontweight=w_bold)
t2 = ax.text(x0, title_y, "  vs  ", transform=ax.transAxes,
             ha="left", va="bottom", fontsize=fs_norm, color=col_norm, fontweight=w_norm)
t3 = ax.text(x0, title_y, "满意度", transform=ax.transAxes,
             ha="left", va="bottom", fontsize=fs_bold, color=col_bold, fontweight=w_bold)
t4 = ax.text(x0, title_y, "（按型号）", transform=ax.transAxes,
             ha="left", va="bottom", fontsize=fs_norm, color=col_norm, fontweight=w_norm)

fig.canvas.draw()
renderer = fig.canvas.get_renderer()

def next_x(prev_text_obj, x_current):
    bb = prev_text_obj.get_window_extent(renderer=renderer)
    ax_bb = ax.get_window_extent(renderer=renderer)
    return x_current + (bb.width / ax_bb.width)

xx = x0
xx = next_x(t1, xx); t2.set_position((xx, title_y))
xx = next_x(t2, xx); t3.set_position((xx, title_y))
xx = next_x(t3, xx); t4.set_position((xx, title_y))

ax.xaxis.set_label_position("top")
ax.xaxis.tick_top()

ax.tick_params(axis="x", pad=2, labelsize=FS_TICK)
ax.tick_params(axis="y", pad=6, labelsize=FS_TICK)

ax.set_xlabel("满意度", fontsize=FS_AXIS, labelpad=0)
ax.xaxis.set_label_coords(0.0, top_label_y)
ax.xaxis.label.set_horizontalalignment("left")

ax.text(0.00, top_corner_y, "满意度低", transform=ax.transAxes,
        fontsize=FS_TOPCOR, color="#6b7280", weight="bold",
        ha="left", va="center")
ax.text(1.00, top_corner_y, "满意度高", transform=ax.transAxes,
        fontsize=FS_TOPCOR, color="#6b7280", weight="bold",
        ha="right", va="center")


y_label_x = -0.12

ax.set_ylabel("每千台\n问题数", fontsize=FS_AXIS, labelpad=18, rotation=0)
ax.yaxis.set_label_coords(y_label_x, 1.02)
ax.yaxis.label.set_verticalalignment("top")
ax.yaxis.label.set_horizontalalignment("left")

ax.text(y_label_x, 0.82, "问题少", transform=ax.transAxes,
        fontsize=FS_SIDE, color="#6b7280", weight="bold",
        ha="left", va="center")
ax.text(y_label_x, 0.08, "问题多", transform=ax.transAxes,
        fontsize=FS_SIDE, color="#6b7280", weight="bold",
        ha="left", va="center")


ax.text(80.5, 320, "高满意度，\n问题少",
        fontsize=FS_QUAD, color="#6b7280", weight="bold",
        ha="left", va="center")
ax.text(80.5, 1230, "高满意度，\n问题多",
        fontsize=FS_QUAD, color=bad_color, weight="bold",
        ha="left", va="center")


ax.set_xticks(np.arange(60, 91, 5))
ax.set_xticklabels([f"{t:d}%" for t in np.arange(60, 91, 5)], fontsize=FS_TICK)

ax.set_yticks(np.arange(0, 1401, 200))

ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)


fig.subplots_adjust(left=0.12, right=0.985, top=0.78, bottom=0.10)

plt.show()

