import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "Noto Sans CJK SC"]
mpl.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


stages = ["首页浏览", "点击浏览", "加购", "下单", "支付成功"]
values = np.array([100, 85, 43, 25, 15])  

colors = ["#7FE3E8", "#52C3D6", "#2F99BF", "#1F6EA1", "#0F4F80"]


max_width = values[0]
left = (max_width - values) / 2
right = left + values

# y 轴位置
y = np.arange(len(stages))


fig, ax = plt.subplots(figsize=(6, 6))

for i in range(len(stages)):
    ax.fill_betweenx(
        [y[i]-0.5, y[i]+0.5],  # 上下边界
        left[i],
        right[i],
        color=colors[i],
        edgecolor='none'
    )


for i, (stage, val) in enumerate(zip(stages, values)):
    ax.text(-5, y[i], stage, va='center', ha='right', fontsize=12)
    ax.text(max_width + 5, y[i], f"{val}%", va='center', ha='left', fontsize=12)


ax.set_xlim(-20, max_width + 20)
ax.set_ylim(-1, len(stages))
ax.axis('off')  
ax.invert_yaxis() 

plt.title("用户转化漏斗图", fontsize=14)
plt.tight_layout()
plt.show()
