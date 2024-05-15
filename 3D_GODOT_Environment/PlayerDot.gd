extends CharacterBody3D

var mouse_sensitivity := 0.005
var twist_input := 0.0 
var pitch_input := 0.0

const SPEED = 5.0
func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	
func _physics_process(delta):

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction := Vector3.ZERO
	direction.x = (Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left"))
	direction.z = -(Input.get_action_strength("ui_up") - Input.get_action_strength("ui_down"))
	direction = direction.rotated(Vector3.UP, twist_input).normalized()
	direction = direction.rotated(Vector3.RIGHT, pitch_input).normalized()

	velocity.x = direction.x * SPEED
	velocity.z = direction.z * SPEED
	velocity.y = direction.y * SPEED
	#else:
		#velocity.x = move_toward(velocity.x, 0, SPEED)
		#velocity.z = move_toward(velocity.z, 0, SPEED)
		#velocity.y = move_toward(velocity.y, 0, SPEED)
		
	#if velocity.length() > 0.2: 
	var look_direction = Vector2(velocity.z, velocity.x)
	rotation.y = twist_input
	rotation.x = pitch_input
		#rotate_object_local(Vector3(0, 1, 0), look_direction.angle())
	move_and_slide()
	
	if Input.is_action_just_pressed("ui_cancel"):
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	
	#rotate_x(pitch_input)
	##rotation.x = clamp(
		##rotation.x,
		##-0.5,
		##0.5
	##)
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED: 
			twist_input -=  event.relative.x * mouse_sensitivity
			twist_input = clamp(twist_input, -3.14/2, 3.14/2)
			pitch_input -= event.relative.y * mouse_sensitivity
			pitch_input = clamp(pitch_input, -3.14/2, 3.14/2)
