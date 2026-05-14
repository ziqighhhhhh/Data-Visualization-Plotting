import numpy as np
import matplotlib.pyplot as plt


plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Arial Unicode MS"
]
plt.rcParams["axes.unicode_minus"] = False


products = ["产品A", "产品B", "产品C", "产品D"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

data = {
    "产品A": [81, 64, 9, 40],
    "产品B": [65, 86, 39, 69],
    "产品C": [40, 18, 90, 65],
    "产品D": [20, 58, 23, 4],
}

highlight_product = "产品A"

highlight_color = "#FE762C"
normal_color = "#504B49"


x_positions = []
x_labels = []

for i, product in enumerate(products):
    for j, q in enumerate(quarters):
        x_positions.append(i * 5 + j)
        x_labels.append(q)

x_positions = np.array(x_positions)


fig, ax = plt.subplots(figsize=(12, 7), dpi=150)


for i, product in enumerate(products):
    start = i * 5 - 0.5
    end = i * 5 + 3.5

    if product == highlight_product:
        ax.axvspan(start, end, color=highlight_color, alpha=0.10, zorder=0)
    else:
        ax.axvspan(start, end, color="#F3F3F3", alpha=0.8, zorder=0)


for i, product in enumerate(products):

    y = data[product]
    x = np.array([i * 5 + j for j in range(4)])

    if product == highlight_product:
        color = highlight_color
        lw = 3.0
        zorder = 4
    else:
        color = normal_color
        lw = 2.0
        zorder = 3

    ax.plot(
        x,
        y,
        color=color,
        linewidth=lw,
        marker="o",
        markersize=7,
        markerfacecolor="white",
        markeredgecolor=color,
        markeredgewidth=2,
        label=product,
        zorder=zorder
    )


    for xi, yi in zip(x, y):
        ax.text(
            xi,
            yi + 3 if yi < 85 else yi - 6,
            f"{yi}%",
            ha="center",
            va="bottom" if yi < 85 else "top",
            fontsize=10,
            color=color,
            fontweight="bold" if product == highlight_product else "normal"
        )


ax.set_title(
    "产品销量目标达成率",
    loc="left",
    fontsize=20,
    fontweight="bold",
    pad=34
)

legend = ax.legend(
    loc="upper left",
    bbox_to_anchor=(0, 1.04),
    frameon=False,
    ncol=4,
    fontsize=10,
    handlelength=2.2,
    handleheight=1,
    columnspacing=1.6,
    borderaxespad=0
)

legend._legend_box.align = "left"


ax.set_xticks(x_positions)
ax.set_xticklabels(x_labels, fontsize=10)

ax.set_xlim(-0.8, 18.8)
ax.set_ylim(0, 105)

ax.set_yticks(np.arange(0, 101, 10))
ax.set_yticklabels([f"{i}%" for i in range(0, 101, 10)], fontsize=10)

ax.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
ax.grid(axis="x", visible=False)

ax.tick_params(axis="x", length=0)
ax.tick_params(axis="y", length=0)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ax.spines["left"].set_color("#DDDDDD")
ax.spines["bottom"].set_color("#DDDDDD")

fig.patch.set_facecolor("white")
ax.set_facecolor("white")


plt.tight_layout()

plt.savefig(
    "产品销量目标达成率.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
