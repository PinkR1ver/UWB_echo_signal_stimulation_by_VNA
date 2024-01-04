from manim import *
import os
import pandas as pd
import numpy as np


base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, 'data', 'exp06')

def generate_color_gradient(start_color, end_color, num_colors):
    # 将起始色和终点色转换为RGB格式
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (0, 2, 4))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (0, 2, 4))

    # 计算颜色渐变的步长
    r_step = (end_rgb[0] - start_rgb[0]) / (num_colors - 1)
    g_step = (end_rgb[1] - start_rgb[1]) / (num_colors - 1)
    b_step = (end_rgb[2] - start_rgb[2]) / (num_colors - 1)

    # 生成颜色列表
    color_list = []
    for i in range(num_colors):
        r = int(start_rgb[0] + (r_step * i))
        g = int(start_rgb[1] + (g_step * i))
        b = int(start_rgb[2] + (b_step * i))
        color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        color_list.append(color)

    return color_list

class FunctionTransform(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-1, 5],
            axis_config={"color": BLUE},
        )

        # Create a function curve
        func_curve = axes.plot(lambda x: x**2, color=WHITE)

        # Add axes and curve to the scene
        self.play(Create(axes), Create(func_curve))

        # Define the transformation
        def transform(x):
            return x**3

        # Apply the transformation to the curve
        transformed_curve = axes.plot(transform, color=YELLOW)

        # Animate the transformation
        self.play(Transform(func_curve, transformed_curve))
        self.wait(2)
        
        
class UWB_echo_signal_S21_transform_by_distance(Scene):
    def construct(self):
        
        labels = []
        
        y_max = -np.inf
        y_min = np.inf
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                
                if 'S2P' in file and file.split('.')[0].isdigit():
                    
                    label = file.split('.')[0] + 'cm'
                    labels.append(label)
                    
                    s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                    
                    freqency = s_df['Frequency'].values
                    phase = s_df['S21_phase'].values
                    S21_amp = s_df['S21_amp'].values
                    
                    y_max = max(S21_amp.max(), y_max)
                    y_min = min(S21_amp.min(), y_min)
                    
        axe = Axes(
            x_range=[freqency[0] * 0.9, freqency[-1] * 1.1, (freqency[-1] - freqency[0])/10],
            y_range=[y_min * 1.1, y_max * 1.1, (y_max - y_min)/10],
            axis_config={"color": BLUE},
            tips=False,
        )
        
                    
        self.play(Create(axe))
        self.wait(1)
        
        
        test_len = 5
        count = 0
        first_flag = 1
        
        
        for root, dirs, files in os.walk(data_path):
            for file in files:
                
                if 'S2P' in file and file.split('.')[0].isdigit():
                    
                    label = file.split('.')[0] + 'cm'
                    labels.append(label)
                    
                    s_df = pd.read_csv(os.path.join(root, file), skiprows=5, delimiter='	', names=['Frequency', 'S11_amp', 'S11_phase', 'S21_amp', 'S21_phase', 'S12_amp', 'S12_phase', 'S22_amp', 'S22_phase'])
                    
                    freqency = s_df['Frequency'].values
                    phase = s_df['S21_phase'].values
                    S21_amp = s_df['S21_amp'].values
                    
                    
                    if first_flag == 1:
                        curve = axe.plot_line_graph(freqency, S21_amp)
                        self.play(Create(curve))
                        self.wait(1)
                    else:
                        self.play(Transform(curve, axe.plot_line_graph(freqency, S21_amp)))
                        self.wait(1)
                    
                    if test_len == count:
                        break
                    else:
                        count += 1