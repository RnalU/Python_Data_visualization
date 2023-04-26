import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data = pd.read_csv('table/国内生产总值.csv', encoding="GBK", sep='\t', header=0)

# 读取数据分类个数
data_nums = 0
for _data in data.values:
    if _data[0].split(",")[0] not in ["数据来源：国家统计局", "数据库：年度数据", "时间：最近10年", "指标"]:
        if not _data[0].split(",")[0].find(".") > 0:
            data_nums += 1

# 根据数据个数，自动生成a * b区域划分数据
num_rows = int(np.sqrt(data_nums))
num_cols = int(np.ceil(data_nums / num_rows))

# 自动生成字体大小
figsize = (num_cols * 3, num_rows * 3)
font_size = min(figsize) / max(num_rows, num_cols)
print("字体大小：", font_size * 6)
# 年份数据处理
years = data.values

# 声明相应数据储存列表
all_datas = []
year_data = []
number_data = []

# 其他数据处理
for index, year in enumerate(years[1][0].replace("年", "").split(",")[1:]):
    all_datas.append([int(year)])
    for i in range(data_nums):
        # years列表的结构为：行与行直接以列表储存，每一个列表中为字符串类型，表格使用，隔开。
        if years[i + 2][0].split(",")[1 + index] == '':
            all_datas[index].append(None)
        else:
            all_datas[index].append(float(years[i + 2][0].split(",")[1 + index]))

# 创建画布
plt.figure(figsize=(10, 8))

for i in range(data_nums):
    # 列表初始化
    number_data = []
    year_data = []

    # 将数据排序
    all_datas = sorted(all_datas, key=lambda x: x[0])

    # 排序好的数据顺序存入相应数组
    for _ in range(len(all_datas)):
        year_data.append(int(all_datas[_][0]))
        number_data.append(all_datas[_][i + 1])
    # print(year_data, number_data)

    # 绘制折线图
    plt.subplot(num_cols, num_rows, (i + 1))
    plt.plot(year_data, number_data)
    plt.scatter(year_data, number_data, s=16)

    x_major_locator = MultipleLocator(2)

    plt.xlim(year_data[0] - 0.5, year_data[-1] + 0.5)

    # 添加图例和标签
    ax = plt.gca()
    # 为每个点绘制数据标签
    for point in range(len(year_data)):
        if not number_data[point]:
            continue
        ax.text(year_data[point], number_data[point], '%.1f' % number_data[point],
                fontdict={'fontsize': font_size * 3.8}, ha='center', va='bottom')

        """废弃调整字符位置"""
        # if point != 0 and abs(number_data[point] - number_data[point - 1]) / abs(max(number_data[point], number_data[point - 1])) > 0.2:
        #     ax.text(year_data[point], number_data[point], '%.0f' %number_data[point],
        #             fontdict={'fontsize':font_size * 5}, va='center')
        # else:
        #     ax.text(year_data[point], number_data[point], '%.0f' % number_data[point],
        #             fontdict={'fontsize': font_size * 5}, ha='center', va='center')

    # ax.set_xlabel('年份', fontsize=10)
    if not len(data.values[i + 2][0].split(",")[0]) > 12:
        ax.set_ylabel(data.values[i + 2][0].split(",")[0], fontsize=10)
    ax.set_title(data.values[i + 2][0].split(",")[0], fontsize=12)

    # 调整横坐标和纵坐标的范围
    # plt.xlim(yearss[0] + 10, yearss[-1] + 10)
    # plt.ylim(datas[0] * 0.5, datas[-1] * 1.5)

    # 调整横坐标的间隔
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xticks(rotation=20, fontsize=10)
    ax.spines['right'].set_color('None')  # 选中上方的脊梁并替换为空
    ax.spines['top'].set_color('None')  # <- now autocompletes

    ax.xaxis.set_ticks_position('bottom')  # 设置x轴位置
    ax.yaxis.set_ticks_position('left')  # 设置y轴位置
    # ax.spines['bottom'].set_position(('data', yearss[i][0] * 0.95))  # 选中并更改位置
    # ax.spines['left'].set_position(('data', yearss[i][0] - 0.4))

plt.subplots_adjust(hspace=0.6, wspace=0.5)

# 显示图形
plt.show()
