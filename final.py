from vpython import *

# scene setup
scene = canvas(title='1D Accelerated Motion with OXY Coordinate',
               width=900, height=400, center=vec(0,0,0),
               background=color.white)

# coordinate axes
x_axis = arrow(pos=vec(-50,0,0), axis=vec(300,0,0), shaftwidth=3, color=color.black)
y_axis = arrow(pos=vec(0,-50,0), axis=vec(0,300,0), shaftwidth=3, color=color.black)

# axis labels
label(pos=vec(305,0,0), text="X", height=10, box=False, color=color.black)
label(pos=vec(0,310,0), text="Y", height=10, box=False, color=color.black)
label(pos=vec(-15,-15,0), text="O", height=10, box=False, color=color.black)
carx = "https://static.vecteezy.com/system/resources/previews/008/957/252/non_2x/flat-red-car-icon-clipart-in-cartoon-graphic-illustration-design-vector.jpg"
# car object

car = box(pos=vec(0,25,0), size=vec(90,60,0.01),texture=carx)
# time setup
t = 0
dt = 0.01


# graphs
graph1 = graph(width=800, height=200, xtitle='time (s)', ytitle='position (m)')
graph2 = graph(width=800, height=200, xtitle='time (s)', ytitle='velocity (m/s)')
graph3 = graph(width=800, height=200, xtitle='time (s)', ytitle='acceleration (m/s²)')
# curves
f1 = gcurve(graph=graph1, color=color.blue)   # position
f2 = gcurve(graph=graph2, color=color.green)  # velocity
f3 = gcurve(graph=graph3, color=color.red)    # acceleration

# motion equations
def x_func(t): return -4*t + 2*t**2
def v_func(t): return -4 + 4*t
def a_func(t): return 4

# animate
t_set = 20
while t <= t_set:
    if abs(t - t_set) < dt/2:
        print(f"position: {x_func(t):.2f}m, v = {v_func(t):.2f}m/s, a = {a_func(t):.2f} m/s^2")
    rate(200)

    # update car position
    car.pos.x = x_func(t)   # move along X-axis

    # plot graphs
    f1.plot(t, x_func(t))
    f2.plot(t, v_func(t))
    f3.plot(t, a_func(t))

    t += dt
#print(f"position: {x_func(1):.2f}m, v = {v_func(1):.2f}m/s, a = {a_func(1):.2f} m/s^2")


