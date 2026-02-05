# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def set_chinese_font():
    """
    """
    candidates = [
        "Microsoft YaHei", "SimHei", "SimSun",          # Windows
        "PingFang SC", "Heiti SC", "Songti SC",         # macOS
        "Noto Sans CJK SC", "WenQuanYi Micro Hei",      # Linux
        "Arial Unicode MS"
    ]
    available = {f.name for f in plt.matplotlib.font_manager.fontManager.ttflist}
    for f in candidates:
        if f in available:
            plt.rcParams["font.sans-serif"] = [f]
            break
    plt.rcParams["axes.unicode_minus"] = False

def slopegraph_employee_feedback(show_delta=False):
    set_chinese_font()

    items = [
        ("同事关系",   85, 91, False),
        ("企业文化",   80, 96, False),
        ("工作环境",   76, 75, False),
        ("领导力",     59, 62, False),
        ("职业发展",   49, 33, True),   
        ("奖励与认可", 41, 45, False),
        ("绩效管理",   33, 42, False),
    ]

    fig, ax = plt.subplots(figsize=(9.2, 6.6), dpi=160)

    grey = "#8f8f8f"
    orange = "#d46a1a"

    x_label = 0.22   
    x_v14   = 0.40   
    x_2014  = 0.50   
    x_2015  = 0.84   
    x_v15   = 0.92   

    y_min, y_max = 20, 105

    for name, v14, v15, highlight in items:
        c = orange if highlight else grey

        ax.plot([x_2014, x_2015], [v14, v15],
                lw=3, color=c, solid_capstyle="round", zorder=2)

        ax.scatter([x_2014, x_2015], [v14, v15], s=70, color=c, zorder=3)

        ax.text(x_label, v14, name, ha="right", va="center",
                fontsize=13, color=c)
        ax.text(x_v14,   v14, f"{v14}%", ha="right", va="center",
                fontsize=13, color=c)

        ax.text(x_v15, v15, f"{v15}%", ha="left", va="center",
                fontsize=13, color=c)

        if show_delta:
            delta = v15 - v14
            if delta > 0:
                dtxt = f"↑ +{delta}pp"
            elif delta < 0:
                dtxt = f"↓ {delta}pp"
            else:
                dtxt = "— 0pp"

            xm = (x_2014 + x_2015) / 2
            ym = (v14 + v15) / 2 + 2.2
            ax.text(xm, ym, dtxt, ha="center", va="center",
                    fontsize=11, color=c, zorder=4)

    ax.text(0.06, 102.0, "员工反馈趋势",
            ha="left", va="bottom", fontsize=20, color="#6e6e6e")
    ax.text(0.06, 98.0, "调查维度  |  好评占比",
            ha="left", va="bottom", fontsize=12.5, color="#9a9a9a")

    yb = 24.0
    ax.plot([x_2014, x_2015], [yb, yb], color="#9a9a9a", lw=2)
    ax.plot([x_2014, x_2014], [yb, yb-2.0], color="#9a9a9a", lw=2)
    ax.plot([x_2015, x_2015], [yb, yb-2.0], color="#9a9a9a", lw=2)

    ax.text(x_2014, yb-4.0, "2014", ha="center", va="top", fontsize=12, color="#9a9a9a")
    ax.text(x_2015, yb-4.0, "2015", ha="center", va="top", fontsize=12, color="#9a9a9a")
    ax.text((x_2014+x_2015)/2, yb-9.0, "调查年份", ha="center", va="top",
            fontsize=12, color="#9a9a9a")

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    slopegraph_employee_feedback(show_delta=False)
