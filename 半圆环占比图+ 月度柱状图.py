
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib import colors as mcolors


def setup_chinese_font():
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "PingFang SC",
        "WenQuanYi Zen Hei", "Arial Unicode MS", "DejaVu Sans"
    ]


def lerp_color(c1, c2, t):
    r1, g1, b1 = mcolors.to_rgb(c1)
    r2, g2, b2 = mcolors.to_rgb(c2)
    return (r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)


def main():
    setup_chinese_font()


    months = np.arange(1, 13)
    month_labels = [f"{m}月" for m in months]
    values = np.array([858, 872, 774, 577, 181, 272, 278, 810, 228, 194, 823, 896], dtype=float)

    total = int(values.sum())
    pct = np.rint(values / values.sum() * 100).astype(int)
    avg = int(np.rint(values.mean()))  


    light_teal = "#BFDDE6"
    dark_teal  = "#1F6E7A"

    blue  = "#2AA6C3"
    gray  = "#4A4A4A"
    red   = "#C7534D"
    green = "#00A85A"

    bar_colors = []
    for m in months:
        if m == 5:
            bar_colors.append(red)
        elif m in (6, 7, 9, 10):
            bar_colors.append(gray)
        elif m == 12:
            bar_colors.append(green)
        else:
            bar_colors.append(blue)

 
    r_outer = 1.0
    ring_width = 0.28
    pad = 0.02

    xlim = r_outer + pad
    y_min = -0.02        
    y_max = r_outer + 0.12
    x_span = 2 * xlim
    y_span = y_max - y_min


    fig = plt.figure(figsize=(7.8, 5.9), dpi=160)

    left  = 0.055
    width = 0.93

    bar_bottom = 0.10
    bar_height = 0.28
    bar_top    = bar_bottom + bar_height

    gap = 0.05

    gauge_height = width * (y_span / x_span)
    gauge_bottom = bar_top + gap

    gauge_top_target = 0.95
    if gauge_bottom + gauge_height > gauge_top_target:
        gauge_bottom = gauge_top_target - gauge_height

    ax_g = fig.add_axes([left, gauge_bottom, width, gauge_height])  
    ax_b = fig.add_axes([left, bar_bottom,   width, bar_height])    


    ax_g.axis("off")
    ax_g.set_aspect("equal", adjustable="box")
    ax_g.set_xlim(-xlim, xlim)
    ax_g.set_ylim(y_min, y_max)

    gauge_colors = [lerp_color(light_teal, dark_teal, i / 11) for i in range(12)]

    order = list(range(11, -1, -1))  # 12..1
    values_rev = values[order]
    pct_rev = pct[order]
    labels_rev = [month_labels[i] for i in order]
    angles = values_rev / values_rev.sum() * 180.0

    cur = 0.0
    for i, ang in enumerate(angles):
        theta1 = cur
        theta2 = cur + ang

        ax_g.add_patch(
            Wedge(
                center=(0, 0),
                r=r_outer,
                theta1=theta1,
                theta2=theta2,
                width=ring_width,
                facecolor=gauge_colors[i],
                edgecolor="none",
            )
        )

        mid = (theta1 + theta2) / 2.0
        rad = np.deg2rad(mid)

        small = ang < 9.0
        if small:
            fs = 6.5
            jitter = 0.07 if (i % 2 == 0) else -0.03
            r_text = r_outer - ring_width / 2.0 + jitter
        else:
            fs = 8
            r_text = r_outer - ring_width / 2.0 + 0.02

        xt, yt = r_text * np.cos(rad), r_text * np.sin(rad)
        ax_g.text(
            xt, yt,
            f"{labels_rev[i]}\n{pct_rev[i]}%",
            ha="center", va="center",
            fontsize=fs, color="#2F2F2F"
        )

        cur = theta2

    ax_g.text(
        0, 0.23,
        f"¥{total:,}万",
        ha="center", va="center",
        fontsize=15, fontweight="bold", color="#2F2F2F"
    )
    ax_g.text(
        0, 0.02,
        "2025年总计",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color="#2F2F2F"
    )

    x = np.arange(1, 13)
    bar_w = 0.78
    bars = ax_b.bar(x, values, color=bar_colors, width=bar_w)

    ax_b.axhline(avg, color="red", linestyle=":", linewidth=1.0, alpha=0.85)

    ax_b.text(
        -0.02, avg,
        f"均值\n{avg}",
        transform=ax_b.get_yaxis_transform(),
        color="red", fontsize=9,
        ha="right", va="center"
    )

    for i, (b, v) in enumerate(zip(bars, values)):
        c = bar_colors[i]
        label_color = c if (i == 11 or i == 4) else "#2F2F2F"  
        ax_b.text(
            b.get_x() + b.get_width() / 2,
            v + 14,
            f"{int(v)}",
            ha="center", va="bottom",
            fontsize=9, color=label_color
        )

    ax_b.set_xticks(x)
    ax_b.set_xticklabels(month_labels, fontsize=9, color="#444444")

    ax_b.set_xlim(0.5, 12.5)
    ax_b.set_ylim(0, max(values) * 1.18)

    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)
    ax_b.spines["left"].set_visible(False)
    ax_b.tick_params(axis="y", left=False, labelleft=False)

    plt.savefig("semi_gauge_bar_span_equal_FINAL.png", dpi=220)
    plt.show()


if __name__ == "__main__":
    main()
