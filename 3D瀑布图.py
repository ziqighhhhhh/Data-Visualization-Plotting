import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib import cm

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

def make_month_curve(days, peak_day, peak_height, width, noise=6, seed=None):
    rng = np.random.default_rng(seed)
    x = days.astype(float)
    main = peak_height * np.exp(-0.5 * ((x - peak_day) / width) ** 2)
    sub  = 0.35 * peak_height * np.exp(-0.5 * ((x - (peak_day + 7)) / (width * 1.2)) ** 2)
    base = 12 + 2 * np.sin(x / 2.8)
    y = base + main + sub + rng.normal(0, noise, size=len(x))
    return np.clip(y, 0, None)

n_months = 12
days_in_month = 30
days = np.arange(1, days_in_month + 1)

curves = []
for m in range(n_months):
    peak_day = 8 + (m % 4) * 2
    peak_height = 260 + m * 10
    width = 2.6 + 0.15 * (m % 3)
    curves.append(make_month_curve(days, peak_day, peak_height, width, noise=7, seed=100 + m))


fig = plt.figure(figsize=(10, 8), dpi=160)
ax = fig.add_subplot(111, projection="3d")

verts = []
for y in curves:
    xs = days
    ys = y
    verts.append([(xs[0], 0)] + list(zip(xs, ys)) + [(xs[-1], 0)])

cmap = cm.get_cmap("Reds")
facecolors = [cmap(0.45 + 0.5 * (i / (n_months - 1))) for i in range(n_months)]

poly = PolyCollection(
    verts,
    facecolors=facecolors,
    edgecolors="white",
    linewidths=1.2,
    alpha=0.98
)

y_positions = np.arange(1, n_months + 1)
ax.add_collection3d(poly, zs=y_positions, zdir="y")


ax.set_xlim(1, days_in_month)
ax.set_ylim(0.5, n_months + 0.8)
ax.set_zlim(0, max(np.max(c) for c in curves) * 1.15)

ax.set_xlabel("日", labelpad=10)

ax.set_yticks(y_positions)
ax.set_yticklabels([f"{i}月" for i in y_positions])

ax.zaxis.set_rotate_label(False)
ax.zaxis.labelpad = 22

ax.zaxis.label.set_color("#000000")

ax.view_init(elev=25, azim=-55)

ax.xaxis.pane.set_alpha(0.0)
ax.yaxis.pane.set_alpha(0.0)
ax.zaxis.pane.set_alpha(0.0)
ax.grid(True)

fig.subplots_adjust(left=0.03, right=0.92, bottom=0.03, top=0.98)


fig.text(0.89, 0.55, "销售额（万元）", rotation=90, va="center", ha="center")

plt.show()
