import time
import numpy as np
from random import randint
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSizePolicy
from adjustText import adjust_text


class MatplotlibDraw(FigureCanvas):
    """绘图类"""
    # 声明回返信号
    commit_log = pyqtSignal(str)

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
        self.color_cake = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu',
                           'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r',
                           'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired',
                           'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu',
                           'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r',
                           'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn',
                           'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r',
                           'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r',
                           'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r',
                           'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis',
                           'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix',
                           'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
                           'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
                           'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2',
                           'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno',
                           'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean',
                           'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow',
                           'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10',
                           'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain',
                           'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted',
                           'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']
        self.color_cake_dict = {
            'b': "Blues_r",
            'c': "ocean_r",
            'r': "Reds",
            'm': "spring",
            'purple': "Purples",
            'y': "YlGn",
            '__random': "__random"
        }
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

    def drawing(self, type_table: str, sub_type=None, sub_color=None, display_data=None, display_name=None):
        """绘制figure"""
        self.fig.clear()  # 清空画布
        self.fig.clf()
        self.draw_detail = []

        new_texts = []
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
                print(self.color_p)
                if self.color_p:
                    if self.color_p != "__random":
                        colors = plt.get_cmap(self.color_cake_dict[self.color_p])(np.linspace(0.2, 0.7, len(_x)))
                    else:
                        colors = plt.get_cmap(self.color_cake[randint(0, 155)])(np.linspace(0.2, 0.7, len(_x)))

                else:
                    colors = plt.get_cmap("Blues")(np.linspace(0.2, 0.7, len(_x)))

                # 坐标轴处理
                self.ax.tick_params(bottom=False, top=False, left=False, right=False)
                self.ax.spines['left'].set_color('None')
                # self.ax.spines['bottom'].set_color('None')
                self.ax.set_yticks([])
                self.ax.set_xticks([])

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
                                if (abs(number_data[point] - number_data[point - 1])) / rule < 0.10 and number_data[point] > number_data[point - 1]:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='bottom')

                                elif (abs(number_data[point] - number_data[point - 1])) / rule < 0.12 and number_data[point] < number_data[point - 1]:
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

            # new_texts.append([plt.text(x_, y_, str(text), fontsize=self.font_size * 3) for x_, y_, text in zip(year_data, number_data, number_data)])

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

        print(self.draw_detail)

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
                # colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(_x)))

                # 坐标轴处理
                self.ax.tick_params(bottom=False, top=False, left=False, right=False)
                self.ax.spines['left'].set_color('None')
                # self.ax.spines['bottom'].set_color('None')
                self.ax.set_yticks([])
                self.ax.set_xticks([])

                if table_line_color:
                    if table_line_color == '__random':
                        colors = plt.get_cmap(self.color_cake[randint(0, 155)])(np.linspace(0.2, 0.7, len(_x)))
                        self.ax.pie(number_data, colors=colors, radius=1, center=(4, 4), labels=year_data,
                                    autopct='%.2f%%',
                                    labeldistance=1.1,
                                    wedgeprops={"linewidth": 1, "edgecolor": "white"},
                                    textprops={'fontsize': self.font_size * 3}, frame=True)

                    else:
                        colors = plt.get_cmap(self.color_cake_dict[table_line_color])(np.linspace(0.2, 0.7, len(_x)))
                        self.ax.pie(number_data, colors=colors, radius=1, center=(4, 4), labels=year_data,
                                    autopct='%.2f%%',
                                    labeldistance=1.1,
                                    wedgeprops={"linewidth": 1, "edgecolor": "white"},
                                    textprops={'fontsize': self.font_size * 3}, frame=True)

                else:
                    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(_x)))
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
                                if (abs(number_data[point] - number_data[point - 1])) / rule < 0.10 and number_data[point] > number_data[point - 1]:
                                    self.ax.text(year_data[point], number_data[point], '%d' % number_data[point],
                                                 fontdict={'fontsize': self.font_size * 3.3}, ha='center', va='bottom')

                                elif (abs(number_data[point] - number_data[point - 1])) / rule < 0.12 and number_data[point] < number_data[point - 1]:
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

    def save_drawing(self, type_pix: str):
        """保存生成的图像"""
        time_log = 0
        try:
            if type_pix == '矢量图':
                # 读取当前时间
                time_log = time.strftime("%Y-%m-%d %H:%M:%S")
                # 保存
                self.fig.savefig(
                    f'.\\output\\{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.eps',
                    dpi=300)
            if type_pix == 'PNG':
                # 读取当前时间
                time_log = time.strftime("%Y-%m-%d %H:%M:%S")
                # 保存
                self.fig.savefig(
                    f'.\\output\\{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.png',
                    dpi=300)

        except Exception as e:
            pass

        else:
            if type_pix == '矢量图':
                self.commit_log.emit(
                    f'生成成功！输出文件位于:\'./output/{time_log.replace(" ", "_").replace(":", "_")}-{self.table_name.replace(".csv", "")}.eps\'')

            elif type_pix == 'PNG':
                self.commit_log.emit(
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
