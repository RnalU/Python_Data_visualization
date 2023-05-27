import shutil
import sys
import os
import time
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem

from UI.form import Ui_Form
from matplotlibClass import MatplotlibDraw


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
        self.fig_size = None  # 画布大小
        self.data_nums = None  # 数据个数
        self.all_datas = []  # 处理后的表格数据
        self.year_data = []  # 横轴年份数据
        self.number_data = []  # 纵轴数据
        self.table_sub_datas = []  # 表格条目数据
        self.figure1 = None  # 定义绘图对象
        self.aim_colors = ['蓝色', '青色', '红色', '品红', '紫色', '黄色', '随机颜色']  # 定义颜色
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
        self.figure1.commit_log.connect(self.submit_log_inf)

    def signal_init(self):
        """信号的相关绑定与声明"""
        self.list_table.itemClicked.connect(self.select_table)
        self.pushButton_drawing.clicked.connect(lambda: self.draw_tables(False))
        self.pushButtont_refresh_read.clicked.connect(self.flushed_tables)
        self.pushButton_save_img.clicked.connect(self.save_img)
        self.pushButton_subplot_change.clicked.connect(self.subplot_change)
        self.pushButton_close_table.clicked.connect(self.clear_table)
        self.pushButton_commit_table.clicked.connect(self.change_table)

    def windows_init(self):
        pass

    def get_table(self):
        """获取选择的表格"""
        # 先清除表格
        self.tableWidget_table.clear()
        col = -1
        for line_list in self.data.values:
            line: str = line_list[0]
            if col == len(line.split(',')):
                break
            col = len(line.split(','))  # 获取行数
        row = len(self.data.values)  # 获取列数
        self.label_table_show_inf.setText(f"当前表格:{self.table_aim}   行:{row}   列{col}")
        self.label_table_show_inf.adjustSize()
        self.tableWidget_table.setColumnCount(col)
        self.tableWidget_table.setRowCount(row)

        max_col_len = 0
        # 写入表格数据
        for row, _line in enumerate(self.data.values):
            line = _line[0].split(',')

            # 得到行数据的最大值
            if len(line[0]) > max_col_len:
                max_col_len = len(line[0])
                if max_col_len > 20:
                    max_col_len = 20

            for col, line_item in enumerate(line):
                temp = QTableWidgetItem(line_item)
                if line_item is None:
                    temp = QTableWidgetItem("None")
                    self.tableWidget_table.setItem(row, col, temp)
                else:
                    self.tableWidget_table.setItem(row, col, temp)

                # 调整行的大小
                self.tableWidget_table.setColumnWidth(0, max_col_len * 18)

                # 设置水平竖直表头是否显示
                self.tableWidget_table.horizontalHeader().setVisible(True)
                self.tableWidget_table.verticalHeader().setVisible(False)

    def clear_table(self):
        """清空tableWidget区域"""
        self.tableWidget_table.clear()
        self.label_table_show_inf.setText("当前表格:None")

    def change_table(self):
        """读取当前表格的数据并重新写入到文件"""
        if self.label_table_show_inf.text().split(':')[1] != "None" and self.label_table_show_inf.text().split(':')[1].count(self.table_aim):
            # 读取tableWidget表格数据
            lines_str = ["数据库：年度数据\n"]

            # 得到行
            rows = len(self.data.values)
            for row in range(rows):
                line_item_list = []
                for col in range(len(self.data.values[row][0].split(","))):
                    line_item = self.tableWidget_table.item(row, col).text()
                    line_item_list.append(line_item)
                lines_str.append(",".join(line_item_list) + '\n')
            # 尝试修改表格, 先进行备份(检测是否存在bak文件夹, 入果不存在则创建)
            if os.path.exists("bak"):
                pass
            else:
                os.mkdir("./bak")

            if os.path.exists("bak"):
                try:
                    # 记录时间
                    time_log = time.strftime("%Y-%m-%d %H:%M:%S")
                    shutil.copy(f"./table/{self.table_aim}",
                                f"./bak/{time_log.replace(' ', '-').replace(':', '-')}-{self.table_aim}.bak")
                except Exception as e:
                    self.submit_log_inf(f"表格文件{self.table_aim}备份失败！系统返回{e}")

                else:
                    self.submit_log_inf(
                        f"文件{self.table_aim}备份成功, 已保存在./bak/{time_log.replace(' ', '-').replace(':', '-')}-{self.table_aim}.bak")
                # 开始重写表格文件
                current_table = open(f'./table/{self.table_aim}', 'w', encoding="GBK")

                for line_idx in range(rows + 1):  # 因为pandas读取CSV表格会自动忽略第一列，因此需要自动将第一行表格内容补全并循环次数多一次
                    current_table.write(lines_str[line_idx])
                current_table.close()

            else:
                self.submit_log_inf("bak备份文件夹创建失败，请检查程序目录并自行创建", 0)

        else:
            self.submit_log_inf("请选择一个表格", 0)

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
        print(self.data.values)
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
        self.get_table()

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

            except Exception as e:
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
            self.submit_log_inf(f"请先选中表格条目, {e}", 0)

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
