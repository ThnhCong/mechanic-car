import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


# --- Setup figure ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

axis_length = 20
tick_interval = 5

# --- Vẽ hệ trục ---
ax.quiver(0, 0, 0, axis_length, 0, 0, color="r", arrow_length_ratio=0.05)
ax.quiver(0, 0, 0, 0, axis_length, 0, color="g", arrow_length_ratio=0.05)
ax.quiver(0, 0, 0, 0, 0, axis_length, color="b", arrow_length_ratio=0.05)

# Nhãn trục
ax.text(axis_length+1, 0, 0, "x", color="r")
ax.text(0, axis_length+1, 0, "y", color="g")
ax.text(0, 0, axis_length+1, "z", color="b")

# Ticks
ax.set_xticks(np.arange(0, axis_length+1, tick_interval))
ax.set_yticks(np.arange(0, axis_length+1, tick_interval))
ax.set_zticks(np.arange(-axis_length, axis_length+1, tick_interval))

# --- Hàm vị trí ---
def position(t):
    x = 9.6 * t
    y = 8.85
    z = -t**2
    return np.array([x, y, z])

# --- Hàm vận tốc ---
def velocity_func(t):
    return np.array([9.6, 0, -2*t])

# --- Tạo quả cầu ---
def create_sphere(center, r=0.5, resolution=20):
    u, v = np.mgrid[0:2*np.pi:resolution*1j, 0:np.pi:resolution*1j]
    x = r * np.cos(u) * np.sin(v) + center[0]
    y = r * np.sin(u) * np.sin(v) + center[1]
    z = r * np.cos(v) + center[2]
    return x, y, z

# Vẽ quả cầu ban đầu
pos0 = position(0)
X, Y, Z = create_sphere(pos0, r=0.5)
ball = ax.plot_surface(X, Y, Z, color="m", shade=True)

# Quỹ đạo
trail, = ax.plot([], [], [], '-', color="m", linewidth=1)

# Vector vận tốc - Khởi tạo là None
v_arrow = None

# Giới hạn khung nhìn
ax.set_xlim(0, axis_length)
ax.set_ylim(0, axis_length)
ax.set_zlim(-axis_length, axis_length)

trail_points = []

# --- Hàm update ---
def update_plot(frame):
    global v_arrow, trail_points, ball

    t = frame * 0.05
    # Reset quỹ đạo khi frame đạt 200 (cuối chu kỳ)
    if frame == 0:
        trail_points = []

    pos = position(t)
    vel = velocity_func(t)

    # Xóa quả cầu cũ
    ball.remove()
    # Vẽ quả cầu mới tại vị trí pos
    X, Y, Z = create_sphere(pos, r=0.5)
    ball = ax.plot_surface(X, Y, Z, color="m", shade=True)

    # Quỹ đạo
    trail_points.append(pos)
    pts = np.array(trail_points)
    # Xóa quỹ đạo cũ trước khi vẽ quỹ đạo mới
    trail.set_data([], [])
    trail.set_3d_properties([])
    trail.set_data(pts[:, 0], pts[:, 1])
    trail.set_3d_properties(pts[:, 2])

    # Arrow: xóa cái cũ rồi vẽ mới
    if v_arrow is not None:
        v_arrow.remove()
    v_arrow = ax.quiver(pos[0], pos[1], pos[2],
                        vel[0]*0.1, vel[1]*0.1, vel[2]*0.1,
                        color="b", arrow_length_ratio=0.2)

    return ball, trail, v_arrow

# --- Animation ---
ani = FuncAnimation(fig, update_plot, frames=200, interval=50, blit=False)
plt.show()

