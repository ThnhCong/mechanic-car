#ae lam bai vui ve
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Hàm vị trí
def position(t):
    return -4*t + 2*t**2

# Vận tốc
def velocity(t):
    return -4 + 4*t

# Gia tốc (hằng số)
acceleration = 4

# Tạo các giá trị thời gian
t_vals = np.linspace(0, 3.5, 100)
x_vals = position(t_vals)


plt.show()
