"""
Square Area Map（比例面积图，正方形）
目标：复刻参考例图2
- 布局：上排 A|B；下排 C | (D over E)
- 约束：C 与 E 底部等高（同一 baseline）
- 间隔：gap_px 固定像素（缩小 gap 只会让方块更“紧凑”，不会把整体缩得很小）
- 四周外边距等距：整体放进外接正方形后居中
- 标注：字母左上 + 金额紧贴其下（例图2风格），避免重叠（必要时缩小）

输出：square_area_map.png
"""

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# -----------------------------
# 1) 虚拟数据（可改）
# -----------------------------
data = {"A": 250, "B": 230, "C": 500, "D": 290, "E": 70}

# -----------------------------
# 2) 颜色（可改）
# -----------------------------
colors = {
    "A": "#B71C2B",
    "B": "#1F2A44",
    "C": "#FF3B30",
    "D": "#E4252D",
    "E": "#E4252D",
}

# -----------------------------
# 3) 计算“像例图2那样”的缩放：gap_px 固定，但整体大小自动填满
# -----------------------------
def _layout_metrics(raw, s, gap_px):
    """
    raw: dict key->sqrt(value)
    s:   缩放系数，把 raw 边长映射到像素：side_px = s * raw
    返回：total_w_px, total_h_px, row1_h_px, row2_h_px, row1_w_px, row2_w_px, right_w_px
    """
    a, b, c, d, e = raw["A"], raw["B"], raw["C"], raw["D"], raw["E"]

    # 上排
    row1_h_px = s * max(a, b)
    row1_w_px = s * a + gap_px + s * b

    # 下排（右列 D over E，中间 gap_px）
    right_h_px = s * d + gap_px + s * e
    row2_h_px = max(s * c, right_h_px)

    right_w_px = s * max(d, e)
    row2_w_px = s * c + gap_px + right_w_px

    total_w_px = max(row1_w_px, row2_w_px)
    total_h_px = row1_h_px + gap_px + row2_h_px
    return total_w_px, total_h_px, row1_h_px, row2_h_px, row1_w_px, row2_w_px, right_w_px

def solve_scale_fill_square(values, canvas_px=1200, outer_margin_px=90, gap_px=28):
    """
    求 s，使得外接正方形边长 bbox_px = usable_bbox_px（尽可能填满）
    bbox_px = max(total_w_px, total_h_px)
    """
    raw = {k: math.sqrt(max(float(values[k]), 0.0)) for k in ["A","B","C","D","E"]}
    usable_bbox_px = canvas_px - 2 * outer_margin_px

    # s 单调 => 二分
    # 下界
    lo = 0.0
    # 上界：让最大方块边长接近 usable_bbox
    hi = usable_bbox_px / (min(v for v in raw.values() if v > 0) + 1e-9)

    for _ in range(80):
        mid = (lo + hi) / 2
        total_w_px, total_h_px, *_ = _layout_metrics(raw, mid, gap_px)
        bbox_px = max(total_w_px, total_h_px)
        if bbox_px <= usable_bbox_px:
            lo = mid
        else:
            hi = mid

    return raw, lo  # lo 为最大可行 s

def compute_layout(values, canvas_px=1200, outer_margin_px=90, gap_px=28):
    """
    返回每个方块的 (x,y,side_px)，并保证：
    - C 与 E 底部等高
    - 参考例图2的结构
    - 四边外边距等距
    """
    raw, s = solve_scale_fill_square(values, canvas_px, outer_margin_px, gap_px)
    total_w_px, total_h_px, row1_h_px, row2_h_px, row1_w_px, row2_w_px, right_w_px = _layout_metrics(raw, s, gap_px)
    bbox_px = max(total_w_px, total_h_px)

    # 四边等距：把 bbox_px 的外接正方形居中
    m = (canvas_px - bbox_px) / 2.0

    # 在外接正方形内部，把实际布局（total_w/total_h）再居中
    x0 = m + (bbox_px - total_w_px) / 2.0
    y0 = m + (bbox_px - total_h_px) / 2.0

    # 像素边长
    side = {k: s * raw[k] for k in raw}

    # Row2 baseline：y0（C 与 E 底对齐）
    baseline = y0

    # 下排：C 在左，右列 D over E
    C_x, C_y = x0, baseline
    right_x = x0 + side["C"] + gap_px

    E_x, E_y = right_x, baseline
    D_x, D_y = right_x, E_y + side["E"] + gap_px

    # 上排：放在下排之上
    row1_base = y0 + row2_h_px + gap_px
    row1_top = row1_base + row1_h_px

    A_x = x0
    A_y = row1_top - side["A"]  # 顶对齐
    B_x = x0 + side["A"] + gap_px
    B_y = row1_top - side["B"]  # 顶对齐

    return {
        "A": (A_x, A_y, side["A"]),
        "B": (B_x, B_y, side["B"]),
        "C": (C_x, C_y, side["C"]),
        "D": (D_x, D_y, side["D"]),
        "E": (E_x, E_y, side["E"]),
    }

# -----------------------------
# 4) 标注：例图2样式（左上两行），避免重叠
# -----------------------------
def _intersect(b1, b2):
    return not (b1.x1 <= b2.x0 or b1.x0 >= b2.x1 or b1.y1 <= b2.y0 or b1.y0 >= b2.y1)

def add_labels(ax, fig, x, y, s, name, value,
               pad_ratio=0.08,
               base_label_fs=34,
               base_value_fs=28):
    pad = max(10, s * pad_ratio)

    # 初始字体按方块大小缩放（例图2：大方块更大字，小方块更小字，但仍清晰）
    scale = max(0.75, min(1.35, s / 260.0))
    lf = base_label_fs * scale
    vf = base_value_fs * scale

    # 例图2：金额在字母下方（靠上，不到底部）
    t1 = ax.text(x + pad, y + s - pad, name,
                 ha="left", va="top", color="white",
                 fontsize=lf, fontweight="bold")
    t2 = ax.text(x + pad, y + s - pad - lf * 1.15, f"${int(value)}",
                 ha="left", va="top", color="white",
                 fontsize=vf)

    # 若放不下/重叠，则逐步缩小；若金额掉出方块则改为左下
    for _ in range(70):
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        b1 = t1.get_window_extent(renderer=r)
        b2 = t2.get_window_extent(renderer=r)

        # 方块内边界（留 pad）
        p0 = ax.transData.transform((x + pad, y + pad))
        p1 = ax.transData.transform((x + s - pad, y + s - pad))
        box_x0, box_y0 = p0
        box_x1, box_y1 = p1

        in_box = (
            b1.x0 >= box_x0 and b1.x1 <= box_x1 and b1.y0 >= box_y0 and b1.y1 <= box_y1 and
            b2.x0 >= box_x0 and b2.x1 <= box_x1 and b2.y0 >= box_y0 and b2.y1 <= box_y1
        )
        if in_box and (not _intersect(b1, b2)):
            return

        # 若金额太靠下超界，改为左下（仍保持“字母左上”）
        if b2.y0 < box_y0:
            t2.set_position((x + pad, y + pad))
            t2.set_va("bottom")

        lf *= 0.96
        vf *= 0.96
        t1.set_fontsize(lf)
        t2.set_fontsize(vf)

        if lf < 12 or vf < 11:
            break

# -----------------------------
# 5) 绘制（关键：不 tight 裁剪）
# -----------------------------
def draw(values, color_map,
         canvas_px=1200, dpi=200,
         outer_margin_px=90,
         gap_px=28,          # 这里调小就“更紧凑”，但不会把整体缩成一小坨
         out_png="square_area_map.png"):

    layout = compute_layout(values, canvas_px=canvas_px, outer_margin_px=outer_margin_px, gap_px=gap_px)

    figsize = (canvas_px / dpi, canvas_px / dpi)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])

    ax.set_xlim(0, canvas_px)
    ax.set_ylim(0, canvas_px)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), canvas_px, canvas_px, facecolor="white", edgecolor="none"))

    for k, (x, y, s) in layout.items():
        ax.add_patch(Rectangle((x, y), s, s, facecolor=color_map.get(k, "#D94A4A"), edgecolor="none"))
        add_labels(ax, fig, x, y, s, k, values[k])

    fig.savefig(out_png, facecolor="white")  # 不要 bbox_inches="tight"
    plt.show()
    print(f"Saved: {out_png}")

if __name__ == "__main__":
    # gap_px 建议范围：18~35（越小越紧凑）
    draw(data, colors, canvas_px=1200, dpi=200, outer_margin_px=90, gap_px=26, out_png="square_area_map.png")
