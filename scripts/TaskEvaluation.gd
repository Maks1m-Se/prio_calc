extends Control

var current_scores = {
	"importance": null,
	"urgency": null,
	"effort": null
}

func _ready():
	var task_name = SceneManager.current_task_name
	print("\n📝 Now evaluating: ", task_name)
	$MarginContainer/VBoxContainer/Label_CurrentTask.text = task_name

	# Connect rating buttons (Importance)
	for button in $MarginContainer/VBoxContainer/HBoxContainer_ImportanceButtons.get_children():
		button.pressed.connect(_on_rating_button_pressed.bind("importance", button.text.to_int()))

	# Connect rating buttons (Urgency)
	for button in $MarginContainer/VBoxContainer/HBoxContainer_UrgencyButtons.get_children():
		button.pressed.connect(_on_rating_button_pressed.bind("urgency", button.text.to_int()))

	# Connect rating buttons (Effort)
	for button in $MarginContainer/VBoxContainer/HBoxContainer_EffortButtons.get_children():
		button.pressed.connect(_on_rating_button_pressed.bind("effort", button.text.to_int()))

	# Connect back button
	$MarginContainer/VBoxContainer/HBoxContainer_ActionButtons/Button_Back.pressed.connect(SceneManager.go_to_main)

func _on_rating_button_pressed(attribute: String, score: int):
	current_scores[attribute] = score
	print("✅ Rated", attribute, " → ", score)

	# Optional: visually highlight chosen score
	_highlight_selected_button(attribute, score)

	# Check if all attributes are rated
	if !current_scores.values().has(null):
		print("✅ All ratings complete for task: ", SceneManager.current_task_name)
		SceneManager.store_score(SceneManager.current_task_name, current_scores)
		# Reset for next task
		current_scores = {"importance": null, "urgency": null, "effort": null}
		SceneManager.finish_task_evaluation()

func _highlight_selected_button(attribute: String, selected_score: int):
	var container
	match attribute:
		"importance": container = $MarginContainer/VBoxContainer/HBoxContainer_ImportanceButtons
		"urgency": container = $MarginContainer/VBoxContainer/HBoxContainer_UrgencyButtons
		"effort": container = $MarginContainer/VBoxContainer/HBoxContainer_EffortButtons

	for button in container.get_children():
		button.disabled = false  # Re-enable all
		if button.text.to_int() == selected_score:
			button.disabled = true  # Highlight selected
