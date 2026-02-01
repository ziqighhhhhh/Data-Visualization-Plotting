import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch
from matplotlib import font_manager
from pathlib import Path

# =========================
# 0) 中文字体：尽量自动找可用字体
# =========================
def pick_chinese_font():
    """
    尝试在本机寻找可显示中文的字体。
    Windows 通常有 Microsoft YaHei / SimHei；
    macOS 常见 PingFang SC；
    Linux 可装 Noto Sans CJK。
    """
    candidates = [
        "Microsoft YaHei", "SimHei",
        "PingFang SC", "Heiti SC", "Songti SC",
        "Noto Sans CJK SC", "Source Han Sans SC",
        "Arial Unicode MS",
    ]
    for f in candidates:
        try:
            font_manager.findfont(f, fallback_to_default=False)
            return f
        except Exception:
            pass
    return None

font_name = pick_chinese_font()
if font_name:
    plt.rcParams["font.sans-serif"] = [font_name]
else:
    # 找不到中文字体就用默认字体，并提示用户安装
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
    print(
        "[警告] 未检测到可用中文字体，图中中文可能显示为方块。\n"
        "建议安装：Noto Sans CJK SC（或在 Windows 使用 Microsoft YaHei/SimHei）。"
    )
plt.rcParams["axes.unicode_minus"] = False


# =========================
# 1) 虚拟数据（单位：万美元）
#    你可以替换成自己的真实数据
# =========================
months = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]

rev_2024 = np.array([300,302,288,339,301,414,388,216,393,349,423,211], dtype=float)
rev_2025 = np.array([472,272,327,418,234,471,294,246,458,383,413,259], dtype=float)

# =========================
# 2) 指标计算：同比 / 环比 / 占比
# =========================
# 同比（YoY）：2025当月 vs 2024同月
yoy = (rev_2025 / rev_2024 - 1.0) * 100.0

# 环比（MoM）：2025当月 vs 上月
# 这里让 1月 用“上年12月(2024年12月)”做上月基数（常见业务口径）
prev_for_mom = np.r_[rev_2024[-1], rev_2025[:-1]]
mom = (rev_2025 / prev_for_mom - 1.0) * 100.0

# 占比：2025每月占2025全年比例
share = rev_2025 / rev_2025.sum() * 100.0
share_round = np.rint(share).astype(int)


# =========================
# 3) 简易平滑（不用 SciPy，保证通用）
# =========================
def smooth_curve(x, y, n=420, window=35):
    """
    先线性插值到更密集的点，再用 Hann 窗做卷积平滑。
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)

    xs = np.linspace(x.min(), x.max(), n)
    ys = np.interp(xs, x, y)

    window = max(5, int(window) | 1)  # 强制奇数且>=5
    kernel = np.hanning(window)
    kernel /= kernel.sum()

    pad = window // 2
    ys_pad = np.r_[np.repeat(ys[0], pad), ys, np.repeat(ys[-1], pad)]
    ys_s = np.convolve(ys_pad, kernel, mode="same")[pad:-pad]
    return xs, ys_s


# =========================
# 4) 配色与画布
# =========================
BG     = "#F7F9FB"
C24    = "#4B4B4B"   # 2024 灰
C25    = "#4FB3C8"   # 2025 蓝
C_POS  = "#00B050"   # 上升绿
C_NEG  = "#C0504D"   # 下降红
C_GRID = "#B5B5B5"

x = np.arange(12)

fig = plt.figure(figsize=(12.4, 7.6), dpi=220, facecolor=BG)
gs = GridSpec(3, 1, height_ratios=[2.1, 1.15, 1.55], hspace=0.28, figure=fig)

ax_mom = fig.add_subplot(gs[0])
ax_yoy = fig.add_subplot(gs[1], sharex=ax_mom)
ax_bar = fig.add_subplot(gs[2], sharex=ax_mom)


# =========================
# 5) 顶部：环比曲线（绿/红分段）
# =========================
ax_mom.axhline(0, color=C_GRID, linestyle="--", linewidth=1.2, alpha=0.9)

xs, ys = smooth_curve(x, mom, n=420, window=35)
ax_mom.plot(xs, np.where(ys >= 0, ys, np.nan), color=C_POS, linewidth=4)
ax_mom.plot(xs, np.where(ys <  0, ys, np.nan), color=C_NEG, linewidth=4)

mom_colors = np.where(mom >= 0, C_POS, C_NEG)
ax_mom.scatter(x, mom, s=46, color=mom_colors, zorder=4)

for xi, yi in zip(x, mom):
    arrow = "↗" if yi >= 0 else "↘"
    txt = f"{arrow}{abs(int(round(yi)))}%"
    dy = 10 if yi >= 0 else -14
    ax_mom.text(xi, yi + dy, txt, ha="center", va="center", fontsize=11, color="#222222")

ax_mom.text(-0.85, 0, "环比", ha="left", va="center", fontsize=13, fontweight="bold", color="#333333")

ax_mom.set_xlim(-0.6, 11.6)
ymin = min(mom.min(), ys.min()) - 25
ymax = max(mom.max(), ys.max()) + 25
ax_mom.set_ylim(ymin, ymax)
ax_mom.set_yticks([])
ax_mom.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
for s in ax_mom.spines.values():
    s.set_visible(False)


# =========================
# 6) 中部：同比柱（绿/红）
# =========================
ax_yoy.axhline(0, color=C_GRID, linestyle="--", linewidth=1.2, alpha=0.9)

yoy_colors = np.where(yoy >= 0, C_POS, C_NEG)
ax_yoy.bar(x, yoy, width=0.55, color=yoy_colors, edgecolor="none")

for xi, yi in zip(x, yoy):
    if yi >= 0:
        ax_yoy.text(xi, yi + 3.0, f"+{int(round(yi))}%", ha="center", va="bottom", fontsize=11, color="#222222")
    else:
        ax_yoy.text(xi, yi - 3.0, f"{int(round(yi))}%", ha="center", va="top", fontsize=11, color="#222222")

ax_yoy.text(-0.85, 0, "同比", ha="left", va="center", fontsize=13, fontweight="bold", color="#333333")

ax_yoy.set_yticks([])
ax_yoy.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
for s in ax_yoy.spines.values():
    s.set_visible(False)


# =========================
# 7) 底部：2024 vs 2025 双柱 + 占比圆点
# =========================
w = 0.33
ax_bar.bar(x - w/2, rev_2024, width=w, color=C24, edgecolor="none")
ax_bar.bar(x + w/2, rev_2025, width=w, color=C25, edgecolor="none")

# 柱内数值
for xi, v in zip(x - w/2, rev_2024):
    ax_bar.text(xi, v - 18, f"{int(v)}", ha="center", va="top", fontsize=10, color="white")
for xi, v in zip(x + w/2, rev_2025):
    ax_bar.text(xi, v - 18, f"{int(v)}", ha="center", va="top", fontsize=10, color="white")

# 占比：空心圆 + 百分比
ymax_bar = float(max(rev_2024.max(), rev_2025.max()))
y_circle = ymax_bar * 1.05
y_pct    = ymax_bar * 1.13

ax_bar.scatter(x, np.full_like(x, y_circle), s=62, facecolors="none", edgecolors="#666666", linewidths=1.3)
for xi, p in zip(x, share_round):
    ax_bar.text(xi, y_pct, f"{p}%", ha="center", va="center", fontsize=11, color="#333333")

ax_bar.text(-0.85, y_circle, "占比", ha="left", va="center", fontsize=13, fontweight="bold", color="#333333")

ax_bar.set_xticks(x)
ax_bar.set_xticklabels(months, fontsize=12)
ax_bar.set_yticks([])
ax_bar.set_ylim(0, ymax_bar * 1.25)
for s in ax_bar.spines.values():
    s.set_visible(False)


# =========================
# 8) 标题、单位、图例、装饰
# =========================
fig.text(0.055, 0.965, "2025年与2024年营收对比分析", fontsize=22, fontweight="bold",
         ha="left", va="top", color="#4D4D4D")
fig.text(0.52, 0.965, "单位：万美元", fontsize=12, ha="left", va="top", color="#666666")

handles = [
    Patch(facecolor=C24, edgecolor="none", label="2024年"),
    Patch(facecolor=C25, edgecolor="none", label="2025年")
]
fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.95, 0.967),
           frameon=False, ncol=2, fontsize=12, handlelength=0.8, columnspacing=1.6)

# 左上装饰条
fig.add_artist(plt.Rectangle((0.055, 0.968), 0.055, 0.008, transform=fig.transFigure,
                             facecolor=C25, edgecolor="none", alpha=1.0))


# =========================
# 9) 保存输出
# =========================
base_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
out_path = base_dir / "revenue_2025_vs_2024_demo.png"

plt.savefig(out_path, bbox_inches="tight")
plt.show()

print(f"已保存：{out_path}")
