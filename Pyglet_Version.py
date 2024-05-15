import pyglet
from OpenGL.GL import *

# Set up window and OpenGL context
window = pyglet.window.Window(width=800, height=600, resizable=True)
glClearColor(0.5, 0.5, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)

# Define the dot's position and velocity
dot_position = [0, 0, -5]
dot_velocity = [0, 0, 0]

# Define function to draw the dot
def draw_dot():
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex3f(*dot_position)
    glEnd()

# Define update function to control the dot's movement
def update(dt):
    global dot_position, dot_velocity
    dot_position[0] += dot_velocity[0] * dt
    dot_position[1] += dot_velocity[1] * dt
    dot_position[2] += dot_velocity[2] * dt

# Define controller handler to control the dot's movement
def update_controller(x, y, dx, dy):
    global dot_velocity
    dot_velocity[0] = dx * 10
    dot_velocity[1] = -dy * 10  # Reverse Y-axis movement

# Set up controller handler
joysticks = pyglet.input.get_joysticks()
if joysticks:
    joystick = joysticks[0]  # Assuming the first joystick found is used
    joystick.open()
    joystick.push_handlers(on_joyaxis_motion=update_controller)

# Define draw function
@window.event
def on_draw():
    window.clear()
    glLoadIdentity()  # Corrected here
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)  # Using gluLookAt from pyglet.gl
    draw_dot()

# Run the application
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
