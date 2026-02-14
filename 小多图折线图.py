

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["font.sans-serif"] = [
    "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
    "Source Han Sans SC", "WenQuanYi Micro Hei", "Arial Unicode MS", "DejaVu Sans"
]


years = np.arange(2010, 2016)

data = {
    "健康":        [67, 53, 61, 65, 70, 75],
    "教育":        [73, 80, 74, 71, 64, 60],
    "公共服务":    [60, 85, 78, 60, 58, 55],
    "艺术与文化":  [20, 24, 27, 42, 30, 43],
    "其他":        [53, 30, 45, 31, 46, 30],
}

title_map = {
    "健康": "Health",
    "教育": "Education",
    "公共服务": "Human\nservices",
    "艺术与文化": "Arts &\nculture",
    "其他": "Other",
}

cats = list(data.keys())


highlight_color = "#FE762C"  
bg_color = "#BFBFBF"         
axis_grey = "#6b6b6b"
spine_grey = "#BFBFBF"
title_blue = "#FE762C"


fig, axes = plt.subplots(
    nrows=1, ncols=len(cats),
    figsize=(13.5, 5.2),
    sharey=True,
    gridspec_kw={"wspace": 0.35, "left": 0.09, "right": 0.98, "top": 0.72, "bottom": 0.22}
)


for ax, focus_cat in zip(axes, cats):
    for cat in cats:
        y = np.array(data[cat], dtype=float)
        if cat == focus_cat:
            continue
        ax.plot(
            years, y,
            color=bg_color, linewidth=2.5,
            solid_capstyle="round", zorder=1
        )

    y_focus = np.array(data[focus_cat], dtype=float)
    ax.plot(
        years, y_focus,
        color=highlight_color, linewidth=3.5,
        solid_capstyle="round", zorder=3
    )

    ax.set_xlim(years.min(), years.max())
    ax.set_ylim(0, 100)

    ax.set_xticks([2010, 2015])
    ax.set_xticklabels(["2010", "2015"], fontsize=12, color=axis_grey)
    ax.set_xticks(years, minor=True)
    ax.tick_params(axis="x", which="minor", length=4, color=spine_grey)
    ax.tick_params(axis="x", which="major", length=0, pad=8)

    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_yticklabels([f"{i}%" for i in range(0, 101, 10)], fontsize=12, color=axis_grey)
    ax.tick_params(axis="y", length=0, pad=6)

    ax.set_title(
        title_map.get(focus_cat, focus_cat),
        fontsize=16, color=title_blue, pad=18, fontweight="bold"
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color(spine_grey)
    ax.spines["bottom"].set_color(spine_grey)

    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)

axes[0].set_ylabel(
    "资\n助\n者\n占\n比",
    fontsize=13,
    color=axis_grey,
    labelpad=18,
    rotation=0,          
    va="center"
)
for ax in axes[1:]:
    ax.tick_params(axis="y", labelleft=False)
    ax.spines["left"].set_visible(False)


fig.suptitle(
    "各地区资助者支持的非营利组织类型",
    x=0.09, ha="left", fontsize=22, color=axis_grey
)

foot = "数据为资助者自报；由于可多选，百分比总和可能超过 100%。"
fig.text(0.09, 0.10, foot, ha="left", va="center", fontsize=11, color=axis_grey)

plt.show()

# fig.savefig("small_multiples_highlight_cn.png", dpi=200, bbox_inches="tight")
