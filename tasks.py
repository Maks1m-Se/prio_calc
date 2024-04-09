import pandas as pd

DICT_TASKS = {
    "A": "Wäsche",
    "B": "Sport",
    "C": "Geschirr",
    "D": "Wand streichen",
}

# Create a list of tuples with (task_label, task_description)
tasks_data = [(key, value) for key, value in DICT_TASKS.items()]

# Create a DataFrame from the list of tuples
df_tasks = pd.DataFrame(tasks_data, columns=['Label', 'Tasks'])

