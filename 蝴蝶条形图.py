import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


years = ["A", "B", "C", "D"]
sales_left  = np.array([50, 80, 30, 50])    
sales_right = np.array([90, 65, 100, 25])   


gap = 12
bar_h = 0.52
label_pad = 4


max_val = int(max(sales_left.max(), sales_right.max()))
step = 25
max_tick = int(np.ceil(max_val / step) * step)

xlim = max_tick + gap + label_pad + 28

left_color  = "#ff3b30"
right_color = "#1f2a44"
grid_color  = "#d9e2ea"
year_color  = "#0f1b3d"
tick_color  = "#6b7a88"
label_color = "#6b7785"

left_label_name  = "销售种类 1"
right_label_name = "销售种类 2"

fig, ax = plt.subplots(figsize=(7.8, 4.8), dpi=150)


ax.barh(
    y,
    width=sales_left,
    left=-(gap + sales_left),
    height=bar_h,
    color=left_color,
    edgecolor="none"
)
ax.barh(
    y,
    width=sales_right,
    left=gap,
    height=bar_h,
    color=right_color,
    edgecolor="none"
)


ax.set_xlim(-xlim, xlim)

ticks = np.arange(-max_tick, max_tick + step, step)
ax.set_xticks(ticks)
ax.set_xticklabels([f"{abs(t):d}" for t in ticks])

ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")
ax.set_xlabel("销售额（万元）", color=tick_color, labelpad=10, fontsize=11)
ax.tick_params(axis="x", colors=tick_color, labelsize=10, length=0, pad=6)

ax.grid(axis="x", color=grid_color, linewidth=1.0)
ax.set_axisbelow(True)


ax.set_yticks(y)
ax.set_yticklabels([""] * len(years))
ax.tick_params(axis="y", length=0)

for yi, lab in zip(y, years):
    ax.text(
        0, yi, lab,
        ha="center", va="center",
        fontsize=12, fontweight="bold", color=year_color,
        zorder=5,
        bbox=dict(facecolor="white", edgecolor="none", pad=2.2)
    )


for yi, (l, r) in enumerate(zip(sales_left, sales_right)):
    left_edge = -(gap + l)
    ax.text(
        left_edge - label_pad, yi, f"{l}",
        ha="right", va="center",
        fontsize=10, color=label_color
    )

    right_edge = gap + r
    ax.text(
        right_edge + label_pad, yi, f"{r}",
        ha="left", va="center",
        fontsize=10, color=label_color
    )


left_handle = Patch(facecolor=left_color, edgecolor="none", label=left_label_name)
right_handle = Patch(facecolor=right_color, edgecolor="none", label=right_label_name)

leg_left = ax.legend(
    handles=[left_handle],
    loc="upper left",
    bbox_to_anchor=(0.02, 1.02),
    frameon=False,
    fontsize=10,
    handlelength=1.4,
    handletextpad=0.5
)
ax.add_artist(leg_left)  

ax.legend(
    handles=[right_handle],
    loc="upper right",
    bbox_to_anchor=(0.98, 1.02),
    frameon=False,
    fontsize=10,
    handlelength=1.4,
    handletextpad=0.5
)


for spine in ["left", "right", "bottom", "top"]:
    ax.spines[spine].set_visible(False)

ax.margins(y=0.22)
plt.tight_layout()
plt.show()
