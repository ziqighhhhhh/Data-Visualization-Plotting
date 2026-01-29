import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "Noto Sans CJK SC"]
mpl.rcParams["axes.unicode_minus"] = False


cats = ["鹅厂", "度厂", "字厂", "阿厂", "团厂", "金厂", "米厂", "蔚厂", "比厂"]

done = np.array([16880, 12099, 7620, 6900, 4320, 3200, 4430, 2100, 1400], dtype=float)

target = np.array([16880, 12896, 9251, 9000, 7911, 7121, 5988, 5100, 4300], dtype=float)


rate = np.array([1.00, 0.94, 0.82, 0.77, 0.55, 0.45, 0.74, 0.41, 0.33], dtype=float)



gap = np.maximum(target - done, 0)  


fig = plt.figure(figsize=(8.2, 6))
gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[3.3, 1.15], wspace=0.25)

ax_bar = fig.add_subplot(gs[0, 0])
ax_rate = fig.add_subplot(gs[0, 1], sharey=ax_bar)

y = np.arange(len(cats))


c_done = "#49AFC7"   
c_gap  = "#545454"   

ax_bar.barh(y, done, color=c_done, height=0.62)
ax_bar.barh(y, gap, left=done, color=c_gap, height=0.62)


ax_bar.set_yticks(y)
ax_bar.set_yticklabels(cats, fontsize=11)
ax_bar.invert_yaxis()


for i, v in enumerate(done):
    ax_bar.text(v * 0.5, y[i], f"{int(v):,}", va="center", ha="center",
                color="white", fontsize=10, fontweight="bold")

for i, t in enumerate(target):
    ax_bar.text(t + target.max()*0.01, y[i], f"{int(t):,}", va="center", ha="left",
                color="#333333", fontsize=10)


ax_bar.set_xlim(0, target.max() * 1.18)
ax_bar.spines["top"].set_visible(False)
ax_bar.spines["right"].set_visible(False)
ax_bar.spines["bottom"].set_visible(False)
ax_bar.tick_params(axis="x", which="both", bottom=False, labelbottom=False)


ax_rate.plot(rate, y, color="#000000", linewidth=1.8, zorder=2)

threshold = 0.70
colors_pt = np.where(rate >= threshold, "#06B35A", "#C94A4A")  
ax_rate.scatter(rate, y, s=60, color=colors_pt, zorder=3)


for yi in y:
    ax_rate.hlines(yi, xmin=0, xmax=1.05, colors="#BDBDBD",
                   linestyles=(0, (2, 2)), linewidth=0.8, zorder=1)


for i, r in enumerate(rate):
    ax_rate.text(r + 0.06, y[i], f"{int(round(r*100))}%", va="center", ha="left",
                 fontsize=10, fontweight="bold", color=colors_pt[i])

ax_rate.set_xlim(0, 1.1)
ax_rate.spines["top"].set_visible(False)
ax_rate.spines["bottom"].set_visible(False)
ax_rate.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
ax_rate.tick_params(axis="y", left=False, labelleft=False)  

plt.tight_layout()
plt.show()
