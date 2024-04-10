# main.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen

class TaskEvaluationApp(App):
    def build(self):
        # Creating screen manager
        sm = ScreenManager()
        sm.add_widget(EvaluationScreen(name='evaluation'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

class EvaluationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = ['Task A', 'Task B', 'Task C']  # Example tasks
        self.comb_index = 0
        self.create_ui()

    def create_ui(self):
        layout = BoxLayout(orientation='vertical')
        self.task_label = Label(text='Evaluate tasks:', size_hint=(1, 0.5))
        layout.add_widget(self.task_label)

        self.spinner = Spinner(text='Task A', values=self.tasks)
        layout.add_widget(self.spinner)

        next_button = Button(text='Next', on_press=self.next_combination)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def next_combination(self, instance):
        self.comb_index += 1
        if self.comb_index < len(self.tasks):
            self.task_label.text = f'Evaluate tasks: {self.tasks[self.comb_index]} vs {self.tasks[self.comb_index - 1]}'
            self.spinner.text = self.tasks[self.comb_index]
        else:
            self.manager.current = 'result'

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()

    def create_ui(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Result Screen'))
        self.add_widget(layout)

if __name__ == '__main__':
    TaskEvaluationApp().run()
