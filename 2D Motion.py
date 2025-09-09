#code moi day nhe

from vpython import *

# scene setup
scene = canvas(title='2D Accelerated Motion',
               width=900, height=400, center=vec(0,0,0),
               background=color.white)
# Change camera view (so Z points up)
scene.forward = vector(-1,-5,-5)   # tilt the camera
scene.up = vector(0,0,10)           # make Z-axis "up" in the view

# coordinate axes
arrow(pos=vector(0,0,0), axis=vector(150,0,0), color=color.red, shaftwidth=2)   # X-axis
arrow(pos=vector(0,0,0), axis=vector(0,150,0), color=color.green, shaftwidth=2) # Y-axis
arrow(pos=vector(0,0,0), axis=vector(0,0,150), color=color.blue, shaftwidth=2)

# axis labels
label(pos=vec(155,0,0), text="X", height=12, box=False, color=color.red)
label(pos=vec(0,155,0), text="Y", height=12, box=False, color=color.green)
label(pos=vec(0,0,155), text="Z", height=12, box=False, color=color.blue)
label(pos=vec(-10,-10,-10), text="O", height=10, box=False, color=color.black)
#carx = "https://static.vecteezy.com/system/resources/previews/008/957/252/non_2x/flat-red-car-icon-clipart-in-cartoon-graphic-illustration-design-vector.jpg"
# car object

#car = box(pos=vec(0,0,0), size=vec(90,60,10),texture=carx)
car = box(pos=vec(0,0,0), size=vec(10,6,4), color=color.orange, make_trail=True)

# time setup
t = 0
dt = 0.02

# graphs
graph1 = graph(width=800, height=200, xtitle='time (s)', ytitle='position (m)')
graph2 = graph(width=800, height=200, xtitle='time (s)', ytitle='velocity (m/s)')
graph3 = graph(width=800, height=200, xtitle='time (s)', ytitle='acceleration (m/s²)')
# curves
f1 = gcurve(graph=graph1, color=color.blue)   # position
f2 = gcurve(graph=graph2, color=color.green)  # velocity
f3 = gcurve(graph=graph3, color=color.red)    # acceleration

# motion equations
def x_func(t): return -t**2 + 9.6*t + 8.85
def v_func(t): return -2*t + 9.6
def a_func(t): return -2
def xf(t): return 9.6*t
def yf(t): return 8.85
def zf(t): return -t**2


# animate
t_set = 10
while t <= t_set:
    #if abs(t - t_set) < dt/2:
        #print(f"at t = {t}, position: {x_func(t):.2f}m, v = {v_func(t):.2f}m/s, a = {a_func(t):.2f} m/s^2")
    rate(150)

    # update car position
    car.pos = vec(xf(t), yf(t), zf(t))
    # plot graphs
    f1.plot(t, x_func(t))
    f2.plot(t, v_func(t))
    f3.plot(t, a_func(t))

    t += dt
#print(f"position: {x_func(1):.2f}m, v = {v_func(1):.2f}m/s, a = {a_func(1):.2f} m/s^2")
print(f"at t = {t_set}, position: {x_func(t_set):.2f}m, v = {v_func(t_set):.2f}m/s, a = {a_func(t_set):.2f} m/s^2, xf = {xf(t_set)}, yf = {yf(t_set)}, zf = {zf(t_set)} ")


