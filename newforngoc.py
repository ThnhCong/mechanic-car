from vpython import *

# setup canvas
scene = canvas(title='1D Accelerated Motion Coding Activity', width=800, height=150, center=vec(250,20,0))
scene.background = color.white

# objects
car = box(pos=vec(0,0,5), size=vec(20,10,0.1),
          texture="https://www.google.com/url?sa=i&url=https%3A%2F%2Fhelloartsy.com%2Fdraw-f1-car%2F&psig=AOvVaw0-u7NQaKX8VpO5en0VH0aH&ust=1757079339750000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCJirreGcv48DFQAAAAAdAAAAABAg")
# initial conditions
x0 = car.pos.x
v = 20
a = 2
t = 0
dt = 0.02

# graphs
graph1 = graph(width=800, height=200, xtitle='time (s)', ytitle='position (m)')
graph2 = graph(width=800, height=200, xtitle='time (s)', ytitle='velocity (m/s)')
graph3 = graph(width=800, height=200, xtitle='time (s)', ytitle='acceleration (m/s²)')  # NEW

f1 = gcurve(graph=graph1, color=color.blue)   # position curve
f2 = gcurve(graph=graph2, color=color.blue)   # velocity curve
f3 = gcurve(graph=graph3, color=color.red)    # acceleration curve (NEW)

# simulation loop
while True:
    rate(50)
    v = v + a*dt
    car.pos.x = car.pos.x + v*dt

    # plotting
    f1.plot(t, car.pos.x)
    f2.plot(t, v)
    f3.plot(t, a)   # acceleration is constant, so this will be a straight line

    t += dt
