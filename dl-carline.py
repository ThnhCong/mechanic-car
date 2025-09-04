from vpython import *
#toi buon ngu quaaaaaa

# ========== Cấu hình canvas ==========
scene = canvas(title="Mô phỏng chuyển động 1D: x(t) = -4t + 2t²",
               width=900, height=300, center=vec(0,0,0), background=color.white)

# Nhập thời gian
t0 = float(input("Nhập thời gian bắt đầu t0 (s): "))
T = float(input("Nhập thời gian kết thúc T (s): "))

# Tham số mô phỏng
dt = 0.02
t = t0

# Công thức
def x_func(t): return -4*t + 2*t**2
def v_func(t): return -4 + 4*t
def a_func(t): return 4

# Tính toán ban đầu
x_t0 = x_func(t0)
x_T = x_func(T)
displacement_total = x_T - x_t0
distance_total = abs(displacement_total)
dt_total = T - t0
avg_velocity = displacement_total/dt_total if dt_total > 0 else 0
avg_speed = distance_total/dt_total if dt_total > 0 else 0

print("\n--- Kết quả tính toán ---")
print(f"Độ dời Δx: {displacement_total:.2f} m")
print(f"Vận tốc TB: {avg_velocity:.2f} m/s")
print(f"Tốc độ TB: {avg_speed:.2f} m/s")
print("-------------------------\n")

# ========== Tạo xe ==========
car = box(pos=vec(x_t0*10,0,0), size=vec(10,5,4), color=color.blue)  # scale 10px/m
wheel1 = cylinder(pos=car.pos+vec(-4,-3,2), axis=vec(0,0,1), radius=2, color=color.black)
wheel2 = cylinder(pos=car.pos+vec(4,-3,2), axis=vec(0,0,1), radius=2, color=color.black)

# ========== Đồ thị ==========
times = [t0 + i*dt for i in range(int((T-t0)/dt)+1)]
x_vals = [x_func(tt) for tt in times]
v_vals = [v_func(tt) for tt in times]
a_vals = [a_func(tt) for tt in times]

graph_pos = graph(title="Đồ thị x(t)", width=900, height=250, xtitle="t (s)", ytitle="x (m)")
f_pos = gcurve(graph=graph_pos, color=color.blue)
for tt, xx in zip(times, x_vals):
    f_pos.plot(tt, xx)

graph_vel = graph(title="Đồ thị v(t)", width=900, height=250, xtitle="t (s)", ytitle="v (m/s)")
f_vel = gcurve(graph=graph_vel, color=color.green)
for tt, vv in zip(times, v_vals):
    f_vel.plot(tt, vv)

graph_acc = graph(title="Đồ thị a(t)", width=900, height=250, xtitle="t (s)", ytitle="a (m/s²)")
f_acc = gcurve(graph=graph_acc, color=color.red)
for tt, aa in zip(times, a_vals):
    f_acc.plot(tt, aa)

# Label hiển thị thông tin
info = label(pos=vec(0,8,0), text="", box=False, height=16, color=color.black)

# ========== Vòng lặp mô phỏng ==========
last_x = x_t0
distance_traveled = 0

while t <= T:
    rate(50)

    # Tính giá trị tại thời điểm t
    x = x_func(t)
    v = v_func(t)
    a = a_func(t)

    dx = (x - last_x) * 10
    car.pos.x += dx
    wheel1.pos.x += dx
    wheel2.pos.x += dx
    wheel1.rotate(angle=-dx / 2, axis=vec(0, 0, 1))  # quay bánh
    wheel2.rotate(angle=-dx / 2, axis=vec(0, 0, 1))
    # Cập nhật quãng đường
    distance_traveled += abs(x - last_x)
    last_x = x

    # Hiển thị thông số
    info.text = f"t = {t:.2f} s | x = {x:.2f} m | v = {v:.2f} m/s | a = {a:.2f} m/s² | s = {distance_traveled:.2f} m"

    t += dt

