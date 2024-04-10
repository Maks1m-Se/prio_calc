from flask import Flask, render_template, request
import random
import os
import pandas as pd
import numpy as np
from tasks import df_tasks


# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', dataframe=df_tasks)


if __name__ == '__main__':
    app.run(debug=True)
