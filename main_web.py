from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from tasks import df_tasks


# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', dataframe=df_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        new_task = request.form['new_task']
        if new_task:
            # Add the new task to the DataFrame
            df_tasks.loc[len(df_tasks)] = [new_task]
            return redirect(url_for('index'))
        else:
            # Handle case where no task is provided
            return "No task provided!"
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
