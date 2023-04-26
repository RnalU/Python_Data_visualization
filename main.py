import sys
import os
import time
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
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        super(MatplotlibDraw, self).__init__()
        plt.rcParams['font.family'] = ['SimHei']  # 更换字体使中文显示正常
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 预声明变量
        self.table_rol = None
        self.table_col = None
        self.data_nums = None
        self.all_datas = []
        self.font_size = None
        self.data = []

        # 创建画布
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axe = self.fig.add_axes
        # 下面这个是画新图后不保留上次的图形，但这个代码似乎有问题报错了，先注释掉
        # self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def receive_values(self, rol, col, data_nums, datalist, fontsize, data):
        """接收主窗口传递的绘图参数"""
        print(rol, col, data_nums, datalist, fontsize)
        # 声明绘图参数
        self.table_rol = rol
        self.table_col = col
        self.data_nums = data_nums
        self.all_datas = datalist
        self.font_size = fontsize
        self.data = data
        self.drawing()

    def drawing(self):
        self.fig.clear()
        self.fig.clf()
        for i in range(self.data_nums):
            # 列表初始化
            number_data = []
            year_data = []

            # 排序好的数据顺序存入相应数组
            for _ in range(len(self.all_datas)):
                year_data.append(int(self.all_datas[_][0]))
                number_data.append(self.all_datas[_][i + 1])

            # 绘制折线图
            # plt.subplot(self.table_rol, self.table_col, (i + 1))
            self.ax = self.fig.add_subplot(self.table_rol, self.table_col, (i + 1))
            self.ax.cla()
            self.ax.plot(year_data, number_data)
            self.ax.scatter(year_data, number_data, s=16)

            x_major_locator = MultipleLocator(2)

            plt.xlim(year_data[0] - 0.5, year_data[-1] + 0.5)

            # # 添加图例和标签
            # ax = plt.gca()
            # 为每个点绘制数据标签
            for point in range(len(year_data)):
                if not number_data[point]:
                    continue
                self.ax.text(year_data[point], number_data[point], '%.1f' % number_data[point],
                        fontdict={'fontsize': self.font_size * 3.8}, ha='center', va='bottom')

                """废弃调整字符位置"""
                # if point != 0 and abs(number_data[point] - number_data[point - 1]) / abs(max(number_data[point], number_data[point - 1])) > 0.2:
                #     ax.text(year_data[point], number_data[point], '%.0f' %number_data[point],
                #             fontdict={'fontsize':font_size * 5}, va='center')
                # else:
                #     ax.text(year_data[point], number_data[point], '%.0f' % number_data[point],
                #             fontdict={'fontsize': font_size * 5}, ha='center', va='center')

            # ax.set_xlabel('年份', fontsize=10)
            if not len(self.data.values[i + 2][0].split(",")[0]) > 12:
                self.ax.set_ylabel(self.data.values[i + 2][0].split(",")[0], fontsize=10)
            self.ax.set_title(self.data.values[i + 2][0].split(",")[0], fontsize=12)

            # 调整横坐标和纵坐标的范围
            # plt.xlim(yearss[0] + 10, yearss[-1] + 10)
            # plt.ylim(datas[0] * 0.5, datas[-1] * 1.5)

            # 调整横坐标的间隔
            self.ax.xaxis.set_major_locator(x_major_locator)
            # self.ax.xticks(rotation=20, fontsize=10)
            self.ax.spines['right'].set_color('None')  # 选中上方的脊梁并替换为空
            self.ax.spines['top'].set_color('None')  # <- now autocompletes

            self.ax.xaxis.set_ticks_position('bottom')  # 设置x轴位置
            self.ax.yaxis.set_ticks_position('left')  # 设置y轴位置
            # ax.spines['bottom'].set_position(('data', yearss[i][0] * 0.95))  # 选中并更改位置
            # ax.spines['left'].set_position(('data', yearss[i][0] - 0.4))

        self.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.fig.canvas.flush_events()  # 画布刷新self.figs.canvas

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
        self.table_aim = None       # 当前表格名称
        self.table_nums = None      # 声明表的个数
        self.num_cols = None        # 预生成图表的列
        self.num_rows = None        # 预生成图表的列
        self.data = None            # 表格数据
        self.font_size = None       # 字体大小
        self.data_nums = None       # 数据个数
        self.all_datas = []       # 处理后的表格数据
        self.year_data = []       # 横轴年份数据
        self.number_data = []     # 纵轴数据
        self.table_sub_datas = []   # 表格条目数据
        self.figure1 = None         # 定义绘图对象

        # 表格读取
        self.read_tables()

        """绘图部分"""


        # 开始作图
        # data = list(range(1000))
        # data2 = list(range(1000, 2000))
        # self.figure_1.axes.plot(data, data2)
        # self.figure_1.axes1.plot(data, data)

    def signal_init(self):
        """信号的相关绑定与声明"""
        self.list_table.itemClicked.connect(self.select_table)
        self.pushButton_drawing.clicked.connect(self.draw_tables)
        self.pushButtont_refresh_read.clicked.connect(self.flushed_tables)

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

    def draw_tables(self):
        """绘制图标"""
        if len(self.all_datas) != 0 and self.font_size and self.num_cols and self.num_rows:
            """调用绘图对象, 绘制图像"""
            try:
                self.vlayout_show_plot.removeWidget(self.figure1)
            except:
                pass

            # 创建绘图对象
            self.figure1 = MatplotlibDraw()

            # 加入垂直布局
            self.vlayout_show_plot.addWidget(self.figure1)

            self.figure1.receive_values(
                rol=self.num_rows,
                col=self.num_cols,
                data_nums=self.data_nums,
                datalist=self.all_datas,
                fontsize=self.font_size,
                data=self.data)
            # try:
            #     self.figure1.drawing()
            #
            # except Exception as e:
            #     self.submit_log_inf(f"绘制错误！系统返回:\n{e}")
            #
            # else:
            #     self.submit_log_inf(f"绘制表格\"{self.table_aim}\"成功!")

        else:
            self.submit_log_inf("表格信息无效！请重新选择", 0)

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
