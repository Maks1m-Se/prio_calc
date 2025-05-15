extends Node

var task_list: Array = []
var task_queue := []
var current_task_name := ""
var task_scores := {}  # ✅ Add this to store evaluated results

var main_scene_path := "res://scenes/MainScene.tscn"
var eval_scene_path := "res://scenes/TaskEvaluation.tscn"
var results_scene_path := "res://scenes/ResultsScene.tscn"

func start_evaluation(task_names: Array):
	task_queue = task_names.duplicate()
	print("\n🧪 Start Evaluation. Tasks: ")
	for task in task_queue:
		print(" - ", task)
	_next_task()

func store_score(task_name: String, scores: Dictionary):
	task_scores[task_name] = scores.duplicate()
	print("✅ Stored score for ", task_name, ":\n", scores)

func _next_task():
	if task_queue.is_empty():
		_show_results()
	else:
		current_task_name = task_queue.pop_front()
		get_tree().change_scene_to_file(eval_scene_path)

func go_to_main():
	get_tree().change_scene_to_file(main_scene_path)
	print("\nBack to main menu")
	
func _show_results():
	print("\n📊 Showing results:")
	for task in task_scores.keys():
		print(" - ", task, ": ", task_scores[task])
	get_tree().change_scene_to_file(results_scene_path)

	
func finish_task_evaluation():
	_next_task()
