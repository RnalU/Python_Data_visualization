import sys
import os
import time
from random import randint
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QWaitCondition, QMutex
from PyQt5.QtGui import QImage, QPixmap

from UI.form import Ui_Form


class MatplotlibDraw(FigureCanvas):
    """绘图类"""
    # 声明回返信号
    commite_log = pyqtSignal(str)

    def __init__(self, parent=None, width=20, height=10, dpi=125):
        super(MatplotlibDraw, self).__init__()
        plt.rcParams['font.family'] = ['SimHei']  # 更换字体使中文显示正常
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 预声明变量
        self.table_rol = None  # 子图的行数
        self.table_col = None  # 子图的列数
        self.data_nums = None  # 表格条目数量
        self.all_datas = []  # 处理后的表格总数居
        self.table_name = None  # 表格名称
        self.font_size = None  # 字体大小
        self.data = []  # CSV文件总集
        self.color = ['black', 'linen', 'forestgreen', 'slategrey', 'k', 'bisque', 'limegreen', 'lightsteelblue',
                      'dimgray', 'darkorange', 'darkgreen', 'cornflowerblue', 'dimgrey', 'burlywood', 'g', 'royalblue',
                      'gray', 'antiquewhite', 'green', 'ghostwhite', 'grey', 'tan', 'lime', 'lavender', 'darkgray',
                      'navajowhite', 'seagreen', 'midnightblue', 'darkgrey', 'blanchedalmond', 'mediumseagreen', 'navy',
                      'silver', 'papayawhip', 'springgreen', 'darkblue', 'lightgray', 'moccasin', 'mintcream',
                      'mediumblue', 'lightgrey', 'orange', 'mediumspringgreen', 'b', 'gainsboro', 'wheat',
                      'mediumaquamarine', 'blue', 'whitesmoke', 'oldlace', 'aquamarine', 'slateblue', 'w',
                      'floralwhite', 'turquoise', 'darkslateblue', 'white', 'darkgoldenrod', 'lightseagreen',
                      'mediumslateblue', 'snow', 'goldenrod', 'mediumturquoise', 'mediumpurple', 'rosybrown',
                      'cornsilk', 'azure', 'rebeccapurple', 'lightcoral', 'gold', 'lightcyan', 'blueviolet',
                      'indianred', 'lemonchiffon', 'paleturquoise', 'indigo', 'brown', 'khaki', 'darkslategray',
                      'darkorchid', 'firebrick', 'palegoldenrod', 'darkslategrey', 'darkviolet', 'maroon', 'darkkhaki',
                      'teal', 'mediumorchid', 'darkred', 'ivory', 'darkcyan', 'thistle', 'r', 'beige', 'c', 'plum',
                      'red', 'lightyellow', 'aqua', 'violet', 'mistyrose', 'lightgoldenrodyellow', 'cyan', 'purple',
                      'salmon', 'olive', 'darkturquoise', 'darkmagenta', 'tomato', 'y', 'cadetblue', 'm', 'darksalmon',
                      'yellow', 'powderblue', 'fuchsia', 'coral', 'olivedrab', 'lightblue', 'magenta', 'orangered',
                      'yellowgreen', 'deepskyblue', 'orchid', 'lightsalmon', 'darkolivegreen', 'skyblue',
                      'mediumvioletred', 'sienna', 'greenyellow', 'lightskyblue', 'deeppink', 'seashell', 'chartreuse',
                      'steelblue', 'hotpink', 'chocolate', 'lawngreen', 'aliceblue', 'lavenderblush', 'saddlebrown',
                      'honeydew', 'dodgerblue', 'palevioletred', 'sandybrown', 'darkseagreen', 'lightslategray',
                      'crimson', 'peachpuff', 'palegreen', 'lightslategrey', 'pink', 'peru', 'lightgreen', 'slategray',
                      'lightpink']  # 颜色集合
        self.color_p = None  # 表格绘制颜色
        self.sub_change = False  # 是否修改子图
        self.sub_idx = None  # 如果修改子图, 则子图对应的索引
        self.draw_detail = []  # 储存绘图的参数
        self.ax = None  # 定义axe
        # 状态
        self.display_data = False  # 是否显示数据
        self.display_table_name = False  # 是否显示表名

        # 创建画布
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 下面这个是画新图后不保留上次的图形，但这个代码似乎有问题报错了，先注释掉
        # self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def receive_values(self, rol, col, data_nums, datalist, fontsize, data, name, sub_change=False, sub_idx=None):
        """接收主窗口传递的绘图参数"""
        print(rol, col, data_nums, datalist, fontsize)
        # 声明绘图参数
        self.table_rol = rol
        self.table_col = col
        self.data_nums = data_nums
        self.all_datas = datalist
        self.font_size = fontsize
        self.data = data
        self.table_name: str = name
        self.sub_change = sub_change
        self.sub_idx = sub_idx

    def drawing(self, type_table: str):
        """绘制figure"""
        self.fig.clear()  # 清空画布
        self.fig.clf()
        self.draw_detail = []

        for i in range(self.data_nums):
            # 列表初始化
            number_data = []
            year_data = []

            if self.sub_change and i != self.sub_idx:
                continue

            # 排序好的数据顺序存入相应数组
            for _ in range(len(self.all_datas)):
                year_data.append(int(self.all_datas[_][0]))
                number_data.append(self.all_datas[_][i + 1])

            # 绘制折线图
            # plt.subplot(self.table_rol, self.table_col, (i + 1))
            self.ax = self.fig.add_subplot(self.table_rol, self.table_col, (i + 1))
            self.ax.cla()

            """绘制不同的图像"""
            if type_table == 'line':
                self.ax.set(xlim=(year_data[0] - 0.5, year_data[-1] + 0.5))

                if self.color_p:
                    if self.color_p == '__random':
                        """随机颜色， 于颜色数组中随机取"""
                        self.ax.plot(year_data, number_data, color=self.color[randint(0, 155)])
                        self.ax.scatter(year_data, number_data, s=16, c=self.color[randint(0, 155)])

                    else:
                        self.ax.plot(year_data, number_data, color=self.color_p)
                        self.ax.scatter(year_data, number_data, s=16, c=self.color_p)

                else:
                    self.ax.plot(year_data, number_data)
                    self.ax.scatter(year_data, number_data, s=16)

            if type_table == 'pot':
                self.ax.set(xlim=(year_data[0] - 0.5, year_data[-1] + 0.5))

                if self.color_p:
                    if self.color_p == '__random':
                        self.ax.scatter(year_data, number_data, s=16, c=self.color[randint(0, 155)])
                    else:
                        self.ax.scatter(year_data, number_data, s=16, c=self.color_p)
                else:
                    self.ax.scatter(year_data, number_data, s=16)

            if type_table == 'bar':
                if number_data.count(None):
                    number_data[number_data.index(None)] = 0

                self.ax.set(xlim=(year_data[0] - 0.5, year_data[-1] + 0.5))
                if self.color_p:
                    if self.color_p == '__random':
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1,
                                    color=self.color[randint(0, 155)])

                    else:
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1, color=self.color_p)

                else:
                    self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1)

            if type_table == 'cake':
                # 对于一些数据可能为空，此处检查空部分的数据并将其置为零
                if number_data.count(None):
                    number_data[number_data.index(None)] = 0

                # 饼图中不可出现复数数据，故将复数部分的数据删除
                for idx, data in enumerate(number_data):
                    if data <= 0:
                        number_data.pop(idx)
                        year_data.pop(idx)

                # 颜色渐变
                _x = list(range(1, len(number_data) + 1))
                colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(_x)))

                # 坐标轴处理
                self.ax.tick_params(bottom=False, top=False, left=False, right=False)
                self.ax.spines['left'].set_color('None')
                # self.ax.spines['bottom'].set_color('None')
                self.ax.set_yticks([])
                self.ax.set_xticks([])

                if self.color_p:
                    if self.color_p == '__random':
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1,
                                    color=self.color[randint(0, 155)])

                    else:
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1, color=self.color_p)

                else:
                    self.ax.pie(number_data, colors=colors, radius=1, center=(4, 4), labels=year_data,
                                autopct='%.2f%%',
                                labeldistance=1.1,
                                wedgeprops={"linewidth": 1, "edgecolor": "white"},
                                textprops={'fontsize': self.font_size * 3}, frame=True)

            x_major_locator = MultipleLocator(2)

            # 为每个点绘制数据标签
            if self.display_data and type_table == "line":  # 如果显示数据
                if number_data.count(None):
                    number_data[number_data.index(None)] = 0

                # 计算全体平均值
                _sums = 0
                for _ in number_data:
                    _sums += _
                _sums = _sums / len(number_data)
                # 取出数据集中的最大值与最小值
                temp_list = number_data[:]
                temp_list.sort()
                rule = temp_list[-1] - temp_list[0]

                for point in range(len(year_data)):
                    if not number_data[point]:
                        continue

                    if number_data[0] < 100:
                        self.ax.text(year_data[point], number_data[point], '%.1f' % number_data[point],
                                     fontdict={'fontsize': self.font_size * 3.8}, ha='center', va='bottom')

                    elif number_data[0] < 5000:
                        self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                     fontdict={'fontsize': self.font_size * 3.8}, ha='center', va='bottom')

                    else:
                        if _sums > 10000:
                            """调整字符位置"""
                            print(abs(number_data[point] - number_data[point - 1]) / rule)
                            if point > 0:
                                if (abs(number_data[point] - number_data[point - 1])) / rule < 0.10 and number_data[
                                    point] > number_data[point - 1]:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='bottom')

                                elif (abs(number_data[point] - number_data[point - 1])) / rule < 0.12 and number_data[
                                    point] < number_data[point - 1]:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='top')
                                else:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='top')

                            else:
                                self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                             fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='bottom')

                    """废弃调整字符位置"""
                    # if point != 0 and abs(number_data[point] - number_data[point - 1]) / abs(max(number_data[point], number_data[point - 1])) > 0.2:
                    #     ax.text(year_data[point], number_data[point], '%.0f' %number_data[point],
                    #             fontdict={'fontsize':font_size * 5}, va='center')
                    # else:
                    #     ax.text(year_data[point], number_data[point], '%.0f' % number_data[point],
                    #             fontdict={'fontsize': font_size * 5}, ha='center', va='center')

            elif self.display_data:
                # 为每个点绘制数据标签
                for point in range(len(year_data)):
                    if not number_data[point]:
                        continue
                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                 fontdict={'fontsize': self.font_size * 3}, ha='center', va='bottom')

            # ax.set_xlabel('年份', fontsize=10)

            if not len(self.data.values[i + 2][0].split(",")[0]) > 12 and type_table != 'cake':
                self.ax.set_ylabel(self.data.values[i + 2][0].split(",")[0], fontsize=10)
            if self.display_table_name:
                self.ax.set_title(self.data.values[i + 2][0].split(",")[0], fontsize=12)

            # 调整横坐标和纵坐标的范围
            # xlim(yearss[0] + 10, yearss[-1] + 10)
            # ylim(datas[0] * 0.5, datas[-1] * 1.5)

            # 调整横坐标的间隔
            self.ax.xaxis.set_major_locator(x_major_locator)
            # self.ax.xticks(rotation=20, fontsize=10)
            self.ax.spines['right'].set_color('None')  # 选中上方的脊梁并替换为空
            self.ax.spines['top'].set_color('None')
            self.ax.xaxis.set_ticks_position('bottom')  # 设置x轴位置
            self.ax.yaxis.set_ticks_position('left')  # 设置y轴位置

            # 将该图标绘制所需参数加入到表格当中 "绘制类型", "图标颜色", "是否显示数据", "是否显示表明"
            self.draw_detail.append([type_table, self.color_p, self.display_data, self.display_table_name])

        print(self.draw_detail)
        self.fig.subplots_adjust(hspace=0.6, wspace=0.5)
        self.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()  # 画布刷新self.figs.canvas

    def subplot_drawing(self, sub_type, sub_color, display_data, display_name):
        """单独绘制sub_figure"""
        self.fig.clear()  # 清空画布
        self.fig.clf()

        # 修改之前储存的表格细节中子图对应的数据
        self.draw_detail[self.sub_idx][0] = sub_type
        self.draw_detail[self.sub_idx][1] = sub_color
        self.draw_detail[self.sub_idx][2] = display_data
        self.draw_detail[self.sub_idx][3] = display_name

        print(self.data_nums)

        for i in range(self.data_nums):
            # 列表初始化
            number_data = []
            year_data = []

            # 得到传递的表格参数
            type_sub = self.draw_detail[i][0]
            table_line_color = self.draw_detail[i][1]
            table_display_data = self.draw_detail[i][2]
            table_display_name = self.draw_detail[i][3]

            # 排序好的数据顺序存入相应数组
            for _ in range(len(self.all_datas)):
                year_data.append(int(self.all_datas[_][0]))
                number_data.append(self.all_datas[_][i + 1])

            # 绘制折线图
            # plt.subplot(self.table_rol, self.table_col, (i + 1))
            self.ax = self.fig.add_subplot(self.table_rol, self.table_col, (i + 1))
            self.ax.cla()

            """绘制不同的图像"""
            if type_sub == 'line':
                self.ax.set(xlim=(year_data[0] - 0.5, year_data[-1] + 0.5))

                if table_line_color:
                    if table_line_color == '__random':
                        """随机颜色， 于颜色数组中随机取"""
                        self.ax.plot(year_data, number_data, color=self.color[randint(0, 155)])
                        self.ax.scatter(year_data, number_data, s=16, c=self.color[randint(0, 155)])

                    else:
                        self.ax.plot(year_data, number_data, color=table_line_color)
                        self.ax.scatter(year_data, number_data, s=16, c=table_line_color)

                else:
                    self.ax.plot(year_data, number_data)
                    self.ax.scatter(year_data, number_data, s=16)

            if type_sub == 'pot':
                self.ax.set(xlim=(year_data[0] - 0.5, year_data[-1] + 0.5))

                if table_line_color:
                    if table_line_color == '__random':
                        self.ax.scatter(year_data, number_data, s=16, c=self.color[randint(0, 155)])
                    else:
                        self.ax.scatter(year_data, number_data, s=16, c=table_line_color)
                else:
                    self.ax.scatter(year_data, number_data, s=16)

            if type_sub == 'bar':
                if number_data.count(None):
                    number_data[number_data.index(None)] = 0

                self.ax.set(xlim=(year_data[0] - 0.5, year_data[-1] + 0.5))
                if table_line_color:
                    if table_line_color == '__random':
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1,
                                    color=self.color[randint(0, 155)])

                    else:
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1,
                                    color=table_line_color)

                else:
                    self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1)

            if type_sub == 'cake':
                # 对于一些数据可能为空，此处检查空部分的数据并将其置为零
                if number_data.count(None):
                    number_data[number_data.index(None)] = 0

                # 饼图中不可出现复数数据，故将复数部分的数据删除
                for idx, data in enumerate(number_data):
                    if data <= 0:
                        number_data.pop(idx)
                        year_data.pop(idx)

                # 颜色渐变
                _x = list(range(1, len(number_data) + 1))
                colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(_x)))

                # 坐标轴处理
                self.ax.tick_params(bottom=False, top=False, left=False, right=False)
                self.ax.spines['left'].set_color('None')
                # self.ax.spines['bottom'].set_color('None')
                self.ax.set_yticks([])
                self.ax.set_xticks([])

                if table_line_color:
                    if table_line_color == '__random':
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1,
                                    color=self.color[randint(0, 155)])

                    else:
                        self.ax.bar(year_data, number_data, width=1, edgecolor="white", linewidth=1,
                                    color=table_line_color)

                else:
                    self.ax.pie(number_data, colors=colors, radius=1, center=(4, 4), labels=year_data,
                                autopct='%.2f%%',
                                labeldistance=1.1,
                                wedgeprops={"linewidth": 1, "edgecolor": "white"},
                                textprops={'fontsize': self.font_size * 3}, frame=True)

            x_major_locator = MultipleLocator(2)

            # 为每个点绘制数据标签
            if table_display_data and type_sub == "line":  # 如果显示数据
                if number_data.count(None):
                    number_data[number_data.index(None)] = 0

                # 计算全体平均值
                _sums = 0
                for _ in number_data:
                    _sums += _
                _sums = _sums / len(number_data)
                # 取出数据集中的最大值与最小值
                temp_list = number_data[:]
                temp_list.sort()
                rule = temp_list[-1] - temp_list[0]

                for point in range(len(year_data)):
                    if not number_data[point]:
                        continue

                    if number_data[0] < 100:
                        self.ax.text(year_data[point], number_data[point], '%.1f' % number_data[point],
                                     fontdict={'fontsize': self.font_size * 3.8}, ha='center', va='bottom')

                    elif number_data[0] < 5000:
                        self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                     fontdict={'fontsize': self.font_size * 3.8}, ha='center', va='bottom')

                    else:
                        if _sums > 10000:
                            """调整字符位置"""
                            if point > 0:
                                if (abs(number_data[point] - number_data[point - 1])) / rule < 0.10 and number_data[
                                    point] > number_data[point - 1]:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='bottom')

                                elif (abs(number_data[point] - number_data[point - 1])) / rule < 0.12 and number_data[
                                    point] < number_data[point - 1]:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='top')
                                else:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='top')

                            else:
                                self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                             fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='bottom')

            elif table_display_data:
                # 为每个点绘制数据标签
                for point in range(len(year_data)):
                    if not number_data[point]:
                        continue
                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                 fontdict={'fontsize': self.font_size * 3}, ha='center', va='bottom')

            # ax.set_xlabel('年份', fontsize=10)

            if not len(self.data.values[i + 2][0].split(",")[0]) > 12 and type_sub != 'cake':
                self.ax.set_ylabel(self.data.values[i + 2][0].split(",")[0], fontsize=10)
            if table_display_name:
                self.ax.set_title(self.data.values[i + 2][0].split(",")[0], fontsize=12)

            # 调整横坐标和纵坐标的范围
            # xlim(yearss[0] + 10, yearss[-1] + 10)
            # ylim(datas[0] * 0.5, datas[-1] * 1.5)

            # 调整横坐标的间隔
            self.ax.xaxis.set_major_locator(x_major_locator)
            # self.ax.xticks(rotation=20, fontsize=10)
            self.ax.spines['right'].set_color('None')  # 选中上方的脊梁并替换为空
            self.ax.spines['top'].set_color('None')
            self.ax.xaxis.set_ticks_position('bottom')  # 设置x轴位置
            self.ax.yaxis.set_ticks_position('left')  # 设置y轴位置

        self.fig.subplots_adjust(hspace=0.6, wspace=0.5)
        self.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()  # 画布刷新self.figs.canvas

    def save_drawing(self, type: str):
        """保存生成的图像"""
        time_log = 0
        try:
            if type == '矢量图':
                # 读取当前时间
                time_log = time.strftime("%Y-%m-%d %H:%M:%S")
                # 保存
                self.fig.savefig(
                    f'.\\output\\{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.eps',
                    dpi=300)
            if type == 'PNG':
                # 读取当前时间
                time_log = time.strftime("%Y-%m-%d %H:%M:%S")
                # 保存
                self.fig.savefig(
                    f'.\\output\\{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.png',
                    dpi=300)

        except Exception as e:
            pass

        else:
            if type == '矢量图':
                self.commite_log.emit(
                    f'生成成功！输出文件位于:\'./output/{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.eps\'')

            elif type == 'PNG':
                self.commite_log.emit(
                    f'生成成功！输出文件位于:\'./output/{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.png\'')


"""子线程测试"""


# class WindowsThread(QThread, Ui_Form):
#     def __init__(self, objects):
#         super(WindowsThread, self).__init__()
#         self.Windows = objects
#         self.i = 0
#
#     def run(self):
#         while True:
#             self.Windows.textBrowser.append(f"{self.i}")
#             self.Windows.textBrowser.moveCursor(-1)
#             self.i += 1
#             time.sleep(0.2)


class MyWindows(QWidget, Ui_Form):
    def __init__(self):
        super(MyWindows, self).__init__()
        # UI初始化
        self.setupUi(self)
        self.signal_init()
        # self.textBrowser.append(f"{'温馨提示':-^28}\n系统会自动在程序目录下创建table文件夹\n请将展示的表格放入table文件夹内")
        # self.textBrowser.moveCursor(-1)

        # 变量初始化
        self.table_draw_on = False  # 表格是否绘制
        self.table_aim = None  # 当前表格名称
        self.table_drawing = None  # 绘制完成的表格名称
        self.table_nums = None  # 声明表的个数
        self.num_cols = None  # 预生成图表的列
        self.num_rows = None  # 预生成图表的列
        self.data = None  # 表格数据
        self.font_size = None  # 字体大小
        self.data_nums = None  # 数据个数
        self.all_datas = []  # 处理后的表格数据
        self.year_data = []  # 横轴年份数据
        self.number_data = []  # 纵轴数据
        self.table_sub_datas = []  # 表格条目数据
        self.figure1 = None  # 定义绘图对象
        self.aim_colors = ['蓝色', '青色', '红色', '品红', '紫色', '随机颜色']  # 定义颜色
        self.colors_dict = {
            '蓝色': 'b',
            '青色': 'c',
            '红色': 'r',
            '品红': 'm',
            '紫色': 'purple',
            '黄色': 'y',
            '随机颜色': '__random'
        }  # 定义颜色对照字典

        # 表格读取
        self.read_tables()

        """绘图部分"""
        # 创建绘图对象
        self.figure1 = MatplotlibDraw()
        # 绑定对象的信号
        self.figure1.commite_log.connect(self.submit_log_inf)

    def signal_init(self):
        """信号的相关绑定与声明"""
        self.list_table.itemClicked.connect(self.select_table)
        self.pushButton_drawing.clicked.connect(lambda: self.draw_tables(False))
        self.pushButtont_refresh_read.clicked.connect(self.flushed_tables)
        self.pushButton_save_img.clicked.connect(self.save_img)
        self.pushButton_subplot_change.clicked.connect(self.subplot_change)

    def windows_init(self):
        pass

    def read_tables(self):
        """读取表格文件"""
        # 先检测是否存在文件夹
        if 'table' in os.listdir('./'):
            # self.submit_log_inf("检测到table文件夹", 1)
            # 检测到文件夹后进行记录
            file_list = [file for file in os.listdir('./table') if file.split('.')[-1] == 'csv']
            file_nums = len(file_list)
            self.table_nums = file_nums
            self.submit_log_inf(f"找到{file_nums}个CSV表格文件:\n{file_list}", 1)

            # 添加到ListWidget对象中
            self.list_table.addItems(file_list)

        # 如果不存在，则创建该文件夹
        else:
            try:
                os.mkdir('./table')

            except Exception as e:
                self.submit_log_inf("不存在table文件夹, 且创建文件夹失败！", 0)
                self.submit_log_inf(f"系统返回:{e}", 0)

            else:
                self.submit_log_inf("未检测到table文件夹, 已自动创建", 1)

    def flushed_tables(self):
        # 清空TableWidget里的内容
        self.list_table.clear()
        older_nums = self.table_nums
        # 先检测是否存在文件夹
        if 'table' in os.listdir('./'):
            # self.submit_log_inf("检测到table文件夹", 1)
            # 检测到文件夹后进行记录
            file_list = [file for file in os.listdir('./table') if file.split('.')[-1] == 'csv']
            file_nums = len(file_list)
            self.table_nums = file_nums

            if file_nums == older_nums:
                self.submit_log_inf(f"刷新成功, 未找到新的CSV表格文件")

            elif older_nums < file_nums:
                self.submit_log_inf(f"刷新成功, 发现{file_nums - older_nums}个新的CSV文件。当前文件如下:\n{file_list}")
            else:
                self.submit_log_inf("你是不是偷偷删除表格了?", 0)

            # 添加到ListWidget对象中
            self.list_table.addItems(file_list)

        # 如果不存在，则创建该文件夹
        else:
            try:
                os.mkdir('./table')

            except Exception as e:
                self.submit_log_inf("不存在table文件夹, 且创建文件夹失败！", 0)
                self.submit_log_inf(f"系统返回:{e}", 0)

            else:
                self.submit_log_inf("未检测到table文件夹, 已自动创建", 1)

    def select_table(self):
        """选中表格条目后执行的操作, 最终获取该表格的全部信息，并封装成一个列表"""
        # 初始化变量
        self.all_datas = []
        self.table_sub_datas = []
        self.listWidget_entries.clear()

        # 获取选中的表格
        self.table_aim = self.list_table.selectedItems()[0].text()

        # 读取数据
        self.data = pd.read_csv(f'table/{self.table_aim}', encoding="GBK", sep='\t', header=0)

        # 读取数据分类个数
        self.data_nums = 0
        for _data in self.data.values:
            if _data[0].split(",")[0] not in ["数据来源：国家统计局", "数据库：年度数据", "时间：最近10年", "指标"]:
                if not _data[0].split(",")[0].find(".") > 0:
                    self.data_nums += 1

        # 根据数据个数，自动生成a * b区域划分数据
        self.num_rows = int(np.sqrt(self.data_nums))
        self.num_cols = int(np.ceil(self.data_nums / self.num_rows))

        # 自动生成字体大小
        self.fig_size = (self.num_cols * 3, self.num_rows * 3)
        self.font_size = min(self.fig_size) / max(self.num_rows, self.num_cols)

        # 年份数据处理
        years = self.data.values

        # 其他数据处理
        for index, year in enumerate(years[1][0].replace("年", "").split(",")[1:]):
            self.all_datas.append([int(year)])
            for i in range(self.data_nums):
                # years列表的结构为：行与行直接以列表储存，每一个列表中为字符串类型，表格使用，隔开。
                if years[i + 2][0].split(",")[1 + index] == '':
                    self.all_datas[index].append(None)
                else:
                    self.all_datas[index].append(float(years[i + 2][0].split(",")[1 + index]))

        # 将数据排序
        self.all_datas = sorted(self.all_datas, key=lambda x: x[0])
        print(self.all_datas)

        # 将读取到的条目数据储存到TableWidget
        for entries in self.data.values[2:]:
            if not entries[0].split(',')[0].count('.') and not entries[0].split(',')[0].count('：'):
                self.table_sub_datas.append(entries[0].split(',')[0])
            else:
                pass

        self.listWidget_entries.addItems(self.table_sub_datas)

    def draw_tables(self, sub_change=False, sub_idx=None):
        """绘制图标"""
        if len(self.all_datas) != 0 and self.font_size and self.num_cols and self.num_rows:
            """调用绘图对象, 绘制图像"""
            try:
                self.vlayout_show_plot.removeWidget(self.figure1)
            except:
                pass

            # 检测相关参数
            if self.checkBox_show_data_v.isChecked():
                self.figure1.display_data = True  # 显示数据
            else:
                self.figure1.display_data = False  # 关闭显示数据
            if self.checkBox_show_table_name.isChecked():
                self.figure1.display_table_name = True  # 显示表名
            else:
                self.figure1.display_table_name = False  # 关闭显示表名

            if self.comboBox_select_color.currentText() in self.aim_colors:
                self.figure1.color_p = self.colors_dict[self.comboBox_select_color.currentText()]
            else:
                self.figure1.color_p = False

            # 加入垂直布局
            self.vlayout_show_plot.addWidget(self.figure1)

            self.figure1.receive_values(
                rol=self.num_rows,
                col=self.num_cols,
                data_nums=self.data_nums,
                datalist=self.all_datas,
                fontsize=self.font_size,
                data=self.data,
                name=self.table_aim,
                sub_change=sub_change,
                sub_idx=sub_idx)

            try:
                if not sub_change:  # 如果确定为子图自定义绘制, 则先取消绘制, 只传递信息
                    if self.radioButton_type_of_line.isChecked():
                        self.figure1.drawing('line')

                    if self.radioButton_type_of_pot.isChecked():
                        self.figure1.drawing('pot')

                    if self.radioButton_bar.isChecked():
                        self.figure1.drawing('bar')

                    if self.radioButton_cake.isChecked():
                        self.figure1.drawing('cake')

            except Exception as e:
                self.submit_log_inf(f"绘制错误！系统返回:\n{e}")

            else:
                # self.submit_log_inf(f"绘制表格\"{self.table_aim}\"成功!")
                self.table_draw_on = True  # 标记已绘制表格
                self.table_drawing = self.table_aim  # 记录当前屏幕显示的表格

        else:
            self.submit_log_inf("表格信息无效！请重新选择", 0)

    def save_img(self):
        """保存图片"""
        if not os.listdir().count('output'):
            os.mkdir('output')
            self.submit_log_inf("未检测到\'output\'文件夹, 已自动创建")

        if self.table_draw_on:
            if self.radioButton_eps.isChecked():
                self.figure1.save_drawing('矢量图')

            elif self.radioButton_png.isChecked():
                self.figure1.save_drawing('PNG')

            else:
                self.submit_log_inf("请选择要保存的格式", 0)

        else:
            self.submit_log_inf("请先绘制图像", 0)

    def subplot_change(self):
        """子图自定义修改"""
        try:
            aim_entry = self.listWidget_entries.selectedItems()[0].text()  # 尝试得到选择的条目
            self.submit_log_inf(f"你选中的条目是'{aim_entry}'")

            if self.table_drawing == self.table_aim:  # 检测当前选择的条目对应表格与绘制的表格是否一致
                subplot_type = None
                subplot_display_data = False
                subplot_display_name = False

                self.submit_log_inf('开始绘制')
                # 先得到条目对应的索引
                aim_entry_idx = self.table_sub_datas.index(aim_entry)
                # 得到要绘制的子图的相关参数
                if self.radioButton_type_of_line.isChecked():
                    subplot_type = 'line'

                if self.radioButton_type_of_pot.isChecked():
                    subplot_type = 'pot'

                if self.radioButton_bar.isChecked():
                    subplot_type = 'bar'

                if self.radioButton_cake.isChecked():
                    subplot_type = 'cake'

                subplot_color = self.comboBox_select_color.currentText()

                if self.checkBox_show_data_v.isChecked():
                    subplot_display_data = True

                if self.checkBox_show_table_name.isChecked():
                    subplot_display_name = True

                # 绘制
                self.draw_tables(True, aim_entry_idx)  # 此处只起到传递信息的作用

                if subplot_color in self.aim_colors:
                    self.figure1.subplot_drawing(subplot_type, self.colors_dict[subplot_color], subplot_display_data,
                                                 subplot_display_name)  # 传递绘制的子图的信息

                else:
                    self.figure1.subplot_drawing(subplot_type, False, subplot_display_data,
                                                 subplot_display_name)  # 传递绘制的子图的信息

            else:
                self.submit_log_inf("请选择当前展示的表格所属条目", 0)

        except Exception as e:
            self.submit_log_inf("请先选中表格条目", 0)

    def submit_log_inf(self, info, env=1):
        """上传日志信息到窗口的textBrowser"""
        # 获取当前时间
        time_log = time.strftime("%Y-%m-%d %H:%M:%S")
        # 得到状态信息
        if env == 1:
            con = "正常"
        else:
            con = "异常"

        # 上传日志
        self.textBrowser.append(f"·{time_log}({con})> {info}")
        self.textBrowser.moveCursor(-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindows()
    w.show()

    app.exec()
