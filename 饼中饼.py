import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

def startangle_to_face_target(sizes, idx_focus, desired_mid_deg):
    sizes = np.asarray(sizes, dtype=float)
    total = sizes.sum()
    angles = 360 * sizes / total
    cum_before = angles[:idx_focus].sum()
    mid_now = cum_before + angles[idx_focus] / 2.0
    # 让 mid_now + startangle == desired_mid_deg
    return (desired_mid_deg - mid_now) % 360


labels_main = ["A类", "B类", "C类", "D类"]
sizes_main  = [35, 30, 20, 15]

labels_sub = ["B1", "B2", "B3", "B4"]
sizes_sub  = [10, 8, 7, 5]

idx_B = 1  

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(11, 5),
    gridspec_kw={"width_ratios": [1.25, 1]}
)

p1 = ax1.get_position()
p2 = ax2.get_position()
c1 = ((p1.x0 + p1.x1)/2, (p1.y0 + p1.y1)/2)
c2 = ((p2.x0 + p2.x1)/2, (p2.y0 + p2.y1)/2)
dx, dy = (c2[0] - c1[0], c2[1] - c1[1])
desired_mid_deg = (np.degrees(np.arctan2(dy, dx)) + 360) % 360

startangle_main = startangle_to_face_target(sizes_main, idx_B, desired_mid_deg)


explode = [0]*len(sizes_main)
explode[idx_B] = 0.10

wedges, _, _ = ax1.pie(
    sizes_main,
    labels=labels_main,
    autopct="%1.1f%%",
    startangle=startangle_main,
    explode=explode,
    pctdistance=0.72
)
ax1.set_title("总饼图")


for i, w in enumerate(wedges):
    if i == idx_B:
        w.set_edgecolor("black")
        w.set_linewidth(2.5)
        w.set_hatch("///")
    else:
        w.set_alpha(0.35)


ax2.pie(
    sizes_sub,
    labels=labels_sub,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.72
)
ax2.set_title("B类拆分")



wB = wedges[idx_B]

theta1, theta2 = np.deg2rad([wB.theta1, wB.theta2])
pad = 0.06
r_out = wB.r * (1 + pad)
cx, cy = wB.center
p1 = (cx + r_out*np.cos(theta1), cy + r_out*np.sin(theta1))
p2 = (cx + r_out*np.cos(theta2), cy + r_out*np.sin(theta2))

if p1[1] < p2[1]:
    p1, p2 = p2, p1


wedges2, *_ = ax2.pie(
    sizes_sub,
    labels=labels_sub,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.72
)
ax2.set_title("B类拆分")

r2 = wedges2[0].r
cx2, cy2 = wedges2[0].center

y_top = 0.65 * r2
y_bot = -0.65 * r2

x_top = cx2 - np.sqrt(max(r2**2 - y_top**2, 0))
x_bot = cx2 - np.sqrt(max(r2**2 - y_bot**2, 0))

push_in = 0.03 * r2   
q1 = (x_top + push_in, cy2 + y_top)
q2 = (x_bot + push_in, cy2 + y_bot)















# 画连接线（建议 clip_on=False，避免被坐标轴裁剪）
c1 = ConnectionPatch(xyA=p1, coordsA=ax1.transData,
                     xyB=q1, coordsB=ax2.transData,
                     color="black", lw=1.8, clip_on=False, zorder=10)
c2 = ConnectionPatch(xyA=p2, coordsA=ax1.transData,
                     xyB=q2, coordsB=ax2.transData,
                     color="black", lw=1.8, clip_on=False, zorder=10)
fig.add_artist(c1)
fig.add_artist(c2)






plt.tight_layout()
plt.show()
