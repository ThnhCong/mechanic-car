import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# --- 1. Tham số bài toán ---
r_A = 0.04  # m
r_B = 0.08  # m
R = r_A + r_B
m_A = 1.0
m_B = 1.0
L = 2.0  # m

# Vị trí tường (theo tâm bi)
X_WALL_L = r_A
X_WALL_R = L - r_B

# --- 2. Trạng thái ban đầu ---
x_A = X_WALL_L + 0.5   # 0.54 m
x_B = X_WALL_R - 0.5   # 1.42 m
v_A = 2.0               # m/s → phải
v_B = 3.0               # m/s → phải

# --- 3. Cấu hình mô phỏng ---
FPS = 30          # giảm FPS -> chuyển động chậm hơn
dt = 1 / FPS / 2  # giảm bước thời gian -> mượt hơn
T_MAX = 3.0

# --- 4. Dữ liệu để vẽ ---
positions_A = []
positions_B = []
times = []
velocities_A = []
velocities_B = []
collisions_AB = []
collisions_AT = 0
collisions_BT = 0

# --- 5. Hàm xử lý va chạm ---
def resolve_collision(v1, v2, m1, m2):
    """Va chạm đàn hồi 1D"""
    v1_new = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
    v2_new = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)
    return v1_new, v2_new

# --- 6. Mô phỏng ---
t = 0.0
while t <= T_MAX:
    x_A += v_A * dt
    x_B += v_B * dt

    # Va chạm tường
    if x_A - r_A <= 0:
        x_A = r_A
        v_A = -v_A
        collisions_AT += 1
    if x_B + r_B >= L:
        x_B = L - r_B
        v_B = -v_B
        collisions_BT += 1

    # Va chạm giữa hai bi
    if abs(x_A - x_B) <= R and (v_A - v_B) * (x_A - x_B) < 0:
        v_A, v_B = resolve_collision(v_A, v_B, m_A, m_B)
        overlap = R - abs(x_A - x_B)
        if x_A < x_B:
            x_A -= overlap / 2
            x_B += overlap / 2
        else:
            x_A += overlap / 2
            x_B -= overlap / 2
        collisions_AB.append((t, (x_A + x_B) / 2))

    positions_A.append(x_A)
    positions_B.append(x_B)
    velocities_A.append(v_A)
    velocities_B.append(v_B)
    times.append(t)
    t += dt

# --- 7. Kết quả ---
print("\n================ KẾT QUẢ ==================")
if len(collisions_AB) >= 1:
    print(f"1️Lần chạm đầu tiên: t₁ = {collisions_AB[0][0]:.4f} s, x ≈ {collisions_AB[0][1]:.4f} m")
if len(collisions_AB) >= 2:
    print(f"2️Lần chạm thứ hai: t₂ = {collisions_AB[1][0]:.4f} s, x ≈ {collisions_AB[1][1]:.4f} m")
print(f"\n3️⃣ Trong 3s:")
print(f"   Bi A chạm tường {collisions_AT} lần.")
print(f"   Bi B chạm tường {collisions_BT} lần.")
print(f"   Hai bi chạm nhau {len(collisions_AB)} lần.")
print("============================================")

# --- 8. Animation ---
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.set_xlim(0, L)
ax.set_ylim(-0.25, 0.25)
ax.set_aspect('equal')

ax.axhline(0, color='gray', lw=1)
ax.set_xlabel("Vị trí (m)")
ax.set_yticks([])
ax.set_xticks(np.arange(0, L + 0.1, 0.2))
ax.grid(True, axis='x', linestyle='--', alpha=0.4)

ax.axvline(0, color='k', lw=4)
ax.axvline(L, color='k', lw=4)

ball_A = patches.Circle((positions_A[0], 0), r_A, fc='red', ec='black')
ball_B = patches.Circle((positions_B[0], 0), r_B, fc='blue', ec='black')
ax.add_patch(ball_A)
ax.add_patch(ball_B)

time_text = ax.text(0.5, 0.9, '', transform=ax.transAxes, ha='center')
vA_text = ax.text(0, 0.12, '', color='red', ha='center', fontsize=9)
vB_text = ax.text(0, 0.12, '', color='blue', ha='center', fontsize=9)

def update(frame):
    ball_A.center = (positions_A[frame], 0)
    ball_B.center = (positions_B[frame], 0)
    vA_text.set_position((positions_A[frame], 0.12))
    vB_text.set_position((positions_B[frame], 0.12))
    vA_text.set_text(f"vA = {velocities_A[frame]:.2f} m/s")
    vB_text.set_text(f"vB = {velocities_B[frame]:.2f} m/s")
    time_text.set_text(f"t = {times[frame]:.2f} s")
    return ball_A, ball_B, time_text, vA_text, vB_text

ani = FuncAnimation(
    fig, update, frames=len(times),
    interval=120,  # 👈 tăng lên để hiển thị chậm hơn
    blit=True, repeat=False
)

plt.show(block=True)
