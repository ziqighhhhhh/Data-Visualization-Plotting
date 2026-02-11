
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


MAIN_COLOR = "#FE762C"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False


data = [
    ("北京", 100),
    ("广东", 86),
    ("浙江", 66),
    ("东北", 56),
    ("上海", 55),
    ("青海", 44),
    ("湖南", 33),
    ("湖北", 24),
    ("吉林", 21),
    ("河南", 15),
    ("河北", 5),
    ("安徽", 4),
    ("江西", 2),
]
vals = np.array([v for _, v in data], dtype=float)


deg_top_left = 105
deg_bottom_left = 235
tightness = 1

mid = 0.5 * (deg_top_left + deg_bottom_left)
span = (deg_bottom_left - deg_top_left) * tightness
deg_start = mid - span / 2
deg_end   = mid + span / 2

angles = np.linspace(np.deg2rad(deg_start), np.deg2rad(deg_end), len(data))

R = 1.05  
x = R * np.cos(angles)
y = R * np.sin(angles)

s_min, s_max = 160, 1800
s = s_min + (vals - vals.min()) / (vals.max() - vals.min()) * (s_max - s_min)


fig = plt.figure(figsize=(7.2, 7.2), dpi=220)
ax = plt.gca()
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1.65, 1.65)
ax.set_ylim(-1.65, 1.95)

ax.text(
    0.06, 0.96, "散点气泡图",
    transform=ax.transAxes,
    ha="left", va="top",
    fontsize=26, fontweight="bold",
    color="#333333"
)


center = (0.25, 0.05)

outer_ring = Circle(center, radius=0.88, facecolor="none",
                    edgecolor=MAIN_COLOR, linewidth=2.5, alpha=0.18)
ax.add_patch(outer_ring)

outer_ring2 = Circle(center, radius=0.94, facecolor="none",
                     edgecolor=MAIN_COLOR, linewidth=2.0, alpha=0.10)
ax.add_patch(outer_ring2)

big_circle = Circle(center, radius=0.82, facecolor=MAIN_COLOR,
                    edgecolor="none", alpha=0.28)
ax.add_patch(big_circle)

info_lines = [
    "销量冠军：北京",
    "销售量：100辆",
    "来源：公开网络",
    "时间：2026年",
]
y0, dy = center[1] + 0.16, 0.18
for i, t in enumerate(info_lines):
    ax.text(
        center[0], y0 - i * dy, t,
        ha="center", va="center",
        fontsize=14 if i != 1 else 22,
        fontweight="bold" if i == 1 else "normal",
        color="white"
    )


ax.scatter(x, y, s=s, c=MAIN_COLOR, alpha=0.45, edgecolors="none")


label_offset = 0.12 

for (name, v), xi, yi in zip(data, x, y):
    vec = np.array([xi - center[0], yi - center[1]])
    norm = np.linalg.norm(vec) if np.linalg.norm(vec) > 1e-9 else 1.0
    u = vec / norm

    lx = xi + u[0] * label_offset
    ly = yi + u[1] * label_offset

    ha = "left" if lx >= center[0] else "right"
    ax.text(lx, ly, f"{name}, {int(v)}",
            ha=ha, va="center", fontsize=12.5, color="#333333")

plt.show()

