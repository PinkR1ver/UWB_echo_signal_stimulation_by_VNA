import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# 生成示例信号
t = np.linspace(0, 1, 1000, endpoint=False)
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)

# 计算 Hilbert 变换
analytic_signal = hilbert(signal)

# 提取包络
amplitude_envelope = np.abs(analytic_signal)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(t, signal, label='Original Signal')
plt.plot(t, amplitude_envelope, label='Amplitude Envelope', linewidth=2)
plt.title('Signal and its Hilbert Transform')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
