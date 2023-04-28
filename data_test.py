# import matplotlib.pyplot as plt
# from random import choice
#
# # 构造数据
# x = [1, 2, 3, 4, 5, 6]
# y = [[3, 7, 8, 9, 6, 2], [1, 4, 9, 16, 25, 36], [21, 19, 17, 15, 13, 11]]
#
# # 创建一个figure对象
# fig, ax = plt.subplots()
#
# # 绘制三条折线，并给每条线条命名，并添加数据标签
# for idx, yi in enumerate(y):
#     c = choice(['r', 'g', 'b', 'y'])   # 随机选择一种颜色
#     l = f'line{idx}'                   # 线条名称
#     ax.plot(x, yi, color=c, label=l)  # 绘制线条及其名称
#     for xi, yi in zip(x, yi):
#         ax.text(xi, yi+0.5, f'({xi}, {yi})', fontsize=10, color=c, ha='center')  # 添加数据标签
#
# # 添加图例并调整位置
# ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1))
#
# # 显示图像
# plt.show()


import matplotlib.pyplot as plt

# 构造数据
x = [1, 2, 3, 4, 5, 6]
y = [1138807.1, 1149237.0, 83216.5, 451544.1, 614476.4, 81370.0]
# y = [1, 2, 3, 4, 5, 6]
# 创建一个figure对象
fig, ax = plt.subplots()

# 绘制折线图
ax.plot(x, y)

# 遍历每个坐标点，并添加数据标签
for i, (xx, yy) in enumerate(zip(x, y)):
    # 计算在这个点周围最多能显示多少个字符，以及能容纳的最大字体大小
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    max_chars = int(round(bbox.width / 8))
    max_fontsize = (bbox.height * 72 / 2) / len(str(yy))

    # 格式化文本
    text = f'({xx}, {yy})'

    # 在初始位置尝试添加数据标签
    t = ax.text(xx, yy, text, fontsize=max_fontsize, ha='center', va='bottom')
    print( t.get_window_extent().width, bbox.width, max_chars, max_fontsize, max_fontsize * bbox.width * max_chars / t.get_window_extent().width)
    # 如果标签超过了预定字符数或字体太大，则缩小字体并将标签移动到上方
    if len(text) > max_chars or t.get_window_extent().width > bbox.width:
        t.set_text(f'({xx}, {yy})')
        t.set_fontsize(max_fontsize * bbox.width * max_chars* 9 / t.get_window_extent().width)
        t.set_position((xx, yy + max_fontsize / bbox.height))

# 显示图像
plt.show()



# import matplotlib.pyplot as plt
#
# # 准备数据
# x = [1, 2, 3, 4, 5, 6]
# y = [1138807.1, 1149237.0, 83216.5, 451544.1, 614476.4, 81370.0]
#
# # 创建图形和两个子图
# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
#
# # 在第一个子图中绘制原始折线图，并用mask数组控制标签的显示
# line1, = ax1.plot(x, y, 'o-', label='data')
# line1.set_label('_nolegend_')
# mask1 = [False] * len(x)
# last_x, last_y = None, None
# min_dist = 50
# for i, (xi, yi) in enumerate(zip(x, y)):
#     show_label = True
#     if last_x is not None:
#         dist = ((ax1.transData.transform([xi, yi]) - ax1.transData.transform([last_x, last_y])) ** 2).sum() ** 0.5
#         if dist < min_dist:
#             show_label = False
#     if show_label:
#         ax1.text(xi, yi, str(yi), fontsize=10, ha='center', va='bottom')
#     else:
#         mask1[i] = True
#     last_x, last_y = xi, yi
# line1.set_markevery(mask1)
# line1.set_markeredgewidth(1)
#
# # 在第二个子图中绘制原始折线图，并用mask数组控制标签的显示
# line2, = ax2.plot(x, y, 'o-', label='data')
# line2.set_label('_nolegend_')
# mask2 = [False] * len(x)
# last_x, last_y = None, None
# min_dist = 80
# for i, (xi, yi) in enumerate(zip(x, y)):
#     show_label = True
#     if last_x is not None:
#         dist = ((ax2.transData.transform([xi, yi]) - ax2.transData.transform([last_x, last_y])) ** 2).sum() ** 0.5
#         if dist < min_dist:
#             show_label = False
#     if show_label:
#         ax2.text(xi, yi, str(yi), fontsize=8, ha='center', va='bottom')
#     else:
#         mask2[i] = True
#     last_x, last_y = xi, yi
# line2.set_markevery(mask2)
# line2.set_markeredgewidth(1)
#
# # 我们手动调整X, Y轴的坐标范围，使其各自适应子图的大小
# ax1.set_xlim((x[0]-1, x[-1]+1))
# ax2.set_xlim((x[0]-1, x[-1]+1))
# ymax = max(y)
# ymin = min(y)
# ydiff = ymax - ymin
# ax1.set_ylim((ymin - 0.1*ydiff, ymax + 0.3*ydiff))
# ax2.set_ylim((ymin - 0.1*ydiff, ymax + 0.3*ydiff))
#
# # 添加图例，可以发现我们用label='_nolegend_'来隐藏最初的数据标签，而手动添加的文本标签在图例中显示出来了
# ax1.legend(['data', 'text'], fontsize=12)
# ax2.legend(['data', 'text'], fontsize=12)
#
# plt.show()

# import matplotlib.pyplot as plt
#
# # 生成一些数据
# x = range(0, 6)
# y = [1138807.1, 1149237.0, 83216.5, 451544.1, 614476.4, 81370.0]
#
# fig = plt.subplot(2, 2, 1)
#
# ax = plt.gca()
#
# # 绘制折线图，并隐藏所有数据点的标签
# line, = ax.plot(x, y, 'o-', label='data')
# line.set_label('_nolegend_')
#
# # 遍历所有数据点，根据条件显示或隐藏标签
# mask = [True] * len(x)  # 标志数组，用于控制哪些标签显示
# min_dist = 30  # 最小的显示距离，单位为像素
# last_x, last_y = None, None  # 上一个数据点的坐标
# for i, (xi, yi) in enumerate(zip(x, y)):
#     show_label = True
#     if last_x is not None:
#         dist = ((ax.transData.transform((xi, yi)) - ax.transData.transform((last_x, last_y))) ** 2).sum() ** 0.5
#         if dist < min_dist:
#             show_label = False
#     if show_label:
#         ax.text(xi, yi, str(yi), ha="center", va="bottom", fontsize=10)
#     else:
#         mask[i] = False
#     last_x, last_y = xi, yi
#
# # 使用掩码来隐藏数据点和标签
# line.set_markevery(mask)
# line.set_markeredgewidth(1)
#
# plt.show()
