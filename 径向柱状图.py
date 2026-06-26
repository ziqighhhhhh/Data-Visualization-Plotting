import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle, Polygon, Wedge
from matplotlib.lines import Line2D
from pathlib import Path


data = [
    {"rank": 1,  "country": "Singapore",     "value": 26, "flag": "SG"},
    {"rank": 2,  "country": "UAE",           "value": 21, "flag": "AE"},
    {"rank": 3,  "country": "EU",            "value": 20, "flag": "EU"},
    {"rank": 4,  "country": "South Korea",   "value": 18, "flag": "KR"},
    {"rank": 5,  "country": "Australia",     "value": 16, "flag": "AU"},
    {"rank": 6,  "country": "UK",            "value": 16, "flag": "UK"},
    {"rank": 7,  "country": "Chile",         "value": 15, "flag": "CL"},
    {"rank": 8,  "country": "China",         "value": 14, "flag": "CN"},
    {"rank": 9,  "country": "U.S.",          "value": 14, "flag": "US"},
    {"rank": 10, "country": "Canada",        "value": 12, "flag": "CA"},
    {"rank": 11, "country": "Peru",          "value": 12, "flag": "PE"},
    {"rank": 12, "country": "NZ",   "value": 12, "flag": "NZ"},
]



BAR = "#075E64"            # 主弧线颜色
BAR_HIGHLIGHT = "#14777D"  # 弧线内部细高光
GRID = "#AAB4A2"           # 背景辅助线
TEXT = "#11140F"           # 主文字
SUBTEXT = "#4A5148"        # 副文字
WHITE = "#FAFCF2"          # 白色文字和 Rank 底栏

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.facecolor"] = "none"
plt.rcParams["axes.facecolor"] = "none"


center = (12.25, -0.30)

r_outer = 9.65
r_inner = 1.95
radii = np.linspace(r_outer, r_inner, len(data))

theta_bottom = 180         
theta_low = 142            
theta_high = 96            

# 弧线粗细
line_width = 23

# flag 尺寸
badge_radius = 0.19

min_value = min(d["value"] for d in data)
max_value = max(d["value"] for d in data)

def value_to_angle(v):
    """将数值映射到角度。数值越高，弧线越长，终点越靠上。"""
    return theta_low + (v - min_value) / (max_value - min_value) * (theta_high - theta_low)

def pol2cart(r, theta_deg):
    """极坐标转笛卡尔坐标。"""
    theta = np.deg2rad(theta_deg)
    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    return x, y

# ============================================================
# 4. Flag drawing helpers
# ============================================================

def draw_star(ax, x, y, r, color, z=20):
    """绘制五角星。"""
    angles = np.linspace(90, 450, 11)[:-1]
    pts = []
    for i, a in enumerate(angles):
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((
            x + rr * np.cos(np.deg2rad(a)),
            y + rr * np.sin(np.deg2rad(a))
        ))
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=z))

def draw_flag_badge(ax, x, y, code, radius=0.19, z=30):
    """绘制简化版圆形旗帜徽章。"""
    # 外圈
    outer = Circle((x, y), radius, facecolor=WHITE, edgecolor=BAR, linewidth=1.5, zorder=z)
    ax.add_patch(outer)

    # 内部裁切圆
    clip = Circle((x, y), radius * 0.86, transform=ax.transData)
    ax.add_patch(Circle((x, y), radius * 0.86, facecolor="white", edgecolor="none", zorder=z + 1))

    def rect(dx, dy, w, h, color):
        p = Rectangle((x + dx, y + dy), w, h, facecolor=color, edgecolor="none", zorder=z + 2)
        p.set_clip_path(clip)
        ax.add_patch(p)

    def circ(dx, dy, rr, color):
        p = Circle((x + dx, y + dy), rr, facecolor=color, edgecolor="none", zorder=z + 3)
        p.set_clip_path(clip)
        ax.add_patch(p)

    R = radius * 0.86

    # Singapore
    if code == "SG":
        rect(-R, 0, 2 * R, R, "#E1262F")
        circ(-0.055, 0.075, 0.055, "white")
        circ(-0.032, 0.075, 0.044, "#E1262F")
        for a in np.linspace(0, 360, 5, endpoint=False):
            draw_star(ax, x + 0.058 + 0.029 * np.cos(np.deg2rad(a)), 
                      y + 0.075 + 0.029 * np.sin(np.deg2rad(a)), 0.010, "white", z + 5)

    # UAE
    elif code == "AE":
        rect(-R, -R, R * 0.55, 2 * R, "#CE1126")
        rect(-R * 0.45, R / 3, 1.45 * R, R * 2 / 3, "#00732F")
        rect(-R * 0.45, -R / 3, 1.45 * R, R * 2 / 3, "white")
        rect(-R * 0.45, -R, 1.45 * R, R * 2 / 3, "black")

    # EU
    elif code == "EU":
        circ(0, 0, R, "#2455A4")
        for a in np.linspace(0, 360, 12, endpoint=False):
            draw_star(ax, x + 0.074 * np.cos(np.deg2rad(a)), 
                      y + 0.074 * np.sin(np.deg2rad(a)), 0.009, "#FFD700", z + 5)

    # South Korea
    elif code == "KR":
        circ(0, 0.016, 0.082, "#CD2E3A")
        ax.add_patch(Wedge((x, y + 0.016), 0.082, 180, 360, facecolor="#0047A0", edgecolor="none", zorder=z + 5))
        for dx in [-0.10, 0.10]:
            ax.add_line(Line2D([x + dx - 0.022, x + dx + 0.022], [y + 0.093, y + 0.076], color="black", lw=0.7, zorder=z + 5))
            ax.add_line(Line2D([x + dx - 0.022, x + dx + 0.022], [y - 0.076, y - 0.093], color="black", lw=0.7, zorder=z + 5))

    # Australia / New Zealand
    elif code in ["AU", "NZ"]:
        circ(0, 0, R, "#123D7A")
        for dx, dy in [(0.06, 0.065), (0.00, -0.015), (0.09, -0.06)]:
            draw_star(ax, x + dx, y + dy, 0.022 if code == "AU" else 0.018, "white", z + 5)
            draw_star(ax, x + dx, y + dy, 0.014 if code == "AU" else 0.011, "#E4002B", z + 6)

    # UK
    elif code == "UK":
        circ(0, 0, R, "#1F3E79")
        rect(-R, -0.022, 2 * R, 0.044, "white")
        rect(-0.022, -R, 0.044, 2 * R, "white")
        rect(-R, -0.012, 2 * R, 0.024, "#C8102E")
        rect(-0.012, -R, 0.024, 2 * R, "#C8102E")

    # Chile
    elif code == "CL":
        rect(-R, -R, 2 * R, R, "#D52B1E")
        rect(-R, 0, 2 * R, R, "white")
        rect(-R, 0, R * 0.82, R, "#0039A6")
        draw_star(ax, x - R * 0.56, y + R * 0.42, 0.028, "white", z + 5)

    # China
    elif code == "CN":
        circ(0, 0, R, "#DE2910")
        draw_star(ax, x - 0.065, y + 0.065, 0.032, "#FFDE00", z + 5)
        for dx, dy in [(0.015, 0.092), (0.050, 0.042), (0.050, -0.015), (0.00, -0.067)]:
            draw_star(ax, x + dx, y + dy, 0.013, "#FFDE00", z + 5)

    # United States
    elif code == "US":
        for i in range(7):
            rect(-R, -R + i * (2 * R / 7), 2 * R, R / 7, "#B22234")
        rect(-R, R * 0.15, R * 0.95, R * 0.85, "#3C3B6E")
        for sx in [-0.115, -0.065, -0.015]:
            for sy in [0.078, 0.132, 0.185]:
                circ(sx, sy, 0.006, "white")

    # Canada
    elif code == "CA":
        rect(-R, -R, R * 0.55, 2 * R, "#D80621")
        rect(R * 0.45, -R, R * 0.55, 2 * R, "#D80621")
        draw_star(ax, x, y, 0.042, "#D80621", z + 5)

    # Peru
    elif code == "PE":
        rect(-R, -R, R * 0.65, 2 * R, "#D91023")
        rect(R * 0.35, -R, R * 0.65, 2 * R, "#D91023")

    # 内部白边
    ax.add_patch(Circle((x, y), radius * 0.86, facecolor="none", edgecolor=WHITE, linewidth=0.5, zorder=z + 8))

# ============================================================
# 5. Create figure
# ============================================================

fig, ax = plt.subplots(figsize=(8, 8), dpi=180)
ax.set_aspect("equal")
ax.axis("off")

# ============================================================
# 6. Background guide lines
# ============================================================

for val in [5, 10, 15, 20, 25]:
    theta = value_to_angle(val)
    x1, y1 = pol2cart(1.3, theta)
    x2, y2 = pol2cart(r_outer + 0.10, theta)
    
    ax.plot([x1, x2], [y1, y2], color=GRID, lw=0.5, alpha=0.16, zorder=1)
    
    tx, ty = pol2cart(r_outer + 0.25, theta)
    ax.text(tx, ty, str(val), fontsize=6, color=GRID, ha="center", va="center", rotation=theta - 90, alpha=0.7, zorder=2)

# ============================================================
# 7. Main arcs, labels, flags and values
# ============================================================

for i, d in enumerate(data):
    r = radii[i]
    theta_end = value_to_angle(d["value"])

    # 主弧线
    ax.add_patch(
        Arc(center, 2 * r, 2 * r, theta1=theta_end, theta2=theta_bottom,
            linewidth=line_width, color=BAR, capstyle="round", zorder=20 + i)
    )

    # 弧线内部细高光
    ax.add_patch(
        Arc(center, 2 * r, 2 * r, theta1=theta_end + 1.2, theta2=theta_bottom - 1.5,
            linewidth=1.0, color=BAR_HIGHLIGHT, alpha=0.30, zorder=50 + i)
    )

    # ============================================================
    # Flag / Value / Country name placement
    # ============================================================

    # 1. Flag: 放在柱体终点附近（内部）
    flag_offset_len = 0.25
    flag_offset_deg = np.degrees(flag_offset_len / r)
    flag_theta = theta_end + flag_offset_deg
    fx, fy = pol2cart(r, flag_theta)

    draw_flag_badge(ax, fx, fy, d["flag"], radius=badge_radius, z=100 + i)

    # 2. 黑色数值: 放在柱体终点前方（外部）
    value_offset_len = 0.35
    value_offset_deg = np.degrees(value_offset_len / r)
    value_theta = theta_end - value_offset_deg
    vx, vy = pol2cart(r, value_theta)

    ax.text(
        vx, vy, str(d["value"]),
        fontsize=10.0, color="black", fontweight="bold",
        rotation=value_theta - 90, rotation_mode="anchor",
        ha="left", va="center", zorder=130
    )

    # 3. Country name: 放在 flag 后方（内部）
    name_gap_len = 0.32
    name_gap_deg = np.degrees(name_gap_len / r)
    label_theta = flag_theta + name_gap_deg
    lx, ly = pol2cart(r, label_theta)

    label_size = 7.8 if len(d["country"]) <= 10 else 6.8

    ax.text(
        lx, ly, d["country"],
        fontsize=label_size, color=WHITE, fontweight="bold",
        rotation=label_theta - 90, rotation_mode="anchor",
        ha="right", va="center", zorder=90
    )

# ============================================================
# 8. Bottom rank band
# ============================================================

rank_y = -0.45
rank_x_positions = [center[0] - r for r in radii]

band_left = min(rank_x_positions) - 0.35
band_right = max(rank_x_positions) + 0.35

ax.add_patch(Rectangle((band_left, rank_y - 0.20), band_right - band_left, 0.42, facecolor=WHITE, edgecolor="none", zorder=80))

for d, x in zip(data, rank_x_positions):
    ax.text(x, rank_y, str(d["rank"]), fontsize=8.5, color=SUBTEXT, ha="center", va="center", zorder=90)

ax.text(band_left - 0.17, rank_y, "Rank", fontsize=7.3, color=TEXT, ha="right", va="center", zorder=90)

# ============================================================
# 9. Left text block
# ============================================================

text_x = 0.35

ax.text(text_x, 9.55, "R A N K E D", fontsize=9.2, fontweight="bold", color=TEXT, ha="left")
ax.text(text_x, 9.05, "Top 12 Countries with", fontsize=15.4, color=TEXT, ha="left")
ax.text(text_x, 8.22, "Digital Trade\nAgreements", fontsize=25.2, fontweight="heavy", color=TEXT, ha="left", va="top", linespacing=0.88)

paragraph = (
    "More than half \n"
    "digital trade.\n"
)

ax.text(text_x, 6.25, paragraph, fontsize=9.5, color=SUBTEXT, ha="left", va="top", linespacing=1.07)

# ============================================================
# 10. Annotation arrow
# ============================================================

sg_r = radii[0]
sg_theta = value_to_angle(data[0]["value"])
sg_x, sg_y = pol2cart(sg_r, sg_theta)

ax.annotate(
    "Number of\nAgreements",
    xy=(sg_x + 0.22, sg_y + 0.05),
    xytext=(10.15, 9.65),
    fontsize=7.4, color=TEXT, ha="left", va="center", rotation=18,
    arrowprops=dict(arrowstyle="-|>", lw=0.7, color=TEXT, shrinkA=2, shrinkB=3),
    zorder=150
)

# ============================================================
# 11. Final frame and save
# ============================================================

ax.set_xlim(-0.25, 11.45)
ax.set_ylim(-0.95, 10.35)

ax.set_xlim(-0.25, 11.45)
ax.set_ylim(-0.95, 10.35)

# 核心：保存为带 Alpha 通道（透明底）的 PNG 格式
plt.savefig(
    "transparent_chart.png", 
    transparent=True,       # 强制透明背景
    bbox_inches="tight",    # 裁切多余边缘
    dpi=1200                 # 输出高分辨率图片
)

plt.show()
