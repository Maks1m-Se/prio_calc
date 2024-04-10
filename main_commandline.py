'''
TT: inital task table (main table; unsorted)
IT: importance table
UT: urgency table
ET: efficiency table
RT: ultimate ranked table (result)
'''

import pandas as pd
import itertools
import inquirer
#import random
from tabulate import tabulate
from tasks import df_tasks

def display_df(df, header=None):
    print('\n')
    print(f'Table: {header}')
    print(tabulate(df, "keys", tablefmt="github"))
    print('\n')

number_of_combs = len(list(itertools.combinations(df_tasks.Tasks, 2)))
number_of_questions = number_of_combs * 3

print("\n### Overview Tasks ###")
display_df(df_tasks, "df_tasks")
print("Count: ", df_tasks["Tasks"].nunique())
print("Combinations: ", number_of_combs)
print("Questions: ", number_of_questions)

print('-----\n\n')

IT_df, UT_df, ET_df = df_tasks.copy(), df_tasks.copy(), df_tasks.copy()
IT_df["Importance_Score"] = 0
UT_df["Urgency_Score"] = 0
ET_df["Effort_Score"] = 0


def add_task():
    '''
    Adding new task to TT.
    User presses button to add task to TT.
    input: User input
    output: None
    ''' 
    pass


def eval_tasks(df):
    '''
    User evaluates tasks in pairs.
    Presents user each pair one by one. Each pair is evaluated for importance, urgency and efficiency.
    input: TT 
    output: IT, UT, ET with scores
    '''
    
    count_question = 0

    # create combination pairs of tasks
    for comb in itertools.combinations(df.Tasks, 2):

        

        ## ask user for evaluation ##

        # Importance
        count_question +=1
        choice = inquirer.list_input(f"({count_question}/{number_of_questions}) Which is more important?", choices=comb)
        print(f"Choice: '{choice}' is more important.")
        IT_df.loc[df['Tasks'] == choice, 'Importance_Score'] = IT_df['Importance_Score'] + 1
        display_df(IT_df, "IT_df")

        # Urgency
        count_question +=1
        choice = inquirer.list_input(f"({count_question}/{number_of_questions}) Which is more urgent?", choices=comb)
        print(f"Choice: '{choice}' is more urgent.")
        UT_df.loc[df['Tasks'] == choice, 'Urgency_Score'] = UT_df['Urgency_Score'] + 1
        display_df(UT_df, "UT_df")
        
        # Effort
        count_question +=1
        choice = inquirer.list_input(f"({count_question}/{number_of_questions}) Which is more effortless?", choices=comb)
        print(f"Choice: '{choice}' is more effortless.")
        ET_df.loc[df['Tasks'] == choice, 'Effort_Score'] = ET_df['Effort_Score'] + 1
        display_df(ET_df, "ET_df")
        


eval_tasks(df_tasks)




def render_task_rank():
    '''
    Calculating the ranks.
    input: TT
    output: RT
    '''
    RT_df = df_tasks.copy()
    RT_df["Sum_of_Scores"] = 0
    
    for task in RT_df.Tasks:

        sum_task_score = 0
        sum_task_score += IT_df.loc[IT_df['Tasks'] == task, 'Importance_Score']
        sum_task_score += UT_df.loc[UT_df['Tasks'] == task, 'Urgency_Score']
        sum_task_score += ET_df.loc[ET_df['Tasks'] == task, 'Effort_Score']

        print(task, sum_task_score)

        RT_df.loc[RT_df['Tasks'] == task, 'Sum_of_Scores'] = sum_task_score

    ## Create Ranks ##
    # Importance
    IT_df["Rank"] = IT_df["Importance_Score"].rank(ascending=False)
    IT_df.sort_values("Rank", inplace = True)
    # Urgency
    UT_df["Rank"] = UT_df["Urgency_Score"].rank(ascending=False)
    UT_df.sort_values("Rank", inplace = True)
    # Effort
    ET_df["Rank"] = ET_df["Effort_Score"].rank(ascending=False)
    ET_df.sort_values("Rank", inplace = True)
    # Result Summary
    RT_df["Rank"] = RT_df["Sum_of_Scores"].rank(ascending=False)
    RT_df.sort_values("Rank", inplace = True)

    #Display
    display_df(IT_df, "IT_df")
    display_df(UT_df, "UT_df")
    display_df(ET_df, "ET_df")
    print("-----\n\n### Result Ranked Tasks ###")
    display_df(RT_df, "RT_df")

render_task_rank()