extends Control

func _ready():
	var screen_size = DisplayServer.window_get_size()
	if screen_size.x > screen_size.y:
		print("Landscape")
	else:
		print("Portrait")
	
	# Connect signals
	$MarginContainer/VBoxContainer/HBoxContainer_TaskInputRow/Button_AddTask.pressed.connect(_on_add_task_pressed)
	$MarginContainer/VBoxContainer/HBoxContainer_ActionButtons/Button_DeleteSelected.pressed.connect(_on_delete_selected_pressed)
	$MarginContainer/VBoxContainer/HBoxContainer_TaskInputRow/HBoxContainer/Button_Evaluate.pressed.connect(_on_Button_Evaluate_pressed)
	$MarginContainer/VBoxContainer/HBoxContainer_TaskInputRow/LineEdit_TaskInput.text_submitted.connect(on_task_input_submitted)

	refresh_task_list()
	update_task_count()

# Add task
func _on_add_task_pressed():
	var task_name = $MarginContainer/VBoxContainer/HBoxContainer_TaskInputRow/LineEdit_TaskInput.text.strip_edges()
	
	if task_name != "":
		SceneManager.task_list.append(task_name)
		print("Add task: ", task_name)
		refresh_task_list()
		update_task_count()
		
		# Scroll to the last item
		var list = $MarginContainer/VBoxContainer/ItemList_TaskDisplayList
		list.select(list.get_item_count() - 1)
		list.ensure_current_is_visible()
		$MarginContainer/VBoxContainer/HBoxContainer_TaskInputRow/LineEdit_TaskInput.clear()
	else:
		print("Task name is empty!")

# Refresh UI
func refresh_task_list():
	var list = $MarginContainer/VBoxContainer/ItemList_TaskDisplayList
	list.clear()
	for task in SceneManager.task_list:
		list.add_item(task)

# Delete tasks
func _on_delete_selected_pressed():
	var list = $MarginContainer/VBoxContainer/ItemList_TaskDisplayList
	var selected_indices = list.get_selected_items()

	if selected_indices.size() > 0:
		# Important: remove from highest to lowest to prevent index shifting
		selected_indices.sort()
		selected_indices.reverse()
		
		for index in selected_indices:
			print("Delete task: ", list.get_item_text(index))
			SceneManager.task_list.remove_at(index)  # 💥 Remove from data model
		list.deselect_all()

		refresh_task_list()  # 💥 Refresh display after changes
		update_task_count()
	else:
		print("No task selected.")

# Enter = Add
func on_task_input_submitted(_new_text: String) -> void:
	_on_add_task_pressed()

# Task count
func update_task_count():
	var count = SceneManager.task_list.size()
	$MarginContainer/VBoxContainer/Label_TaskCount.text = "Tasks: %d" % count

# Start evaluation
func _on_Button_Evaluate_pressed():
	if SceneManager.task_list.size() > 0:
		SceneManager.start_evaluation(SceneManager.task_list)
	else:
		print("No tasks to evaluate")
