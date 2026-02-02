import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch, Circle, Wedge
from matplotlib.offsetbox import DrawingArea, AnnotationBbox
import matplotlib.patheffects as pe

FONT_CANDIDATES = [
    "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
    "Source Han Sans SC", "WenQuanYi Zen Hei", "Arial Unicode MS", "DejaVu Sans"
]

def pick_font(candidates):
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return name
    return "DejaVu Sans"

plt.rcParams["font.sans-serif"] = [pick_font(FONT_CANDIDATES)]
plt.rcParams["axes.unicode_minus"] = False

plan_total = 187
actual_total = 134

plan_q = np.array([44, 55, 46, 42], dtype=float)
actual_q = np.array([34, 41, 25, 34], dtype=float)
gap_q = plan_q - actual_q
gap_pct_q = gap_q / plan_q
gap_pct_total = (plan_total - actual_total) / plan_total

c_grey = "#4F4F4F"
c_teal = "#49AFC4"
c_dash = "#C7C7C7"
c_text = "#666666"

def add_donut(ax, x, y, pct, size=30, ring_width=7, base_color="#4F4F4F", seg_color="#49AFC4"):
    da = DrawingArea(size, size, 0, 0)
    r = size / 2
    da.add_artist(Wedge((r, r), r, 0, 360, width=ring_width, facecolor=base_color, edgecolor="none"))
    a2 = 90
    a1 = 90 - 360 * float(pct)
    da.add_artist(Wedge((r, r), r, a1, a2, width=ring_width, facecolor=seg_color, edgecolor="none"))
    da.add_artist(Circle((r, r), r - ring_width - 0.5, facecolor="white", edgecolor="none"))
    ab = AnnotationBbox(da, (x, y), frameon=False, box_alignment=(0.5, 0.5), zorder=10)
    ax.add_artist(ab)
    ax.text(
        x, y, f"{int(round(pct*100))}%",
        ha="center", va="center", fontsize=9.5, color=c_grey, zorder=11,
        path_effects=[pe.withStroke(linewidth=3, foreground="white", alpha=0.95)]
    )

fig = plt.figure(figsize=(10.0, 6.2), dpi=220)
ax = fig.add_axes([0.07, 0.16, 0.90, 0.72])

x_total = np.array([0.0, 1.55])
x_q = np.array([3.55, 4.85, 6.15, 7.45])

w_total = 0.65
w_q = 0.70

ax.bar(x_total[0], plan_total, width=w_total, color=c_grey, zorder=2)
ax.bar(x_total[1], actual_total, width=w_total, color=c_teal, zorder=3)

ax.text(x_total[0], plan_total-12, f"{plan_total}", ha="center", va="top",
        fontsize=11, color="white", fontweight="bold", zorder=5)
ax.text(x_total[1], actual_total-12, f"{actual_total}", ha="center", va="top",
        fontsize=11, color="white", fontweight="bold", zorder=5)

ax.bar(x_q, actual_q, width=w_q, color=c_teal, zorder=3)
ax.bar(x_q, gap_q, bottom=actual_q, width=w_q, color=c_grey, zorder=2)

for i in range(4):
    ax.text(x_q[i], actual_q[i]*0.55, f"{int(actual_q[i])}", ha="center", va="center",
            fontsize=10.5, color="white", fontweight="bold", zorder=6)
    ax.text(x_q[i], plan_q[i]+3.2, f"{int(plan_q[i])}", ha="center", va="bottom",
            fontsize=10, color=c_text, fontweight="bold", zorder=6)

y_top = max(plan_total, actual_total) + 18
raise_pct = 6
y_bracket = y_top + raise_pct

ax.plot([x_total[0], x_total[0]], [plan_total, y_bracket], color=c_grey, lw=1.2, zorder=6)
ax.plot([x_total[0], x_total[1]], [y_bracket, y_bracket], color=c_grey, lw=1.2, zorder=6)
ax.annotate("", xy=(x_total[1], actual_total), xytext=(x_total[1], y_bracket),
            arrowprops=dict(arrowstyle="->", color=c_grey, lw=1.2), zorder=6)

cx = (x_total[0] + x_total[1]) / 2
bubble_dy = 7          # 数值越大，圆圈离括号线越远（建议 5~12）
cy = y_bracket + bubble_dy

ax.add_patch(Circle((cx, cy), 0.22, facecolor="white", edgecolor=c_grey, lw=1.2, zorder=7))
ax.text(cx, cy, f"{int(round(gap_pct_total*100))}%", ha="center", va="center",
        fontsize=9.5, color=c_grey, fontweight="bold", zorder=8)



donut_y = 78 + gap_pct_q * 135
ax.plot(x_q, donut_y, color=c_dash, lw=1.0, ls=(0, (2, 3)), zorder=1)

for i in range(4):
    add_donut(ax, x_q[i], donut_y[i], gap_pct_q[i], size=32, ring_width=7, base_color=c_grey, seg_color=c_teal)

handles = [Patch(facecolor=c_grey, edgecolor="none"), Patch(facecolor=c_teal, edgecolor="none")]
ax.legend(handles, ["计划数", "实际数"], loc="upper right", frameon=False, fontsize=10, ncol=2,
          bbox_to_anchor=(0.98, 1.04), handlelength=1.0, handletextpad=0.4, columnspacing=1.2)

fig.text(0.07, 0.92, "2025年各季度项目完工进度分析", fontsize=16, fontweight="bold", color=c_grey)

xticks = [x_total[0], x_total[1], *x_q.tolist()]
xlabels = ["2025\n计划", "2025\n实际", "1季度", "2季度", "3季度", "4季度"]
ax.set_xticks(xticks)
ax.set_xticklabels(xlabels, fontsize=10, color=c_text)

ax.set_xlim(-0.8, 8.35)
ax.set_ylim(0, 215)
ax.set_yticks([])

for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#B0B0B0")
ax.spines["bottom"].set_linewidth(1.0)
ax.tick_params(axis="x", length=0)


plt.show()
