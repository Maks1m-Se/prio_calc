extends Control

var show_details := false  # Controls whether to show Importance, Urgency, Effort columns

func _ready():
	# Set up default toggle state
	$MarginContainer/VBoxContainer/CheckBox_ShowDetails.button_pressed = false
	$MarginContainer/VBoxContainer/CheckBox_ShowDetails.toggled.connect(_on_toggle_details)
	$MarginContainer/VBoxContainer/HBoxContainer_ActionButtons/Button_BackToMain.pressed.connect(SceneManager.go_to_main)

	_populate_tree()  # Initial tree display

func _on_toggle_details(visible: bool):
	show_details = visible
	_populate_tree()

func _populate_tree():
	var task_scores = SceneManager.task_scores

	# Calculate and sort results
	var results = []
	for task_name in task_scores.keys():
		var score_data = task_scores[task_name]
		var result_score = score_data.importance + score_data.urgency - score_data.effort
		results.append({
			"task": task_name,
			"score": result_score,
			"importance": score_data.importance,
			"urgency": score_data.urgency,
			"effort": score_data.effort
		})

	results.sort_custom(func(a, b): return a.score > b.score)

	# Set up Tree
	var tree = $MarginContainer/VBoxContainer/Tree_Results
	tree.clear()

	if show_details:
		tree.columns = 5
		tree.set_column_title(0, "Task")
		tree.set_column_title(1, "Score")
		tree.set_column_title(2, "Importance")
		tree.set_column_title(3, "Urgency")
		tree.set_column_title(4, "Effort")
	else:
		tree.columns = 2
		tree.set_column_title(0, "Task")
		tree.set_column_title(1, "Score")

	tree.set_column_titles_visible(true)
	
	# Control column expansion
	for i in tree.columns:
		tree.set_column_expand(i, i < 2)  # Only expand Task (0) and Score (1)
	
	var root = tree.create_item()
	for result in results:
		var item = tree.create_item(root)
		item.set_text(0, result.task)
		item.set_text(1, str(result.score))
		item.set_text_alignment(0, HORIZONTAL_ALIGNMENT_CENTER)
		item.set_text_alignment(1, HORIZONTAL_ALIGNMENT_CENTER)
		if show_details:
			item.set_text(2, str(result.importance))
			item.set_text(3, str(result.urgency))
			item.set_text(4, str(result.effort))
			item.set_text_alignment(2, HORIZONTAL_ALIGNMENT_RIGHT)
			item.set_text_alignment(3, HORIZONTAL_ALIGNMENT_RIGHT)
			item.set_text_alignment(4, HORIZONTAL_ALIGNMENT_RIGHT)
