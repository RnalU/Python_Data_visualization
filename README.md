# Python_Data_visualization
## 介绍

这是一个Python数据可视化的项目。

项目基于 PyQT + Matplotlib 实现读取CSV表格中的数据并展示。

CSV数据源自于国家统计局网站导出的格式。项目的数据也按此格式进行读取

目前项目功能尚不完善。

## 如何部署

项目环境基于 Anaconda Python3.9进行搭建，因此需要安装Anaconda，和一个支持conda语法的terminal 一般Windows的CMD即可满足。

```
// 验证是否Anaconda安装成功
conda info -e	// 输出Anaconda内所有的虚拟环境名称
conda -V        // 输出Anaconda当前版本
```

环境搭建

```
conda create -n "你的虚拟环境名称(py3.9)" python=3.9	
cd /../../"准备克隆的目录路径"
git clone https://github.com/RnalU/Python_Data_visualization.git	// 使用git进行克隆，如果未找到命令，请添加环境变量
															   // 或安装git
cd ./Python_Data_visualization	// 进入目录
conda activate py3.9 		   // 进入你的虚拟环境
pip install -r requirement.txt	// 安装依赖
python main.py				   // 执行main.py
```

