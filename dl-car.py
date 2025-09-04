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

# Thiết lập biểu đồ
fig, ax = plt.subplots()
ax.set_xlim(-5, 10)
ax.set_ylim(-2, 5)
ax.set_xlabel('Vị trí x (m)')
ax.set_ylabel('Trục mô phỏng')
ax.set_title('Mô phỏng chuyển động của ô tô trên trục x')

# Xe là điểm đỏ
car, = ax.plot([], [], 'ro', markersize=12)

# Text hiển thị thông số
v_text = ax.text(-5, 4, '', fontsize=10)
a_text = ax.text(-5, 3.5, '', fontsize=10)
time_text = ax.text(-5, 3, '', fontsize=10)

# Khởi tạo
def init():
    car.set_data([], [])
    return car,

# Cập nhật từng frame
def update(frame):
    t = t_vals[frame]
    x = position(t)
    v = velocity(t)

    car.set_data(x, 0)

    # Xoá vector cũ
    ax.patches.clear()

    # Vẽ vector vận tốc và gia tốc
    ax.add_patch(plt.Arrow(x, 0, v*0.3, 0, width=0.3, color='blue'))
    ax.add_patch(plt.Arrow(x, 0, acceleration*0.3, 0.5, width=0.3, color='green'))

    # Hiển thị thông số
    v_text.set_text(f'v(t) = {v:.2f} m/s')
    a_text.set_text(f'a = {acceleration:.2f} m/s²')
    time_text.set_text(f'Time = {t:.2f} s')

    return car, v_text, a_text, time_text

# Tạo animation
ani = animation.FuncAnimation(fig, update, frames=len(t_vals),
                              init_func=init, blit=True, interval=100)

plt.grid()
plt.show()
