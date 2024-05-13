import pandas as pd

DICT_TASKS = {
    "A": "Geschirr",
    "B": "Wäsche",
    "C": "Steuern",
    "D": "App",
}

# Create a list of tuples with (task_label, task_description)
tasks_data = [(key, value) for key, value in DICT_TASKS.items()]

# Create a DataFrame from the list of tuples
df_tasks = pd.DataFrame(tasks_data, columns=['Label', 'Tasks'])
df_tasks = df_tasks.set_index("Label")
