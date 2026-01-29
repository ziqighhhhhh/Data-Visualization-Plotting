import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import to_rgba


quarters = ["Q1", "Q2", "Q3", "Q4"]
values   = [304, 456, 162, 237]

unit = "万"         
axis_label = f"销量（{unit}）"  
title_unit = f"（单位：{unit}）"  

mus    = np.array([1.0, 2.1, 3.2, 4.3])
sigmas = np.array([0.22, 0.24, 0.18, 0.22])
x = np.linspace(0.2, 5.1, 2000)

def gradient_under_curve(ax, x, y, color, alpha_top=0.95, alpha_bottom=0.0, zorder=2):
    y = np.maximum(y, 0)
    ymin, ymax = 0.0, float(y.max())
    if ymax <= 0:
        return

    rgba = np.array(to_rgba(color))
    n = 256
    img = np.ones((n, 2, 4), dtype=float)
    img[..., :3] = rgba[:3]
    img[..., 3] = np.linspace(alpha_bottom, alpha_top, n)[:, None]

    im = ax.imshow(
        img,
        extent=[x.min(), x.max(), ymin, ymax],
        origin="lower",
        aspect="auto",
        zorder=zorder,
        interpolation="bicubic",
    )

    verts = np.vstack([np.column_stack([x, y]), [x[-1], ymin], [x[0], ymin]])
    clip_poly = Polygon(verts, closed=True, facecolor="none", edgecolor="none")
    ax.add_patch(clip_poly)
    im.set_clip_path(clip_poly)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(12, 4.8), dpi=200)

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

for i, (mu, sigma, v) in enumerate(zip(mus, sigmas, values)):
    y = v * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    c = colors[i % len(colors)]

    gradient_under_curve(ax, x, y, c, alpha_top=0.95, alpha_bottom=0.0, zorder=2+i)


    ax.text(
        mu, y.max() + max(values)*0.05,
        f"{quarters[i]}, {values[i]} {unit}",   
        ha="center", va="bottom",
        fontsize=12, fontweight="bold",
        color=c
    )

ax.set_title(f"2025年各季度销量 {title_unit}", fontsize=16, fontweight="bold", pad=14)

ax.axhline(0, color="0.55", lw=1.2)

ax.set_xlabel(axis_label, fontsize=12, labelpad=10)

ax.set_yticks([])
ax.set_xticks([])
for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.set_xlim(0.2, 5.1)
ax.set_ylim(0, max(values) * 1.35)

plt.tight_layout()
plt.show()
