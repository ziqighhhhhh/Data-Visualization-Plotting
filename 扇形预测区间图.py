import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

t_hist = np.arange(0, 7)
y_hist = np.array([200, 300, 290, 330, 250, 275, 400], dtype=float)

t_fcst = np.arange(6, 11)  
y_fcst_mean = np.array([400, 520, 540, 620, 600], dtype=float)

sigma = np.array([0, 35, 55, 75, 95], dtype=float)

z_levels = {
    "50%": 0.674,
    "80%": 1.282,
    "95%": 1.960
}

bands = []
for name, z in z_levels.items():
    lower = y_fcst_mean - z * sigma
    upper = y_fcst_mean + z * sigma
    bands.append((name, lower, upper))


main_red = "#FF3B30"
edge_red = "#C81E1E"

alpha_map = {"95%": 0.18, "80%": 0.28, "50%": 0.42}

fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=160)

for name in ["95%", "80%", "50%"]:
    lower = [b[1] for b in bands if b[0] == name][0]
    upper = [b[2] for b in bands if b[0] == name][0]
    ax.fill_between(
        t_fcst, lower, upper,
        color=main_red,
        alpha=alpha_map[name],
        linewidth=0,
        zorder=1
    )

ax.plot(
    t_hist, y_hist,
    color=main_red,
    linewidth=2.6,
    marker="o",
    markersize=7,
    markerfacecolor=main_red,
    markeredgecolor="white",
    markeredgewidth=1.2,
    zorder=3
)

ax.plot(
    t_fcst, y_fcst_mean,
    color=edge_red,
    linewidth=2.6,
    marker="o",
    markersize=6.5,
    markerfacecolor=edge_red,
    markeredgecolor="white",
    markeredgewidth=1.2,
    zorder=4
)

ax.axvline(6, linestyle="--", linewidth=1.1, color=edge_red, alpha=0.55, zorder=2)

ax.set_xlabel("时间（期）", labelpad=10)

# ✅ y轴单位：按你的业务替换，例如“元 / 万元 / 件 / 单 / kWh”
ax.set_ylabel("销售额（万元）", labelpad=10)

ax.yaxis.grid(True, linestyle="--", alpha=0.30)
ax.xaxis.grid(False)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ax.set_xlim(t_hist.min(), t_fcst.max())
ax.margins(x=0.02)

ax.text(
    0.01, 0.95,
    "红色扇形：预测区间（95/80/50%）\n深红线：预测中心值",
    transform=ax.transAxes,
    ha="left", va="top"
)

plt.tight_layout()
plt.show()
