from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from tasks import df_tasks
from WEBAPP_funcs import evaluate_tasks, compare_tasks, render_task_rank
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prio_calc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#### Tables ####
# Task Table
class Todo(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False, unique=True)
    done=db.Column(db.Boolean)
    datetime_added = db.Column(db.DateTime, default=datetime.now())
    


# Importance Table
class IT_db(db.Model):
    task_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    Importance_Score=db.Column(db.Integer)


# Urgency Table

# Effort Table

# Results Table

#Variables to pass to subdomains
attribute = "Importance"

#Initilize empty dataframes
IT_df = pd.DataFrame()
UT_df = pd.DataFrame()
ET_df = pd.DataFrame()



#### ROUTES ####

# Main Page
@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index_WEBAPP.html', title='Main Page', dataframe=df_tasks, todo_list=todo_list)

# Return to Main Page
@app.route('/return_to_index', methods=['POST'])
def return_to_index():
    return render_template('index_WEB+APP.html', title='Main Page')

# Add Task
@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form.get("name")
    new_task = Todo(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

# Update Tasks
@app.route('/update_task/<int:todo_id>')
def update_task(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))

# Delete Tasks
@app.route('/delete_task/<int:todo_id>')
def delete_task(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


# Evalute Tasks
@app.route('/evaluate_tasks', methods=['POST'])
def evaluate_tasks_route():
    IT_df, UT_df, ET_df = evaluate_tasks(df_tasks)
    return render_template('evaluate.html', title='Evaluate Page',
                           IT_df=IT_df, UT_df=UT_df, ET_df=ET_df,
                           attribute=attribute)

# Update Scores
@app.route('/update_scores', methods=['GET', 'POST'])
def update_scores():
    if request.method == "POST":
        IT_df.loc[IT_df['Tasks'] == 0, 'Importance_Score'] += 1
        IT_df, UT_df, ET_df = evaluate_tasks(df_tasks)
    return redirect(url_for("evaluate.html"))    

#### END ROUTES ####


if __name__ == '__main__':
    app.run(debug=True, port=5000)
