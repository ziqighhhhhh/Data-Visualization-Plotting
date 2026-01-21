import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({
    "text.color": "#575864",
    "figure.facecolor": "#ffffff"
})

def create_colors(hex_colors, data):
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list("custom_cmap", hex_colors)
    norm = Normalize(vmin=min(data), vmax=max(data))
    sm = ScalarMappable(cmap=cmap, norm=norm)
    return [sm.to_rgba(val)[:3] for val in data]

np.random.seed(42)

n_categories = 30
years = list(range(2016, 2026))  
category_name_col = "类别"


categories = [
    "电力行业", "钢铁行业", "建材行业", "化工行业", "焦化行业", "供热行业", "交通运输",
    "居民生活", "农业", "服务业", "有色金属", "造纸行业", "纺织行业", "机械制造",
    "煤制油", "煤制气", "煤化工", "矿山开采", "港口物流", "水泥熟料",
    "玻璃行业", "陶瓷行业", "发电供汽", "区域一", "区域二", "区域三",
    "区域四", "区域五", "区域六", "其他"
][:n_categories]


base = np.random.lognormal(mean=3.2, sigma=0.55, size=n_categories) * 10

data = {category_name_col: categories}
for y in years:
    drift = 1 + (y - years[0]) * np.random.uniform(-0.01, 0.02)  # 轻微趋势
    noise = np.random.normal(loc=1.0, scale=0.06, size=n_categories)
    vals = np.clip(base * drift * noise, a_min=0, a_max=None)
    data[str(y)] = vals

df = pd.DataFrame(data)


year_cols = [str(y) for y in years]
df["总计"] = df[year_cols].sum(axis=1)

top_n = 15
df_top = df.sort_values("总计", ascending=False).head(top_n)
df_top = df_top.sort_values("总计")  

company_name = df_top[category_name_col].tolist()
growth_data = df_top["总计"].tolist()


fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"}, dpi=150)

max_value = max(growth_data) * 1.2
colors = create_colors(["#214e81", "#a5d57d"], growth_data)

initial_radius = 15
ring_width = 2
ring_gap = 1

for i, (label, value) in enumerate(zip(company_name, growth_data)):
    inner_radius = initial_radius + i * (ring_width + ring_gap)
    theta_start = 0
    theta_end = (value / max_value) * 2 * np.pi

    ax.bar(
        x=(theta_start + theta_end) / 2,
        height=ring_width,
        width=theta_end - theta_start,
        bottom=inner_radius,
        color=colors[i],
        alpha=0.85,
    )

    if theta_end < np.pi / 2:
        text_attr = {
            "color": colors[i],
            "rotation": np.degrees(theta_end) + 5,
            "ha": "left",
        }
    else:
        text_attr = {
            "color": "#ffffff",
            "rotation": np.degrees(theta_end - np.pi) - 5,
            "ha": "left",
        }

    ax.text(
        x=(theta_start + theta_end),
        y=inner_radius + ring_width / 2,
        s=f"{value:.1f}",
        va="center",
        fontsize=8,
        fontweight="bold",
        rotation_mode="anchor",
        **text_attr,
    )

    ax.text(
        x=0,
        y=inner_radius + ring_width / 2,
        s=label,
        ha="right",
        va="center",
        color=colors[i],
        fontsize=8,
        fontweight="bold",
        rotation=0,
        rotation_mode="anchor",
    )

ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.set_theta_direction(1)
ax.set_theta_offset(np.pi * 1.5)
ax.spines["polar"].set_visible(False)

fig.text(
    0.1, 1.2,
    "消费总量各类汇总（单位：吨）",
    fontsize=28, ha="left", va="top", fontweight="bold"
)

plt.subplots_adjust(left=0.35, right=1.1, top=1.3, bottom=0.15)
plt.savefig("煤炭消费总量环形柱状图_模拟数据.png", dpi=300, bbox_inches="tight")
plt.show()
