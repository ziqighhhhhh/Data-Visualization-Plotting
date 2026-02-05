import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm
from matplotlib.gridspec import GridSpec

def pick_cjk_fontprop():
    keywords = [
        "Microsoft YaHei", "msyh", "SimHei", "simhei", "SimSun", "simsun",
        "PingFang", "Heiti", "Songti",
        "NotoSansCJK", "Noto Sans CJK", "NotoSansSC", "Noto Sans SC",
        "WenQuanYi", "SourceHanSans", "Source Han Sans", "Arial Unicode"
    ]
    font_files = (
        fm.findSystemFonts(fontext="ttf")
        + fm.findSystemFonts(fontext="ttc")
        + fm.findSystemFonts(fontext="otf")
    )
    for kw in keywords:
        kw_low = kw.lower()
        for fp in font_files:
            if kw_low in fp.lower():
                return fm.FontProperties(fname=fp)
    return fm.FontProperties(family="sans-serif")

def build_layers_inner_to_outer(stages, values, colors):

    values = np.array(values, dtype=int)
    n = len(values)
    layers = []
    for i in range(n - 1, -1, -1):
        if i == n - 1:
            cnt = int(values[i])
            label = f"{stages[i]}：{cnt}%"
            col = colors[i]
        else:
            cnt = int(values[i] - values[i + 1])
            label = f"{stages[i]}（未到下一步）：{cnt}%"
            col = colors[i]
        layers.append((label, col, cnt))
    return layers  

def waffle_100grid_only_legend(stages, values, colors, n_cols=10, title="用户转化漏斗（100格面积图）"):
    fp = pick_cjk_fontprop()

    values = np.array(values, dtype=int)
    if values[0] != 100:
        raise ValueError("该图固定 100 格表示 100%，请保证 values[0] == 100")
    if not np.all(values[:-1] >= values[1:]):
        raise ValueError("values 必须递减（漏斗）")

    layers_inner_to_outer = build_layers_inner_to_outer(stages, values, colors)

    fills = []
    for label, col, cnt in layers_inner_to_outer:
        fills.extend([(label, col)] * cnt)
    fills = fills[:100]

    n_total = 100
    n_rows = int(np.ceil(n_total / n_cols))
    coords = []
    for idx in range(n_total):
        r = idx // n_cols
        c = idx % n_cols
        x = (n_cols - 1 - c)
        y = r
        coords.append((x, y))

    fig = plt.figure(figsize=(12.6, 4.6), dpi=160)
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.45, 0.85], wspace=0.08)

    ax_grid = fig.add_subplot(gs[0, 0])
    ax_leg  = fig.add_subplot(gs[0, 1])
    ax_leg.axis("off")

    fig.text(0.06, 0.96, title, fontproperties=fp, fontsize=18,
             color="#6e6e6e", ha="left", va="top")

    gap = 0.10
    for (x, y), (_, col) in zip(coords, fills):
        ax_grid.add_patch(Rectangle(
            (x + gap/2, y + gap/2),
            1 - gap, 1 - gap,
            facecolor=col,
            edgecolor="white",
            linewidth=0.8
        ))
    ax_grid.set_xlim(0, n_cols)
    ax_grid.set_ylim(0, n_rows)
    ax_grid.set_aspect("equal")
    ax_grid.axis("off")


    layers_outer_to_inner = list(reversed(layers_inner_to_outer))

    y0 = 0.18
    dy = 0.12
    box_w, box_h = 0.08, 0.07

    for i, (label, col, _) in enumerate(layers_outer_to_inner):
        y = y0 + (len(layers_outer_to_inner) - 1 - i) * dy
        ax_leg.add_patch(Rectangle((0.02, y - box_h/2), box_w, box_h, facecolor=col, edgecolor="none"))
        ax_leg.text(0.14, y, label, fontproperties=fp, fontsize=13,
                    color="#666666", ha="left", va="center")

    plt.show()

if __name__ == "__main__":
    stages = ["首页浏览", "点击浏览", "加购", "下单", "支付成功"]
    values = [100, 85, 43, 25, 15]

    colors = [
        "#D9D9D9",  
        "#8FD3E8",  
        "#00A6D6",  
        "#FF8C42", 
        "#1F4E79",  
    ]

    waffle_100grid_only_legend(stages, values, colors, n_cols=10)
