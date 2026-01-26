import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager

df = pd.DataFrame({
    "国家": ["布基纳法索","多哥","佛得角","冈比亚","几内亚","加纳","科特迪瓦","利比里亚","马里","毛里塔尼亚","尼日利亚","塞拉利昂","塞内加尔"],
    "Y25达成": [26, 8167, 187, 1757, 6353, 10218, 6824.1, 2038.3, 15, 1930, 68645.1, 2967, 1068],
    "绝对值增长": [19, 3186, 0, 1199, 61, -1488, 2893.1, 147.7, -170, 842, 4730, 89, 836],
    "同比": [2.36, 0.64, 0.00, 2.15, 0.01, -0.13, 0.74, 0.08, -0.92, 0.77, 0.07, 0.03, 3.61],  # ratio
})


candidates = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS"]
available = {f.name for f in font_manager.fontManager.ttflist}
for f in candidates:
    if f in available:
        plt.rcParams["font.sans-serif"] = [f]
        break
plt.rcParams["axes.unicode_minus"] = False


def fmt_num(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    if isinstance(x, (int, np.integer)):
        return f"{x:,d}"
    if isinstance(x, (float, np.floating)):
        if math.isclose(x, round(x), rel_tol=0, abs_tol=1e-9):
            return f"{int(round(x)):,d}"
        s = f"{x:,.1f}"
        return s[:-2] if s.endswith(".0") else s
    return str(x)

def fmt_pct(r):
    if r is None or (isinstance(r, float) and np.isnan(r)):
        return ""
    return f"{int(round(r*100))}%"

def draw_databar(ax, xL, xR, yC, cell_h, val, min_neg, max_pos,
                 color_pos="#16a34a", color_neg="#dc2626", alpha=1.0):
    pad_x = (xR - xL) * 0.04
    barL = xL + pad_x
    barR = xR - pad_x
    barW = barR - barL

    barH = cell_h * 0.32
    yB = yC - barH / 2

    if min_neg < 0 and max_pos > 0:
        zero_pos = (-min_neg) / (max_pos - min_neg)
    elif min_neg < 0 and max_pos <= 0:
        zero_pos = 1.0
    else:
        zero_pos = 0.0

    x0 = barL + zero_pos * barW

    ax.plot([x0, x0], [yC - cell_h*0.35, yC + cell_h*0.35], lw=0.6, color="#d1d5db", zorder=1)

    if val == 0 or (isinstance(val, float) and np.isnan(val)):
        return

    if val > 0:
        denom = max_pos if max_pos > 0 else 1.0
        w = (val / denom) * (barW * (1 - zero_pos))
        ax.add_patch(Rectangle((x0, yB), w, barH, facecolor=color_pos, edgecolor="none", alpha=alpha, zorder=2))
    else:
        denom = abs(min_neg) if min_neg < 0 else 1.0
        w = (abs(val) / denom) * (barW * zero_pos)
        ax.add_patch(Rectangle((x0 - w, yB), w, barH, facecolor=color_neg, edgecolor="none", alpha=alpha, zorder=2))


n = len(df)
fig, ax = plt.subplots(figsize=(13.5, 5.2), dpi=200)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

x0 = 0.00
x_country = 0.22
x_y25 = 0.38
x_abs = 0.70
x3 = 1.00

top = 0.96
bottom = 0.04
total_h = top - bottom
row_h = total_h / (n + 1)  

grid = "#e5e7eb"
header_bg = "#f3f4f6"
text_c = "#111827"

ax.add_patch(Rectangle((x0, top - row_h), x3 - x0, row_h, facecolor=header_bg, edgecolor="none"))

for xx in [x0, x_country, x_y25, x_abs, x3]:
    ax.plot([xx, xx], [bottom, top], color=grid, lw=1.0)

for i in range(n + 2):
    y = top - i * row_h
    ax.plot([x0, x3], [y, y], color=grid, lw=1.0)

ax.text((x0 + x_country) / 2, top - row_h / 2, "国家", ha="center", va="center", fontsize=11, color=text_c, weight="bold")
ax.text((x_country + x_y25) / 2, top - row_h / 2, "Y25达成", ha="center", va="center", fontsize=11, color=text_c, weight="bold")
ax.text((x_y25 + x_abs) / 2, top - row_h / 2, "绝对值增长", ha="center", va="center", fontsize=11, color=text_c, weight="bold")
ax.text((x_abs + x3) / 2, top - row_h / 2, "同比", ha="center", va="center", fontsize=11, color=text_c, weight="bold")

abs_vals = df["绝对值增长"].astype(float).values
yoy_vals = df["同比"].astype(float).values

abs_min = min(0.0, float(np.nanmin(abs_vals)))
abs_max = max(0.0, float(np.nanmax(abs_vals)))
yoy_min = min(0.0, float(np.nanmin(yoy_vals)))
yoy_max = max(0.0, float(np.nanmax(yoy_vals)))

for i, row in df.iterrows():
    y_top_i = top - (i + 1) * row_h
    yC = y_top_i - row_h / 2

    ax.text(x0 + 0.01, yC, str(row["国家"]), ha="left", va="center", fontsize=10.5, color=text_c)

    ax.text(x_y25 - 0.01, yC, fmt_num(row["Y25达成"]), ha="right", va="center", fontsize=10.5, color=text_c)

    draw_databar(ax, x_y25, x_abs, yC, row_h, float(row["绝对值增长"]), abs_min, abs_max)
    ax.text(x_abs - 0.01, yC, fmt_num(row["绝对值增长"]), ha="right", va="center", fontsize=10.5, color=text_c)

    draw_databar(ax, x_abs, x3, yC, row_h, float(row["同比"]), yoy_min, yoy_max)
    ax.text(x3 - 0.01, yC, fmt_pct(float(row["同比"])), ha="right", va="center", fontsize=10.5, color=text_c)

plt.tight_layout()
plt.show()

