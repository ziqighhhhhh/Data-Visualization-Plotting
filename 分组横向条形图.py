import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


np.random.seed(7)

categories = ["价格", "便利性", "关系", "服务", "选择"]

series = [
    "我方业务",
    "对手A",
    "对手B",
    "对手C",
    "对手D",
    "对手E",
]

color_map = {
    "我方业务": "#4E86C6",
    "对手A":   "#BFC2C5",
    "对手B":   "#BFC2C5",
    "对手C":   "#BFC2C5",
    "对手D":   "#BFC2C5",
    "对手E":   "#BFC2C5",
}

vals = {}
for c in categories:
    base = np.random.uniform(50, 98, size=len(series))
    if c == "价格":
        base[0] = 92
    elif c == "便利性":
        base[0] = 78
    elif c == "关系":
        base[0] = 60
    elif c == "服务":
        base[0] = 35
    elif c == "选择":
        base[0] = 33
    vals[c] = base

ranks = {}
for c in categories:
    order = np.argsort(vals[c])[::-1]
    ranks[c] = int(np.where(order == 0)[0][0]) + 1

forced_rank_text = {
    "价格": "1 / 6",
    "便利性": "2 / 6",
    "关系": "4 / 6",
    "服务": "6 / 6",
    "选择": "6 / 6",
}


plt.rcParams["font.family"] = ["Microsoft YaHei", "SimHei", "Arial", "DejaVu Sans", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

n_series = len(series)
gap = 1.1
bar_h = 0.18
within_gap = 0.03
row_step = bar_h + within_gap
group_height = n_series * row_step

fig = plt.figure(figsize=(13.5, 7.2), dpi=140)
ax = fig.add_axes([0.28, 0.12, 0.68, 0.78])


y_centers = []
y0 = 0.0

for cat in categories:
    ys = [y0 + i * row_step for i in range(n_series)]  

    y_centers.append(y0 + (group_height - row_step) / 2.0)

    for i in range(1, n_series):
        name = series[i]
        ax.barh(
            ys[i],
            vals[cat][i],
            height=bar_h,
            color=color_map[name],
            edgecolor="none",
            zorder=1
        )

    ax.barh(
        ys[0],
        vals[cat][0],
        height=bar_h,
        color=color_map["我方业务"],
        edgecolor="none",
        zorder=3
    )

    rank_txt = forced_rank_text.get(cat, f"{ranks[cat]} / {n_series}")
    ax.text(
        vals[cat][0] + 1.2,
        ys[0],
        rank_txt,
        va="center",
        ha="left",
        fontsize=11,
        color=color_map["我方业务"]
    )

    y0 += group_height + gap


ax.set_xlim(0, 100)
ax.set_ylim(-0.6, y0 - gap + 0.8)
ax.invert_yaxis()

ax.set_xticks([])
ax.set_yticks(y_centers)
ax.set_yticklabels(categories, fontsize=18, color="#5A5A5A")
ax.tick_params(axis="y", length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.text(
    0.0, 1.02,
    "加权表现指数 | 相对排名",
    transform=ax.transAxes,
    ha="left",
    va="bottom",
    fontsize=14,
    color="#7A7A7A"
)


fig.text(0.03, 0.93, "表现概览", fontsize=26, color="#7A7A7A", ha="left", va="top")

legend_handles = [Patch(facecolor=color_map[name], edgecolor="none", label=name) for name in series]
leg = fig.legend(
    handles=legend_handles,
    loc="upper left",
    bbox_to_anchor=(0.03, 0.84),
    frameon=False,
    ncol=1,
    fontsize=14,
    handlelength=0.9,
    handletextpad=0.6,
    borderaxespad=0.0
)

for t in leg.get_texts():
    if t.get_text() == "我方业务":
        t.set_color(color_map["我方业务"])
        t.set_fontweight("bold")
    else:
        t.set_color("#8A8A8A")

plt.show()
