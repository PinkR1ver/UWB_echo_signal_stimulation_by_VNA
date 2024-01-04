import numpy as np
import pandas as pd
import os
import math
import matplotlib.pyplot as plt


labels = [5, 8, 16, 20, 24, 28, 32, 40, 45, 55, 60]
left_point = [(5712212120, 179.5), (5712212120, 179.7), (5712212120, 179.0), (5712212120, 179.8), (5712212120, 179.5), (5712212120, 179.1), (5712212120, 178.8), (5712212120, 180), (5712212120, 179.4), (5712212120, 178.4), (5712212120, 178.3)]
right_point = [(6222454270, -179.4), (6151605360, -179.7), (6083356410, -179.3), (6062556730, -179.5), (6028757250, -179.0), (5982607960, -180.0), (5961808280, -178.7), (5930608760, -179.9), (5894859310, -179.9), (5874709620, -178.1), (5871459670, -178.6)]


if __name__ == '__main__':
    
    # print(len(labels), len(left_point), len(right_point))
    slope = []
    
    for label, left, right in zip(labels, left_point, right_point):
        
        # calculate the slope
        slope.append(-(right[1] - left[1]) / (right[0] - left[0]))
        # print('{}cm Slope: '.format(label), slope)
        
        
    # fitting labels and slope
    labels = np.array(labels)
    slope = np.array(slope)
    coefficient = np.polyfit(slope, labels, 1)
    polynomial = np.poly1d(coefficient)
    
    x_range = np.linspace(min(slope), max(slope), 100)
    y_fit = polynomial(x_range)
    
    plt.scatter(slope, labels, color='blue', label='Data')
    plt.plot(x_range, y_fit, color='red', label='Fitting')
    
    # 添加标题和标签
    plt.title('Linear Fit Example')
    plt.xlabel('Slope')
    plt.ylabel('Distance(cm)')

    # 添加图例
    plt.legend()

    # 显示图形
    plt.show()
    