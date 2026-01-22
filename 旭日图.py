import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import math


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


unit = "万元"  

data = {
    "菲律宾": {"锂电储能柜": 420, "户用套装": 310, "逆变器": 160, "太阳能板": 110},
    "坦桑尼亚": {"锂电储能柜": 260, "户用套装": 180, "逆变器": 140, "太阳能板": 90},
    "尼日利亚": {"锂电储能柜": 380, "户用套装": 220, "逆变器": 150, "太阳能板": 70},
    "加纳": {"锂电储能柜": 210, "户用套装": 160, "逆变器": 100, "太阳能板": 60},
}

countries = list(data.keys())
country_totals = {c: sum(data[c].values()) for c in countries}
grand_total = sum(country_totals.values())

countries = sorted(countries, key=lambda c: country_totals[c], reverse=True)


base_colors = [
    "#FF3B30",  
    "#1F2A44",  
    "#C61D2C",  
    "#2B3550",  
    "#FF6A63", 
    "#3B4768",  
]
def lighten(hex_color, factor=0.25):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02X}{g:02X}{b:02X}"

country_color = {}
for i, c in enumerate(countries):
    country_color[c] = base_colors[i % len(base_colors)]


fig, ax = plt.subplots(figsize=(8, 8), dpi=160)
ax.set_aspect("equal")
ax.axis("off")

r0 = 0.38  
r1 = 0.62   
r2 = 0.94   

inner_width = r1 - r0
outer_width = r2 - r1

start_angle = 90.0  

label_color = "#2B2B2B"
line_color = "#B8C0CC"

def pol2cart(r, theta_deg):
    theta = np.deg2rad(theta_deg)
    return r * np.cos(theta), r * np.sin(theta)

# -----------------------------
# 5) 画内圈：国家总量
# -----------------------------
current_angle = start_angle

country_angle_span = {}

for c in countries:
    v = country_totals[c]
    if v <= 0:
        continue
    frac = v / grand_total
    span = 360.0 * frac
    theta1 = current_angle
    theta2 = current_angle - span  
    country_angle_span[c] = (theta2, theta1)  

    w = Wedge(
        center=(0, 0),
        r=r1,
        theta1=theta2,
        theta2=theta1,
        width=inner_width,
        facecolor=country_color[c],
        edgecolor="white",
        linewidth=1.2,
    )
    ax.add_patch(w)

    mid = (theta1 + theta2) / 2.0
    tx, ty = pol2cart((r0 + r1) / 2.0, mid)
    pct = 100.0 * v / grand_total
    ax.text(
        tx, ty,
        f"{c}\n{v:.0f}{unit}\n({pct:.1f}%)",
        ha="center", va="center",
        fontsize=10,
        color="white",
        weight="bold",
        linespacing=1.15
    )

    current_angle = theta2


for c in countries:
    if c not in country_angle_span:
        continue
    a0, a1 = country_angle_span[c]  
    total = country_totals[c]
    cats = list(data[c].items())
    cats.sort(key=lambda x: x[1], reverse=True)

    ang = a1  
    for j, (cat, val) in enumerate(cats):
        if val <= 0:
            continue
        frac = val / total
        span = (a1 - a0) * frac  
        t1 = ang
        t2 = ang - span

        col = lighten(country_color[c], factor=0.18 + 0.18 * (j % 4))

        w2 = Wedge(
            center=(0, 0),
            r=r2,
            theta1=t2,
            theta2=t1,
            width=outer_width,
            facecolor=col,
            edgecolor="white",
            linewidth=1.1,
        )
        ax.add_patch(w2)

        mid = (t1 + t2) / 2.0

 
        if (span >= 12): 
            x0, y0 = pol2cart(r2, mid)
            x1, y1 = pol2cart(r2 + 0.06, mid)
            align = "left" if x1 >= 0 else "right"
            x2 = x1 + (0.16 if x1 >= 0 else -0.16)
            y2 = y1

            ax.plot([x0, x1, x2], [y0, y1, y2], color=line_color, linewidth=1.0)

            pct_in_country = 100.0 * val / total
            ax.text(
                x2, y2,
                f"{cat}  {val:.0f}{unit}  ({pct_in_country:.0f}%)",
                ha=align, va="center",
                fontsize=6,
                color=label_color
            )

        ang = t2


center_circle = plt.Circle((0, 0), r0, color="white")
ax.add_artist(center_circle)

ax.text(
    0, 0,
    f"总销售\n{grand_total:.0f}{unit}",
    ha="center", va="center",
    fontsize=13,
    color="#1F2A44",
    weight="bold",
    linespacing=1.2
)


plt.tight_layout()
plt.show()

