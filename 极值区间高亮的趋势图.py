import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import font_manager

FONT_CANDIDATES = [
    "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
    "Source Han Sans SC", "WenQuanYi Zen Hei", "Arial Unicode MS", "DejaVu Sans"
]

def pick_font(candidates):
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return name
    return "DejaVu Sans"

plt.rcParams["font.sans-serif"] = [pick_font(FONT_CANDIDATES)]
plt.rcParams["axes.unicode_minus"] = False

months = np.arange(1, 13)
months_cn = [f"{i}月" for i in months]

revenue = np.array([650, 320, 420, 937, 520, 710, 280, 740, 450, 600, 153, 364], dtype=float)

mean_val = revenue.mean()
idx_max = int(np.argmax(revenue))
idx_min = int(np.argmin(revenue))

x = months.astype(float)
y = revenue

def catmull_rom_spline(x, y, samples_per_seg=45):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < 4:
        raise ValueError("Catmull-Rom spline needs at least 4 points.")
    x_pad = np.r_[x[0] - (x[1] - x[0]), x, x[-1] + (x[-1] - x[-2])]
    y_pad = np.r_[y[0] - (y[1] - y[0]), y, y[-1] + (y[-1] - y[-2])]
    xs_all, ys_all = [], []
    for i in range(1, n):
        p0 = np.array([x_pad[i-1], y_pad[i-1]])
        p1 = np.array([x_pad[i],   y_pad[i]])
        p2 = np.array([x_pad[i+1], y_pad[i+1]])
        p3 = np.array([x_pad[i+2], y_pad[i+2]])
        t = np.linspace(0, 1, samples_per_seg, endpoint=False)
        t2 = t * t
        t3 = t2 * t
        a = 2 * p1
        b = (-p0 + p2)
        c = (2*p0 - 5*p1 + 4*p2 - p3)
        d = (-p0 + 3*p1 - 3*p2 + p3)
        pts = 0.5 * (a + np.outer(t, b) + np.outer(t2, c) + np.outer(t3, d))
        xs_all.append(pts[:, 0])
        ys_all.append(pts[:, 1])
    xs = np.concatenate(xs_all + [np.array([x[-1]])])
    ys = np.concatenate(ys_all + [np.array([y[-1]])])
    return xs, ys

xs, ys = catmull_rom_spline(x, y, samples_per_seg=45)

fig = plt.figure(figsize=(7.6, 9.2), dpi=220)
ax = fig.add_axes([0.08, 0.20, 0.84, 0.62])

ax.axvspan(x[idx_max]-0.38, x[idx_max]+0.38, color="#CDEFD8", alpha=0.85, zorder=0)
ax.axvspan(x[idx_min]-0.38, x[idx_min]+0.38, color="#F2D6D6", alpha=0.85, zorder=0)

ax.axhline(mean_val, color="#F28E2B", lw=1.6, ls="--", alpha=0.95, zorder=1)

main_color = "#6FB6C4"
outline_color = "#2E6E7A"

line, = ax.plot(xs, ys, color=main_color, lw=6.5, solid_capstyle="round", zorder=3)
line.set_path_effects([
    pe.SimpleLineShadow(offset=(0, -1.2), alpha=0.20),
    pe.Stroke(linewidth=12, foreground=outline_color, alpha=0.22),
    pe.Normal()
])

ax.scatter([x[idx_max]], [y[idx_max]], s=120, facecolors="white",
           edgecolors="#1FA35B", linewidths=2.8, zorder=5)
ax.scatter([x[idx_min]], [y[idx_min]], s=120, facecolors="white",
           edgecolors="#D64C4C", linewidths=2.8, zorder=5)

ax.text(x[idx_max]-0.45, y[idx_max]+60, f"MAX, {int(y[idx_max])}",
        color="#1FA35B", fontsize=12, fontweight="bold", zorder=7,
        path_effects=[pe.withStroke(linewidth=4, foreground="white", alpha=0.9)])
ax.text(x[idx_min]-0.55, y[idx_min]+40, f"MIN, {int(y[idx_min])}",
        color="#D64C4C", fontsize=12, fontweight="bold", zorder=7,
        path_effects=[pe.withStroke(linewidth=4, foreground="white", alpha=0.9)])

ax.text(12.45, mean_val+10, f"均值\n{int(mean_val)}",
        color="#F28E2B", fontsize=12, fontweight="bold",
        ha="left", va="bottom", zorder=7,
        path_effects=[pe.withStroke(linewidth=4, foreground="white", alpha=0.9)])

ymax = max(y) * 1.18
ax.set_xlim(0.6, 12.8)
ax.set_ylim(0, ymax)

txt_pe = [pe.withStroke(linewidth=4, foreground="white", alpha=0.95)]

for i, v in enumerate(y):
    off = 12 if v >= mean_val else -14
    ax.annotate(
        f"{int(v)}",
        xy=(x[i], v),
        xytext=(0, off),
        textcoords="offset points",
        ha="center",
        va="bottom" if off > 0 else "top",
        fontsize=10.5,
        color="#4A4A4A",
        zorder=6,
        path_effects=txt_pe
    )

ax.set_xticks(x)
ax.set_xticklabels(months_cn, fontsize=11, color="#6B6B6B")
ax.tick_params(axis="x", length=0)
ax.set_yticks([])

for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#B0B0B0")
ax.spines["bottom"].set_linewidth(1.0)

fig.text(0.08, 0.86, "2025年各月营收情况", fontsize=18, fontweight="bold", color="#4A4A4A")
fig.text(0.40, 0.86, "单位：万元", fontsize=11, color="#6B6B6B")


plt.show()

