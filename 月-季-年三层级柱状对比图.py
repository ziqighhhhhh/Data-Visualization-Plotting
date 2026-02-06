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

m24 = [13.4, 8.7, 29.0, 24.8, 21.9, 18.0, 20.9, 26.9, 46.9, 22.8, 55.1, 54.8]  # 原 2023 -> 显示为 2024
m25 = [13.7, 16.7, 38.4, 28.2, 41.4, 29.7, 29.2, 23.0, 53.3, 43.4, 57.6, 70.7]  # 原 2024 -> 显示为 2025

YEAR_L = "2024"
YEAR_R = "2025"

months = [f"{i}月" for i in range(1, 13)]
quarters = [(0, 3), (3, 6), (6, 9), (9, 12)]

def quarter_sums(m):
    return [round(sum(m[a:b]), 1) for a, b in quarters]

def quarter_max(m):
    return [max(m[a:b]) for a, b in quarters]

q24 = quarter_sums(m24)
q25 = quarter_sums(m25)
qmax24 = quarter_max(m24)
qmax25 = quarter_max(m25)

total24 = round(sum(m24))
total25 = round(sum(m25))

best_q24 = int(np.argmax(q24))  
best_q25 = int(np.argmax(q25))  

Y_UNIT = "万元"

HILITE = "#FE762C"   
BASE   = "#504B49"   

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

x24, next_start = build_x_positions(start=0.0, month_step=1.0, q_gap=0.8, year_gap=1.8)
x25, _ = build_x_positions(start=next_start, month_step=1.0, q_gap=0.8, year_gap=1.8)
x_all = np.r_[x24, x25]

def month_colors_by_best_quarter(best_q):
    colors = []
    for qi in range(4):
        c = HILITE if qi == best_q else BASE
        colors += [c] * 3
    return colors

c24 = month_colors_by_best_quarter(best_q24)
c25 = month_colors_by_best_quarter(best_q25)

fig, ax = plt.subplots(figsize=(16, 7))

vals_all = m24 + m25
ymax = max(vals_all) * 1.45
ax.set_ylim(0, ymax)

bar_w = 0.72

def add_year_bg(x, face="#D9EDF7", alpha=0.18):
    left = x.min() - 0.9
    right = x.max() + 0.9
    ax.add_patch(Rectangle((left, 0), right-left, ymax,
                           facecolor=face, edgecolor="none",
                           alpha=alpha, zorder=0))

add_year_bg(x24, face="#E9F2FF", alpha=0.18)
add_year_bg(x25, face="#E9F2FF", alpha=0.18)

pad = ymax * 0.06

def add_quarter_overlay(x, qmax, best_q, alpha=0.10, lw=1.6):
    for qi, (a, b) in enumerate(quarters):
        left = x[a] - 0.55
        right = x[b-1] + 0.55
        h = min(qmax[qi] + pad, ymax)
        edge = HILITE if qi == best_q else BASE
        face = HILITE if qi == best_q else BASE
        ax.add_patch(Rectangle((left, 0), right-left, h,
                               facecolor=face, edgecolor=edge,
                               linewidth=lw, alpha=alpha, zorder=1))

add_quarter_overlay(x24, qmax24, best_q24, alpha=0.10, lw=1.6)
add_quarter_overlay(x25, qmax25, best_q25, alpha=0.10, lw=1.6)

bars24 = ax.bar(x24, m24, width=bar_w, color=c24, zorder=3)
bars25 = ax.bar(x25, m25, width=bar_w, color=c25, zorder=3)

def add_month_labels(bars):
    for b in bars:
        h = int(round(b.get_height()))
        ax.text(b.get_x()+b.get_width()/2,
            b.get_height()+ymax*0.01,
            f"{h}",
            ha="center", va="bottom", fontsize=10)

add_month_labels(bars24)
add_month_labels(bars25)

ax.set_xticks(x_all)
ax.set_xticklabels(months + months, rotation=0, ha="center", fontsize=10)

def add_quarter_sum_only(x, q_sums, qmax, y_offset=ymax*0.015):
    for qi, (a, b) in enumerate(quarters):
        xc = np.mean([x[a], x[b-1]])
        h = min(qmax[qi] + pad, ymax)
        ax.text(xc, h + y_offset, f"{int(round(q_sums[qi]))}",
                ha="center", va="bottom", fontsize=12, zorder=5)

add_quarter_sum_only(x24, q24, qmax24)
add_quarter_sum_only(x25, q25, qmax25)

ax.text(np.mean([x24[0],x24[-1]]), ymax*0.80,
        f"{YEAR_L}：{total24}（{Y_UNIT}）",
        ha="center", fontsize=16,
        color="#FE762C", fontweight="bold")

ax.text(np.mean([x25[0],x25[-1]]), ymax*0.80,
        f"{YEAR_R}：{total25}（{Y_UNIT}）",
        ha="center", fontsize=16,
        color="#FE762C", fontweight="bold")

ax.text(np.mean([x24[0], x24[-1]]), -ymax*0.07, YEAR_L, ha="center", va="top", fontsize=12)
ax.text(np.mean([x25[0], x25[-1]]), -ymax*0.07, YEAR_R, ha="center", va="top", fontsize=12)

title = rf"$\bf{{{YEAR_L}}}$ vs $\bf{{{YEAR_R}}}$ 月度销售额与季度汇总"
ax.text(-0.16, 1.18, title, transform=ax.transAxes,
        ha="left", va="top", fontsize=16)

ax.set_ylabel(f"金额（{Y_UNIT}）", fontsize=12, rotation=0, labelpad=20)
ax.yaxis.set_label_coords(-0.06, 0.96)  

ax.grid(False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.subplots_adjust(bottom=0.20)
plt.tight_layout()
plt.show()
