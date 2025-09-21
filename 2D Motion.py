#{INSTRUCTION}!!!
#use right click to rotate the coordinates
#scroll to zoom in or out











from vpython import *
scale = 50
scene = canvas(title="3D Coordinate System with Ticks",
               width=1000, height=600, background=color.white)

scene.forward = vector(-1, -2, -0.5)   # tilt to see all axes
scene.up = vector(0, 0, 1)             # keep z axis pointing up



#scene.autoscale = False


axis_length = 20   # length of each axis
tick_interval = 5 # spacing between ticks
tick_size = 0.1   # half length of tick mark

# Draw axes
x_axis = arrow(pos=vec(0,0,0), axis=vec(axis_length,0,0), color=color.red, shaftwidth=0.1)
y_axis = arrow(pos=vec(0,0,0), axis=vec(0,axis_length,0), color=color.green, shaftwidth=0.1)
z_axis = arrow(pos=vec(0,0,0), axis=vec(0,0,axis_length), color=color.blue, shaftwidth=0.1)

# Function to draw ticks and labels
def draw_ticks(axis_vec, axis_label, color_axis):
    for i in range(1, axis_length+1, tick_interval):
        pos = i*axis_vec

        # Draw tick perpendicular to axis
        if axis_vec.x: # x-axis
            curve(pos=[pos+vec(0,-tick_size,0), pos+vec(0,tick_size,0)], color=color.black)
            label(pos=pos+vec(0,-2*tick_size,0), text=str(i), height=10, box=False, color=color.black)
        elif axis_vec.y: # y-axis
            curve(pos=[pos+vec(-tick_size,0,0), pos+vec(tick_size,0,0)], color=color.black)
            label(pos=pos+vec(-2*tick_size,0,0), text=str(i), height=10, box=False, color=color.black)
        elif axis_vec.z: # z-axis
            curve(pos=[pos+vec(-tick_size,0,0), pos+vec(tick_size,0,0)], color=color.black)
            label(pos=pos+vec(0,0,0.2), text=str(i), height=10, box=False, color=color.black)

    # Add axis label
    label(pos=(axis_length+0.3)*axis_vec, text=axis_label, height=14, box=False, color=color_axis)

# Add ticks + labels
draw_ticks(vec(1,0,0), "x", color.red)
draw_ticks(vec(0,1,0), "y", color.green)
draw_ticks(vec(0,0,1), "z", color.blue)

# Moving ball with trail
ball = sphere(pos=vector(0,0,0), radius=0.3, color=color.magenta,
              make_trail=True)
v_arrow = arrow(pos=ball.pos, axis=vector(1,0,0), color=color.blue, shaftwidth=0.08)

# Define velocity function v(t)
def velocity_func(t):
    return vector(9.6, 0, -2*t)

# Label for velocity
v_label = label(pos=v_arrow.pos + v_arrow.axis,
                text="v", xoffset=10, yoffset=10,
                space=30, height=16, box=False, color=color.blue)

# Info label
info = label(pos=vector(20, 20, 0),
             text="", height=12, box=False, opacity=0,
             color=color.black)
# Animate motion
t = 0
dt = 0.01
while True:     
    rate(20)

    if t > 3:
        t = 0
        ball.clear_trail()

    # Physics position
    x = 9.6 * t
    y = 8.85
    z = -t**2

    # Scaled position
    ball.pos = vector(x, y, z)
    v_arrow.pos = ball.pos
    #v_arrow.axis = velocity_func(t)
    v_arrow.axis = hat(velocity_func(t)) * 2   # always length 3, only shows direction

    v_label.pos = v_arrow.pos + v_arrow.axis*2
   
    # Info text shows actual physics units (not scaled)
    info.text = f"t={t:.2f} s | x = ({x:.2f} | y = {y:.2f} | z = {z:.2f})"

    t += dt

