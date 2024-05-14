from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from tasks import df_tasks
from WEBAPP_funcs import evaluate_tasks, compare_tasks, render_task_rank

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prio_calc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instantiate data base object
db = SQLAlchemy(app)


#### Database Models ####
# Task Table
class Todo(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False, unique=True)
    done=db.Column(db.Boolean)
    datetime_added = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<{self.task_id} {self.name} {self.done} {self.datetime_added}>'
    


# Importance Table
class IT_db(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    Importance_Score=db.Column(db.Integer)

    def __repr__(self):
        return f'<{self.task_id} {self.name} {self.Importance_Score}>'


# Urgency Table

# Effort Table

# Results Table

### Global Vars and Funcs ###
attribute = "Importance"
tasks_list = []
first_task = ''
pop_task = False

#### Helper Functions ####
def get_tasks_list():
    """Query the Todo table and return a list of task names."""
    tasks = Todo.query.order_by(Todo.task_id).all()
    return [task.name for task in tasks]

#### ROUTES ####
# Main Page
@app.route('/')
def index():
    global tasks_list, pop_task
    print('INDEX') # Debugging

    todo_list = Todo.query.all()

    pop_task = True
    print('Pop on: ', pop_task) # Debugging

    tasks_list = get_tasks_list()
    print('Task List:\n', tasks_list) # Debugging
    
    return render_template('index_WEBAPP.html', title='Main Page',
                           dataframe=df_tasks, todo_list=todo_list)

# Return to Main Page
@app.route('/return_to_index', methods=['POST'])
def return_to_index():
    return render_template('index_WEBAPP.html', title='Main Page')


# Add Task
@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form.get("name")
    add_task_Todo = Todo(name=name, done=False)
    add_task_IT = IT_db(name=name, Importance_Score=0)
    db.session.add(add_task_Todo)
    db.session.add(add_task_IT)
    db.session.commit()
    return redirect(url_for("index"))

# Update DONE Tasks
@app.route('/update_task/<int:todo_id>')
def update_task(todo_id):
    update_task_Todo = Todo.query.get(todo_id)
    update_task_Todo.done = not update_task_Todo.done
    db.session.commit()
    return redirect(url_for("index"))

# Delete Tasks
@app.route('/delete_task/<int:todo_id>')
def delete_task(todo_id):
    del_task_Todo = Todo.query.get(todo_id)
    del_task_IT = IT_db.query.get(todo_id)
    db.session.delete(del_task_Todo)
    db.session.delete(del_task_IT)
    db.session.commit()
    return redirect(url_for("index"))


# Evalute Tasks
@app.route('/evaluate_tasks', methods=['GET', 'POST'])
def evaluate_tasks_route():
    global tasks_list, first_task
    print('EVALUATE') # Debugging
    print('Pop on: ', pop_task) # Debugging

    if not pop_task:
        tasks_list = get_tasks_list()
    
    print('Task List:\n', tasks_list) # Debugging

    # get first task
    if tasks_list:
        first_task = tasks_list[0]

    IT_df, UT_df, ET_df = evaluate_tasks(df_tasks)
    IT_list = IT_db.query.all()

    return render_template('evaluate.html', title='Evaluate Page',
                           IT_df=IT_df, UT_df=UT_df, ET_df=ET_df,
                           IT_list=IT_list, first_task=first_task,
                           attribute=attribute)

# Update Scores
@app.route('/update_scores', methods=['GET', 'POST'])
def update_scores():
    global tasks_list, first_task, pop_task
    print('UPDATE') # Debugging

    IT_value = request.form.get("IT_value")
    IT_value = int(IT_value) if IT_value is not None else 0  # Convert to integer
    
    task = IT_db.query.filter_by(name=first_task).first()
    if task.Importance_Score is None:
        task.Importance_Score = 0  # Ensure Importance_Score is not None
    task.Importance_Score += IT_value
    db.session.commit()

    pop_task = True
    print('Pop on: ', pop_task) # Debugging

    # pop first task
    if tasks_list:
        removed_task = tasks_list.pop(0)
        print('Pop: ', removed_task) # Debugging

    # get new first task
    if not tasks_list:
        pass # or first_task = "--- (no tasks left)"
    else: 
        first_task = tasks_list[0]
    print('Task List:\n', tasks_list) # Debugging
    

    return redirect(url_for("evaluate_tasks_route"))    

#### END ROUTES ####

#### Main ####
if __name__ == '__main__':
    app.run(debug=True, port=5000)
