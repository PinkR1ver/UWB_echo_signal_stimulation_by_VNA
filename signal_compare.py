import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from ipywidgets import interact



if __name__ == '__main__':
    
    # 生成一些示例数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # 定义一个函数，用于更新图表
    def update_plot(show_sin, show_cos):
        lines[0].set_visible(show_sin)
        lines[1].set_visible(show_cos)
        plt.draw()

    # 创建初始图表
    fig, ax = plt.subplots()
    lines, = ax.plot(x, y1, label='sin')
    lines_cos, = ax.plot(x, y2, label='cos')
    ax.set_ylim(-1.5, 1.5)
    ax.legend()

    # 使用 ipywidgets 中的 interact 函数创建交互部件
    interact(update_plot, show_sin=True, show_cos=True)

    # 显示图表
    plt.show()