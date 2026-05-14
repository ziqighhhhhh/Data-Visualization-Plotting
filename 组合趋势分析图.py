import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


plt.rcParams['font.sans-serif'] = [
    'Microsoft YaHei',
    'SimHei',
    'Noto Sans CJK SC',
    'Arial Unicode MS'
]
plt.rcParams['axes.unicode_minus'] = False


months = np.arange(1, 13)
month_labels = [f"{i}月" for i in months]

values = np.array([
    112, 125, 220, 152, 251, 200,
    225, 266, 198, 287, 269, 278
])

current_month = 12

bar_colors = [
    "#FE762C" if m == current_month else "#504B49"
    for m in months
]

trend_pct = np.array([
    12, 76, -31, 65, -20, 13,
    18, -26, 45, -6, 3, 8
])


fig, ax = plt.subplots(figsize=(12, 8), dpi=150)

bars = ax.bar(
    months,
    values,
    width=0.52,
    color=bar_colors,
    zorder=2
)

for x, y in zip(months, values):
    ax.text(
        x,
        y + 5,
        str(y),
        ha='center',
        va='bottom',
        fontsize=10,
        color='white' if y > 180 else '#333333',
        fontweight='bold'
    )

for i in range(1, len(months)):

    diff = values[i] - values[i - 1]
    x = months[i]

    if diff >= 0:
        ax.annotate(
            '',
            xy=(x - 0.35, values[i] + 40),
            xytext=(x - 0.35, values[i - 1] + 10),
            arrowprops=dict(
                arrowstyle='->',
                lw=1.8,
                color='#00A95C'
            )
        )

        ax.text(
            x - 0.55,
            max(values[i], values[i - 1]) + 48,
            f'+{diff}',
            color='#00A95C',
            fontsize=9,
            fontweight='bold'
        )

    else:
        ax.annotate(
            '',
            xy=(x + 0.35, values[i] + 10),
            xytext=(x + 0.35, values[i - 1] + 40),
            arrowprops=dict(
                arrowstyle='->',
                lw=1.8,
                color='#C85A5A'
            )
        )

        ax.text(
            x + 0.15,
            max(values[i], values[i - 1]) + 48,
            f'{diff}',
            color='#C85A5A',
            fontsize=9,
            fontweight='bold'
        )


baseline = 400
line_y = baseline + trend_pct * 0.9

x_smooth = np.linspace(months.min(), months.max(), 300)
spline = make_interp_spline(months, line_y, k=3)
y_smooth = spline(x_smooth)

for i in range(len(x_smooth) - 1):
    color = '#00A95C' if y_smooth[i] >= baseline else '#C85A5A'

    ax.plot(
        x_smooth[i:i + 2],
        y_smooth[i:i + 2],
        color=color,
        lw=3,
        zorder=3
    )

ax.axhline(
    baseline,
    color='#999999',
    lw=1,
    linestyle='--',
    dashes=(4, 4),
    zorder=1
)

for x, pct, y in zip(months, trend_pct, line_y):

    if pct >= 0:
        ax.text(
            x,
            y + 12,
            f'▲{pct}%',
            color='#00A95C',
            fontsize=9,
            ha='center',
            fontweight='bold'
        )
    else:
        ax.text(
            x,
            y - 20,
            f'▼{abs(pct)}%',
            color='#C85A5A',
            fontsize=9,
            ha='center',
            fontweight='bold'
        )


ax.set_title(
    '月度销售趋势分析',
    loc='left',
    fontsize=20,
    fontweight='bold',
    pad=36
)

legend_handles = [
    plt.Rectangle(
        (0, 0),
        1,
        1,
        color='#504B49',
        label='历史月份'
    ),
    plt.Rectangle(
        (0, 0),
        1,
        1,
        color='#FE762C',
        label='当月'
    )
]

legend = ax.legend(
    handles=legend_handles,
    loc='upper left',
    bbox_to_anchor=(0, 1.02),
    frameon=False,
    fontsize=11,
    ncol=2,
    handleheight=1,
    handlelength=1.6,
    columnspacing=1.5,
    borderaxespad=0
)

legend._legend_box.align = "left"

ax.set_xticks(months)
ax.set_xticklabels(month_labels, fontsize=11)

ax.set_xlim(0.5, 12.5)
ax.set_ylim(0, 520)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.tick_params(axis='y', left=False, labelleft=False)
ax.tick_params(axis='x', bottom=False)

ax.grid(False)

fig.patch.set_facecolor('white')
ax.set_facecolor('white')

plt.tight_layout()

plt.savefig(
    '月度销售趋势.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
