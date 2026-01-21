import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Patch
from matplotlib.offsetbox import DrawingArea, AnnotationBbox
from matplotlib.text import Text

def add_pie(ax, ratios, x, y, size_px=90, colors=None, startangle=90,
            label_fontsize=7, label_weight="normal"):
    ratios = np.asarray(ratios, dtype=float)
    ratios = ratios / ratios.sum()

    da = DrawingArea(size_px, size_px, 0, 0)
    r = size_px / 2
    cx, cy = r, r

    theta = startangle
    for frac, c in zip(ratios, colors):
        dtheta = 360.0 * frac
        mid = theta + dtheta / 2.0

        da.add_artist(
            Wedge((cx, cy), r, theta, theta + dtheta,
                  facecolor=c, edgecolor="white", linewidth=1.0)
        )

        rad = np.deg2rad(mid)
        tx = cx + 0.55 * r * np.cos(rad)
        ty = cy + 0.55 * r * np.sin(rad)

        da.add_artist(
            Text(tx, ty, f"{frac*100:.1f}%",
                 ha="center", va="center",
                 fontsize=label_fontsize, color="white",
                 weight=label_weight)
        )

        theta += dtheta

    ax.add_artist(AnnotationBbox(da, (x, y), frameon=False, box_alignment=(0.5, 0.5)))

# -------------------------
# Random data
# -------------------------
rng = np.random.default_rng(30)

years = np.array([2020, 2021, 2022, 2023, 2024])
x_gap = 7
x_start = 4
x = np.arange(len(years)) * x_gap + x_start

categories = ["类别 A", "类别 B", "类别 C"]
colors = ["#1f2a44", "#e7262f", "#ff3b30"]

total_sales = rng.integers(250, 900, size=len(years))
shares = rng.dirichlet(np.ones(len(categories))*1.6, size=len(years))
category_sales = shares * total_sales[:, None]

# -------------------------
# Plot
# -------------------------
fig, ax = plt.subplots(figsize=(9, 7), dpi=140)

ax.set_xlim(0, x.max() + 2)
ax.set_ylim(0, max(total_sales) * 1.25)

ax.set_xticks(x)
ax.set_xticklabels(years)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#cfd6de")
ax.spines["bottom"].set_color("#cfd6de")
ax.tick_params(axis="both", colors="#7b8794", length=4, width=1, pad=5)
ax.set_facecolor("white")

for i in range(len(years)):
    add_pie(
        ax,
        category_sales[i],
        x[i],
        total_sales[i],
        size_px=90,         
        colors=colors
    )

ax.set_ylabel("年销售 (万元)")

legend_handles = [Patch(facecolor=c, label=lab)
                  for c, lab in zip(colors, categories)]
ax.legend(handles=legend_handles,
          title="产品类别",
          frameon=False,
          loc="upper right")

plt.tight_layout()
plt.show()
