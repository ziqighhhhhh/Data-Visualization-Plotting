
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
    "健康":        [67, 62, 65, 67, 69, 75],
    "教育":        [73, 75, 72, 70, 66, 60],
    "公共服务":    [60, 72, 69, 60, 59, 55],
    "艺术与文化":  [20, 22, 24, 30, 26, 43],
    "其他":        [53, 40, 48, 41, 47, 30],
}


line_color  = "#FE762C"
sep_color   = "#D9D9D9"
label_color = "#504B49"

categories = list(data.keys())
n = len(categories)

fig_h = 1.15 * n + 1.2
fig, axes = plt.subplots(
    nrows=n, ncols=1, figsize=(10.5, fig_h), sharex=True,
    gridspec_kw={"hspace": 0.30, "top": 0.88, "bottom": 0.16, "left": 0.20, "right": 0.95}
)
if n == 1:
    axes = [axes]

x_min, x_max = years.min(), years.max()
x_pad = 0.45
xlim = (x_min - x_pad, x_max + x_pad)

cat_x = xlim[0] - 1


def smart_annotate(ax, x, y, text, *,
                   side="right",
                   slope=None,
                   fontsize=12,
                   bold=False,
                   color=line_color,
                   occupied=None,      
                   min_sep_pt=14):     

    if occupied is None:
        occupied = []

    ymin, ymax = ax.get_ylim()
    yr = ymax - ymin if ymax > ymin else 1.0

    dx = 10 if side == "right" else -10

    if slope is None:
        dy = 0
    else:
        dy = -10 if slope > 0 else 10

    if (y > ymax - 0.12 * yr) and (dy > 0):
        dy = -abs(dy)
    if (y < ymin + 0.12 * yr) and (dy < 0):
        dy = abs(dy)


    pt_to_px = ax.figure.dpi / 72.0
    min_sep_px = min_sep_pt * pt_to_px

    x_disp, y_disp = ax.transData.transform((x, y))
    y_target = y_disp + dy * pt_to_px

    step_pt = 10
    max_iter = 30
    sign = 1 if dy >= 0 else -1  

    def too_close(y_px):
        return any(abs(y_px - yy) < min_sep_px for yy in occupied)

    it = 0
    while too_close(y_target) and it < max_iter:
        dy += sign * step_pt
        y_target = y_disp + dy * pt_to_px

        if y_target > ax.bbox.y1 - 6 * pt_to_px or y_target < ax.bbox.y0 + 6 * pt_to_px:
            sign *= -1
            dy += sign * step_pt
            y_target = y_disp + dy * pt_to_px

        it += 1

    occupied.append(y_target)

    weight = "bold" if bold else "normal"
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(dx, dy),
        textcoords="offset points",
        ha="left" if side == "right" else "right",
        va="center",
        fontsize=fontsize,
        color=color,
        fontweight=weight,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.6),
        zorder=5
    )



for ax, cat in zip(axes, categories):
    y = np.array(data[cat], dtype=float)

    ax.plot(
        years, y, color=line_color, linewidth=3.0,
        solid_capstyle="round", zorder=2
    )

    ax.scatter([years[-1]], [y[-1]], s=140, color=line_color, zorder=3)
    ax.scatter([years[0]],  [y[0]],  s=40,  color=line_color, zorder=3)

    y_min, y_max = y.min(), y.max()
    pad = max(6, 0.22 * (y_max - y_min + 1e-9))
    ax.set_ylim(y_min - pad, y_max + pad)

    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.axhline(ax.get_ylim()[0], color=sep_color, linewidth=2.0, zorder=1)

    ax.text(
        cat_x, np.mean(ax.get_ylim()), cat,
        ha="left", va="center", fontsize=20, color=label_color
    )

    slope_start = (y[1] - y[0]) / (years[1] - years[0]) if len(y) >= 2 else 0
    slope_end   = (y[-1] - y[-2]) / (years[-1] - years[-2]) if len(y) >= 2 else 0

    smart_annotate(
        ax, years[0], y[0], f"{int(round(y[0]))}%",
        side="right", slope=slope_start,
        fontsize=12, bold=False
    )

    smart_annotate(
        ax, years[-1], y[-1], f"{int(round(y[-1]))}%",
        side="right", slope=slope_end,
        fontsize=16, bold=True
    )

    ax.set_xlim(*xlim)


axes[0].xaxis.set_ticks_position("top")
axes[0].xaxis.set_label_position("top")
axes[0].set_xticks(years)
axes[0].set_xticklabels([str(y) for y in years], fontsize=12, color="#666666")
axes[0].tick_params(axis="x", length=0, pad=10)

for ax in axes[1:]:
    ax.tick_params(axis="x", which="both",
                   bottom=False, top=False,
                   labelbottom=False, labeltop=False)

fig.add_artist(plt.Line2D(
    [0.07, 0.95], [0.88, 0.88],
    transform=fig.transFigure, color=sep_color, linewidth=2.0
))


bbox_kw = dict(facecolor="white", edgecolor="none", pad=2.5)

fig.text(
    0.07, 0.895, "% 的资助者",
    ha="left", va="center", fontsize=12, color=line_color,
    transform=fig.transFigure, bbox=bbox_kw
)

foot = "百分比可理解为“选择该领域的受访者占比”。"
fig.text(
    0.065, 0.07, foot,
    ha="left", va="center", fontsize=10, color="#777777",
    transform=fig.transFigure, bbox=bbox_kw
)

plt.show()

# fig.savefig("figure_pull_lines_apart_cn.png", dpi=200, bbox_inches="tight")
