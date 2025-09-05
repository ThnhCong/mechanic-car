from vpython import *

# Nhập thời gian
t0 = float(input("Nhập thời gian bắt đầu t0 (s): "))
T  = float(input("Nhập thời gian kết thúc T (s): "))

# setup canvas
scene = canvas(title='1D Accelerated Motion Coding Activity',
               width=800, height=200, center=vec(250,20,0))
scene.background = color.white
###############
ground = curve(pos=[vec(-5000,-200,0), vec(5000,-200,0)], color=color.black, radius=10)

# objects (ảnh xe, cần link trực tiếp)
car = box(pos=vec(0,0,0), size=vec(1000,500,100),
          texture="car.png")

# initial conditions
a = 2          # gia tốc
v = 20         # vận tốc ban đầu tại t=0
dt = 0.02
t = t0         # bắt đầu từ t0

# Tính toán trước tại t0
x_t0 = x0 = v*t0 + 0.5*a*(t0**2)
v_t0 = v + a*t0
car.pos.x = x_t0

# Tính toán trước tại T
x_T = v*T + 0.5*a*(T**2)
v_T = v + a*T

displacement_total = x_T - x_t0
distance_total = abs(displacement_total)
dt_total = T - t0

avg_velocity = displacement_total/dt_total if dt_total>0 else 0
avg_speed = distance_total/dt_total if dt_total>0 else 0

print("\n--- Kết quả tính toán ---")
print(f"Độ dời Δx từ t0={t0:.2f}s đến T={T:.2f}s: {displacement_total:.2f} m")
print(f"Vận tốc trung bình: {avg_velocity:.2f} m/s")
print(f"Tốc độ trung bình: {avg_speed:.2f} m/s")
print("---------------------------\n")

# graphs
graph1 = graph(width=800, height=200, xtitle='time (s)', ytitle='position (m)')
graph2 = graph(width=800, height=200, xtitle='time (s)', ytitle='velocity (m/s)')
graph3 = graph(width=800, height=200, xtitle='time (s)', ytitle='acceleration (m/s²)')

f1 = gcurve(graph=graph1, color=color.blue)   # position curve
f2 = gcurve(graph=graph2, color=color.blue)   # velocity curve
f3 = gcurve(graph=graph3, color=color.red)    # acceleration curve

# simulation loop
while t <= T:
    rate(50)
    x = v*t + 0.5*a*t**2   # phương trình chuyển động
    v_inst = v + a*t

    car.pos.x = x

    # plotting
    f1.plot(t, x)
    f2.plot(t, v_inst)
    f3.plot(t, a)

    t += dt
