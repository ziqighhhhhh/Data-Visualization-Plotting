import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.font_manager as fm
import os



def setup_font():
    win_font_candidates = [
        r"C:\Windows\Fonts\msyh.ttc",   
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\simhei.ttf", 
        r"C:\Windows\Fonts\simsun.ttc", 
    ]
    for fp in win_font_candidates:
        if os.path.exists(fp):
            try:
                fm.fontManager.addfont(fp)
                name = fm.FontProperties(fname=fp).get_name()
                plt.rcParams["font.sans-serif"] = [name]
                break
            except Exception:
                pass

    if not plt.rcParams.get("font.sans-serif"):
        candidates = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans CN", "Arial Unicode MS"]
        available = {f.name for f in fm.fontManager.ttflist}
        for name in candidates:
            if name in available:
                plt.rcParams["font.sans-serif"] = [name]
                break

    plt.rcParams["axes.unicode_minus"] = False



def make_virtual_sales(n_months=12,
                       products=("大号电池", "碱性电池", "其他电光源"),
                       seed=9):
    rng = np.random.default_rng(seed)

    month_labels = [str(i) for i in range(1, n_months + 1)]

    t = np.arange(n_months)
    season = 0.85 + 0.25 * np.sin((t - 1) / n_months * 2 * np.pi) + 0.10 * np.sin((t + 1) / 6 * 2 * np.pi)
    season = np.clip(season, 0.55, None)
    total = 1000 * season * rng.lognormal(mean=0.0, sigma=0.18, size=n_months)

    wave = np.vstack([
        1.2 + 0.7 * np.sin((t + 0) / n_months * 2 * np.pi),
        1.0 + 0.6 * np.sin((t + 3) / n_months * 2 * np.pi),
        0.9 + 0.5 * np.sin((t + 6) / n_months * 2 * np.pi),
    ]).T
    wave = np.clip(wave, 0.15, None)

    alpha = 1.2 * wave  
    shares = np.array([rng.dirichlet(alpha[i]) for i in range(n_months)])

    values = total[:, None] * shares  
    return month_labels, list(products), values



def plot_polar_area(month_labels,
                    products,
                    values,
                    colors=("#1F2D4D", "#B81E2F", "#FF3B30"),  
                    edge_lw=2.2,                               
                    gap_frac=0.0,                             
                    label_color="#7A8B95",
                    label_size=14,
                    label_pad=0.028,                          
                    show_legend=True,
                    legend_loc="lower center",
                    legend_ncol=None,
                    save_path="polar_area_12months_refstyle.png"):

    month_labels = list(month_labels)
    products = list(products)
    values = np.asarray(values, dtype=float)

    n = len(month_labels)
    k = len(products)
    assert values.shape == (n, k), f"values 应为 shape ({n},{k})，但得到 {values.shape}"

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(7.2, 7.2), dpi=220)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    ax.set_facecolor("white")

    width = 2 * np.pi / n
    gap = gap_frac * width
    starts = np.arange(n) * width

    totals = values.sum(axis=1)
    r_max = 1.0
    scale = (r_max ** 2) / totals.max()

    for i in range(n):
        theta = starts[i] + gap / 2
        w = width - gap

        cum = 0.0
        for j in range(k):
            v = float(values[i, j])
            r0 = np.sqrt(scale * cum)
            r1 = np.sqrt(scale * (cum + v))

            ax.bar(
                theta,
                height=(r1 - r0),
                width=w,
                bottom=r0,
                align="edge",
                color=colors[j],
                edgecolor="white",
                linewidth=edge_lw,
                zorder=3
            )
            cum += v

    r_totals = np.sqrt(scale * totals)
    ax.set_ylim(0, float(r_totals.max() + label_pad + 0.12))  

    offset = ax.get_theta_offset()
    direction = ax.get_theta_direction()

    for i, lab in enumerate(month_labels):
        th = starts[i] + width / 2
        phi = offset + direction * th
        rot = np.degrees(phi) - 90

        r_label = float(r_totals[i] + label_pad)

        ax.text(
            th, r_label, lab,
            ha="center", va="center",
            fontsize=label_size,
            color=label_color,
            rotation=rot,
            rotation_mode="anchor",
            zorder=10
        )

    if show_legend:
        handles = [Patch(facecolor=colors[j], edgecolor="none", label=products[j]) for j in range(k)]
        if legend_ncol is None:
            legend_ncol = k

        ax.legend(
            handles=handles,
            loc=legend_loc,
            bbox_to_anchor=(0.5, -0.10),  
            ncol=legend_ncol,
            frameon=False,
            fontsize=12,
            handlelength=1.2,
            columnspacing=1.6
        )

    fig.savefig(save_path, bbox_inches="tight", facecolor="white")
    plt.show()
    print(f"Saved: {save_path}")


if __name__ == "__main__":
    setup_font()

    months, products, values = make_virtual_sales(
        n_months=12,
        products=("大号电池", "碱性电池", "其他电光源"),
        seed=9
    )

    plot_polar_area(
        months, products, values,
        show_legend=True,      
        gap_frac=0.0,
        edge_lw=2.2,
        label_pad=0.028,
        save_path="polar_area_12months_refstyle_with_legend.png"
    )
