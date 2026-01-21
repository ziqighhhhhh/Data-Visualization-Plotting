import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle


def set_cn_font():
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for fp in candidates:
        try:
            font_manager.fontManager.addfont(fp)
            prop = font_manager.FontProperties(fname=fp)
            mpl.rcParams["font.family"] = prop.get_name()
            mpl.rcParams["axes.unicode_minus"] = False
            return True
        except Exception:
            continue
    mpl.rcParams["axes.unicode_minus"] = False
    return False

set_cn_font()


m23 = [13.4, 8.7, 29.0, 24.8, 21.9, 18.0, 20.9, 26.9, 46.9, 22.8, 55.1, 54.8]
m24 = [13.7, 16.7, 38.4, 28.2, 41.4, 29.7, 29.2, 23.0, 53.3, 43.4, 57.6, 70.7]

months = [f"{i}月" for i in range(1, 13)]
quarters = [(0, 3), (3, 6), (6, 9), (9, 12)]

def quarter_sums(m):
    return [round(sum(m[a:b]), 1) for a, b in quarters]

def quarter_max(m):
    return [max(m[a:b]) for a, b in quarters]

q23 = quarter_sums(m23)
q24 = quarter_sums(m24)
qmax23 = quarter_max(m23)
qmax24 = quarter_max(m24)

total23 = round(sum(m23), 1)
total24 = round(sum(m24), 1)

# Y轴单位（只在这里体现）
Y_UNIT = "万元"   


def build_x_positions(start=0.0, month_step=1.0, q_gap=0.8, year_gap=1.8):
    x = []
    cur = start
    for _ in range(4):
        for _ in range(3):
            x.append(cur)
            cur += month_step
        cur += q_gap
    end = cur
    return np.array(x), end + year_gap

x23, next_start = build_x_positions(start=0.0, month_step=1.0, q_gap=0.8, year_gap=1.8)
x24, _ = build_x_positions(start=next_start, month_step=1.0, q_gap=0.8, year_gap=1.8)
x_all = np.r_[x23, x24]


q_colors_23 = ["#f2a0a0", "#f4b183", "#f7d58a", "#6fa8dc"]  # 2023 Q1-Q4
q_colors_24 = ["#ffe599", "#b6d7a8", "#76d7c4", "#3d85c6"]  # 2024 Q1-Q4

def month_colors_by_quarter(q_colors):
    c = []
    for qi in range(4):
        c += [q_colors[qi]] * 3
    return c

c23 = month_colors_by_quarter(q_colors_23)
c24 = month_colors_by_quarter(q_colors_24)

# 季度框颜色（半透明覆盖层）随季度变化
q_box_faces_23 = ["#ffe5e7", "#ffe8d6", "#fff3da", "#e0efff"]
q_box_faces_24 = ["#fff6d6", "#e8f5e6", "#dff7f3", "#d8ecff"]

q_box_edges_23 = ["#e99aa0", "#e6a37c", "#e3c37b", "#8bb3dd"]
q_box_edges_24 = ["#e3c37b", "#97c38a", "#6bbfb1", "#6fa8dc"]


fig, ax = plt.subplots(figsize=(16, 7))

vals_all = m23 + m24
ymax = max(vals_all) * 1.45
ax.set_ylim(0, ymax)

bar_w = 0.72

def add_year_bg(x, face="#d9edf7", alpha=0.22):
    left = x.min() - 0.9
    right = x.max() + 0.9
    ax.add_patch(Rectangle((left, 0), right-left, ymax,
                           facecolor=face, edgecolor="none",
                           alpha=alpha, zorder=0))

add_year_bg(x23, face="#d9edf7", alpha=0.22)
add_year_bg(x24, face="#d9edf7", alpha=0.22)

pad = ymax * 0.06  

def add_quarter_overlay_varcolor(x, qmax, faces, edges, alpha=0.55, lw=1.4):
    for qi, (a, b) in enumerate(quarters):
        left = x[a] - 0.55
        right = x[b-1] + 0.55
        h = min(qmax[qi] + pad, ymax)
        ax.add_patch(Rectangle((left, 0), right-left, h,
                               facecolor=faces[qi], edgecolor=edges[qi],
                               linewidth=lw, alpha=alpha, zorder=1))

add_quarter_overlay_varcolor(x23, qmax23, q_box_faces_23, q_box_edges_23, alpha=0.55, lw=1.4)
add_quarter_overlay_varcolor(x24, qmax24, q_box_faces_24, q_box_edges_24, alpha=0.55, lw=1.4)

bars23 = ax.bar(x23, m23, width=bar_w, color=c23, zorder=3)
bars24 = ax.bar(x24, m24, width=bar_w, color=c24, zorder=3)

def add_month_labels(bars):
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width()/2,
                h + ymax*0.010,
                f"{h:.1f}",
                ha="center", va="bottom",
                fontsize=10, zorder=4)

add_month_labels(bars23)
add_month_labels(bars24)

ax.set_xticks(x_all)
ax.set_xticklabels(months + months, rotation=90)

def add_quarter_sum_only(x, q_sums, qmax, y_offset=ymax*0.015):
    for qi, (a, b) in enumerate(quarters):
        xc = np.mean([x[a], x[b-1]])
        h = min(qmax[qi] + pad, ymax)
        ax.text(xc, h + y_offset, f"{q_sums[qi]:.1f}",
                ha="center", va="bottom", fontsize=12, zorder=5)

add_quarter_sum_only(x23, q23, qmax23)
add_quarter_sum_only(x24, q24, qmax24)

ax.text(np.mean([x23[0], x23[-1]]), ymax*0.80, f"{total23:.1f}", ha="center", fontsize=16, zorder=6)
ax.text(np.mean([x24[0], x24[-1]]), ymax*0.80, f"{total24:.1f}", ha="center", fontsize=16, zorder=6)

ax.text(np.mean([x23[0], x23[-1]]), -ymax*0.07, "2023", ha="center", va="top", fontsize=12)
ax.text(np.mean([x24[0], x24[-1]]), -ymax*0.07, "2024", ha="center", va="top", fontsize=12)

# ---- Y轴单位----
ax.set_ylabel(f"金额（{Y_UNIT}）", fontsize=12)

ax.grid(axis="y", alpha=0.18, zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.subplots_adjust(bottom=0.20)
plt.tight_layout()
plt.show()
