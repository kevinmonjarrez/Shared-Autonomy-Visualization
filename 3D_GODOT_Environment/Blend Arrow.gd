extends CharacterBody3D

# Reference to the target node
@onready var Arrow = get_node("/root/Node3D/PlayerDot/Arrow") 
@onready var Goal_Arrow = get_node("/root/Node3D/PlayerDot/Goal Arrow") 

var ALPHA  = 0.5
func _ready():
	pass

func _physics_process(delta):
	blend()

func blend():
	var midpoint = (Arrow.global_transform.origin + Goal_Arrow.global_transform.origin) * ALPHA
	global_transform.origin = midpoint
	print(Arrow.global_transform.origin)
	print(Goal_Arrow.global_transform.origin)
	print(midpoint)


#extends MeshInstance3D
#
#export(NodePath) var arrow1_path: NodePath
#export(NodePath) var arrow2_path: NodePath
#
#onready var arrow1 = get_node_or_null(arrow1_path)
#onready var arrow2 = get_node_or_null(arrow2_path)
#
#func _process(delta):
	#update_position()
#
#func update_position():
	#if arrow1 and arrow2:
		## Calculate the midpoint between Arrow1 and Arrow2
		#var midpoint = (arrow1.global_transform.origin + arrow2.global_transform.origin) * 0.5
		#global_transform.origin = midpoint
	#else:
		#print("One or both of the arrow nodes are not set or have been freed.")
