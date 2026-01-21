import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

months = np.arange(1, 13)
sales = np.array([230, 260, 310, 350, 345, 310, 295, 330, 395, 435, 428, 405], dtype=float)

def smooth(y, w=3):
    if w <= 1:
        return y
    pad = w // 2
    ypad = np.r_[y[0] * np.ones(pad), y, y[-1] * np.ones(pad)]
    kernel = np.ones(w) / w
    return np.convolve(ypad, kernel, mode="valid")

sales_smooth = smooth(sales, w=3)

events = [
    {"month": 4,  "label": "A"},
    {"month": 7,  "label": "B"},
    {"month": 11, "label": "C"},
]

fig, ax = plt.subplots(figsize=(9.2, 5.6), dpi=160)

area_color = "#FF3B30"
axis_color = "#1F2A44"
tick_color = "#5B6B7A"
label_box_color = "#1F2A44"

ax.fill_between(months, sales_smooth, 0, color=area_color, alpha=0.95, zorder=1)
ax.plot(months, sales_smooth, color=area_color, linewidth=2.6, zorder=2)

ax.set_xticks(months)
ax.set_xticklabels([f"{m}月" for m in months], color=tick_color)
ax.set_xlabel("月份", labelpad=10, color=axis_color)
ax.set_ylabel("销售额（万元）", labelpad=10, color=axis_color)

y_min = float(np.min(sales_smooth))
y_max = float(np.max(sales_smooth))
y_range = max(y_max - y_min, 1e-9)

gap_ratio = 0.12              
gap = gap_ratio * y_range     

label_offset = 0.35 * gap

top_padding = gap * 2.2
ax.set_ylim(0, y_max + top_padding)

for e in events:
    m = e["month"]
    y = float(sales_smooth[m - 1])

    y_line_top = y + gap
    y_label = y_line_top + label_offset

    ax.vlines(m, 0, y_line_top, color=axis_color, alpha=0.35, linewidth=1.2, zorder=3)

    ax.annotate(
        e["label"],
        xy=(m, y_label),
        xytext=(m, y_label),
        ha="center", va="center",
        color="white", fontsize=11,
        bbox=dict(
            boxstyle="round,pad=0.35,rounding_size=0.2",
            facecolor=label_box_color, edgecolor="none"
        ),
        zorder=5
    )

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#CAD5E2")
ax.spines["bottom"].set_color("#CAD5E2")
ax.tick_params(axis="x", colors=tick_color, length=7, width=2, direction="out", pad=8)
ax.tick_params(axis="y", colors=tick_color, length=0)

plt.tight_layout()
plt.show()
