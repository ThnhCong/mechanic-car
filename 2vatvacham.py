import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# --- Cấu hình Tham số (Giữ nguyên) ---
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
dt = 1e-4  # Bước thời gian tính toán
T_ANIMATION = 15000  # 15000 ms = 15 giây cho 3 giây mô phỏng


# --- 2. Hàm Mô phỏng (Giữ nguyên) ---
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

        # Va chạm A-B
        if v_A != v_B:
            dist_AB = x_B - x_A
            dt_AB = (dist_AB - R) / (v_A - v_B)
            if dt_AB > 0 and dt_AB < t_collision:
                t_collision = dt_AB
                event_type = "AB"

        # Va chạm A-Tường Trái
        if v_A < 0:
            dt_AT = (x_A - X_WALL_L) / abs(v_A)
            if dt_AT > 0 and dt_AT < t_collision:
                t_collision = dt_AT
                event_type = "AT"

        # Va chạm B-Tường Phải
        if v_B > 0:
            dt_BT = (X_WALL_R - x_B) / abs(v_B)
            if dt_BT > 0 and dt_BT < t_collision:
                t_collision = dt_BT
                event_type = "BT"

        # Xử lý sự kiện (va chạm hoặc di chuyển bình thường)
        if t + t_collision < t_next_save and t + t_collision < T_MAX:
            t += t_collision
            x_A += v_A * t_collision
            x_B += v_B * t_collision

            if event_type == "AB":
                v_A, v_B = v_B, v_A
                count_AB += 1
                collisions.append({"t": t, "type": "A-B", "x_A": x_A, "x_B": x_B})
            elif event_type == "AT":
                v_A = -v_A
                x_A = X_WALL_L
                count_AT += 1
                collisions.append({"t": t, "type": "A-Tường", "x_A": x_A, "x_B": x_B})
            elif event_type == "BT":
                v_B = -v_B
                x_B = X_WALL_R
                count_BT += 1
                collisions.append({"t": t, "type": "B-Tường", "x_A": x_A, "x_B": x_B})

        else:
            # Di chuyển bình thường
            dt_move = min(dt_save, T_MAX - t)

            t += dt_move
            x_A += v_A * dt_move
            x_B += v_B * dt_move

            trajectory.append((t, x_A, x_B, v_A, v_B))
            t_next_save = t + dt_save

            if t >= T_MAX:
                break

    return trajectory, collisions, count_AB, count_AT, count_BT


# Chạy mô phỏng
trajectory, collisions, count_AB, count_AT, count_BT = simulate_collisions()

# Chuyển đổi dữ liệu sang mảng numpy
data = np.array(trajectory)
T_data = data[:, 0]
X_A_data = data[:, 1]
X_B_data = data[:, 2]

# --- 3. Tạo Hoạt ảnh với Hình tròn thật ---
fig, ax = plt.subplots(figsize=(10, 3))
ax.set_xlim(0, L)
ax.set_ylim(-L / 10, L / 10)
ax.set_aspect('equal', adjustable='box')
ax.set_yticks([0])
ax.set_xlabel(f"Vị trí (m) - Tổng thời gian mô phỏng: {T_MAX}s")
ax.set_title("Mô phỏng Va chạm Đàn hồi (Tỷ lệ chậm)")

# Vẽ tường
ax.axvline(0, color='k', linestyle='-', linewidth=5)
ax.axvline(L, color='k', linestyle='-', linewidth=5)
ax.axhline(0, color='gray', linestyle='--')

# --- Hai hình tròn thật ---
ball_A = patches.Circle((X_A_data[0], 0), r_A, fc='blue', ec='black')
ball_B = patches.Circle((X_B_data[0], 0), r_B, fc='red', ec='black')
ax.add_patch(ball_A)
ax.add_patch(ball_B)

time_text = ax.text(0.5, 0.8, '', transform=ax.transAxes, ha='center')

def init():
    ball_A.center = (X_A_data[0], 0)
    ball_B.center = (X_B_data[0], 0)
    time_text.set_text(f'Thời gian: {T_data[0]:.3f} s / {T_MAX:.1f} s')
    return ball_A, ball_B, time_text

def update(frame):
    xA = X_A_data[frame]
    xB = X_B_data[frame]
    t = T_data[frame]
    ball_A.center = (xA, 0)
    ball_B.center = (xB, 0)
    time_text.set_text(f'Thời gian: {t:.3f} s / {T_MAX:.1f} s')
    return ball_A, ball_B, time_text

interval_ms = T_ANIMATION / len(trajectory)
ani = FuncAnimation(fig, update, frames=len(trajectory),
                    init_func=init, blit=True, interval=interval_ms, repeat=False)

plt.show(block=True)


def update(frame):
    t_current = T_data[frame]
    x_A_current = X_A_data[frame]
    x_B_current = X_B_data[frame]

    ball_A.set_data(x_A_current, 0)
    ball_B.set_data(x_B_current, 0)

    time_text.set_text(f'Thời gian: {t_current:.3f} s / {T_MAX:.1f} s')

    return ball_A, ball_B, time_text


interval_ms = T_ANIMATION / len(trajectory)

ani = FuncAnimation(fig, update, frames=len(trajectory),
                    init_func=init, blit=True, interval=interval_ms, repeat=False)

# *** ĐIỀU CHỈNH 2: Cửa sổ không tắt khi kết thúc ***
plt.show(block=True)

# --- 4. In Kết quả Thời gian Va chạm (Giữ nguyên) ---

print("\n" + "=" * 50)
print("KẾT QUẢ TÍNH TOÁN CÁC SỰ KIỆN VA CHẠM (TRONG 3s)")
print("=" * 50)

print(f"\n1. Tóm tắt Va chạm giữa A và B: {count_AB} lần")
print("---------------------------------------")
count_ab = 0
for i, col in enumerate(collisions):
    if col['type'] == 'A-B':
        count_ab += 1
        print(
            f"Lần {count_ab}: Thời điểm t = {col['t']:.3f} s | Vị trí A: {col['x_A']:.3f} m, Vị trí B: {col['x_B']:.3f} m")

print(f"\n2. Tóm tắt Va chạm với Tường (A: {count_AT} lần, B: {count_BT} lần)")
print("---------------------------------------")
for col in collisions:
    if col['type'] != 'A-B':
        print(
            f"{col['type']}: Thời điểm t = {col['t']:.3f} s | Vị trí A: {col['x_A']:.3f} m, Vị trí B: {col['x_B']:.3f} m")

print("\n" + "=" * 50)
print(f"TỔNG SỐ VA CHẠM: {count_AB + count_AT + count_BT} lần")
print("=" * 50)
