import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# --- 1. Cấu hình Tham số ---
r_A = 0.04  # m
r_B = 0.08  # m
R = r_A + r_B
m_A = 1.0  # kg
m_B = 1.0  # kg
L = 2.0  # m
X_WALL_L = r_A
X_WALL_R = L - r_B

# Trạng thái ban đầu
x_A_0 = 0.5
v_A_0 = 2.0
x_B_0 = L - 0.5
v_B_0 = -3.0

T_MAX = 3.0
dt = 1e-4
T_ANIMATION = 30000  # 30 giây animation

# --- 2. Hàm mô phỏng ---
def simulate_collisions():
    t = 0.0
    x_A, v_A = x_A_0, v_A_0
    x_B, v_B = x_B_0, v_B_0

    trajectory = []
    count_AB = 0
    count_AT = 0
    count_BT = 0
    collisions = []

    trajectory.append((t, x_A, x_B, v_A, v_B))
    dt_save = 0.01
    t_next_save = dt_save

    while t < T_MAX:
        t_collision = T_MAX + 1
        event_type = None

        # --- Tính thời gian đến va chạm tiếp theo ---
        # Va chạm A-B
        if v_A != v_B:
            dist_AB = x_B - x_A
            dt_AB = (dist_AB - R) / (v_A - v_B)
            if dt_AB > 0 and dt_AB < t_collision:
                t_collision = dt_AB
                event_type = "AB"

        # Va chạm A - tường trái
        if v_A < 0:
            dt_AT = (x_A - X_WALL_L) / abs(v_A)
            if dt_AT > 0 and dt_AT < t_collision:
                t_collision = dt_AT
                event_type = "AT"

        # Va chạm B - tường phải
        if v_B > 0:
            dt_BT = (X_WALL_R - x_B) / abs(v_B)
            if dt_BT > 0 and dt_BT < t_collision:
                t_collision = dt_BT
                event_type = "BT"

        # --- Xử lý va chạm ---
        if t + t_collision < t_next_save and t + t_collision < T_MAX:
            # Di chuyển đến thời điểm va chạm
            t += t_collision
            x_A += v_A * t_collision
            x_B += v_B * t_collision

            # Giữ bi không chồng nhau:
            if event_type == "AB":
                x_B = x_A + R  # đặt lại đúng vị trí chạm nhau
                # Công thức va chạm đàn hồi 1D
                v_A_new = (v_A * (m_A - m_B) + 2 * m_B * v_B) / (m_A + m_B)
                v_B_new = (v_B * (m_B - m_A) + 2 * m_A * v_A) / (m_A + m_B)
                v_A, v_B = v_A_new, v_B_new
                count_AB += 1
                collisions.append({"t": t, "type": "A-B", "x_A": x_A, "x_B": x_B})

            elif event_type == "AT":
                x_A = X_WALL_L
                v_A = -v_A
                count_AT += 1
                collisions.append({"t": t, "type": "A-Tường", "x_A": x_A, "x_B": x_B})

            elif event_type == "BT":
                x_B = X_WALL_R
                v_B = -v_B
                count_BT += 1
                collisions.append({"t": t, "type": "B-Tường", "x_A": x_A, "x_B": x_B})

        else:
            # Không có va chạm -> di chuyển bình thường
            dt_move = min(dt_save, T_MAX - t)
            t += dt_move
            x_A += v_A * dt_move
            x_B += v_B * dt_move

            trajectory.append((t, x_A, x_B, v_A, v_B))
            t_next_save = t + dt_save

            if t >= T_MAX:
                break

    return trajectory, collisions, count_AB, count_AT, count_BT


# --- 3. Chạy mô phỏng ---
trajectory, collisions, count_AB, count_AT, count_BT = simulate_collisions()
data = np.array(trajectory)
T_data, X_A_data, X_B_data = data[:, 0], data[:, 1], data[:, 2]

# --- 4. Animation ---
fig, ax = plt.subplots(figsize=(10, 3))
ax.set_xlim(0, L)
ax.set_ylim(-L / 10, L / 10)
ax.set_aspect('equal')
ax.set_yticks([0])
ax.set_xlabel(f"Vị trí (m) - Tổng thời gian mô phỏng: {T_MAX}s")
ax.set_title("Mô phỏng Va chạm Đàn hồi 1D (Không xuyên qua)")

# Tường
ax.axvline(0, color='k', lw=5)
ax.axvline(L, color='k', lw=5)
ax.axhline(0, color='gray', ls='--')

# Bi
ball_A = patches.Circle((X_A_data[0], 0), r_A, fc='blue', ec='black')
ball_B = patches.Circle((X_B_data[0], 0), r_B, fc='red', ec='black')
ax.add_patch(ball_A)
ax.add_patch(ball_B)

time_text = ax.text(0.5, 0.8, '', transform=ax.transAxes, ha='center')

def init():
    ball_A.center = (X_A_data[0], 0)
    ball_B.center = (X_B_data[0], 0)
    time_text.set_text(f'Thời gian: {T_data[0]:.3f} s')
    return ball_A, ball_B, time_text

def update(frame):
    xA, xB, t = X_A_data[frame], X_B_data[frame], T_data[frame]
    ball_A.center = (xA, 0)
    ball_B.center = (xB, 0)
    time_text.set_text(f'Thời gian: {t:.3f} s / {T_MAX:.1f} s')
    return ball_A, ball_B, time_text

interval_ms = T_ANIMATION / len(trajectory)

ani = FuncAnimation(
    fig, update, frames=len(trajectory),
    init_func=init, blit=True,
    interval=interval_ms, repeat=False
)

# 🔹 Cửa sổ không tự đóng
plt.show(block=True)

# --- 5. Kết quả ---
print("\n" + "=" * 50)
print("KẾT QUẢ VA CHẠM TRONG 3 GIÂY")
print("=" * 50)
print(f"A-B: {count_AB} lần, A-tường: {count_AT}, B-tường: {count_BT}")
for col in collisions:
    print(f"{col['type']} tại t = {col['t']:.3f}s | xA={col['x_A']:.3f}, xB={col['x_B']:.3f}")
print("=" * 50)
print(f"Tổng số va chạm: {count_AB + count_AT + count_BT}")
print("=" * 50)

