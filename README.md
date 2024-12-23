Overview
The Priority Calculator Application is a web-based task management system designed to help users prioritize their tasks based on three criteria: Importance, Urgency, and Effort. The app evaluates tasks through a structured scoring process, enabling users to focus on high-priority items.

The application is built with Python using the Flask framework, HTML/CSS for the front-end, and SQLite for the database.

Features
Add, Update, and Delete Tasks: Users can manage their task list easily through the web interface.
Evaluate Tasks: Rate tasks on Importance, Urgency, and Effort, or compare them pairwise to generate priority scores.
Dynamic Scoring: Real-time calculation of task priority scores based on user input.
Results Display: View tasks sorted by their calculated scores to prioritize effectively.
Architecture
Backend
Framework: Flask.
Database: SQLite, with SQLAlchemy as the ORM.
Data Models:
Todo: Stores task details and their completion status.
IT_db, UT_db, ET_db: Store Importance, Urgency, and Effort scores for tasks respectively.
RT_db: Stores the aggregated Results Score for each task.
Frontend
Templates: HTML with Jinja2 templating.
Styling: CSS for a clean, user-friendly interface.
Pages:
Home Page: Add tasks and view the task list.
Evaluation Page: Rate tasks and update their scores.
Results Page: View sorted tasks based on their calculated priorities.
Key Components
Python Files
main.py:

Core Flask app managing routes and database operations.
Key functionalities:
Task creation (/add_task).
Updating task completion status (/update_task).
Deleting tasks (/delete_task).
Evaluation of tasks through /evaluate_tasks and /update_scores.
tasks.py:

Contains a dictionary of sample tasks (DICT_TASKS) and their DataFrame representation (df_tasks).
WEBAPP_funcs.py:

Provides utility functions for task comparison, evaluation, and ranking:
compare_tasks: Pairwise comparison of tasks.
evaluate_tasks: Individual evaluation of tasks.
render_task_rank: Calculates and sorts tasks by total priority score.
HTML Files
index_WEBAPP.html:

Displays the main task list with options to add, update, or delete tasks.
A button leads to the evaluation page.
evaluate.html:

Allows users to rate tasks on a scale from 0–10 for Importance, Urgency, and Effort.
Displays intermediate scores and ongoing evaluations.
results.html:

Shows sorted tasks by their aggregated Results Score.
Displays the breakdown of scores for Importance, Urgency, and Effort.
CSS Files
style.css:
General styling for the main task list and results page.
style_evaluate.css:
Custom styling for the evaluation page, including button groups and layouts.
Usage
Run the Application:
bash
Code kopieren
python main.py
Access the Web Interface: Open a browser and navigate to http://127.0.0.1:5000.
Add Tasks:
Enter a task name and submit to add it to the list.
Evaluate Tasks:
Rate tasks or compare them pairwise on Importance, Urgency, and Effort.
Task scores update dynamically based on inputs.
View Results:
Once all tasks are evaluated, view the sorted results to identify high-priority items.
Future Enhancements
Implement user authentication for personal task management.
Extend evaluation criteria (e.g., deadlines, dependencies).
Export task priorities to CSV or PDF formats.
Add API endpoints for integration with other tools.