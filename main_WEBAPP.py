from flask import Flask, render_template, request
import os
import pandas as pd
from tasks import df_tasks
from WEBAPP_funcs import evaluate_tasks, compare_tasks, render_task_rank

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_WEBAPP.html', dataframe=df_tasks)

@app.route('/evaluate_tasks', methods=['POST'])
def evaluate_tasks_route():
    IT_df, UT_df, ET_df = evaluate_tasks(df_tasks)
    return render_template('result.html', IT_df=IT_df, UT_df=UT_df, ET_df=ET_df)

@app.route('/compare_tasks', methods=['POST'])
def compare_tasks_route():
    IT_df, UT_df, ET_df = compare_tasks(df_tasks)
    return render_template('result.html', IT_df=IT_df, UT_df=UT_df, ET_df=ET_df)

if __name__ == '__main__':
    app.run(debug=True)
