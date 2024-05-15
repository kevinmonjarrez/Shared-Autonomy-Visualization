import tkinter as tk
import math 
import Helper as H
from PIL import Image, ImageDraw, ImageTk
import serial as ser
import time
import serial_helper as sh


ser_connection = ser.Serial('COM3', 9600)
# Constants

GRID_ROWS = 10
GRID_COLS = 10
GRID_CELL_SIZE = 40  
ALPHA  = 0.5 


root = tk.Tk()
root.title("2D Shared Autonomy Enviornment")

# Creates Canvas
canvas = tk.Canvas(root, width=GRID_COLS * GRID_CELL_SIZE, height=GRID_ROWS * GRID_CELL_SIZE, bg="white")
canvas.pack()

# Snippet Below Creates Grid
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        x1 = col * GRID_CELL_SIZE
        y1 = row * GRID_CELL_SIZE
        x2 = x1 + GRID_CELL_SIZE
        y2 = y1 + GRID_CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="black")

# Drawing the User Red Dot
red_dot_row = 0
red_dot_col = 0

dot_radius = 15
red_dot_id = canvas.create_oval(
    red_dot_col * GRID_CELL_SIZE + 10,
    red_dot_row * GRID_CELL_SIZE + 10,
    (red_dot_col + 1) * GRID_CELL_SIZE - 10,
    (red_dot_row + 1) * GRID_CELL_SIZE - 10,
    fill="red",
)

# Initializing Transluscency of Previous Shadow Dot (Currentlty makes a square???)
dot_image = Image.new("RGBA", (15, 15), (255, 0, 0, 128))  
draw = ImageDraw.Draw(dot_image)
draw.ellipse((0, 0, 15, 15), fill=(255, 0, 0, 128))  

dot_tk_image = ImageTk.PhotoImage(dot_image)

shadow_dot_col = 0
shadow_dot_row = 0
shadow_dot_id = canvas.create_image(
    (shadow_dot_col * GRID_CELL_SIZE) + GRID_CELL_SIZE / 2,
    (shadow_dot_row * GRID_CELL_SIZE) + GRID_CELL_SIZE / 2,
    image=dot_tk_image,
)

# Position of Gaol
goal_corner = "bottom_right"  

if goal_corner == "bottom_right":
    goal_row = GRID_ROWS - 1
    goal_col = GRID_COLS - 1
elif goal_corner == "top_right":
    goal_row = 0
    goal_col = GRID_COLS - 1
elif goal_corner == "bottom_left":
    goal_row = GRID_ROWS - 1
    goal_col = 0
else:  # "top_left"
    goal_row = 0
    goal_col = 0

#Drawing Goal Dot
goal_dot_id = canvas.create_oval(
    goal_col * GRID_CELL_SIZE + 10,
    goal_row * GRID_CELL_SIZE + 10,
    (goal_col + 1) * GRID_CELL_SIZE - 10,
    (goal_row + 1) * GRID_CELL_SIZE - 10,
    fill="green",
)

arrow_id = None  

# Function to draw the arrow
def draw_arrow():
    global arrow_id, red_dot_col_past, red_dot_row_past
    if arrow_id:
        canvas.delete(arrow_id)  

    # Angle Between Shadow Dot and Goal
    dx = goal_col - red_dot_col_past
    dy = goal_row - red_dot_row_past
    angle = math.atan2(dy, dx)

    arrow_length = GRID_CELL_SIZE  

    # arrow_x = red_dot_col * GRID_CELL_SIZE + 20 + math.cos(angle) * arrow_length
    # arrow_y = red_dot_row * GRID_CELL_SIZE + 20 + math.sin(angle) * arrow_length
    start_x = red_dot_col_past * GRID_CELL_SIZE + GRID_CELL_SIZE/2
    start_y = red_dot_row_past * GRID_CELL_SIZE + GRID_CELL_SIZE/2

    end_x = start_x + math.cos(angle) * arrow_length
    end_y = start_y + math.sin(angle) * arrow_length
   
    # Draw the arrow
    arrow_id = canvas.create_line(
        start_x,
        start_y,
        end_x,
        end_y,
        arrow="last",  
        fill="blue",  
        width=2,  
    )

    return start_x,end_x,start_y,end_y

#Drawing Arrows Between Dots
past_arrow_id = None

def draw_past_arrow():
    global past_arrow_id, arrow_id, red_dot_col_past, red_dot_row_past, red_dot_col, red_dot_row
    if past_arrow_id:
        canvas.delete(past_arrow_id) 

    start_x = red_dot_col_past * GRID_CELL_SIZE + GRID_CELL_SIZE/2
    start_y = red_dot_row_past * GRID_CELL_SIZE + GRID_CELL_SIZE/2
    end_x = red_dot_col * GRID_CELL_SIZE + GRID_CELL_SIZE/2
    end_y = red_dot_row * GRID_CELL_SIZE + GRID_CELL_SIZE/2
   
    # Draw the arrow
    past_arrow_id = canvas.create_line(
        start_x,
        start_y,
        end_x,
        end_y,
        arrow="last",  
        fill="orange", 
        width=2, 
    )

    return start_x,end_x,start_y,end_y

blend_arrow_id = None

def draw_blend_arrow(blend_x,blend_y):
    global blend_arrow_id, past_arrow_id, arrow_id, red_dot_col_past, red_dot_row_past, red_dot_col, red_dot_row
    if blend_arrow_id:
        canvas.delete(blend_arrow_id) 

    start_x = red_dot_col_past * GRID_CELL_SIZE + GRID_CELL_SIZE/2
    start_y = red_dot_row_past * GRID_CELL_SIZE + GRID_CELL_SIZE/2
    end_x = blend_x
    end_y = blend_y
   
    # Draw the arrowS
    blend_arrow_id = canvas.create_line(
        start_x,
        start_y,
        end_x,
        end_y,
        arrow="last",  
        fill="pink", 
        width=2, 
    )


# Moving Red Dot As well as everything else 
def move_red_dot(event):
    global red_dot_row, red_dot_col, red_dot_row_past, red_dot_col_past
    global shadow_dot_row, shadow_dot_col
    #Store Position of Last Dot
    red_dot_row_past = red_dot_row
    red_dot_col_past = red_dot_col

    # Moving on key Press
    if event.keysym == "Up":
        if red_dot_row > 0:
            red_dot_row -= 1
    elif event.keysym == "Down":
        if red_dot_row < GRID_ROWS - 1:
            red_dot_row += 1
    elif event.keysym == "Left":
        if red_dot_col > 0:
            red_dot_col -= 1
    elif event.keysym == "Right":
        if red_dot_col < GRID_COLS - 1:
            red_dot_col += 1

    # Moving Red Dot
    canvas.coords(
        red_dot_id,
        red_dot_col * GRID_CELL_SIZE + 10,
        red_dot_row * GRID_CELL_SIZE + 10,
        (red_dot_col + 1) * GRID_CELL_SIZE - 10,
        (red_dot_row + 1) * GRID_CELL_SIZE - 10,
    )

    #Moving Shadow
    canvas.coords(
        shadow_dot_id, 
        ((red_dot_col_past * GRID_CELL_SIZE) + GRID_CELL_SIZE / 2),
        ((red_dot_row_past * GRID_CELL_SIZE) + GRID_CELL_SIZE / 2),
    )
    # Drawing Arrow Based off CURRENT dot positions 
    x1,x2,y1,y2 = draw_arrow()
    x3,x4,y3,y4 = draw_past_arrow()

    blend_x,blend_y = H.blend([x2,y2], [x4,y4], ALPHA)
    draw_blend_arrow(blend_x,blend_y)
    angle_difference = H.angle_between_arrows(x1,y1,x2,y2,x3,y3,x4,y4)
    angle_difference_blend = H.angle_between_arrows(x1,y1,x2,y2,x3,y3,blend_x,blend_y)
    print(f"Optimal vs Human {angle_difference}")
    print(f"Human vs Blend {angle_difference_blend}")

    sh.write_to_port(angle_difference_blend, ser_connection)




#Binding Arrow Keys to Moving 
root.bind("<Up>", move_red_dot)
root.bind("<Down>", move_red_dot)
root.bind("<Left>", move_red_dot)
root.bind("<Right>", move_red_dot)


# Start the main loop to run the application
root.mainloop()
