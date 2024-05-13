# your_program_file.py

import pandas as pd
import itertools
from tasks import df_tasks

# Function to compare tasks based on importance, urgency, and effort
def compare_tasks(df_tasks, form_data):
    '''
    User compares tasks in pairs.
    Presents user each pair one by one. Each pair is evaluated for importance, urgency and efficiency.
    input: df_tasks (DataFrame of tasks), form_data (data submitted from the form)
    output: IT_df, UT_df, ET_df with scores
    '''
    # Extract tasks from form data
    tasks = df_tasks['Tasks'].tolist()

    # Initialize DataFrames for Importance, Urgency, and Effort
    IT_df = pd.DataFrame({'Tasks': tasks, 'Importance_Score': 0})
    UT_df = pd.DataFrame({'Tasks': tasks, 'Urgency_Score': 0})
    ET_df = pd.DataFrame({'Tasks': tasks, 'Effort_Score': 0})

    # Process form data
    for task1, task2 in itertools.combinations(tasks, 2):
        importance_key = f"importance_{task1}_{task2}"
        urgency_key = f"urgency_{task1}_{task2}"
        effort_key = f"effort_{task1}_{task2}"
        importance_score = int(form_data.get(importance_key, 0))
        urgency_score = int(form_data.get(urgency_key, 0))
        effort_score = int(form_data.get(effort_key, 0))
        IT_df.loc[IT_df['Tasks'] == task1, 'Importance_Score'] += importance_score
        IT_df.loc[IT_df['Tasks'] == task2, 'Importance_Score'] += (10 - importance_score)
        UT_df.loc[UT_df['Tasks'] == task1, 'Urgency_Score'] += urgency_score
        UT_df.loc[UT_df['Tasks'] == task2, 'Urgency_Score'] += (10 - urgency_score)
        ET_df.loc[ET_df['Tasks'] == task1, 'Effort_Score'] += effort_score
        ET_df.loc[ET_df['Tasks'] == task2, 'Effort_Score'] += (10 - effort_score)

    return IT_df, UT_df, ET_df

# Function to evaluate tasks based on importance, urgency, and effort
def evaluate_tasks(df_tasks):
    '''
    User evaluates each tasks.
    Presents user each task one by one. Each task is evaluated for importance, urgency and efficiency from 0 to 10.
    input: df_tasks (DataFrame of tasks), form_data (data submitted from the form)
    output: IT_df, UT_df, ET_df with scores
    '''
    # Extract tasks from form data
    tasks = df_tasks['Tasks'].tolist()

       # Initialize DataFrames for Importance, Urgency, and Effort
    IT_df = pd.DataFrame({'Tasks': tasks, 'Importance_Score': 0})
    UT_df = pd.DataFrame({'Tasks': tasks, 'Urgency_Score': 0})
    ET_df = pd.DataFrame({'Tasks': tasks, 'Effort_Score': 0})

    # Process form data
    for task in tasks:
        importance_key = f"importance_{task}"
        urgency_key = f"urgency_{task}"
        effort_key = f"effort_{task}"
        importance_score = 1
        urgency_score = 2
        effort_score = 3
        # importance_score = int(form_data.get(importance_key, 0))
        # urgency_score = int(form_data.get(urgency_key, 0))
        # effort_score = int(form_data.get(effort_key, 0))
        IT_df.loc[IT_df['Tasks'] == task, 'Importance_Score'] = importance_score
        UT_df.loc[UT_df['Tasks'] == task, 'Urgency_Score'] = urgency_score
        ET_df.loc[ET_df['Tasks'] == task, 'Effort_Score'] = effort_score

    return IT_df, UT_df, ET_df

# Function to render task ranks
def render_task_rank(df_tasks, IT_df, UT_df, ET_df):
    '''
    Calculating the ranks.
    input: df_tasks (DataFrame of tasks), IT_df, UT_df, ET_df (Importance, Urgency, Effort DataFrames)
    output: RT_df (Ranked DataFrame)
    '''
    # Calculate total scores
    IT_df['Total_Score'] = IT_df['Importance_Score'] + UT_df['Urgency_Score'] + ET_df['Effort_Score']

    # Rank tasks based on total score
    IT_df['Rank'] = IT_df['Total_Score'].rank(ascending=False)
    IT_df.sort_values(by='Rank', inplace=True)

    return IT_df

# Main function
def main():

    # Sample form data (replace with actual form data retrieval)
    form_data = {
        'importance_Task1_Task2': '5',
        'importance_Task1_Task3': '8',
        'urgency_Task1_Task2': '7',
        'urgency_Task1_Task3': '3',
        'effort_Task1_Task2': '4',
        'effort_Task1_Task3': '9',
    }

    # Call compare_tasks function with sample data
    IT_df, UT_df, ET_df = compare_tasks(df_tasks, form_data)
    print("Importance Scores:")
    print(IT_df)
    print("Urgency Scores:")
    print(UT_df)
    print("Effort Scores:")
    print(ET_df)

    # Call evaluate_tasks function with sample data
    IT_df, UT_df, ET_df = evaluate_tasks(df_tasks, form_data)
    print("Importance Scores:")
    print(IT_df)
    print("Urgency Scores:")
    print(UT_df)
    print("Effort Scores:")
    print(ET_df)

    # Call render_task_rank function with sample data
    RT_df = render_task_rank(df_tasks, IT_df, UT_df, ET_df)
    print("Ranked Tasks:")
    print(RT_df)

if __name__ == "__main__":
    main()
