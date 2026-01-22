
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.ticker import FuncFormatter

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def _best_text_color(rgb_or_rgba):
    r, g, b = rgb_or_rgba[:3]
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "white" if luminance < 0.55 else "#111111"

def plot_marimekko(widths, composition, colors, *,
                   gap=0.006,
                   rounding=0.015,
                   show_segment_labels=True,
                   segment_label_min_height=0.08,
                   title="",
                   figsize=(9, 5),
                   dpi=150):

    widths = pd.Series(widths).astype(float)
    widths = widths[widths > 0]
    categories = widths.index.tolist()

    comp = composition.copy()
    comp = comp[categories]
    comp = comp.apply(pd.to_numeric, errors="coerce").fillna(0.0)

    col_sums = comp.sum(axis=0).replace(0, np.nan)
    comp = (comp / col_sums).fillna(0.0)

    n = len(categories)
    total_gap = gap * (n - 1)
    if total_gap >= 0.35:
        raise ValueError("gap is too large relative to number of categories.")
    usable = 1.0 - total_gap
    w = widths / widths.sum()
    w = w * usable

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#C9D3DD")
    ax.spines["bottom"].set_color("#C9D3DD")

    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    pct = FuncFormatter(lambda x, pos: f"{int(round(x*100))}%")
    ax.xaxis.set_major_formatter(pct)
    ax.yaxis.set_major_formatter(pct)
    ax.set_xticks(np.linspace(0, 1, 6)) 
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.tick_params(axis="both", labelsize=12, colors="#5E7284", length=0, pad=8)

    ax.set_title(title, fontsize=14, pad=18, color="#2B3A47")

    x_left = 0.0
    for i, cat in enumerate(categories):
        width_i = float(w.loc[cat])

        clip = FancyBboxPatch(
            (x_left, 0), width_i, 1.0,
            boxstyle=f"round,pad=0,rounding_size={rounding}",
            linewidth=0,
            facecolor="none"
        )
        ax.add_patch(clip)

        y_bottom = 0.0
        for seg in comp.index:
            h = float(comp.loc[seg, cat])
            if h <= 0:
                continue

            rect = Rectangle(
                (x_left, y_bottom),
                width_i, h,
                facecolor=colors.get(seg, "#999999"),
                edgecolor="white",
                linewidth=2.0
            )
            rect.set_clip_path(clip)
            ax.add_patch(rect)

            if show_segment_labels and h >= segment_label_min_height:
                cx = x_left + width_i / 2
                cy = y_bottom + h / 2
                fc = rect.get_facecolor()
                ax.text(
                    cx, cy,
                    f"{seg}\n{h*100:.0f}%",
                    ha="center", va="center",
                    fontsize=10,
                    color=_best_text_color(fc),
                    clip_on=True
                )

            y_bottom += h

        ax.text(
            x_left + width_i / 2, 1.02,
            str(cat),
            ha="center", va="bottom",
            fontsize=12, color="#1E2A36",
            fontweight="bold"
        )

        x_left += width_i
        if i < n - 1:
            x_left += gap

    handles = [Rectangle((0, 0), 1, 1, facecolor=colors[s], edgecolor="none") for s in comp.index]
    ax.legend(
        handles, comp.index.tolist(),
        loc="center left", bbox_to_anchor=(1.02, 0.5),
        frameon=False, fontsize=11
    )

    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":

    widths = pd.Series(
        {"国家 1": 40, "国家 2": 30, "国家 3": 18, "国家 4": 12},
        name="Total"
    )


    composition = pd.DataFrame(
        {
            "国家 1": [48, 29, 23],
            "国家 2": [38, 20, 42],
            "国家 3": [19, 30, 51],
            "国家 4": [7,  32, 61],
        },
        index=["产品 1", "产品 2", "产品 3"]
    )

    colors = {
        "产品 1": "#111B2E",  
        "产品 2": "#B91D2D",  
        "产品 3": "#FF3B30",  
    }

    fig, ax = plot_marimekko(
        widths=widths,
        composition=composition,
        colors=colors,
        gap=0.006,                   
        rounding=0.02,               
        show_segment_labels=False,   
        segment_label_min_height=0.10
    )


    plt.show()
