from vpython import *

scene = canvas(title='1D Motion Model',
               width=1200, height=400, center=vec(0,0,0),
               background=color.white)

scale = 30   # 1 m = 50 px

    
# motion equations (x in meters)
def x_func(t): return -4*t + 2*t**2
def v_func(t): return -4 + 4*t
def a_func(t): return 4


# time
t, dt, t_set = 0, 0.01, 3

# ruler line
x_min, x_max = -x_func(t_set), x_func(t_set)
line = curve(pos=[vec(x_min*scale, 0, 0), vec(x_max*scale, 0, 0)], color=color.black)

# ticks + labels
for x in range(x_min, x_max+1, 1):   
    curve(pos=[vec(x*scale, -3, 0), vec(x*scale, 3, 0)], color=color.black)
    label(pos=vec(x*scale, -15, 0), text=str(x), height=12, box=False, color=color.black)


# car
carx = "https://static.vecteezy.com/system/resources/previews/008/957/252/non_2x/flat-red-car-icon-clipart-in-cartoon-graphic-illustration-design-vector.jpg"
car = box(pos=vec(0, 15, 0), size=vec(40, 20, 0.01), texture=carx)



# graph
graph1 = graph(width=800, height=200, xtitle='time (s)', ytitle='position (m)')

curve1 = gcurve(graph=graph1, color=color.blue)

# sample the function over time
N = 200   # number of sample points
for i in range(N+1):
    tt = i * t_set / N    # go from 0 → t_set
    curve1.plot(tt, x_func(tt))


# curves
f1 = gcurve(graph=graph1, color=color.blue)   # position


#dot
dot = gdots(color=color.red)
    
# info label (fixed position above the ruler)
info = label(pos=vec(0,50,0), text="", height=16, box=False, color=color.black)

while t <= t_set:
    rate(50)

    # update car position 
    car.pos.x = x_func(t) * scale
    
    # update label text
    info.text = f"t={t:.2f} s | x={x_func(t):.2f} m | v={v_func(t):.2f} m/s | a={a_func(t):.2f} m/s²"
    
    f1.plot(t, x_func(t))
    #f2.plot(t, v_func(t))
    #f3.plot(t, a_func(t))

    dot.delete()                 # clear old dot
    dot = gdots(color=color.red) # create a fresh one
    dot.plot(t, x_func(t))
    t += dt

