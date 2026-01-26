import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

months = np.arange(1, 13)
labels = [f"{m}月" for m in months]

y2024 = np.array([55, 92, 130, 88, 84, 105, 86, 112, 98, 80, 110, 83]) * 1000
y2025 = np.array([19, 150, 94, 100, 109, 127, 90, 113, 141, 55, 109, 100]) * 1000
yoy = (y2025 / y2024 - 1) * 100

sum_2024 = int(y2024.sum())
sum_2025 = int(y2025.sum())
share_2024 = 0.10
share_2025 = 0.11
yoy_total = (sum_2025 / sum_2024 - 1) * 100

fig = plt.figure(figsize=(14, 7), dpi=150)
gs = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[1.05, 2.95], wspace=0.15)
ax_left = fig.add_subplot(gs[0, 0])
ax = fig.add_subplot(gs[0, 1])

x = np.arange(len(months))
bar_w = 0.34
ax.bar(x - bar_w/2, y2024, width=bar_w, label="2024")
ax.bar(x + bar_w/2, y2025, width=bar_w, label="2025")

ax2 = ax.twinx()

ax2.plot(
    x, yoy,
    color="black",            
    marker="o",
    linewidth=2.6,
    markersize=5.5,
    markerfacecolor="white", 
    markeredgecolor="black",
    label="同比"
)

for xi, yi in zip(x, yoy):
    ax2.annotate(
        f"{yi:.0f}%",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 10 if yi >= 0 else -16),
        ha="center",
        va="center",
        fontsize=9,
        bbox=dict(
            boxstyle="round,pad=0.25,rounding_size=0.8",
            fc="white", ec="black", lw=0.8
        ),
        zorder=10,
    )

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_title("月度出口趋势（25年 vs. 24年）", fontsize=13, fontweight="bold", pad=10)
ax.set_ylabel("出口额（虚拟单位）")
ax2.set_ylabel("同比（%）")

ax.grid(False)
ax2.grid(False)

handles1, labels1 = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax.legend(handles1 + handles2, labels1 + labels2, loc="upper center", ncol=3, frameon=False)

ax_left.axis("off")
ax_left.set_xlim(0, 1)
ax_left.set_ylim(0, 1)

def draw_card(axc, xy, wh, title, rows, facecolor="#0B2E57", title_color="white", text_color="white"):
    x0, y0 = xy
    w, h = wh
    card = FancyBboxPatch(
        (x0, y0), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=0,
        facecolor=facecolor,
    )
    axc.add_patch(card)

    header_h = 0.22 * h
    header = FancyBboxPatch(
        (x0, y0 + h - header_h), w, header_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=0,
        facecolor=facecolor,
    )
    axc.add_patch(header)

    axc.text(x0 + w/2, y0 + h - header_h/2, title,
             ha="center", va="center", fontsize=12, color=title_color, fontweight="bold")

    start_y = y0 + h - header_h - 0.12*h
    line_gap = 0.22*h
    for i, (k, v, sub) in enumerate(rows):
        yy = start_y - i * line_gap
        axc.text(x0 + 0.08*w, yy, k, ha="left", va="center", fontsize=11, color=text_color, fontweight="bold")
        axc.text(x0 + 0.92*w, yy, v, ha="right", va="center", fontsize=12, color=text_color, fontweight="bold")
        if sub:
            axc.text(x0 + 0.08*w, yy - 0.10*h, sub, ha="left", va="center", fontsize=9, color=text_color, alpha=0.95)

rows_2025 = [
    ("达成", f"{sum_2025:,}", ""),
    ("同比", f"{yoy_total:.0f}%", ""),
    ("份额%", f"{int(share_2025*100)}%", "占全国出口比例"),
]
draw_card(ax_left, xy=(0.06, 0.56), wh=(0.88, 0.38), title="2025年",
          rows=rows_2025, facecolor="#0B2E57", title_color="white", text_color="white")

rows_2024 = [
    ("达成", f"{sum_2024:,}", ""),
    ("份额%", f"{int(share_2024*100)}%", "占全国出口比例"),
]
draw_card(ax_left, xy=(0.06, 0.10), wh=(0.88, 0.32), title="2024年",
          rows=rows_2024, facecolor="#F7B79A", title_color="black", text_color="black")

plt.tight_layout()
plt.show()
