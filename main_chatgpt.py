import pandas as pd
import itertools
import inquirer
from tabulate import tabulate
from tasks import df_tasks

# Function to display DataFrame nicely
def display_df(df, header=None):
    print('\n')
    print(f'Table: {header}')
    print(tabulate(df, "keys", tablefmt="github"))
    print('\n')

# Function to evaluate tasks based on importance, urgency, and effort
def eval_tasks(df):
    '''
    User evaluates tasks in pairs.
    Presents user each pair one by one. Each pair is evaluated for importance, urgency and efficiency.
    input: df (DataFrame of tasks) 
    output: IT_df, UT_df, ET_df with scores
    '''
    # Counting the number of questions
    number_of_combs = len(list(itertools.combinations(df.Tasks, 2)))
    number_of_questions = number_of_combs * 3
    count_question = 0

    # Creating copies of DataFrame for Importance, Urgency, and Effort tables
    IT_df, UT_df, ET_df = df.copy(), df.copy(), df.copy()
    IT_df["Importance_Score"] = 0
    UT_df["Urgency_Score"] = 0
    ET_df["Effort_Score"] = 0

    # Iterating through combinations of tasks
    for comb in itertools.combinations(df.Tasks, 2):

        # Importance
        count_question += 1
        choice = inquirer.list_input(f"({count_question}/{number_of_questions}) Which is more important?", choices=comb)
        print(f"Choice: '{choice}' is more important.")
        IT_df.loc[df['Tasks'] == choice, 'Importance_Score'] += 1
        display_df(IT_df, "IT_df")

        # Urgency
        count_question += 1
        choice = inquirer.list_input(f"({count_question}/{number_of_questions}) Which is more urgent?", choices=comb)
        print(f"Choice: '{choice}' is more urgent.")
        UT_df.loc[df['Tasks'] == choice, 'Urgency_Score'] += 1
        display_df(UT_df, "UT_df")

        # Effort
        count_question += 1
        choice = inquirer.list_input(f"({count_question}/{number_of_questions}) Which is more effortless?", choices=comb)
        print(f"Choice: '{choice}' is more effortless.")
        ET_df.loc[df['Tasks'] == choice, 'Effort_Score'] += 1
        display_df(ET_df, "ET_df")

    return IT_df, UT_df, ET_df

def render_task_rank(df_tasks, IT_df, UT_df, ET_df):
    '''
    Calculating the ranks.
    input: df_tasks (DataFrame of tasks), IT_df, UT_df, ET_df (Importance, Urgency, Effort DataFrames)
    output: RT_df (Ranked DataFrame)
    '''
    # Creating a copy of the main DataFrame
    RT_df = df_tasks.copy()
    RT_df["Sum_of_Scores"] = IT_df["Importance_Score"] + UT_df["Urgency_Score"] + ET_df["Effort_Score"]

    # Calculating ranks for each criterion
    for criterion_df in [IT_df, UT_df, ET_df]:
        criterion_df["Rank"] = criterion_df[criterion_df.columns[-1]].rank(ascending=False)
        criterion_df.sort_values("Rank", inplace=True)

    # Calculating ranks for the result
    RT_df["Rank"] = RT_df["Sum_of_Scores"].rank(ascending=False)
    RT_df.sort_values("Rank", inplace=True)

    # Displaying all rankings
    display_df(IT_df, "IT_df")
    display_df(UT_df, "UT_df")
    display_df(ET_df, "ET_df")
    print("-----\n\n### Result Ranked Tasks ###")
    display_df(RT_df, "RT_df")

# Main function
def main():
    print("\n### Overview Tasks ###")
    display_df(df_tasks, "df_tasks")
    print("Count: ", df_tasks["Tasks"].nunique())
    
    IT_df, UT_df, ET_df = eval_tasks(df_tasks)
    render_task_rank(df_tasks, IT_df, UT_df, ET_df)

if __name__ == "__main__":
    main()
