import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


UNIT = "万元"
months_cn = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]

monthly_2024 = np.array([386, 759, 796, 388, 706, 595, 430, 561, 623, 798, 582, 520], dtype=float)
monthly_2025 = np.array([735, 518, 458, 614, 470, 721, 782, 375, 889, 825, 448, 593], dtype=float)

total_2024 = 7144
total_2025 = 7428

q_idx = [(0,3), (3,6), (6,9), (9,12)]
q_labels = ["Q1","Q2","Q3","Q4"]
q_2024 = np.array([monthly_2024[a:b].sum() for a,b in q_idx], dtype=float)
q_2025 = np.array([monthly_2025[a:b].sum() for a,b in q_idx], dtype=float)

def yoy(new, old):
    old = np.asarray(old, dtype=float)
    new = np.asarray(new, dtype=float)
    out = np.full_like(new, np.nan, dtype=float)
    mask = old != 0
    out[mask] = new[mask] / old[mask] - 1
    return out

yoy_total = (total_2025/total_2024 - 1) if total_2024 != 0 else np.nan
yoy_q = yoy(q_2025, q_2024)
yoy_m = yoy(monthly_2025, monthly_2024)


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

c24 = "#595959"
c25 = "#43B3C6"
c_pos = "#2ca02c"
c_neg = "#d62728"
c_line = "#8c8c8c"

W = 0.28                 
LABEL_PAD = 0.03         
YOY_TEXT_PAD = 0.06     
RIGHT_PAD = 0.35         

BBOX = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85)  # 遮罩，压线神器

def fmt_num(x): 
    return f"{x:,.0f}"

def pct_color(p):
    return c_pos if (not np.isnan(p) and p >= 0) else (c_neg if not np.isnan(p) else "#808080")

def fmt_pct(p):
    if np.isnan(p): 
        return "—"
    return ("↑ " if p >= 0 else "↓ ") + f"{abs(p)*100:.0f}%"


fig = plt.figure(figsize=(10.6, 7.2), dpi=220)
gs = GridSpec(2, 2, width_ratios=[1.05, 3.25], height_ratios=[1.05, 1.35], wspace=0.10, hspace=0.28)

ax_total = fig.add_subplot(gs[:, 0])
ax_q     = fig.add_subplot(gs[0, 1])
ax_m     = fig.add_subplot(gs[1, 1])

fig.subplots_adjust(left=0.05, right=0.98, top=0.84, bottom=0.08)


x0 = np.array([0, 1])
ax_total.bar(x0[0], total_2024, width=0.55, color=c24)
ax_total.bar(x0[1], total_2025, width=0.55, color=c25)

tmax = max(total_2024, total_2025)
ax_total.text(x0[0], total_2024 + tmax*0.03, fmt_num(total_2024),
              ha="center", va="bottom", fontsize=11, color=c24, bbox=BBOX)
ax_total.text(x0[1], total_2025 + tmax*0.03, fmt_num(total_2025),
              ha="center", va="bottom", fontsize=11, color=c25, bbox=BBOX)

top = tmax * 1.13
ax_total.plot([x0[0], x0[0]], [total_2024, top], color="#6e6e6e", lw=1.2)
ax_total.plot([x0[1], x0[1]], [total_2025, top], color="#6e6e6e", lw=1.2)
ax_total.plot([x0[0], x0[1]], [top, top], color="#6e6e6e", lw=1.2)

cx = (x0[0] + x0[1]) / 2
ax_total.scatter([cx], [top], s=420, facecolors="white",
                 edgecolors=pct_color(yoy_total), lw=2.0, zorder=6)
ax_total.text(cx, top, fmt_pct(yoy_total),
              ha="center", va="center", fontsize=11,
              color=pct_color(yoy_total), zorder=7, bbox=BBOX)

ax_total.set_xticks([cx])
ax_total.set_xticklabels(["2024年&2025年"], fontsize=11)
ax_total.set_ylim(0, top*1.18)
ax_total.set_yticks([])
ax_total.spines[:].set_visible(False)

ax_total.set_title(f"总计（单位：{UNIT}）", fontsize=13, pad=10)


xq = np.arange(4)
ax_q.bar(xq - W/2, q_2024, width=W, color=c24, label="2024年")
ax_q.bar(xq + W/2, q_2025, width=W, color=c25, label="2025年")

qmax = max(q_2024.max(), q_2025.max())
for i in range(4):
    ax_q.text(xq[i]-W/2, q_2024[i] + qmax*LABEL_PAD, fmt_num(q_2024[i]),
              ha="center", va="bottom", fontsize=10, color=c24, bbox=BBOX)
    ax_q.text(xq[i]+W/2, q_2025[i] + qmax*LABEL_PAD, fmt_num(q_2025[i]),
              ha="center", va="bottom", fontsize=10, color=c25, bbox=BBOX)

y_line = qmax * 1.35
ax_q.plot([xq[0]-RIGHT_PAD, xq[-1]+RIGHT_PAD], [y_line, y_line],
          ls="--", lw=1.2, color=c_line, zorder=1)

for i, p in enumerate(yoy_q):
    ax_q.scatter([xq[i]], [y_line], s=75, facecolors="white",
                 edgecolors=pct_color(p), lw=2.0, zorder=5)
    ax_q.text(xq[i], y_line + qmax*YOY_TEXT_PAD, fmt_pct(p),
              ha="center", va="bottom", fontsize=11,
              color=pct_color(p), bbox=BBOX)

ax_q.set_xticks(xq)
ax_q.set_xticklabels(q_labels, fontsize=12)
ax_q.set_ylim(0, y_line*1.12)
ax_q.set_yticks([])
ax_q.spines[:].set_visible(False)

ax_q.set_title(f"季度对比（单位：{UNIT}）", fontsize=13, pad=12)


xm = np.arange(12)
ax_m.bar(xm - W/2, monthly_2024, width=W, color=c24)
ax_m.bar(xm + W/2, monthly_2025, width=W, color=c25)

mmax = max(monthly_2024.max(), monthly_2025.max())

for i in range(12):
    a = monthly_2024[i]
    b = monthly_2025[i]
    base_off = mmax*LABEL_PAD
    bump = mmax*0.05 if abs(a-b) < mmax*0.06 else 0  

    ax_m.text(xm[i]-W/2, a + base_off + bump, fmt_num(a),
              ha="center", va="bottom", fontsize=9.5, color=c24, bbox=BBOX)
    ax_m.text(xm[i]+W/2, b + base_off, fmt_num(b),
              ha="center", va="bottom", fontsize=9.5, color=c25, bbox=BBOX)

y_line2 = mmax * 1.30
ax_m.plot([xm[0]-RIGHT_PAD, xm[-1]+RIGHT_PAD], [y_line2, y_line2],
          ls="--", lw=1.2, color=c_line, zorder=1)

for i, p in enumerate(yoy_m):
    ax_m.scatter([xm[i]], [y_line2], s=65, facecolors="white",
                 edgecolors=pct_color(p), lw=2.0, zorder=5)
    ax_m.text(xm[i], y_line2 + mmax*YOY_TEXT_PAD, fmt_pct(p),
              ha="center", va="bottom", fontsize=10.5,
              color=pct_color(p), bbox=BBOX)

ax_m.set_xticks(xm)
ax_m.set_xticklabels(months_cn, fontsize=11)
ax_m.set_ylim(0, y_line2*1.15)
ax_m.set_yticks([])
ax_m.spines[:].set_visible(False)

ax_m.set_title(f"月度对比（单位：{UNIT}）", fontsize=13, pad=6)


handles = [
    plt.Rectangle((0,0), 1, 1, color=c24),
    plt.Rectangle((0,0), 1, 1, color=c25),
]

fig.legend(
    handles, ["2024年", "2025年"],
    loc="upper center",
    ncol=2,
    frameon=False,
    bbox_to_anchor=(0.55, 0.975),   
    bbox_transform=fig.transFigure, 
    fontsize=12
)

plt.show()
