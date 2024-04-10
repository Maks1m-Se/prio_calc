import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
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
    # Dummy evaluation for demonstration
    IT_df = df.copy()
    UT_df = df.copy()
    ET_df = df.copy()
    RT_df = df.copy()
    return IT_df, UT_df, ET_df, RT_df

# Function to render task rank
def render_task_rank(IT_df, UT_df, ET_df, RT_df):
    # Dummy print for demonstration
    print("IT_df:", IT_df)
    print("UT_df:", UT_df)
    print("ET_df:", ET_df)
    print("RT_df:", RT_df)

class EvaluationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = df_tasks.index.tolist()
        self.comb_index = 0
        self.IT_df = None
        self.UT_df = None
        self.ET_df = None
        self.RT_df = None
        self.create_ui()

    def create_ui(self):
        layout = BoxLayout(orientation='vertical')

        # Display tasks in a table
        table_layout = GridLayout(cols=2)
        table_layout.add_widget(Label(text="Task Label"))
        table_layout.add_widget(Label(text="Task Description"))
        for label, description in df_tasks.itertuples():
            table_layout.add_widget(Label(text=str(label)))
            table_layout.add_widget(Label(text=description))
        layout.add_widget(table_layout)

        next_button = Button(text='Next', on_press=self.next_combination)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def next_combination(self, instance):
        if self.comb_index < len(self.tasks) - 1:
            task_a = self.tasks[self.comb_index]
            task_b = self.tasks[self.comb_index + 1]
            self.comb_index += 1
            print(f'Evaluate tasks: {task_a} vs {task_b}')
            # Perform evaluation
            # Dummy evaluation for demonstration
            self.IT_df, self.UT_df, self.ET_df, self.RT_df = eval_tasks(df_tasks)

        else:
            self.manager.current = 'result'
            self.manager.get_screen('result').display_results(self.IT_df, self.UT_df, self.ET_df, self.RT_df)

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_results(self, IT_df, UT_df, ET_df, RT_df):
        # Display result tables
        print("-----\n\n### Result Ranked Tasks ###")
        print("IT_df:", IT_df)
        print("UT_df:", UT_df)
        print("ET_df:", ET_df)
        print("RT_df:", RT_df)

class TaskEvaluationApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EvaluationScreen(name='evaluation'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    TaskEvaluationApp().run()
