from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import logging
from tasks import df_tasks
from WEBAPP_funcs import evaluate_tasks, compare_tasks, render_task_rank

logging.basicConfig(level=logging.DEBUG)

#print('Test ############')

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
class UT_db(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    Urgency_Score=db.Column(db.Integer)

    def __repr__(self):
        return f'<{self.task_id} {self.name} {self.Urgency_Score}>'

# Effort Table
class ET_db(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    Effort_Score=db.Column(db.Integer)

    def __repr__(self):
        return f'<{self.task_id} {self.name} {self.Effort_Score}>'

# Results Table
class RT_db(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    Results_Score=db.Column(db.Integer)

    def __repr__(self):
        return f'<{self.task_id} {self.name} {self.Results_Score}>'

#### END Database Models ####


### Global Vars and Funcs ###
attribute = "Importance"
tasks_list = []
first_task = ''
pop_task = False
IT_is_rated = False
UT_is_rated = False
ET_is_rated = False
### END Global Vars and Funcs ###


#### Helper Functions ####
def get_tasks_list():
    """Query the Todo table and return a list of task names."""
    tasks = Todo.query.order_by(Todo.task_id).all()
    return [task.name for task in tasks]

#### ROUTES ####
# Main Page
@app.route('/')
def index():
    global tasks_list, pop_task, IT_is_rated, UT_is_rated, ET_is_rated
    print('\nINDEX PAGE') # Debugging

    todo_list = Todo.query.all()

    IT_is_rated = False
    UT_is_rated = False
    ET_is_rated = False
    print("IT_is_rated: ", IT_is_rated) # Debugging
    print("UT_is_rated: ", UT_is_rated) # Debugging
    print("ET_is_rated: ", ET_is_rated) # Debugging

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
    add_task_UT = UT_db(name=name, Urgency_Score=0)
    add_task_ET = ET_db(name=name, Effort_Score=0)
    add_task_RT = RT_db(name=name, Results_Score=0)
    db.session.add(add_task_Todo)
    db.session.add(add_task_IT)
    db.session.add(add_task_UT)
    db.session.add(add_task_ET)
    db.session.add(add_task_RT)
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
    del_task_UT = UT_db.query.get(todo_id)
    del_task_ET = ET_db.query.get(todo_id)
    del_task_RT = RT_db.query.get(todo_id)
    db.session.delete(del_task_Todo)
    db.session.delete(del_task_IT)
    db.session.delete(del_task_UT)
    db.session.delete(del_task_ET)
    db.session.delete(del_task_RT)
    db.session.commit()
    return redirect(url_for("index"))


# Evalute Tasks
@app.route('/evaluate_tasks', methods=['GET', 'POST'])
def evaluate_tasks_route():
    global tasks_list, first_task, IT_is_rated, UT_is_rated, ET_is_rated
    print('\nEVALUATE PAGE') # Debugging
    print("IT_is_rated: ", IT_is_rated) # Debugging
    print("UT_is_rated: ", UT_is_rated) # Debugging
    print("ET_is_rated: ", ET_is_rated) # Debugging
    print('Pop task on: ', pop_task) # Debugging

    if not pop_task:
        tasks_list = get_tasks_list()
    
    print('Task List:\n', tasks_list) # Debugging

    # get first task
    if tasks_list:
        first_task = tasks_list[0]

    IT_df, UT_df, ET_df = evaluate_tasks(df_tasks)
    RT_list = RT_db.query.all()
    IT_list = IT_db.query.all()
    UT_list = UT_db.query.all()
    ET_list = ET_db.query.all()

    return render_template('evaluate.html', title='Evaluate Page',
                           IT_df=IT_df, UT_df=UT_df, ET_df=ET_df,
                           RT_list=RT_list, IT_list=IT_list, UT_list=UT_list, ET_list=ET_list,
                           first_task=first_task, attribute=attribute,
                           IT_is_rated=IT_is_rated, UT_is_rated=UT_is_rated, ET_is_rated=ET_is_rated)

# Update Scores
@app.route('/update_scores', methods=['GET', 'POST'])
def update_scores():
    global tasks_list, first_task, pop_task, IT_is_rated, UT_is_rated, ET_is_rated
    print('\nUPDATE SCORES') # Debugging

    rated = request.form.get("rated")

    if rated == "Importance":
        # Retrieve IT vars from evaluation page
        IT_is_rated = bool(request.form.get("IT_is_rated")) # retreive and convert to bool
    IT_value = request.form.get("IT_value")
    IT_value = int(IT_value) if IT_value is not None else 0  # Convert to integer
    print("IT_is_rated: ", IT_is_rated) # Debugging

    if rated == "Urgency":
        # Retrieve UT vars from evaluation page
        UT_is_rated = bool(request.form.get("UT_is_rated")) # retreive and convert to bool
    UT_value = request.form.get("UT_value")
    UT_value = int(UT_value) if UT_value is not None else 0  # Convert to integer
    print("UT_is_rated: ", UT_is_rated) # Debugging

    if rated == "Effort":
        # Retrieve ET vars from evaluation page
        ET_is_rated = bool(request.form.get("ET_is_rated")) # retreive and convert to bool
    ET_value = request.form.get("ET_value")
    ET_value = int(ET_value) if ET_value is not None else 0  # Convert to integer
    print("ET_is_rated: ", ET_is_rated) # Debugging


    print("IT_value: ", IT_value) # Debugging
    print("UT_value: ", UT_value) # Debugging
    print("ET_value: ", ET_value) # Debugging

    RT_task = RT_db.query.filter_by(name=first_task).first()
    IT_task = IT_db.query.filter_by(name=first_task).first()
    UT_task = UT_db.query.filter_by(name=first_task).first()
    ET_task = ET_db.query.filter_by(name=first_task).first()

    if RT_task.Results_Score is None:
        RT_task.Results_Score = 0 # Ensure Results_Score is not None

    if IT_task.Importance_Score is None:
        IT_task.Importance_Score = 0  # Ensure Importance_Score is not None
    IT_task.Importance_Score += IT_value
    RT_task.Results_Score += IT_value
    if UT_task.Urgency_Score is None:
        UT_task.Urgency_Score = 0  # Ensure Urgency_Score is not None
    UT_task.Urgency_Score += UT_value
    RT_task.Results_Score += UT_value
    if ET_task.Effort_Score is None:
        ET_task.Effort_Score = 0  # Ensure Effort_Score is not None
    ET_task.Effort_Score -= ET_value
    RT_task.Results_Score -= ET_value
    db.session.commit()



    ### Logik wenn IT, UT u. ET gerated ###
    if IT_is_rated and UT_is_rated and ET_is_rated:
        pop_task = True
        print('Pop task on: ', pop_task) # Debugging

        # pop first task
        if tasks_list:
            removed_task = tasks_list.pop(0)
            print('Popped task: ', removed_task) # Debugging

        # get new first task
        if not tasks_list: # if empty list
            print("To Do List empty") # Debugging
            print("Show results") # Debugging
            ### If EMPTY SHOW RESULT ######
            # Sort RT_db table by Results_Score in descending order
            sorted_results = RT_db.query.order_by(RT_db.Results_Score.desc()).all()
            return render_template('results.html', sorted_results=sorted_results)
        else: 
            first_task = tasks_list[0]

        # reset is_rated variables
        print("Reset is_rated variables") # Debugging
        IT_is_rated, UT_is_rated, ET_is_rated = False, False, False
        print("IT_is_rated: ", IT_is_rated) # Debugging
        print("UT_is_rated: ", UT_is_rated) # Debugging
        print("ET_is_rated: ", ET_is_rated) # Debugging

        print('Task List:\n', tasks_list) # Debugging
    else:
        print('Pop task on: ', pop_task)
    ### END Logik wenn IT, UT u. ET gerated ###


    return redirect(url_for("evaluate_tasks_route"))    

#### END ROUTES ####

#### Main ####
if __name__ == '__main__':
    app.run(debug=True, port=5000)
