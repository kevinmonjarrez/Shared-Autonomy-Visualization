extends CharacterBody3D

# Define movement speed and rotation speed
var speed = 5
var rotation_speed = 2
var target_direction = Vector3()

# Visualization
var visual_indicator

func _ready():
	# Access the pre-created visual indicator (arrow) in the scene
	visual_indicator = $VisualIndicator

func _physics_process(delta):
	# Calculate rotation based on mouse movement
	var mouse_movement = -Input.get_action_strength("mouse_look") * rotation_speed * delta
	rotate_y(mouse_movement)

	# Calculate movement direction based on rotation
	var forward = global_transform.basis.z.normalized()
	var right = global_transform.basis.x.normalized()

	var movement = Vector3()

	if Input.is_action_pressed("ui_right"):
		movement += right
	if Input.is_action_pressed("ui_left"):
		movement -= right

	# Normalize the movement vector to ensure consistent speed
	movement = movement.normalized()

	# Calculate the target direction based on mouse movement
	if Input.is_action_pressed("mouse_look"):
		var mouse_pos = get_viewport().get_mouse_position()
		var screen_size = get_viewport().size
		var center = screen_size / 2
		var delta_mouse = (mouse_pos - center) / center.y
		target_direction = Vector3(delta_mouse.x, 0, delta_mouse.y)

	# Interpolate towards the target direction for smoother movement

	# Move the character using the calculated movement vector
	move_and_slide()

	# Update visual indicator position and rotation
	visual_indicator.global_transform.origin = global_transform.origin
	visual_indicator.global_transform.basis = global_transform.basis
