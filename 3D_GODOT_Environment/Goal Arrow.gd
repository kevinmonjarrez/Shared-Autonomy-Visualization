extends CharacterBody3D

# Reference to the target node
@onready var GoalDot = get_node("/root/Node3D/Goal_Dot")
func _ready():
	pass

func _process(delta):
	look_at_target()

func look_at_target():
	look_at(GoalDot.global_transform.origin, Vector3.UP)
